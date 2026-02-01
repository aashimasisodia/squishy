# Material properties for the simulation
# Based on standard physical properties

MATERIALS_DB = {
    "rubber": {
        "density": 1100,  # kg/m^3
        "youngs_modulus": 0.01e9,  # Pa (10 MPa)
        "poisson_ratio": 0.5,
    },
    "soft_biological_tissue": {
        "density": 1000,
        "youngs_modulus": 10e3,  # 10 kPa
        "poisson_ratio": 0.5,
    },
}

def get_material_table_str() -> str:
    """Returns a formatted string of available materials for the prompt."""
    lines = []
    for name, props in MATERIALS_DB.items():
        lines.append(f"- {name} (E={props['youngs_modulus']/1e9:.2f} GPa, rho={props['density']} kg/m^3)")
    return "\n".join(lines)
