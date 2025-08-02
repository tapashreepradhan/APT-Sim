# This file contains functions for post-processing the results of a Pyvaporate run.
# Visualization tool designed to generate a detector hit map from the results of a Pyvaporate run.
# Gives a 2D top-down view of the detector hits - showing where atoms hit the detector surface
# after being field evaporarted from the emitter tip.

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_detector_hits(filename="detector_hits.png", xlim=(-0.15, 0.15),
                       ylim=(-0.15, 0.15)):
    """
    Create a detector hit map by aggregating
    detector hits from each interval step of the
    Pyvaporate run. `xlim` and `ylim` should be set to
    roughly +- the radius of your emitter.
    """
    results_files = []
    dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    for d in dirs:
        results_files += ["{}/{}".format(d, f) for f in os.listdir(os.getcwd())
                          if "results_data." in f]
    detector_hits = []
    ids = []

    for f in results_files:
        try:
            # reads each result file line by line containing information
            # about a detected atom - its x and y coordinates on the detector
            tapsim_results = open(f).readlines()
            for line in tapsim_results[2:]:
                split_line = line.split()
                if not "#" in split_line[0] and not split_line[0]=="ASCII":
                    ids.append(split_line[0])
                    detector_hits.append(
                        (float(split_line[7]), float(split_line[8]))
                    )
        except Exception as e:
            print(e)

    ax = plt.figure(figsize=(8, 8)).gca()
    ax.plot([i[0] for i in detector_hits], [i[1] for i in detector_hits],
            marker = ".", linewidth=0, markersize=0.5, color="k")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    plt.savefig(filename)
    plt.close()