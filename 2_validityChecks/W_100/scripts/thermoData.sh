#!/bin/bash

# current date in YYYYMMDD format
current_date=$(date +%Y%m%d)

# path definitions
log_file="../input/log.lammps"
output_file="../output/thermostatData_${current_date}.yaml"

# checking if the log file exists
if [ ! -f "$log_file" ]; then
    echo "Error: Log file $log_file not found."
    exit 1
fi

# extracting relevant lines and save to output file
egrep '^(keywords:|data:$|---$|\.\.\.$|  - \[)' "$log_file" > "$output_file"

echo "Thermostat data extracted to $output_file"

