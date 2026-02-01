import json
from typing import Dict, Any, List
from backend.materials import MATERIALS_DB


def generate_script_from_scene(scene_data: Dict[str, Any]) -> str:
    """
    Converts a JSON scene description into a runnable PyElastica Python script.
    """

    objects = scene_data.get("objects", [])
    render_settings = scene_data.get("render", {})

    duration = render_settings.get("duration", 10.0)
    fps = render_settings.get("fps", 60)
    total_steps = int(duration * 1e4)  # Approximation, refined below

    # Start building the script content
    script_lines = [
        "import numpy as np",
        "import elastica as ea",
        "from collections import defaultdict",
        "import pickle",
        "",
        "# --- INLINED TEMPLATES ---",
    ]

    # Read the templates content and inline it
    try:
        with open("backend/templates.py", "r") as f:
            template_code = f.read()
            # Remove imports from templates as we already imported them
            lines = template_code.split('\n')
            filtered_lines = [l for l in lines if not l.startswith("import")]
            script_lines.extend(filtered_lines)
    except FileNotFoundError:
        # Fallback if file not found (though it should exist)
        script_lines.append("# Error: backend/templates.py not found.")

    script_lines.extend([
        "",
        "# --- GENERATED SIMULATION CODE ---",
        "def main():",
        "    # 1. Setup Simulator",
        "    sim = create_simulator()",
        "",
        "    # 2. Create Objects",
        "    rods = []"
    ])

    # Process objects
    for idx, obj in enumerate(objects):
        obj_type = obj.get("type")

        if obj_type == "rod":
            material_name = obj.get("material", "rubber")
            mat_props = MATERIALS_DB.get(material_name, MATERIALS_DB["rubber"])

            length = obj.get("length", 1.0)
            radius = obj.get("radius", 0.025)
            n_elem = obj.get("n_elem", 50)

            # Parse positions and orientation from JSON, defaulting if missing
            start_pos = obj.get("start", [0.0, 0.0, 0.0])
            direction = obj.get("direction", [0.0, 0.0, 1.0])
            normal = obj.get("normal", [0.0, 1.0, 0.0])

            script_lines.append(f"    # Rod {idx} ({material_name})")
            script_lines.append(f"    rod_{idx} = make_rod(")
            script_lines.append(f"        sim,")
            script_lines.append(f"        n_elem={n_elem},")
            script_lines.append(f"        length={length},")
            script_lines.append(f"        radius={radius},")
            script_lines.append(f"        density={mat_props['density']},")
            script_lines.append(
                f"        youngs_modulus={mat_props['youngs_modulus']},")
            script_lines.append(
                f"        poisson_ratio={mat_props['poisson_ratio']},")
            script_lines.append(f"        start={start_pos},")
            script_lines.append(f"        direction={direction},")
            script_lines.append(f"        normal={normal}")
            script_lines.append(f"    )")
            script_lines.append(f"    rods.append(rod_{idx})")

            # Process constraints
            constraints = obj.get("constraints", [])
            for constraint in constraints:
                if constraint == "clamped_start":
                    script_lines.append(f"    clamp_start(sim, rod_{idx})")
                elif constraint == "clamped_end":
                    script_lines.append(f"    clamp_end(sim, rod_{idx})")

            # Process forces
            forces = obj.get("forces", [])
            for force_spec in forces:
                # Handle both string (old schema) and dict (new schema)
                if isinstance(force_spec, str):
                    force_type = force_spec
                    params = {}
                else:
                    force_type = force_spec.get("type")
                    params = force_spec
                
                if force_type == "gravity":
                    acc = params.get("acc", [0.0, 0.0, -9.81])
                    # Calculate direction and g from acc vector
                    acc_np = f"[{acc[0]}, {acc[1]}, {acc[2]}]"
                    # We can pass the vector directly if we modify add_gravity, 
                    # but the current add_gravity takes g and direction.
                    # Let's just pass the vector as 'direction' and g=1.0 or modify add_gravity.
                    # Actually, looking at templates.py:
                    # def add_gravity(sim, rod, g=9.81, direction=(0.0, 0.0, -1.0)):
                    #    acc_gravity = np.array(direction) * g
                    # So we can just pass g=1.0 and direction=acc
                    script_lines.append(f"    add_gravity(sim, rod_{idx}, g=1.0, direction={acc_np})")
                    
                elif force_type == "endpoint_force":
                    force_vec = params.get("force", [0.1, 0.0, 0.0])
                    ramp = params.get("ramp", 0.1)
                    force_str = f"[{force_vec[0]}, {force_vec[1]}, {force_vec[2]}]"
                    script_lines.append(
                        f"    add_endpoint_force(sim, rod_{idx}, force={force_str}, ramp_up_time={ramp})")


            # Add damping
            script_lines.append(
                f"    add_damping(sim, rod_{idx}, damping_constant=0.1, time_step=1e-4)")
            script_lines.append("")

    # Process connections
    connections = scene_data.get("connections", [])
    if connections:
        script_lines.append("    # Process Connections")
        for conn in connections:
            idx_a = conn.get("rod_a_index")
            idx_b = conn.get("rod_b_index")
            offset_a_str = conn.get("offset_a", "end")
            offset_b_str = conn.get("offset_b", "start")
            conn_type = conn.get("type", "fixed_joint")

            # Map offset strings to indices
            # "start" -> 0, "end" -> -1
            map_offset = lambda x: 0 if x == "start" else -1
            idx_one = map_offset(offset_a_str)
            idx_two = map_offset(offset_b_str)
            
            # Check for joint type
            if conn_type == "spherical_joint":
                script_lines.append(f"    # Connection: Rod {idx_a} ({offset_a_str}) -> Rod {idx_b} ({offset_b_str}) (Spherical)")
                script_lines.append(f"    connect_spherical(sim, rods[{idx_a}], rods[{idx_b}], index_one={idx_one}, index_two={idx_two})")
            
            elif conn_type == "hinge_joint":
                normal = conn.get("normal", [0.0, 1.0, 0.0])
                script_lines.append(f"    # Connection: Rod {idx_a} ({offset_a_str}) -> Rod {idx_b} ({offset_b_str}) (Hinge)")
                script_lines.append(f"    connect_hinge(sim, rods[{idx_a}], rods[{idx_b}], index_one={idx_one}, index_two={idx_two}, normal={normal})")
            
            else: # fixed_joint or default
                script_lines.append(f"    # Connection: Rod {idx_a} ({offset_a_str}) -> Rod {idx_b} ({offset_b_str}) (Fixed)")
                script_lines.append(f"    connect_fixed(sim, rods[{idx_a}], rods[{idx_b}], index_one={idx_one}, index_two={idx_two})")
        
        script_lines.append("")

    # Diagnostics
    script_lines.append("    # 3. Setup Diagnostics")
    script_lines.append("    history_list = []")
    script_lines.append("    for rod in rods:")
    script_lines.append(
        "        history_list.append(record_history(sim, rod, step_skip=200))")
    script_lines.append("")

    # Simulation loop
    script_lines.append("    # 4. Run Simulation")
    script_lines.append(f"    final_time = {duration}")
    script_lines.append("    dt = 1e-4")
    script_lines.append("    total_steps = int(final_time / dt)")
    script_lines.append(
        "    print(f'Running simulation for {final_time}s ({total_steps} steps)...')")
    script_lines.append(
        "    finalize_and_integrate(sim, final_time=final_time, total_steps=total_steps)")
    script_lines.append("")

    # Save results
    script_lines.append("    # 5. Save Results")
    script_lines.append(
        "    print('Saving results to simulation_data.pkl...')")
    script_lines.append(
        "    data = {'rods': history_list, 'metadata': {'fps': " + str(fps) + "}}")
    script_lines.append("    with open('simulation_data.pkl', 'wb') as f:")
    script_lines.append("        pickle.dump(data, f)")
    script_lines.append("    print('Done.')")

    script_lines.append("")
    script_lines.append("if __name__ == '__main__':")
    script_lines.append("    main()")

    return "\n".join(script_lines)
