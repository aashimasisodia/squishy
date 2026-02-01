import os
import sys
import uuid
import subprocess
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Add backend to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.pipeline import SceneGeneratorPipeline
from backend.app.renderer import render_simulation

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED_DIR = os.path.join(BASE_DIR, "generated")

# Ensure generated dir exists
os.makedirs(GENERATED_DIR, exist_ok=True)

class GenerateRequest(BaseModel):
    prompt: str

class SimulationResponse(BaseModel):
    id: str
    status: str
    message: str
    gif_url: Optional[str] = None

app = FastAPI()

# Mount generated directory to serve static files (GIFs)
app.mount("/generated", StaticFiles(directory=GENERATED_DIR), name="generated")

pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load pipeline on startup
    global pipeline
    try:
        pipeline = SceneGeneratorPipeline()
        print("Pipeline initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize pipeline: {e}")
    yield
    # Cleanup if needed

app = FastAPI(lifespan=lifespan)
app.mount("/generated", StaticFiles(directory=GENERATED_DIR), name="generated")

def run_simulation_task(sim_id: str, prompt: str):
    """
    Background task to run the full pipeline.
    """
    sim_dir = os.path.join(GENERATED_DIR, sim_id)
    os.makedirs(sim_dir, exist_ok=True)
    
    script_path = os.path.join(sim_dir, "simulation.py")
    pkl_path = os.path.join(sim_dir, "simulation_data.pkl")
    gif_path = os.path.join(sim_dir, "simulation.gif")
    
    try:
        # 1. Generate Code
        print(f"[{sim_id}] Generating scene for: {prompt}")
        scene = pipeline.generate_scene(prompt)
        code = pipeline.generate_python_script(scene)
        
        with open(script_path, "w") as f:
            f.write(code)
            
        # 2. Run Simulation
        print(f"[{sim_id}] Running simulation...")
        # We run the script with cwd=sim_dir so pkl is saved there
        # The generated script saves to 'simulation_data.pkl' in current dir
        cmd = [sys.executable, "simulation.py"]
        subprocess.run(cmd, cwd=sim_dir, check=True)
        
        if not os.path.exists(pkl_path):
            print(f"[{sim_id}] Simulation failed to produce pkl.")
            return

        # 3. Render
        print(f"[{sim_id}] Rendering...")
        render_simulation(pkl_path, gif_path)
        print(f"[{sim_id}] Done.")
        
    except Exception as e:
        print(f"[{sim_id}] Task failed: {e}")

@app.post("/generate", response_model=SimulationResponse)
async def generate_simulation(req: GenerateRequest, background_tasks: BackgroundTasks):
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    sim_id = str(uuid.uuid4())
    background_tasks.add_task(run_simulation_task, sim_id, req.prompt)
    
    return SimulationResponse(
        id=sim_id,
        status="queued",
        message="Simulation started in background.",
        gif_url=f"/generated/{sim_id}/simulation.gif" 
    )

@app.get("/status/{sim_id}")
async def get_status(sim_id: str):
    sim_dir = os.path.join(GENERATED_DIR, sim_id)
    if not os.path.exists(sim_dir):
        raise HTTPException(status_code=404, detail="Simulation ID not found")
    
    gif_path = os.path.join(sim_dir, "simulation.gif")
    if os.path.exists(gif_path):
        return {"status": "completed", "gif_url": f"/generated/{sim_id}/simulation.gif"}
    
    pkl_path = os.path.join(sim_dir, "simulation_data.pkl")
    if os.path.exists(pkl_path):
        return {"status": "rendering"}
        
    script_path = os.path.join(sim_dir, "simulation.py")
    if os.path.exists(script_path):
        return {"status": "simulating"}
        
    return {"status": "generating"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
