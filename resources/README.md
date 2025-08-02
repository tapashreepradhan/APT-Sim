# Resources Directory

This directory contains files that are used across different stages of the simulation. These files should not be duplicated in other folders but rather referenced using relative paths.

## Contents

### `executables/`
- **lmp**: The LAMMPS executable, which is used to run the simulations. It can be invoked from various scripts by referencing this path.

### `potentials/`
- **W_MNB_JPCM17.eam.fs**: The potential file used in LAMMPS simulations for defining material interactions. This file is referenced in the input files for emitter creation and simulations.

## How to Reference Resources in Your Workflow

Instead of duplicating the files in each simulation directory, reference the resources using relative paths in your input files and scripts. For example:
```
pair_coeff * * resources/potentials/W_MNB_JPCM17.eam.fs