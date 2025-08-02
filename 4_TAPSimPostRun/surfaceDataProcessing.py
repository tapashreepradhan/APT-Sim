import pandas as pd
import os
import glob

# creating output directory if it doesn't exist
output_dir = "converted_surface_data"
os.makedirs(output_dir, exist_ok=True)

emittertype = '100_W' # change this to '110_W' depending on the emitter type
# getting all surface data files
surface_files = sorted(glob.glob("../3_TAPsimRun/simulations/{emittertype}/surface_data.*"))

for surfaceFile in surface_files:
    # extracting time snapshot from the filename
    time_snapshot = os.path.splitext(surfaceFile)[1][1:]
    
    # defining output file paths
    surface_csv = os.path.join(output_dir, f'surfaceEmitter_{time_snapshot}.csv')
    surface_lmp = os.path.join(output_dir, f'surfaceEmitter_{time_snapshot}.lmp')

    # finding the line number where NODES keyword is located
    linNum = 0
    with open(surfaceFile, 'r') as file:
        for line in file:
            if 'NODES' in line:
                break
            linNum += 1

    df = pd.read_csv(surfaceFile, delimiter='\t', skiprows=linNum+1)

    # converting the coordinates tuple into separate columns
    coords_tuple = df.iloc[:, 1]
    tuple_name = pd.Series(coords_tuple.iloc[0].strip("()").split(", "))  # Extracting first row for column names
    coords_extracted = coords_tuple.str.extract(r'\(([^,]+), ([^,]+), ([^,]+)\)')  # Splitting the tuple
    coords_extracted.columns = tuple_name
    coords_extracted = coords_extracted.astype(float)

    # concatenating extracted columns to original dataframe
    df = pd.concat([df, coords_extracted], axis=1)
    label = str(df.columns[1])
    df.drop(label, axis=1, inplace=True)
    columns = ['node index', 'charge', 'efieldX', 'efieldY', 'efieldZ', 'unitX', 'unitY', 'unitZ', 'x', 'y', 'z']
    firstRow = df.columns.tolist()
    df.columns = columns

    # convert first row into numeric values
    numeric_list = []
    for x in firstRow:
        try:
            numeric_list.append(float(x))
        except ValueError:
            if 'e' in x:
                parts = x.split('e')
                if len(parts) == 2:
                    base = float(parts[0])
                    exponent = float(parts[1])
                    numeric_list.append(base * 10 ** exponent)

    df.loc[-1] = numeric_list
    df.index = df.index + 1
    df = df.sort_index(axis=0)
    
    # dropping unnecessary columns
    df.drop(['unitX', 'unitY', 'unitZ'], axis=1, inplace=True)

    # extracting emitter atoms (charge == 1000) and converting units
    dfEmitter = df[df['charge'] == 1000]
    dfEmitter[['x', 'y', 'z']] = dfEmitter[['x', 'y', 'z']] * 10**10  # Convert meters to Ångstroms
    dfEmitter[['efieldX', 'efieldY', 'efieldZ']] = dfEmitter[['efieldX', 'efieldY', 'efieldZ']] * 1.602 * 10**(-9)  # Convert E(V/m) to E(eV/Å)
    dfEmitter.drop('charge', axis=1, inplace=True)

    print(f"Starting the conversion to LAMMPS format for {surfaceFile} ..\n")

    # reordering columns for LAMMPS format
    dfLammps = dfEmitter[['node index', 'node index', 'x', 'y', 'z', 'efieldX', 'efieldY', 'efieldZ']]
    dfLammps.columns = ['id', 'type', 'x', 'y', 'z', 'fx', 'fy', 'fz']

    # atom type modification
    dfLammps['type'] = 1

    # reordering atom IDs
    dfLammps['id'] = dfLammps['id'] - dfLammps['id'].min() + 1

    total_atoms = len(dfLammps)

    # getting boundaries
    x_min, x_max = dfLammps['x'].min(), dfLammps['x'].max()
    y_min, y_max = dfLammps['y'].min(), dfLammps['y'].max()
    z_min, z_max = dfLammps['z'].min(), dfLammps['z'].max()

    # writing LAMMPS file
    with open(surface_lmp, 'w') as file:
        file.write("ITEM: TIMESTEP\n0\n")
        file.write("ITEM: NUMBER OF ATOMS\n")
        file.write(f"{total_atoms}\n")
        file.write("ITEM: BOX BOUNDS pp pp pp\n")
        file.write(f"{x_min} {x_max}\n")
        file.write(f"{y_min} {y_max}\n")
        file.write(f"{z_min} {z_max}\n")
        file.write("ITEM: ATOMS id type x y z fx fy fz\n")
        dfLammps.to_csv(file, sep='\t', index=False, header=False)

    print(f"Processed: {surfaceFile} -> {surface_csv}, {surface_lmp}")

print("All files processed successfully.")