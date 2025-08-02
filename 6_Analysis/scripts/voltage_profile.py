import numpy as np

def extract_voltages(approach_data):
    step_voltages = {}
    for step, df in approach_data.items():
        step_voltages[step] = df['voltage'].mean()
    return step_voltages

def compare_voltage_profiles(approachA_data, approachB_data):
    voltA = extract_voltages(approachA_data)
    voltB = extract_voltages(approachB_data)
    steps = sorted(set(voltA.keys()) & set(voltB.keys()))
    return [voltA[s] for s in steps], [voltB[s] for s in steps], steps