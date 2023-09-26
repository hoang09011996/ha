#!/bin/bash

# Specify the source file you want to clone
source_file="test_.sql"

# Number of copies you want to create
num_copies=100

# Destination directory
destination_dir="/root/ha/dbt/test_cc/models"

# Loop to create the copies
for ((i=1; i<=num_copies; i++)); do
    cp "$source_file" "$destination_dir/clone_$i.sql"
done