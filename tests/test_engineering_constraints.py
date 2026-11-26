"""
Provides automated unit tests to verify boundary conditions and physical monotonicity.
"""



from src.physics_solver import ControlArmPhysicsModel
from src.verification_rubric import evaluate_candidate_design


def test_fillet_radius_reduces_stress():
    solver = ControlArmPhysicsModel()
    sharp_corner = solver.evaluate_design(300.0, 15.0, 2.0, 2500.0)
    smooth_fillet = solver.evaluate_design(300.0, 15.0, 8.0, 2500.0)
    assert smooth_fillet["max_stress_mpa"] < sharp_corner["max_stress_mpa"]


def test_rubric_passes_valid_geometry():
    report = evaluate_candidate_design(
        {"length_mm": 300.0, "thickness_mm": 19.0, "fillet_radius_mm": 7.0, "load_n": 2400.0}
    )
    assert report["status"] == "PASS"
  
