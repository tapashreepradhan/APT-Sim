import pandas as pd
import os
import glob

# creating output directory
output_dir = "converted_grid_data"
os.makedirs(output_dir, exist_ok=True)

emittertype = '100_W' # change this to '110_W' depending on the emitter type
# getting all grid data files
grid_files = sorted(glob.glob("../3_TAPsimRun/simulations/100_W/grid_data.*"))

for grid_file in grid_files:
    # extracting time snapshot from filename
    time_snapshot = os.path.splitext(grid_file)[1][1:]

    # output filenames
    lammps_output = os.path.join(output_dir, f"gridEmitter_{time_snapshot}.lmp")

    # reading grid file (skip first 3 lines as in the original script)
    df = pd.read_csv(grid_file, skiprows=3, delimiter='\t')

    # rename columns
    columns = [
        'id', 'uni_num', 'x', 'y', 'z','charge', 'potX', 'potY', 'potZ',
        'efieldvecX', 'efieldvecY', 'efieldvecZ'
    ]
    first_row = df.columns.tolist()
    df.columns = columns

    # converting first row into numeric values (if needed)
    numeric_list = []
    for x in first_row:
        try:
            numeric_list.append(float(x))
        except ValueError:
            if 'e' in x:
                base, exponent = x.split('e')
                numeric_list.append(float(base) * 10 ** float(exponent))

    df.loc[-1] = numeric_list
    df.index = df.index + 1
    df = df.sort_index()

    # extracting emitter nodes where id == 10
    df_emitter = df[df['id'] == 10]

    # Unit conversions
    df_emitter.loc[:, ['x', 'y', 'z']] *= 10**10      # Convert to Ångstroms
    df_emitter.loc[:, ['potX', 'potY', 'potZ']] *= 1.602 * 10**(-9)  # E(V/m) to E(eV/Å)

    # Prepare LAMMPS DataFrame
    df_lammps = pd.DataFrame({
        'id': df_emitter['uni_num'],
        'type': 1,  # Assuming single atom type
        'x': df_emitter['x'],
        'y': df_emitter['y'],
        'z': df_emitter['z'],
        'fx': df_emitter['potX'],
        'fy': df_emitter['potY'],
        'fz': df_emitter['potZ']
    })

    # Reorder IDs to start from 1
    df_lammps['id'] = df_lammps['id'] - df_lammps['id'].min() + 1
    total_atoms = len(df_lammps)

    # Box boundaries
    x_min, x_max = df_lammps['x'].min(), df_lammps['x'].max()
    y_min, y_max = df_lammps['y'].min(), df_lammps['y'].max()
    z_min, z_max = df_lammps['z'].min(), df_lammps['z'].max()

    # Write LAMMPS output
    with open(lammps_output, 'w') as file:
        file.write("ITEM: TIMESTEP\n0\n")
        file.write("ITEM: NUMBER OF ATOMS\n")
        file.write(f"{total_atoms}\n")
        file.write("ITEM: BOX BOUNDS pp pp pp\n")
        file.write(f"{x_min} {x_max}\n{y_min} {y_max}\n{z_min} {z_max}\n")
        file.write("ITEM: ATOMS id type x y z fx fy fz\n")
        df_lammps.to_csv(file, sep='\t', index=False, header=False)

    print(f"Processed: {grid_file} -> {lammps_output}")

print("All grid files successfully converted.")