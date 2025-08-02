import numpy as np
import os
# conversion factor from Å to m
ang2m = 1e-10

# getting the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# file paths relative to the script directory
material_file_path = os.path.join(script_dir, '..', 'output', 'Material.txt')
vacuum_file_path = os.path.join(script_dir, '..', 'output', 'Vaccum.txt')
fixed_file_path = os.path.join(script_dir, '..', 'output', 'Fixed.txt')

# file definitions
input_files = [
    (material_file_path, 10),
    (vacuum_file_path, 0),
    (fixed_file_path, 2)
]

combinedNode = []

# reading each LAMMPS dump file to extract lattice positions, convert units and
# assign IDs relevant to the TAPSim NODE file requirements
for filename, point_id in input_files:
    with open(filename, 'r') as file:
        lines = file.readlines()

    # finding the line where the atom data starts
    atom_data_start = lines.index('ITEM: ATOMS x y z type\n') + 1

    # processing atom data now
    for line in lines[atom_data_start:]:
        parts = line.split()
        x, y, z = map(float, parts[:3])

        # converting Å to m
        x *= ang2m
        y *= ang2m
        z *= ang2m

        # floating-point cleanup: treat near-zero values as zero
        x = 0.0 if abs(x) < 1e-20 else x
        y = 0.0 if abs(y) < 1e-20 else y
        z = 0.0 if abs(z) < 1e-20 else z
        # appending data in the format required by TAPSim (scientific notation + ID)
        combinedNode.append(f'{x:.8E}\t{y:.8E}\t{z:.8E}\t{point_id}'.strip())

# total number of data points
total_points = len(combinedNode)

# writing the combined data to the NODE file in ASCII format
output_file = 'NODE.txt'
with open(output_file, 'w') as file:
    file.write(f'ASCII {total_points} 0 0\n')
    file.write('\n'.join(combinedNode).strip())

print(f'Combined data written to {output_file} with {total_points} points.')