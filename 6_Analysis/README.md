# Simulation Analysis

This directory contains all scripts, notebooks, and output files used for the analysis of atom probe tomography (APT) simulation results. The goal is to provide a comprehensive framework for statistical, spatial, and comparative analysis of evaporation behavior across different simulation cases and emitter configurations.

## Purpose

The analysis performed in this directory helps interpret the physical meaning of the simulation results, quantify differences between methods (such as TAPSim-only vs. TAPSim with MD relaxation), and visualize key trends in atomic evaporation, emitter morphology, and sequence reordering.

## Workflow Overview

1. **Data Loading:**  
   Scripts and notebooks load processed results from TAPSim and MD-coupled simulations. Data includes atomic positions, evaporation sequences, timing information, and field values.

2. **Statistical Analysis:**  
   Notebooks and scripts perform statistical comparisons between cases, including mean, median, variance, and distribution profiles of key quantities (e.g., apex height, evaporation timing).

3. **Spatial Analysis:**  
   Tools are provided for analyzing the spatial distribution of evaporated atoms, center of mass evolution, and root mean square displacement (RMSD) between cases.

4. **Temporal Shift Analysis:**  
   Specialized routines quantify how the evaporation sequence changes between simulation methods, including timing differences, sequence reordering, and atomic correspondence.

5. **Visualization:**  
   The directory includes scripts and utilities for generating publication-quality plots, such as KDE heatmaps, box plots, scatter plots, and time series of physical properties.

## Directory Structure

- **Jupyter Notebooks:**  
  Main analysis notebooks (e.g., `W_100.ipynb`, `Al_100.ipynb`, `Al_CSL.ipynb`) work through each analysis step, from loading data to generating figures and interpreting results.

- **scripts/**  
  Contains Python scripts for modular analysis tasks:
  - `load_data.py`: Load and parse simulation output files.
  - `compare_ids.py`: Jaccard similarity and atomic correspondence analysis.
  - `spatial_analysis.py`: Center of mass and RMSD comparisons.
  - `displacement_analysis.py`: Trends in evaporation height and displacement.
  - `plot_utils.py`: Functions for clean, labeled plotting.

- **Case Subfolders:**  
  Subdirectories (e.g., `Case2_W`, `Case3_Al`) store results data for each simulation case, organized for batch analysis.

- **Plots Subfolders:**  
  Output directories (e.g., `Plots_W100`, `Plots_Al100`) contain generated figures and visualizations.

## Notes

- All analysis steps are documented in the notebooks and scripts for reproducibility.
- Results from this directory support the main conclusions and figures in the thesis.

---

_Last updated: 2nd August 2025_
