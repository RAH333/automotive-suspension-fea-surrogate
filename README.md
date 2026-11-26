# automotive-suspension-fea-surrogate

# Automotive Suspension Control Arm: DOE Simulation & Surrogate Validation

## Overview
An end-to-end engineering simulation, Design of Experiments (DOE), and automated verification pipeline built in Python. This repository demonstrates physics-based stress/fatigue modeling, surrogate machine learning prediction, and automated design verification rubrics for automotive mechanical components.

## Key Engineering Capabilities
* **Parametric Physics & Fatigue Modeling (`src/physics_solver.py`):** Evaluates Von Mises stress, tip deflection, stress concentration factors ($K_t$), and Basquin fatigue life across varying geometric and load boundary conditions using Latin Hypercube Sampling (DOE).
* **ML Surrogate Modeling (`src/surrogate_model.py`):** Trains a Gradient Boosting regressor on simulation outputs to rapidly predict structural stress and component degradation.
* **Automated Design Verification Rubric (`src/verification_rubric.py`):** Validates proposed geometries against strict automotive safety factors ($\ge 1.5$), deflection limits ($\le 2.5\text{ mm}$), and fatigue cycle thresholds.

## Quick Start
```bash
pip install -r requirements.txt
mkdir -p data
python src/physics_solver.py
python src/surrogate_model.py
python src/verification_rubric.py
pytest
```



It combines mechanical simulation, Design of Experiments (DOE), and Python predictive validation. bridge classical mechanical design (stress/fatigue validation) with Python-based simulation and verification rubrics.

```
automotive-suspension-fea-surrogate/
├── README.md
├── requirements.txt
├── data/
│   └── doe_simulation_dataset.csv
├── src/
│   ├── physics_solver.py
│   ├── surrogate_model.py
│   └── verification_rubric.py
└── tests/
    └── test_engineering_constraints.py
```
