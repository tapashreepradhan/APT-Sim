import os
import pandas as pd
import glob

def parse_grid_file(path):
    """
    Faster TAPSim grid file parser using pandas.read_csv.
    Assumes file has 3-line header.
    """
    columns = [
        'id', 'uni_num', 'x', 'y', 'z', 'charge',
        'potX', 'potY', 'potZ',
        'efieldvecX', 'efieldvecY', 'efieldvecZ'
    ]

    try:
        # Read file and filter rows with id == 10 directly using pandas' condition
        df = pd.read_csv(
            path,
            sep=r'\s+',       # Split columns by one or more whitespaces
            skiprows=3,       # Skip header lines
            names=columns,    # Define column names
            engine='c',       # Use the fast 'c' engine
            dtype={'id': int} # Ensure 'id' is treated as integer
        )

        # Keep only emitter structure
        df = df[df['id'] == 10].copy()

        # Unit conversions
        #df[['x', 'y', 'z']] *= 1e10                 # meters -> Ångströms
        #df[['potX', 'potY', 'potZ']] *= 1.602e-9    # V/m -> eV/Å

        return df
        
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return pd.DataFrame(columns=columns)

def load_grid_batches(folder, case_type):
    """
    Loads grid data for different case types.
    
    Args:
        folder (str): Base folder path.
        case_type (str): One of ['case1', 'case2', 'case3'].
    
    Returns:
        dict[int, pd.DataFrame]: {step_index: DataFrame}
    """
    batches = {}

    if case_type == 'case1':
        # Path pattern: .../grid_data.*
        files = sorted(glob.glob(os.path.join(folder, "grid_data.*")))
        for path in files:
            try:
                step = int(os.path.basename(path).split('.')[-1])
                batches[step] = parse_grid_file(path)
            except ValueError:
                continue

    elif case_type in ['case2', 'case3']:
        # Folder structure: .../{step}/grid_data.00000000
        for step_dir in sorted(os.listdir(folder)):
            step_path = os.path.join(folder, step_dir, "grid_data.00000000")
            if os.path.isfile(step_path):
                try:
                    step = int(step_dir)
                    batches[step] = parse_grid_file(step_path)
                except ValueError:
                    continue

    else:
        raise ValueError(f"Unknown case_type: {case_type}")

    return batches