import os
import shutil

def flatten_case_results(case_name, source_root, target_root):
    """
    Flattens nested result_data files from a TAPSim-MD directory into a single-level directory.

    Parameters:
    - case_name: Name for print/debugging (e.g., "Case 2")
    - source_root: Path to the nested simulation folder
    - target_root: Path where flattened results should go
    """
    print(f"Flattening results for {case_name}...")
    os.makedirs(target_root, exist_ok=True)

    copied = 0
    for item in os.listdir(source_root):
        item_path = os.path.join(source_root, item)
        if os.path.isdir(item_path) and item.isdigit() and int(item) >= 0:
            for fname in os.listdir(item_path):
                if fname.startswith("results_data."):
                    source_file = os.path.join(item_path, fname)
                    dest_file = os.path.join(target_root, f"results_data_{item}.txt")
                    shutil.copy(source_file, dest_file)
                    copied += 1
                    break  # Only one results_data file per step
    print(f"{case_name}: Flattened {copied} files to {target_root}")

def flatten_all_cases():
    flatten_case_results(
        case_name="Case 2",
        #source_root="../5_TAPSimMD/W_100_1000_5",
        source_root="../5_TAPSimMD/Al_100_1000_5",
        #source_root="../5_TAPSimMD/CSL_5_1000_5",
        #target_root="../6_simulationAnalysis/Case2_W"
        target_root="../6_simulationAnalysis/Case2_Al"
        #target_root="../6_simulationAnalysis/Case2_CSL5"
    )
    flatten_case_results(
        case_name="Case 3",
        #source_root="../5_TAPSimMD/W_100_1000_10",
        source_root="../5_TAPSimMD/Al_100_1000_10",
        #source_root="../5_TAPSimMD/CSL_5_1000_10",
        #target_root="../6_simulationAnalysis/Case3_W"
        target_root="../6_simulationAnalysis/Case3_Al"
        #target_root="../6_simulationAnalysis/Case3_CSL5"
    )
