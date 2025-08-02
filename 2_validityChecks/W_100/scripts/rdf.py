import yaml
import pandas as pd
from matplotlib import pyplot as plt
import os

# BCC tungsten lattice constant (in Ångstroms)
a = 3.165  # Å

# Compute theoretical NN and 2NN distances
d_1NN = (3**0.5 / 2) * a  # 1NN: body diagonal/2
d_2NN = a  # 2NN: face diagonal (one full lattice constant)

# defining file paths relative to the script location
base_dir = os.path.dirname(os.path.dirname(__file__))  # Go up to parent directory
rdf_file_path = os.path.join(base_dir, 'output', 'rdfOutput.yaml')
plot_output_path = os.path.join(base_dir, 'plots', 'rdf.png')

# loading the RDF yaml data
with open(rdf_file_path, 'r') as file:
    rdfData = yaml.safe_load(file)

# extracting keywords and data
keywords = rdfData['keywords']
rdf_steps = rdfData['data']

# creating a dataframe to hold the multi-timestep data
allData = []

for timestep, rows in rdf_steps.items():
    for row in rows:
        allData.append([timestep] + row)

# converting into a DataFrame
df = pd.DataFrame(allData, columns=['timestep'] + keywords)

# renaming columns for better readability
df.columns = ['Timestep', 'r', 'g(r)', 'g(r) error']

# extracting first and last timesteps
timesteps = sorted(rdfData['data'].keys())
first_timestep = timesteps[0]
last_timestep = timesteps[-1]

plt.figure(figsize=(12, 6))

# plotting RDF for first and last timestep
for timestep in [first_timestep, last_timestep]:
    values = rdfData['data'][timestep]
    distances = [row[0] for row in values]
    rdf_values = [row[1] for row in values]
    plt.plot(distances, rdf_values, label=f"Timestep {timestep}")

# adding vertical lines for theoretical BCC NN distances
plt.axvline(d_1NN, color='red', linestyle='--', label=f'1NN (BCC) = {d_1NN:.2f} Å')
plt.axvline(d_2NN, color='green', linestyle='--', label=f'2NN (BCC) = {d_2NN:.2f} Å')

# formatting
plt.xlabel('Distance r (Å)')
plt.ylabel('g(r)')
plt.title('Radial Distribution Function (First vs Last Timestep)')
plt.legend()

plt.savefig(plot_output_path, dpi =300)
plt.show()