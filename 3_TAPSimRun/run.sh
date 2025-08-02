#!/bin/bash

# setting emitter type (100_W or 110_W or 100_Al or 110_Al etc)
EMITTER_TYPE="100_W"

# defining paths based on the folder structure
SRC_FOLDER="../../1_emitterCreation/${EMITTER_TYPE}/scripts"
TAPSIM_BIN="../../resources/executables"

# defining file names
NODE_FILE="NODE.txt"
MESHGEN_BINARY_NAME="meshgen"
TAPSIM_BINARY_NAME="tapsim"
NODE_FILE_PREFIX="NODE"
OUTPUT_TAR_FILE="${EMITTER_TYPE}_output.tar.gz"

# Set simulation directory (path where everything will be stored)
SIMULATION_DIR="../simulations/${EMITTER_TYPE}/"
mkdir -p "$SIMULATION_DIR"

# Function to check if a file exists
check_file() {
    if [[ ! -f "$1" ]]; then
        echo "Error: File '$1' not found!"
        exit 1
    fi
}

# Step 1: Checking and copying the node file to simulation directory
check_file "${SRC_FOLDER}/${NODE_FILE}"
cp "${SRC_FOLDER}/${NODE_FILE}" "$SIMULATION_DIR"
echo "Copied NODE file '${NODE_FILE}' from '${SRC_FOLDER}' to simulation directory '$SIMULATION_DIR'."

# Step 2: Checking and copying the meshgen binary to simulation directory
check_file "${TAPSIM_BIN}/${MESHGEN_BINARY_NAME}"
cp "${TAPSIM_BIN}/${MESHGEN_BINARY_NAME}" "$SIMULATION_DIR"
echo "Copied meshgen binary '${MESHGEN_BINARY_NAME}' from '${TAPSIM_BIN}' to simulation directory '$SIMULATION_DIR'."

# Copying meshgen.ini file (if exists)
cp meshgen.ini "$SIMULATION_DIR"
echo "Copied meshgen.ini file to simulation directory '$SIMULATION_DIR'."

# Make meshgen executable
chmod +x "$SIMULATION_DIR/meshgen"

# Listing available .txt files in simulation directory
echo "Listing available .txt files in simulation directory '$SIMULATION_DIR':"
ls "$SIMULATION_DIR"/*.txt 2>/dev/null || { echo "No .txt files found in simulation directory!"; exit 1; }

CONFIG_FILE="${NODE_FILE_PREFIX}_Mesh.cfg"
MESH_FILE="${NODE_FILE_PREFIX}_Mesh.txt"
TAPSIM_LOGFILE="TAPsim.log"

# Step 3: Running meshgen to generate mesh and config file
check_file "$SIMULATION_DIR/$NODE_FILE"
check_file "$SIMULATION_DIR/meshgen"
echo "Running: $SIMULATION_DIR/meshgen $SIMULATION_DIR/$NODE_FILE $SIMULATION_DIR/$MESH_FILE --create-config-template=$SIMULATION_DIR/$CONFIG_FILE --write-ascii"
$SIMULATION_DIR/meshgen $SIMULATION_DIR/$NODE_FILE $SIMULATION_DIR/$MESH_FILE --create-config-template=$SIMULATION_DIR/$CONFIG_FILE --write-ascii | tee "$SIMULATION_DIR/MeshGen.log"
echo "Mesh generation completed."

# Step 4: Prompting for user input to modify the config file
read -p "Enter NAME: " SET_NAME
read -p "Enter MASS: " MASS
read -p "Enter EVAPORATION_CHARGE_STATE: " EVAPORATION_CHARGE_STATE
read -p "Enter EVAPORATION_FIELD_STRENGTH: " EVAPORATION_FIELD_STRENGTH

# Updating config file with user inputs
sed -i.bak \
    -e "s|NAME = \*\*\*_SET_NAME_HERE_\*\*\*|NAME = ${SET_NAME}|" \
    -e "s|MASS = \*\*\*_SET_MASS_HERE_\*\*\*|MASS = ${MASS}|" \
    -e "s|EVAPORATION_FIELD_STRENGTH = \*\*\*_SET_EVAPORATION_FIELD_STRENGTH_HERE_\*\*\*|EVAPORATION_FIELD_STRENGTH = ${EVAPORATION_FIELD_STRENGTH}|" \
    -e "s|EVAPORATION_CHARGE_STATE = [0-9]*|EVAPORATION_CHARGE_STATE = ${EVAPORATION_CHARGE_STATE}|" \
    "$SIMULATION_DIR/$CONFIG_FILE"
echo "Configuration updated successfully!"
echo "Backup of the original file saved as '${SIMULATION_DIR}/${CONFIG_FILE}.bak'."

# Step 5: Checking if TAPsim binary exists and copying it to simulation directory
check_file "${TAPSIM_BIN}/${TAPSIM_BINARY_NAME}"
cp "${TAPSIM_BIN}/${TAPSIM_BINARY_NAME}" "$SIMULATION_DIR"
echo "Copied TAPsim binary '${TAPSIM_BINARY_NAME}' from '${TAPSIM_BIN}' to simulation directory '$SIMULATION_DIR'."

# Make TAPsim executable
chmod +x "$SIMULATION_DIR/tapsim"

cp tapsim.ini "$SIMULATION_DIR"
echo "Copied tapsim.ini file to simulation directory '$SIMULATION_DIR'."

# Confirming required files exist
check_file "$SIMULATION_DIR/$CONFIG_FILE"
check_file "$SIMULATION_DIR/$MESH_FILE"

# Step 6: Running TAPSim in the background
echo "Running: nohup $SIMULATION_DIR/tapsim evaporation $SIMULATION_DIR/$CONFIG_FILE $SIMULATION_DIR/$MESH_FILE --write-ascii --no-trajectories --no-dump --event-limit=100 | tee $SIMULATION_DIR/$TAPSIM_LOGFILE &"
"$SIMULATION_DIR/tapsim" evaporation "$SIMULATION_DIR/$CONFIG_FILE" "$SIMULATION_DIR/$MESH_FILE" --write-ascii --no-trajectories --no-dump --event-limit=100 | tee "$SIMULATION_DIR/$TAPSIM_LOGFILE" &

# Getting the PID of the last background process (TAPsim)
TAPSIM_PID=$!

echo "TAPSim started in the background. Log: $SIMULATION_DIR/$TAPSIM_LOGFILE"

# Wait for TAPSim process to complete
wait $TAPSIM_PID

echo "TAPSim process completed."

# Step 7: Compressing all output files into a tar.gz archive
echo "Compressing all output files into a tar archive: $SIMULATION_DIR/$OUTPUT_TAR_FILE"
tar -czf "$SIMULATION_DIR/$OUTPUT_TAR_FILE" -C "$SIMULATION_DIR" *.dat grid_data.* surface_data.* results_data.*

echo "Output files compressed into '$SIMULATION_DIR/$OUTPUT_TAR_FILE'."