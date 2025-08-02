# TAPSim Simulation Run

This directory contains all files, scripts, and configuration resources required to set up and execute field evaporation simulations using TAPSim. TAPSim is a specialized tool for modelling atom probe tomography (APT) by simulating the field-driven evaporation of atoms from a tip-shaped emitter.

## Purpose

The main goal of this directory is to provide a reproducible workflow for running TAPSim simulations on different emitter configurations. It covers the entire process from mesh generation and configuration to execution and output management.

## Workflow Overview

1. **Mesh Generation:**  
   The `meshgen` binary and `meshgen.ini` configuration file are used to generate a computational mesh for the emitter geometry. This mesh defines the spatial domain for the field evaporation simulation.

2. **Configuration:**  
   The `NODE.txt` file (from emitter creation) and the mesh are used to create a TAPSim configuration file (`*_Mesh.cfg`). User input is required to specify physical parameters such as element name, mass, charge state, and evaporation field strength.

3. **Simulation Execution:**  
   The `run.sh` script automates the setup and execution of TAPSim. It copies necessary files, generates the mesh, updates configuration parameters, and runs TAPSim in the background. Simulation progress and results are logged.

4. **Output Management:**  
   Simulation results are stored in the `simulations/` subdirectory, organized by emitter type (e.g., `Al_100_1000_0`, `W_100_1000_0`). Output files include grid data, surface data, and results data, which are compressed into a tar archive for easy management.

## Directory Contents

- `meshgen.ini`: Configuration file for mesh generation.
- `tapsim.ini`: Configuration file for TAPSim simulation parameters.
- `run.sh`: Bash script to automate the simulation workflow.
- `simulations/`: Subdirectory containing all simulation outputs, organized by emitter type.

## How to Use

1. Set the desired emitter type in `run.sh` (e.g., `EMITTER_TYPE="100_W"`).
2. Ensure that all required binaries and input files are available in the specified locations.
3. Run `run.sh` from the command line to start the simulation workflow.
4. Follow prompts to enter physical parameters for the simulation.
5. After completion, find all output files in the appropriate subfolder under `simulations/`.

## Notes

- The TAPSim binaries (`meshgen`, `tapsim`) must be compiled and placed in the `resources/executables` directory.
- The workflow assumes that emitter node files have been generated in the emitter creation step.
- Output files are compressed for convenience; decompress as needed for post-processing and analysis.

---
_Last updated: 2nd August 2025_
