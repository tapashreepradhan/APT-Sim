# Emitter Creation

This directory contains all resources and scripts required to generate atomic emitter geometries for atom probe tomography simulations. The emitters are constructed for various crystallographic orientations and sizes, and serve as the starting point for subsequent simulation steps in the workflow.

## Purpose

The main goal of this directory is to provide a reproducible and organized workflow for building atomic models of emitter tips. These models are used as input for molecular dynamics and field evaporation simulations. The emitter creation process ensures that the atomic structure, geometry, and boundary conditions are physically meaningful and tailored for the intended simulation scenario.

## Workflow Overview

1. **Configuration:**  
   Define the emitter geometry, material type, and crystallographic orientation using LAMMPS input scripts.

2. **Simulation:**  
   Run LAMMPS to generate the atomic structure, perform energy minimization, and output the relevant atom positions and regions (e.g., material, vacuum, fixed base).

3. **Post-processing:**  
   Use Python scripts to process the simulation output, generate node files for TAPSim, and prepare the emitter for further analysis or simulation.

## Subfolder Structure

Each subfolder corresponds to a specific emitter configuration (e.g., `100_W`, `110_W`, `100_Al`, etc.) and contains:

- `input/` — LAMMPS input scripts and configuration files for emitter setup.
- `output/` — Output files from LAMMPS simulations, including atomic coordinates, region definitions, and log files.
- `scripts/` — Python scripts for post-processing, node file generation, and visualization.

## How to Use

1. Select the desired emitter configuration subfolder.
2. Edit the input files in the `input/` directory as needed for your simulation parameters.
3. Run the LAMMPS simulation using the provided input script.
4. Use the scripts in the `scripts/` directory to process the output and prepare files for TAPSim or other downstream applications.

## Notes

- The emitter geometries generated here are intended for use in the subsequent steps of the thesis workflow, including validity checks, field evaporation simulations, and molecular dynamics coupling.
- For details on each configuration and its physical meaning, refer to the README files within each subfolder.

---
