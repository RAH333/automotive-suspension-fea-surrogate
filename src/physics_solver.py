"""
Simulates structural stress, deflection, and fatigue life for an automotive control arm
using analytical beam/FEA boundary approximations and Latin Hypercube Design of Experiments (DOE).
"""


import numpy as np
import pandas as pd
from scipy.stats import qmc


class ControlArmPhysicsModel:
    """Analytical structural & fatigue solver for an automotive suspension control arm."""

    def __init__(self, yield_strength_mpa: float = 350.0, elastic_modulus_gpa: float = 205.0):
        self.yield_strength = yield_strength_mpa
        self.E = elastic_modulus_gpa * 1e3  # Convert GPa to MPa

    def evaluate_design(self, length_mm: float, thickness_mm: float, fillet_radius_mm: float, load_n: float) -> dict:
        # Effective cross-section modulus (mm^3) and second moment of area (mm^4)
        width_mm = 45.0
        moment_of_inertia = (width_mm * (thickness_mm ** 3)) / 12.0
        section_modulus = moment_of_inertia / (thickness_mm / 2.0)

        # Stress concentration factor (Kt) driven by fillet radius
        kt = 1.0 + 1.8 * np.exp(-0.25 * fillet_radius_mm)

        # Peak Von Mises equivalent stress (MPa)
        bending_moment = load_n * length_mm
        nominal_stress = bending_moment / section_modulus
        max_stress_mpa = nominal_stress * kt

        # Maximum tip deflection (mm)
        max_deflection_mm = (load_n * (length_mm ** 3)) / (3.0 * self.E * moment_of_inertia)

        # Safety factor and Basquin fatigue life estimation (cycles)
        safety_factor = self.yield_strength / max_stress_mpa
        fatigue_cycles = 1e6 * ((self.yield_strength / (max_stress_mpa * 1.4)) ** 3.2)

        return {
            "length_mm": round(length_mm, 2),
            "thickness_mm": round(thickness_mm, 2),
            "fillet_radius_mm": round(fillet_radius_mm, 2),
            "load_n": round(load_n, 2),
            "max_stress_mpa": round(max_stress_mpa, 2),
            "max_deflection_mm": round(max_deflection_mm, 3),
            "safety_factor": round(safety_factor, 2),
            "fatigue_cycles": int(min(fatigue_cycles, 1e8)),
        }


def generate_doe_dataset(n_samples: int = 250, seed: int = 42) -> pd.DataFrame:
    """Generates a Latin Hypercube Design of Experiments (DOE) dataset."""
    sampler = qmc.LatinHypercube(d=4, seed=seed)
    sample = sampler.random(n=n_samples)

    # Bounds: [length_mm, thickness_mm, fillet_radius_mm, load_n]
    lower_bounds = [280.0, 10.0, 2.0, 1500.0]
    upper_bounds = [360.0, 22.0, 10.0, 4500.0]
    scaled = qmc.scale(sample, lower_bounds, upper_bounds)

    solver = ControlArmPhysicsModel()
    records = [solver.evaluate_design(*row) for row in scaled]
    return pd.DataFrame(records)


if __name__ == "__main__":
    df = generate_doe_dataset()
    df.to_csv("data/doe_simulation_dataset.csv", index=False)
    print(f"Generated {len(df)} DOE simulation runs.")
  
