from backend.pipeline import SceneGeneratorPipeline
import os
import subprocess
import sys
import time

# Ensure the project root is in sys.path so we can import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    print("--- Starting Pipeline Automation ---")

    # 1. Initialize Pipeline
    print("\n[1/5] Initializing SceneGeneratorPipeline...")
    try:
        pipeline = SceneGeneratorPipeline()
    except Exception as e:
        print(f"Failed to initialize pipeline: {e}")
        return

    # 2. Generate Script
    # prompt = "A horizontal rod made of soft biological tissue fixed at the left end, being pulled down by gravity and pulled to the right by a 5N force at the tip."
    prompt = """
       Generate a PyElastica simulation of a single Cosserat rod in 3D where the base of the rod is clamped (fixed position and fixed director frame at s=0).
The rod should be actuated by a time-varying intrinsic curvature that forms a traveling sinusoidal wave along the rod (kappa(s,t) = A sin(2π(s/λ − t/T))).


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
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    script_filename = "generated_simulation.py"
    script_path = os.path.join(backend_dir, script_filename)

    print(f"\n[3/5] Saving generated script to: {script_path}")
    with open(script_path, "w") as f:
        f.write(script_content)

    # 4. Run Simulation
    print(f"\n[4/5] Running simulation script ({script_filename})...")

    # We run the script in the backend directory so output files appear there
    cmd_sim = [sys.executable, script_filename]

    try:
        start_time = time.time()
        # capture_output=True allows us to see stdout if it fails, or we can just let it stream
        result = subprocess.run(cmd_sim, cwd=backend_dir, check=True)
        elapsed = time.time() - start_time
        print(f"Simulation completed in {elapsed:.2f}s.")
    except subprocess.CalledProcessError as e:
        print(f"Simulation failed with return code {e.returncode}.")
        return
    except Exception as e:
        print(f"Failed to run simulation: {e}")
        return

    # Check if pkl exists
    pkl_path = os.path.join(backend_dir, "simulation_data.pkl")
    if not os.path.exists(pkl_path):
        print(f"Error: {pkl_path} was not created by the simulation.")
        return

    # 5. Run Renderer
    renderer_filename = "elastica_render.py"
    renderer_path = os.path.join(backend_dir, renderer_filename)
    print(f"\n[5/5] Running renderer ({renderer_filename})...")

    if not os.path.exists(renderer_path):
        print(f"Renderer not found at {renderer_path}")
        return

    cmd_render = [sys.executable, renderer_filename, "simulation_data.pkl"]

    try:
        result_render = subprocess.run(cmd_render, cwd=backend_dir, check=True)
        print("Rendering completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Rendering failed with return code {e.returncode}.")
    except Exception as e:
        print(f"Failed to run renderer: {e}")

    print("\n--- Pipeline Finished ---")


if __name__ == "__main__":
    main()
