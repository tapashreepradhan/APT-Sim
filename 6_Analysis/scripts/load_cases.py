import os
import pandas as pd

def parse_results_file(path):
    """
    Parses a results_data file and returns a DataFrame with one row per atom.
    Each field (x, y, z, voltage, etc.) is a separate column.
    """
    columns = [
        'index', 'type', 'number', 'voltage', 'x', 'y', 'z',
        'stopX', 'stopY', 'stopZ', 'tof', 'probability',
        'potential_before', 'field_beforeX', 'field_beforeY', 'field_beforeZ',
        'potential_after', 'field_afterX', 'field_afterY', 'field_afterZ',
        'normalX', 'normalY', 'normalZ', 'apexX', 'apexY', 'apexZ'
    ]
    data = []
    with open(path, 'r') as f:
        lines = f.readlines()

    in_data = False
    for line in lines:
        if line.strip() == "ASCII":
            in_data = True
            continue
        if not in_data or not line.strip() or line.startswith("#"):
            continue

        parts = line.strip().split()
        if len(parts) < 26:
            continue

        try:
            row = [float(p) for p in parts[:26]]
            data.append(row)
        except ValueError:
            continue  # skip malformed lines

    return pd.DataFrame(data, columns=columns)

def load_case1_batches():
    """
    Loads evaporation data for Case 1 (TAPSim only).
    """
    base = "../3_TAPsimRun/simulations/Al_100_1000_0"
    #base = "../3_TAPsimRun/simulations/W_100_1000_0"
    #base = "../3_TAPsimRun/simulations/CSL_5_1000_0"
    batches = {}
    step_idx = 0

    for idx, fname in enumerate(sorted(os.listdir(base))):
        if fname.startswith("results_data"):
            df = parse_results_file(os.path.join(base, fname))
            for _, row in df.iterrows():
                batches[step_idx] = pd.DataFrame([row])
                step_idx += 1
    return batches

def load_caseX_batches(directory):
    """
    Generic loader for Case 2 and Case 3 (TAPSim + MD Relaxation).
    Each file may contain multiple atoms; each atom is treated as one step.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    batches = {}
    step_idx = 0
    for fname in sorted(os.listdir(directory)):
        if fname.startswith("results_data_") and fname.endswith(".txt"):
            file_path = os.path.join(directory, fname)
            df = parse_results_file(file_path)
            for _, row in df.iterrows():
                batches[step_idx] = pd.DataFrame([row])
                step_idx += 1
    return batches
