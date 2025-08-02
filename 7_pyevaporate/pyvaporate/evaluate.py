def assign_ids_by_cn(lammps_file):
    """
    Assign ID's to distinguish between atoms of various
    coordinations.
    1. reads a LAMMPS data file -> contains atom positions, types, and CN
    2. for each atom, modifies the atom type (ID) based on its CN
    3. atoms with lower CN will have different IDs than atoms with higher CN.
    helpful to differentiate surface atoms (low CN) from bulk atoms (high CN)
    """

    lammps_lines = open(lammps_file).readlines()
    with open(lammps_file, "w") as l:
        for line in lammps_lines[:9]:
            l.write(line)
        for line in lammps_lines[9:]:
            sl = line.split()
            original_atom_base = sl[-2]+"0"
            cn = int(sl[-1])
            if cn > 9:
                cn = 9
            atom_type = str(int(original_atom_base)+cn)
            sl[3] = atom_type
            l.write(" ".join(sl))
            l.write("\n")