"""
This python script is essentially the workflow automation script for running TAPSim-LAMMPS simulations.
Here's the typical workflow of the script:
- generates a TAPSim emitter mesh from a node file
- runs field evaporation simulations in TAPSim
- relax the structure using LAMMPS molecular dynamics
- convert data between TAPSim and LAMMPS formats
"""
import subprocess
import os

from pyvaporate.evaluate import assign_ids_by_cn
from pyvaporate.mgn import mgn_ini_lines, mesh_cfg_lines

from monty.serialization import loadfn


def call_meshgen(setup, node_file):
    """
    1. Run the `meshgen` script (part of TAPSim) to generate a mesh file from the node file.
    2. Writes the meshgen.ini (default configuration to avoid interactive prompts)
    3. Adds a comment to `mesh.txt` listing element IDs and their corresponding names.
    4. Writes the `mesh.cfg` file with the evaporaton properties.
    """
    write_meshgen_ini()

    _ = subprocess.check_output(
        [setup["evaporation"]["meshgen_bin"], node_file, "mesh.txt",
         "--create-config-template=mesh.cfg", "--write-ascii"]
    )
    with open("mesh.txt", "a") as m:
        comment = "#"
        for ID in setup["id_dict"]:
            comment += " {}={}".format(ID, setup["id_dict"][ID])
        m.write(comment)

    write_mesh_cfg(setup)

def call_tapsim(setup):
    """
    Run the TAPSim program, starting with building a voronoi mesh for
    an emitter (node) file and then running a set number of
    evaporation steps before stopping.
    """

    _ = subprocess.check_output(
        [setup["evaporation"]["tapsim_bin"], "evaporation", "mesh.cfg", "mesh.txt",
         "--event-limit={}".format(setup["evaporation"]["events_per_step"]), "--write-ascii"]
    )
    update_mesh()


def update_mesh():
    """
    Remove evaporated nodes from the TAPSim mesh.
    1. reads the `mesh.txt` (the current state of the emitter)
    2. scans the results_data files (TAPSim output), which lists the evaporated atoms
    3. updates the `mesh.txt` to mark evaporated atoms by setting their type to 0.
    4. writes an `updated_mesh.txt` file.
    """
    emitter_lines = open("mesh.txt").readlines()
    results_files = [f for f in os.listdir(os.getcwd()) if "results_data" in f]
    remove_ids = []
    for f in results_files:
        results_lines = open(f).readlines()
        results_lines = results_lines[results_lines.index("ASCII\n")+1:]
        remove_ids += [line.split()[2] for line in results_lines]
    new_emitter_lines = []
    i = 1
    for line in emitter_lines[1:-1]:
        sl = line.split()
        if str(i) in remove_ids:
            sl = [sl[0], sl[1], sl[2], "0", "0"]
        new_line = "{}\n".format("	".join(sl))
        new_emitter_lines.append(new_line)
        i += 1
    with open("updated_mesh.txt", "w") as ue:
        ue.write(emitter_lines[0])
        for line in new_emitter_lines:
            ue.write(line)
        ue.write(emitter_lines[-1])


def write_meshgen_ini():
    """
    Write the default meshgen.ini file so that
    meshgen doesn't ask for it mid-run and
    interrupt the python process.
    """
    with open("meshgen.ini", "w") as mgn:
        for line in mgn_ini_lines:
            mgn.write(line)


def write_mesh_cfg(setup):
    """
    Writes a `mesh.cfg` file describing the physical 
    and evaporation properties for each element type.
    This is what TAPSim uses to determine how atoms evaporate.
    """
    with open("mesh.cfg", "w") as cfg:
        for line in mesh_cfg_lines:
            cfg.write(line)
        for elt in setup["emitter"]["elements"]:
            charge = setup["emitter"]["elements"][elt]["charge"]
            mass = setup["emitter"]["elements"][elt]["mass"]
            for e_field in setup["emitter"]["elements"][elt]["e_fields"]:
                cfg.write("\n")
                f = setup["emitter"]["elements"][elt]["e_fields"][e_field]
                base_id = [
                    i for i in setup["id_dict"] if setup["id_dict"][i] == elt
                ][0]
                ID = str(int(e_field)+int(base_id))
                cfg.write("ID = {}\n".format(ID))
                cfg.write("NAME = {}_{}\n".format(elt, e_field))
                cfg.write("CHARGE_DENSITY = 0.00000e+00\n")
                cfg.write("DIELECTRICITY = 1.00000e+00\n")
                cfg.write("REMOVABLE = 1\n")
                cfg.write("NEUMANN_BOUNDARY = 0\n")
                cfg.write("DIRICHLET_BOUNDARY = 1\n")
                cfg.write("POTENTIAL = 1.00000e+03\n")
                cfg.write("MASS = {}\n".format(mass))
                cfg.write("EVAPORATION_CHARGE_STATE = {}\n".format(charge))
                cfg.write("EVAPORATION_FIELD_STRENGTH = {}\n".format(f))
                cfg.write("EVAPORATION_ACTIVATION_ENERGY = 1.00000e+00\n")


def call_lammps(n_nodes, setup):
    """
    Convert a TAPSim emitter node file to a LAMMPS
    structure (Only the actual atoms, not the vacuum nodes,
    etc) and then make a call to LAMMPS to relax it.
    1. prepares the emitter (after evaporation) for LAMMPS relaxation
    2. converts the `updated_mesh.txt` to a LAMMPS data file
    3. runs LAMMPS to relax the structure
    4. re-assigns coordination numbers to atoms after relaxation
    5. converts the relaxed LAMMPS structure back to a TAPSim emitter node file
    6. adds the vacuum nodes back to the emitter node file
    """

    convert_emitter_to_lammps(find_surface_atoms(), setup)
    write_lammps_input_file(setup)

    _ = subprocess.check_output([setup["lammps"]["bin"], "-l", "log.lammps",
                                 "-i", "in.emitter_relax"])
    assign_ids_by_cn("relaxed_emitter.lmp")
    convert_lammps_to_emitter(n_nodes)
    add_original_vacuum_nodes()


def find_surface_atoms():
    """
    Read from the TAPSim-generated surface_data file
    which atoms are at the emitter's surface. This is
    convenient if these are the only atoms you want to
    allow to relax in LAMMPS (surface_only: true in your
    setup.yaml) to speed up the relaxation.
    """

    surface_files = [f for f in os.listdir(os.getcwd()) if "surface_data" in f]
    if len(surface_files):
        surface_file = surface_files[-1]
        surface_lines = open(surface_file).readlines()
        surface_numbers = []
        for line in surface_lines[5:]:
            split_line = line.split()
            if len(split_line) == 0:
                break
            elif split_line[1] == "10":
                surface_numbers.append(split_line[0])
    else:
        surface_numbers = []
    return surface_numbers


def convert_emitter_to_lammps(surface_numbers, setup):
    """
    Convert a TAPSim emitter node file to a LAMMPS
    structure file.
    """

    emitter_lines = open("updated_mesh.txt").readlines()
    atom_lines = [l for l in emitter_lines[1:-1] if l.split()[-2] not in
                  ["0", "1", "2", "3"]]
    atom_types = [t.split("=")[0][0] for t in emitter_lines[-1].split()[1:]]
    atom_names = [t.split("=")[1] for t in emitter_lines[-1].split()[1:]]

    atom_coords = []
    n = 1
    for line in atom_lines:
        split_line = line.split()
        atom_coords.append(
            [str(n), split_line[-2][0]]+
            [str(float(x)*1e10) for x in split_line[:3]]
        )
        n += 1

    x_coords = [float(a[2]) for a in atom_coords]
    y_coords = [float(a[3]) for a in atom_coords]
    z_coords = [float(a[4]) for a in atom_coords]
    xlim = (min(x_coords)-10, max(x_coords)+10)
    ylim = (min(y_coords)-10, max(y_coords)+10)
    zlim = (min(z_coords)-10, max(z_coords)+10)

    with open("data.emitter", "w") as dat:
        dat.write("LAMMPS Emitter\n\n")
        dat.write("{} atoms\n\n".format(len(atom_lines)))
        dat.write("{} atom types\n\n".format(len(atom_types)))
        dat.write("{} {} xlo xhi\n".format(xlim[0], xlim[1]))
        dat.write("{} {} ylo yhi\n".format(ylim[0], ylim[1]))
        dat.write("{} {} zlo zhi\n\n".format(zlim[0], zlim[1]))
        dat.write("Masses\n\n")
        for i in range(len(atom_types)):
            dat.write("{} {}\n".format(
                atom_types[i],
                setup["emitter"]["elements"][atom_names[i]]["mass"])
            )
        dat.write("\nAtoms\n\n")
        fixed_indices = []
        for atom in atom_coords:
            if atom[0] not in surface_numbers:
                fixed_indices.append(atom[0])
            dat.write("{}\n".format(" ".join(atom)))
    with open("fixed_indices.txt", "w") as fi:
        for index in fixed_indices:
            fi.write("{}\n".format(index))


def convert_lammps_to_emitter(n_nodes):
    """
    Convert a relaxed LAMMPS structure file back to
    a TAPSim emitter node file.
    """

    xyz_lines = open("relaxed_emitter.lmp").readlines()
    with open("relaxed_emitter.txt", "w") as e:
        e.write("ASCII {} 0 0\n".format(n_nodes))
        i = 1
        for line in xyz_lines[9:]:
            sl = line.split()
            x = str(float(sl[0])*1e-10)
            y = str(float(sl[1])*1e-10)
            z = float(sl[2])*1e-10

            # Check if the z-coordinate is beyond e-10 precision limit
            if abs(z) < 1e-10:
                z = 0.0  # Set to zero if beyond e-10 precision limit
                z = str(z)
            else:
                z = str(z)
            atom_type = sl[3]
            n_lost = 0
            if atom_type[-1] == "0":
                n_lost += 1
            else:
                e.write("{}\n".format("	".join([x, y, z, "10", "0"])))
            i += 1
    print("{} atoms lost from surface".format(n_lost))


def add_original_vacuum_nodes():
    """
    Add the vaccuum, etc. nodes back to a TAPSim
    emitter node file created from a LAMMPS structure,
    which neither needs nor has these nodes.
    """
    original_emitter_lines = open("../0/mesh.txt").readlines()
    original_vacuum_lines = [
        l for l in original_emitter_lines[1:] if l[0] == "#" or
        l.split()[3] in [str(i) for i in range(4)]
    ]

    emitter_lines = open("relaxed_emitter.txt").readlines()
    emitter_lines = [
        l for l in emitter_lines[1:-1] if l.split()[3] not in
        ["0", "2"]
    ]
    n_nodes = len(emitter_lines)+len(original_vacuum_lines)-1

    with open("relaxed_emitter.txt", "w") as e:
        e.write("ASCII {} 0 0\n".format(n_nodes))
        for line in emitter_lines + original_vacuum_lines:
            e.write(line)


def write_lammps_input_file(setup):
    """
    Write the input file specifying the type
    of relaxation to perform in LAMMPS.
    """

    etol = setup["lammps"]["minimize"]["etol"]
    ftol = setup["lammps"]["minimize"]["ftol"]
    maxiter = setup["lammps"]["minimize"]["maxiter"]
    maxeval = setup["lammps"]["minimize"]["maxeval"]
    temp = setup["lammps"]["minimize"]["temperature"]
    pot = setup["lammps"]["potentials_location"]
    elts = " ".join(setup["emitter"]["elements"])

    fixed_indices = [l.replace("\n", "") for l in open("fixed_indices.txt").readlines()]
    with open("in.emitter_relax", "w") as er:
        er.write("# Emitter Relaxation\n\n")
        er.write("units real\natom_style atomic\n\nread_data data.emitter\n\n")
        er.write("pair_style eam/alloy\n")
        er.write("pair_coeff * * %s %s\n\n" % (pot, elts))
        er.write("neighbor 1.0 bin\n")
        if setup["lammps"]["minimize"]["surface_only"] == True:
            er.write("group inner id {}\n".format(" ".join([i for i in fixed_indices])))
            er.write("velocity inner set 0 0 0\n")
            er.write("fix frozen inner setforce 0 0 0\n\n")
        er.write("compute cnum all coord/atom cutoff 3.0\n")
        er.write("dump 1 all custom 1000 cnum.dump c_cnum\n")
        er.write("fix 1 all nvt temp %s %s 100.0\n" % (temp, temp))
        er.write("minimize %s %s %s %s\n" % (etol, ftol, maxiter, maxeval))
        er.write("compute 1 all coord/atom cutoff 3.0\n")
        er.write("write_dump all custom relaxed_emitter.lmp x y z type c_cnum")