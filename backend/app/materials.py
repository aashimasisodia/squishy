# Material properties for the simulation
# Based on standard physical properties

MATERIALS_DB = {
    "rubber": {
        "density": 1100,  # kg/m^3
        "youngs_modulus": 0.01e9,  # Pa (10 MPa)
        "poisson_ratio": 0.5,
    },
    "steel": {
        "density": 7850,
        "youngs_modulus": 200e9,
        "poisson_ratio": 0.3,
    },
    "copper": {
        "density": 8960,
        "youngs_modulus": 120e9,
        "poisson_ratio": 0.34,
    },
    "aluminum": {
        "density": 2700,
        "youngs_modulus": 69e9,
        "poisson_ratio": 0.33,
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
