from backend.api.pipeline import SceneGeneratorPipeline
import os
import subprocess
import sys
import time
import datetime

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    print("--- Starting Pipeline Automation ---")

    # 0. Setup Directories
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    generated_base_dir = os.path.join(backend_dir, "generated")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(generated_base_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory created: {output_dir}")

    # 1. Initialize Pipeline
    print("\n[1/5] Initializing SceneGeneratorPipeline...")
    try:
        pipeline = SceneGeneratorPipeline()
    except Exception as e:
        print(f"Failed to initialize pipeline: {e}")
        return

    # 2. Generate Script
    prompt = """
       Generate a PyElastica simulation of a single Cosserat rod made of soft biological tissues in 3D where the endpoints of the rod are free to move. The rod should be actuated by a time-varying intrinsic curvature that forms a traveling sinusoidal wave along the rod (kappa(s,t) = A sin(2π(s/λ - t/T))).
    """
    print(f"\n[2/5] Generating scene for prompt: '{prompt}'")

    try:
        scene = pipeline.generate_scene(prompt)
        print("Scene JSON generated successfully.")
        script_content = pipeline.generate_python_script(scene)
        print("Python script generated successfully.")
    except Exception as e:
        print(f"Error during generation: {e}")
        return

    # 3. Save Script
    script_filename = "generated_simulation.py"
    script_path = os.path.join(output_dir, script_filename)

    print(f"\n[3/5] Saving generated script to: {script_path}")
    with open(script_path, "w") as f:
        f.write(script_content)

    # 4. Run Simulation
    print(f"\n[4/5] Running simulation script ({script_filename})...")

    cmd_sim = [sys.executable, script_filename]

    try:
        start_time = time.time()
        # Run inside the output_dir so output files appear there
        result = subprocess.run(cmd_sim, cwd=output_dir, check=True)
        elapsed = time.time() - start_time
        print(f"Simulation completed in {elapsed:.2f}s.")
    except subprocess.CalledProcessError as e:
        print(f"Simulation failed with return code {e.returncode}.")
        return
    except Exception as e:
        print(f"Failed to run simulation: {e}")
        return

    # Check if pkl exists
    pkl_filename = "simulation_data.pkl"
    pkl_path = os.path.join(output_dir, pkl_filename)
    if not os.path.exists(pkl_path):
        print(f"Error: {pkl_path} was not created by the simulation.")
        return

    # 5. Run Renderer
    # We locate the renderer in backend/api/elastica_render.py
    renderer_path = os.path.join(backend_dir, "api", "elastica_render.py")
    print(f"\n[5/5] Running renderer...")

    if not os.path.exists(renderer_path):
        print(f"Renderer not found at {renderer_path}")
        return

    # We run the renderer, passing the pkl file path
    # Since we are running from output_dir context (cwd), passing just filename works if we set cwd
    cmd_render = [sys.executable, renderer_path, pkl_filename]

    try:
        result_render = subprocess.run(cmd_render, cwd=output_dir, check=True)
        print("Rendering completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Rendering failed with return code {e.returncode}.")
    except Exception as e:
        print(f"Failed to run renderer: {e}")

    print(f"\n--- Pipeline Finished ---")
    print(f"Outputs saved to: {output_dir}")


if __name__ == "__main__":
    main()
