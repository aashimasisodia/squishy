import os
import sys
import time
import datetime
import subprocess
from backend.api.pipeline import SceneGeneratorPipeline


def run_simulation_workflow(prompt: str, timestamp_id: str = None) -> str:
    """
    Runs the full simulation pipeline.
    If timestamp_id is provided, uses it for the folder name.
    Otherwise, generates a new timestamp.
    Returns the timestamp_id used.
    """
    # 0. Setup Directories
    # backend/api/workflow.py -> backend/api -> backend
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if os.environ.get("VERCEL"):
        generated_base_dir = os.path.join("/tmp", "generated")
    else:
        generated_base_dir = os.path.join(backend_dir, "generated")

    if timestamp_id is None:
        timestamp_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = os.path.join(generated_base_dir, timestamp_id)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory created: {output_dir}")

    try:
        # 1. Initialize Pipeline
        print("\n[1/5] Initializing SceneGeneratorPipeline...")
        pipeline = SceneGeneratorPipeline()

        # 2. Generate Script
        print(f"\n[2/5] Generating scene for prompt: '{prompt}'")
        scene = pipeline.generate_scene(prompt)
        script_content = pipeline.generate_python_script(scene)

        # 3. Save Script
        script_filename = "generated_simulation.py"
        script_path = os.path.join(output_dir, script_filename)

        print(f"\n[3/5] Saving generated script to: {script_path}")
        with open(script_path, "w") as f:
            f.write(script_content)

        # 4. Run Simulation
        print(f"\n[4/5] Running simulation script ({script_filename})...")
        cmd_sim = [sys.executable, script_filename]

        # Run inside the output_dir so output files appear there
        # Capture output to log file for debugging
        with open(os.path.join(output_dir, "simulation.log"), "w") as log_file:
            subprocess.run(cmd_sim, cwd=output_dir, check=True,
                           stdout=log_file, stderr=subprocess.STDOUT)

        # 5. Run Renderer
        renderer_path = os.path.join(backend_dir, "api", "elastica_render.py")
        pkl_filename = "simulation_data.pkl"
        print(f"\n[5/5] Running renderer...")

        cmd_render = [sys.executable, renderer_path, pkl_filename]
        with open(os.path.join(output_dir, "render.log"), "w") as log_file:
            subprocess.run(cmd_render, cwd=output_dir, check=True,
                           stdout=log_file, stderr=subprocess.STDOUT)

        print(f"Workflow completed successfully for ID: {timestamp_id}")
        return timestamp_id

    except Exception as e:
        print(f"Workflow failed for ID {timestamp_id}: {e}")
        # Write error to a status file
        with open(os.path.join(output_dir, "error.log"), "w") as f:
            f.write(str(e))
        raise e
