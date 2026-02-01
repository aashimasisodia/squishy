from fastapi import FastAPI, HTTPException, BackgroundTasks, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
import os
import datetime
from backend.api.workflow import run_simulation_workflow

app = FastAPI(title="Text-to-Physics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

router = APIRouter(prefix="/api")


class PromptRequest(BaseModel):
    prompt: str


def get_output_dir(timestamp_id: str):
    if os.environ.get("VERCEL"):
        # On Vercel, we can only write to /tmp
        generated_dir = os.path.join("/tmp", "generated")
    else:
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        generated_dir = os.path.join(backend_dir, "generated")

    return os.path.join(generated_dir, timestamp_id)


@router.post("/generate")
async def generate_simulation(request: PromptRequest, background_tasks: BackgroundTasks):
    """
    Starts a simulation generation task in the background.
    Returns the generation ID.
    """
    timestamp_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Run the workflow in the background
    background_tasks.add_task(run_simulation_workflow,
                              request.prompt, timestamp_id)

    return {
        "id": timestamp_id,
        "status": "processing",
        "message": "Simulation started in background. Poll /status/{id} or check /gif/{id}."
    }


@router.get("/status/{timestamp_id}")
async def get_status(timestamp_id: str):
    output_dir = get_output_dir(timestamp_id)
    if not os.path.exists(output_dir):
        raise HTTPException(status_code=404, detail="Generation ID not found")

    error_log = os.path.join(output_dir, "error.log")
    if os.path.exists(error_log):
        with open(error_log, "r") as f:
            error = f.read()
        return {"status": "failed", "error": error}

    gif_path = os.path.join(output_dir, "simulation.gif")
    if os.path.exists(gif_path):
        return {"status": "completed"}

    return {"status": "processing"}


@router.get("/gif/{timestamp_id}")
async def get_gif(timestamp_id: str):
    output_dir = get_output_dir(timestamp_id)
    gif_path = os.path.join(output_dir, "simulation.gif")

    if not os.path.exists(gif_path):
        # Check if failed
        if os.path.exists(os.path.join(output_dir, "error.log")):
            raise HTTPException(
                status_code=400, detail="Simulation failed. Check status.")
        raise HTTPException(
            status_code=404, detail="GIF not ready or ID not found")

    return FileResponse(gif_path, media_type="image/gif")


@router.get("/code/{timestamp_id}")
async def get_code(timestamp_id: str):
    output_dir = get_output_dir(timestamp_id)
    code_path = os.path.join(output_dir, "generated_simulation.py")

    if not os.path.exists(code_path):
        raise HTTPException(status_code=404, detail="Code not found")

    with open(code_path, "r") as f:
        content = f.read()

    return PlainTextResponse(content)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
