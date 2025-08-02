# MODIFIED VERSION OF PYVAPORATE

Pyvaporate enables the simulated evaporation of
atom-probe tips. It uses a monte carlo approach for evaporation events
(TAPsim), interrupted by molecular dynamics relaxations (LAMMPS) at specified
intervals to allow for simulated temperature and surface migration. Evaporation
fields for each atom in the emitter are updated after each relaxation interval
based on their coordination numbers to allow the dynamic assignment of
site-specific evaporation fields.

# Installation
------
```bash
$ git clone https://github.com/ashtonmv/pyvaporate
```

Add pyvaporate to your `$PYTHONPATH`.

Pyvaporate requires the installation of LAMMPS (molecular dynamics) and TAPSim
(monte carlo field evaporation).

## LAMMPS Installation

```
$ git clone https://github.com/lammps/lammps.git
$ cd lammps/src/
$ make yes-user-meamc
$ make mpi
```

Note the location of the LAMMPS executable (`lmp_mpi`), since you will need this
to run Pyvaporate (see the setup file below).

## TAPSim Installation

Visit [the University of Stuttgart's webpage](http://www.uni-stuttgart.de/imw/mp/forschung/atom_probe_RD_center/software.en.html)
and download the TAPSim tarball. Unpack it and then execute the following:

```
$ cd tapsim_v1.0b_r3225/
$ make
```

Again, note the location of the `tapsim` and `meshgen` binaries created in
`tapsim_v1.0b_r3225/bin` so you can use them in your setup files for Pyvaporate.

# Usage
------

Create a `setup.yaml` file with specifications of the system you wish to evaporate.
Default values exist for most available fields, but the user should familiarize
his/herself with these fields anyway. Below is a sample input file with all
the default values listed:

```yaml
cleanup: false  # Set to `true` to delete large files created by TAPsim
emitter:
  elements:
    W:
      mass: 183.85
      charge: 3
      fract_occ: 1.0  # Fraction of all sites occupied by that element
      e_fields:  # Evaporation fields for atoms of given coordination numbers
        0: 57e-9
        1: 27e-9
        2: 37e-9
        3: 47e-9
        4: 57e-9
        5: 67e-9
        6: 77e-9
        7: 87e-9
        8: 97e-9
        9: 107e-9
  source:
    node_file: none  # If not `none`, read and use an existing node file (specify path to file)
    uc_file: none  # If not `none`, create node file based on a unit cell in a common structure file format (POSCAR, XYZ, etc.)
  basis: BCC
  orientation:
    z: [1, 1, 0]
    y: auto  # Automatically choose an orthogonal set of axes
    x: auto
  radius: 50  # Emitter tip radius in Angstroms
  side_height: 25  # Emitter height before hemispherical tip
evaporation:
  tapsim_bin: ~/bin/tapsim  # Path to your tapsim executable
  meshgen_bin: ~/bin/meshgen  # Path to your meshgen executable
  total_events: 10%  # total_events can be a percentage or an absolute number of evaporated atoms
  events_per_step: 5%  # Same goes for events_per_step
lammps:
  bin: ~/software/lammps/src/lmp_mpi  # Path to your lammps executable
  read_file: none  # Specify the path to a LAMMPS input file to use as a
                   # template for all MD relaxations. If not "none", this
                   # overrides the other commands in this section.
  potentials_location: ~/software/lammps/potentials/library.meam  # MEAM library file. This file is
                                                                  # usually in your lammps/potentials
                                                                  # directory.
  minimize:
    surface_only: true  # Only relax top layer of atoms
    etol: 1e-8  # LAMMPS minimization parameters ...
    ftol: 1e-8
    maxiter: 1000  # Set to 1 to evaporate in "static" mode
    maxeval: 1000
```

After the input file is created, PyVaporate can be called simply by running

```python
> from pyvaporate.run import yaml_run
> yaml_run("path/to/your/setup.yaml")
```

in Python.
