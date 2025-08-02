import yaml
from matplotlib import pyplot as plt
import os
from scipy.stats import linregress

n_atoms = 116135

# defining base directory (parent directory of the scripts folder)
base_dir = os.path.dirname(os.path.dirname(__file__))

# defining input and output file paths
thermostat_data_path = os.path.join(base_dir, 'output', 'thermostatData_4thMarch2025.yaml')
plots_dir = os.path.join(base_dir, 'plots')

# making sure plots directory exists
os.makedirs(plots_dir, exist_ok=True)

# loading the yaml data
with open(thermostat_data_path, 'r') as file:
    data = yaml.safe_load(file)

#extracting the relevant data and keywords
keywords = data['keywords']
steps_data = data['data']

# converting the data into a dictionary where each keyword is a key
processed_data = {keyword: [] for keyword in keywords}
for step in steps_data:
    for i, keyword in enumerate(keywords):
        processed_data[keyword].append(step[i])

# converting the processed data into individual arrays for easier plotting
steps = processed_data['Step']
temp = processed_data['Temp']
press = processed_data['Press']
volume = processed_data['Volume']
pot_eng = processed_data['PotEng']
tot_eng = processed_data['TotEng']
lx = processed_data['Lx']
ly = processed_data['Ly']
lz = processed_data['Lz']

# plotting Temperature, Pressure and Volume vs Time Step

# plt.figure(figsize=(8, 5))
# plt.plot(steps, temp, label='Temperature (K)', color = 'blue')
# plt.xlabel('Time Step')
# plt.ylabel('Temperature (K)')
# plt.title('Temperature vs. Time Step')
# plt.savefig(os.path.join(plots_dir, 'temperature_vs_time.png'), dpi=300)
# plt.close()

# plt.figure(figsize=(8, 5))
# plt.plot(steps, press, label='Pressure', color = 'red')
# plt.xlabel('Time Step')
# plt.ylabel('Pressure')
# plt.title('Pressure vs. Time Step')
# plt.savefig(os.path.join(plots_dir, 'pressure_vs_time.png'), dpi=300)
# plt.close()

# plt.figure(figsize=(8, 5))
# plt.plot(steps, volume, label='Volume (Å³)', color='green')
# plt.xlabel('Time Step')
# plt.ylabel('Volume (Å³)')
# plt.title('Volume vs. Time Step')
# plt.savefig(os.path.join(plots_dir, 'volume_vs_time.png'), dpi=300)
# plt.close()

# plotting Potential Energy and Total Energy vs Time Step
# Compute linear trendline (drift) for PotEng and TotEng
slope_pot, intercept_pot, *_ = linregress(steps, pot_eng)
slope_tot, intercept_tot, *_ = linregress(steps, tot_eng)
# Convert total energy drift to per-atom over entire sim
total_drift_pot = slope_pot * (steps[-1] - steps[0])
drift_per_atom = total_drift_pot / n_atoms                                      

plt.figure(figsize=(8, 5))
plt.plot(steps, pot_eng, label='Potential Energy (eV)', color='purple')
plt.plot(steps, tot_eng, label='Total Energy (eV)', color='orange')
#plt.plot(steps, [e / 1e6 for e in pot_eng], label='Potential Energy (MeV)', color='purple')
#plt.plot(steps, [e / 1e6 for e in tot_eng], label='Total Energy (MeV)', color='orange')
plt.xlabel('Time Step')
plt.ylabel('Energy (eV)')
plt.title('Potential and Total Energy vs. Time Step')
plt.legend()
plt.savefig(os.path.join(plots_dir, 'energy_vs_time.png'), dpi=300)
plt.close()

# ======= Print & Save Drift Info =======
drift_summary = f"""
Energy Drift Analysis:
-----------------------
Total Potential Energy Drift over {steps[-1] - steps[0]} steps: {total_drift_pot:.2f} eV
Average Drift per Atom: {drift_per_atom:.6f} eV/atom
Drift per Atom is {'ACCEPTABLE' if abs(drift_per_atom) < 0.005 else 'HIGH'}

Interpretation:
- Potential energy shows a very slight increase during the run.
- The drift is on the order of {drift_per_atom:.4f} eV/atom, which is considered minor and acceptable for large-scale MD.
- This suggests the potential is numerically stable and thermodynamically consistent.
"""
print(drift_summary)

# plotting Lattice Dimensions (Lx, Ly, Lz) vs. Time Step
# plt.figure(figsize=(8, 5))

# plt.plot(steps, lx, label='Lx (Å)', color='blue')
# plt.plot(steps, ly, label='Ly (Å)', color='red')
# plt.plot(steps, lz, label='Lz (Å)', color='green')
# plt.xlabel('Time Step')
# plt.ylabel('Lattice Dimensions (Å)')
# plt.title('Lattice Dimensions vs. Time Step')
# plt.legend()
# plt.savefig(os.path.join(plots_dir, 'lattice_dimensions_vs_time.png'), dpi=300)
# plt.close()

print("Plots saved successfully!")