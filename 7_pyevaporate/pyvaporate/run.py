# This is the main control script for Pyvaporate. 
"""
1. Emitter creation (either from scratch or from a file)
2. Mesh generation
3. Sequential field evaporation simulation steps using TAPSim
4. Relaxation steps using LAMMPS
5. Iterative stepwise simulation until the emitter is fully evaporated
"""
from monty.serialization import loadfn

from pyvaporate.build import build_emitter_from_scratch, build_emitter_from_file
from pyvaporate.call import call_meshgen, call_tapsim, call_lammps
from pyvaporate import SETUP

import os
import sys
from contextlib import contextmanager

import numpy as np
import math


@contextmanager
def redirected(stdout):
    saved_stdout = sys.stdout
    sys.stdout = open(stdout, 'a')
    yield
    sys.stdout = saved_stdout


def yaml_run(config_file):
    """
    The main wrapper function for calling Pyvaporate
    based on a yaml input file (`config_file`).

    The stdout is written to pyvaporate.log in the
    head directory (same location as the yaml file).
    """

    # --------- STEP 1: Load the configuration --------- #
    CONFIGURATION = loadfn(config_file)
    for key in SETUP:
        if key in CONFIGURATION:
            SETUP[key] = CONFIGURATION[key]
    with open("pyvaporate.log", "w") as log: # logging setup
        log.write("")
    # retriving executable paths    
    lammps = SETUP["lammps"]["bin"]
    tapsim = SETUP["evaporation"]["meshgen_bin"]
    meshgen = SETUP["evaporation"]["tapsim_bin"]
    n_events_total = SETUP["evaporation"]["total_events"]
    n_events_per_step = SETUP["evaporation"]["events_per_step"]

    # setting up alloy composition
    elements = [e for e in SETUP["emitter"]["elements"]]
    alloy = {}
    SETUP["id_dict"] = {}
    n = 10
    for e in elements:
        SETUP["id_dict"][str(n)] = e
        n += 10
    if len(elements) > 1:
        for e in elements[1:]:
            alloy[e] = SETUP["emitter"]["elements"][e]["fract_occ"]

    if not os.path.isdir("0"):
        os.mkdir("0")
    os.chdir("0")

    # --------- STEP 2: Emitter creation --------- #
    if SETUP["emitter"]["source"]["node_file"] == "none" and SETUP["emitter"]["source"]["uc_file"] == "none":
        with redirected(stdout="../pyvaporate.log"):
            print("Building initial emitter")
        basis = SETUP["emitter"]["basis"]
        emitter_radius = SETUP["emitter"]["radius"]
        emitter_side_height = SETUP["emitter"]["side_height"]
        z_axis = SETUP["emitter"]["orientation"]["z"]
        y_axis = SETUP["emitter"]["orientation"]["y"]
        x_axis = SETUP["emitter"]["orientation"]["x"]
        build_emitter_from_scratch(
            element=elements[0], basis=basis, z_axis=z_axis,
            filename="emitter.txt", emitter_radius=emitter_radius,
            emitter_side_height=emitter_side_height, alloy=alloy
        )
    elif SETUP["emitter"]["source"]["node_file"] != "none":
        with redirected(stdout="pyvaporate.log"):
            print("Importing emitter from {}".format(SETUP["emitter"]["source"]["node_file"]))
        os.system("cp {} ./emitter.txt".format(SETUP["emitter"]["source"]["node_file"]))

    elif SETUP["emitter"]["source"]["uc_file"] != "none":
        with redirected(stdout="../pyvaporate.log"):
            print("Building emitter based on {}".format(SETUP["emitter"]["source"]["uc_file"]))
        emitter_radius = SETUP["emitter"]["radius"]
        emitter_side_height = SETUP["emitter"]["side_height"]
        z_axis = SETUP["emitter"]["orientation"]["z"]
        y_axis = SETUP["emitter"]["orientation"]["y"]
        x_axis = SETUP["emitter"]["orientation"]["x"]
        build_emitter_from_file(
            SETUP["emitter"]["source"]["uc_file"], z_axis=z_axis,
            filename="emitter.txt", emitter_radius=emitter_radius,
            emitter_side_height=emitter_side_height
        )
    # --------- STEP 3: Mesh Generation --------- #    
    with redirected(stdout="../pyvaporate.log"):
        print("Running Meshgen")
        call_meshgen(SETUP, "emitter.txt")
    n_atoms = len([l for l in open("emitter.txt").readlines()[1:-1] if
                   l.split()[3] not in ["0", "1", "2", "3"]])

    if "%" in str(n_events_total):
        total_percent = float(n_events_total.replace("%",""))/100.
        SETUP["evaporation"]["total_events"] = math.ceil(total_percent * n_atoms)
    if "%" in str(n_events_per_step):
        step_percent = float(n_events_per_step.replace("%",""))/100.
        SETUP["evaporation"]["events_per_step"] = math.ceil(step_percent * n_atoms)

    lines = open("emitter.txt").readlines()
    with open("updated_mesh.txt", "w") as f:
        f.write(lines[0])
        for l in lines[1:]:
            split_line = l.split()
            split_line.append("0\n")
            f.write(" ".join(split_line))
        f.write("# 10=Al")
    # --------- STEP 4: LAMMPS Relaxation ------------- #
    with redirected(stdout="../pyvaporate.log"):
        print("Running LAMMPS")
        call_lammps(n_atoms, SETUP)
    os.chdir("../")

    # --------- STEP 5: Main Evaporation Loop --------- #
    step_number = 1
    while step_number * SETUP["evaporation"]["events_per_step"] <= SETUP["evaporation"]["total_events"]:
        if not os.path.isdir(str(step_number)):
            os.mkdir(str(step_number))
        os.chdir(str(step_number))
        with redirected(stdout="../pyvaporate.log"):
            print("\nSTEP {}\n------".format(step_number))
        os.system("cp ../{}/relaxed_emitter.txt mesh.txt".format(step_number-1))
        os.system("cp ../0/mesh.cfg .")

        with redirected(stdout="../pyvaporate.log"):
            print("Running TAPSim")
        call_tapsim(SETUP)
        n_atoms = len([l for l in open("mesh.txt").readlines()[1:-1] if
                       l.split()[3] not in ["0", "1", "2", "3"]])
        with redirected(stdout="../pyvaporate.log"):
            print("Running LAMMPS")
            call_lammps(n_atoms, SETUP)
        if SETUP["cleanup"] == True:
            os.system("rm trajectory_data.*")
            os.system("rm dump.*")
            os.system("rm dump")
            os.system("rm geometry.dat")

        step_number += 1
        os.chdir("../")
    with redirected(stdout="pyvaporate.log"):
        print("\n------\nEvaporation complete.")