# Material properties for the simulation
# Based on standard physical properties from:
# - https://www.sonelastic.com/en/fundamentals/tables-of-materials-properties/polymers.html
# - https://www.engineersedge.com/materials/poissons_ratio_metals_materials_chart_13160.htm

MATERIALS_DB = {
    # --- METALS ---
    "steel": {
        "density": 7850,
        "youngs_modulus": 200e9,
        "poisson_ratio": 0.29, # Average of range 0.27-0.30
    },
    "stainless_steel": {
        "density": 8000,
        "youngs_modulus": 193e9,
        "poisson_ratio": 0.305, # Average of 0.30-0.31
    },
    "copper": {
        "density": 8960,
        "youngs_modulus": 120e9,
        "poisson_ratio": 0.33,
    },
    "aluminum": {
        "density": 2700,
        "youngs_modulus": 69e9,
        "poisson_ratio": 0.32, # 2024-T4
    },
    "brass": {
        "density": 8500, # Approx for yellow brass
        "youngs_modulus": 100e9,
        "poisson_ratio": 0.331,
    },
    "titanium": {
        "density": 4500,
        "youngs_modulus": 110e9,
        "poisson_ratio": 0.34,
    },
    "gold": {
        "density": 19300,
        "youngs_modulus": 79e9,
        "poisson_ratio": 0.43, # Average of 0.42-0.44
    },
    "magnesium": {
        "density": 1740,
        "youngs_modulus": 45e9,
        "poisson_ratio": 0.35,
    },
    "zinc": {
        "density": 7140,
        "youngs_modulus": 108e9, # Varies, typical value
        "poisson_ratio": 0.331,
    },

    # --- POLYMERS ---
    "rubber": {
        "density": 1100,
        "youngs_modulus": 0.01e9,  # 10 MPa (Soft rubber)
        "poisson_ratio": 0.50, # Approximate for rubber
    },
    "pvc": { # Poly (vinyl chloride)
        "density": 1380,
        "youngs_modulus": 3.275e9, # Average of 2.41-4.14 GPa
        "poisson_ratio": 0.38,
    },
    "nylon": { # Nylon 6.6
        "density": 1150,
        "youngs_modulus": 2.69e9, # Average of 1.59-3.79 GPa
        "poisson_ratio": 0.39,
    },
    "polycarbonate": { # PC
        "density": 1200,
        "youngs_modulus": 2.38e9,
        "poisson_ratio": 0.36, # Using 0.36 from source (0.345 also listed)
    },
    "polystyrene": { # PS
        "density": 1050,
        "youngs_modulus": 2.78e9, # Average of 2.28-3.28 GPa
        "poisson_ratio": 0.33,
    },
    "polyethylene": { # LDPE
        "density": 920,
        "youngs_modulus": 1.08e9,
        "poisson_ratio": 0.157, # Wait, LDPE usually has higher Poisson ratio (~0.49). Source says 0.157?? 
                                # Re-checking standard engineering values: LDPE is typically ~0.49.
                                # The source provided (Sonelastic) lists 0.157 for LDPE. We will stick to the user provided source
                                # but add a comment.
                                # Actually, standard FEA practice uses ~0.49 for LDPE. 0.157 is extremely low for a polymer.
                                # However, I must follow the provided source.
        "poisson_ratio": 0.157, 
    },
    "peek": { # Polyetheretherketone
        "density": 1320,
        "youngs_modulus": 1.10e9, # Source says 1.10 GPa? Typically PEEK is ~3.6 GPa. Using source value.
        "poisson_ratio": 0.16,
    },
    "epoxy": {
        "density": 1200, # Approximate
        "youngs_modulus": 2.41e9,
        "poisson_ratio": 0.35,
    },
    "acrylic": { # PMMA
        "density": 1180,
        "youngs_modulus": 2.74e9, # Average of 2.24-3.24 GPa
        "poisson_ratio": 0.325, # Using lower bound of 0.325-0.470 range
    },

    # --- OTHER ---
    "glass": {
        "density": 2500,
        "youngs_modulus": 70e9,
        "poisson_ratio": 0.24, # Average of 0.18-0.3
    },
    "concrete": {
        "density": 2400,
        "youngs_modulus": 30e9,
        "poisson_ratio": 0.20,
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
        lines.append(f"- {name} (E={props['youngs_modulus']/1e9:.3f} GPa, rho={props['density']} kg/m^3)")
    return "\n".join(lines)
