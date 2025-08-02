# Influence of local atomic positions on the simulated evaporation sequence in Atom Probe Tomography

This repository contains all code, data, and analysis for the master thesis **"Influence of local atomic positions on the simulated evaporation sequence in Atom Probe Tomography"** by Tapashree Pradhan (MS Materials Engineering, KU Leuven).

The project provides a complete workflow for simulating and analyzing atom evaporation in atom probe tomography (APT), from initial atomic emitter creation to advanced data analysis. Each directory in the repository corresponds to a major step in the workflow, with dedicated scripts, input files, and documentation.

---

## Repository Structure and Workflow

### 1. `1_emitterCreation/` — Emitter Creation

Contains all resources and scripts for generating atomic emitter geometries for APT simulations. Emitters are constructed for various crystallographic orientations and sizes using LAMMPS input scripts. The workflow includes configuration, simulation, and post-processing steps to ensure physically meaningful atomic models. Each subfolder represents a specific emitter configuration and includes input files, output data, and post-processing scripts.

### 2. `2_validityChecks/` — Validity Checks

Includes scripts and data for validating the atomic emitter configurations. Checks such as radial distribution function (RDF) analysis and thermodynamic property tracking are performed using LAMMPS to confirm structural correctness and stability. The directory provides plots and analysis scripts to interpret the physical meaning of RDF peaks and thermodynamic trends, ensuring emitters are suitable for further simulation.

### 3. `3_TAPSimRun/` — TAPSim Simulation Run

Contains all files and scripts required to set up and execute field evaporation simulations using TAPSim. The workflow covers mesh generation, configuration, simulation execution, and output management. The `run.sh` script automates the process, and simulation results are organized by emitter type. All necessary binaries and configuration files are included.

### 4. `4_TAPSimPostRun/` — TAPSim Post-Processing

Provides scripts for post-processing TAPSim output data. The main tasks are converting grid and surface data files into formats compatible with molecular dynamics simulations and analysis tools. Python scripts automate extraction, unit conversion, and organization of processed files, enabling direct coupling with MD simulations and visualization.

### 5. `5_TAPSimMD/` — TAPSimMD Output Storage

Serves as a repository for TAPSim output files that have been coupled with LAMMPS molecular dynamics simulations. Files are organized by emitter type and relaxation frequency, facilitating comparison and downstream analysis. No scripts are included; this directory is for data storage only.

### 6. `6_Analysis/` — Simulation Analysis

Contains all scripts, notebooks, and output files for analyzing APT simulation results. The analysis framework covers statistical, spatial, and temporal comparisons between simulation cases, including visualization tools for generating publication-quality figures. Subfolders organize results and plots by case and emitter type.

### 7. `7_pyevaporate/` — Modified Pyvaporate

Includes a modified version of the Pyvaporate package. Documentation covers installation, setup, and usage instructions, including sample configuration files and integration with TAPSim and LAMMPS.

### `resources/` — Shared Resources

Provides executables, potential files, and other shared resources required throughout the workflow.

---

## Project Workflow Summary

1. Create emitter geometries using LAMMPS.
2. Validate emitter structures with RDF and thermodynamic checks.
3. Run field evaporation simulations using TAPSim.
4. Post-process TAPSim results for compatibility with MD and analysis.
5. Store TAPSim-LAMMPS output files.
6. Analyze simulation results using statistical, spatial, and temporal methods.
7. Use Pyvaporate for coupled TAPSim-LAMMPS simulations.

---

## Citations

- LAMMPS: https://www.lammps.org/
- TAPSim: http://www.uni-stuttgart.de/imw/mp/forschung/atom_probe_RD_center/software.en.html
- Pyvaporate: Modified from https://github.com/ashtonmv/pyvaporate

---

For detailed instructions and documentation, refer to the README files in each subdirectory.
