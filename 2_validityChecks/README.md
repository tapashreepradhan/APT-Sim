# Validity Checks

This directory contains all scripts, input files, and output data used to validate the atomic emitter configurations before they are used in further simulations. The goal is to ensure that the emitters are physically realistic, structurally stable, and suitable for atom probe tomography and molecular dynamics workflows.

## Purpose

Validity checks are essential for confirming that the atomic structures generated in the emitter creation step are correct and reliable. These checks help identify any issues such as incorrect atomic ordering, unwanted defects, or thermal instability that could affect the accuracy of subsequent simulations.

## Workflow Overview

1. **Radial Distribution Function (RDF) Analysis:**  
   The RDF is calculated using LAMMPS to assess the local atomic ordering and crystallinity of the emitter. Peaks in the RDF correspond to preferred interatomic distances, and their positions and sharpness indicate the degree of order in the structure.

2. **Thermodynamic Property Tracking:**  
   Simulations are run to monitor temperature, pressure, and volume over time. Stable values indicate that the emitter is equilibrated and suitable for further simulation.

3. **Structural Output:**  
   Final atomic coordinates and structure files are generated for use in downstream steps. These files are checked for consistency and completeness.

## Subfolder Structure

Each subfolder corresponds to a specific emitter configuration (e.g., `W_100`, `Al_100`) and contains:

- `input/` — Input files for LAMMPS validity check simulations.
- `output/` — Output files including RDF data, thermodynamic logs, and final structure files.
- `plots/` — Plots visualizing RDFs, energy, temperature, and other properties.
- `scripts/` — Python scripts for post-processing and analysis.

## Key Concepts

### Radial Distribution Function (RDF)

- **Definition:** The RDF, \( g(r) \), describes how atomic density varies as a function of distance from a reference atom.
- **Interpretation:**  
  - **First Peak:** Nearest-neighbor distance (e.g., ~2.74 Å for BCC Tungsten).
  - **Second Peak:** Second-nearest neighbor distance (e.g., ~3.15 Å for BCC Tungsten).
  - **Sharp Peaks:** Indicate a well-ordered, crystalline structure.
  - **Broad/Shifted Peaks:** Suggest disorder, defects, or phase transitions.

### Thermodynamic Stability

- **Stable Temperature and Pressure:** Indicates the system is equilibrated.
- **Energy Minimization:** Confirms the structure is at a local minimum and not artificially strained.

### Interpretation for Tungsten

Tungsten (W) is a **BCC (Body-Centered Cubic)** metal at room temperature. In a BCC lattice, atoms are arranged in such a way that the first few neighbor distances are well-defined:

- **First Peak**: Typically corresponds to the **nearest neighbors**, or the distance between the central atom and atoms positioned at the corners of the cube.
- **Second Peak**: This corresponds to the **second-nearest neighbors**, which are atoms in adjacent unit cells (further away but still part of the crystal structure).

### What Two Peaks Represent

- **First Peak (~2.7 - 2.8 Å)**: This is the **nearest-neighbor distance**, which in Tungsten is around **2.74 Å** in a BCC structure.
- **Second Peak (~3.15 Å)**: This is the **next-nearest neighbors**, atoms positioned further away within the BCC unit cell.

### Physical Meaning

- **Sharp and well-defined peaks**: Indicate a well-ordered, crystalline, and stable structure.
- **Broad or shifted peaks**: Could indicate:
    - **Thermal disorder** (higher temperature simulations).
    - **Phase transition** (potential melting or amorphization).
    - **Stress-induced defects**.

### Nearest Neighbor (1NN) Distance in BCC

For a **BCC crystal structure**, the nearest neighbors are located along the **body diagonal** of the cubic cell. The distance between these nearest neighbors (denoted as $(d_{1NN})$) is given by the formula:

$$
d_{1NN} = \frac{\sqrt{3}}{2} \cdot a
$$

Where:
- $(a = 3.165 \, \text{Å})$ is the lattice constant for Tungsten.

$$
d_{1NN} = \frac{\sqrt{3}}{2} \cdot 3.165 \, \text{Å} \approx 2.74 \, \text{Å}
$$

**This aligns almost perfectly with the location of the first RDF peak (~2.7 Å), confirming that the simulation is reproducing the correct BCC atomic structure.**

---

### Second Nearest Neighbor (2NN) Distance in BCC

The **second-nearest neighbors** are atoms located at the corners of adjacent unit cells. The distance between these atoms (denoted as $(d_{2NN}$) is equal to the lattice constant:

$$
d_{2NN} = a
$$

Where:
- $(a = 3.165 \, \text{Å})$.

Thus, the second-nearest neighbor distance $(d_{2NN})$ is:

$$
d_{2NN} = 3.165 \, \text{Å}
$$

**The second RDF peak (~3.15 Å) aligns almost exactly with this expected 2NN distance, further confirming that the system is maintaining the correct BCC structure.**

This RDF analysis validates that the simulation results are in line with the expected crystalline structure of Tungsten.

---

_Last updated: 2025-08-01
