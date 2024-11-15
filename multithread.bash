#!/bin/bash

num_cores=$(nproc)
num_cores=8
python3 split_annotation.py --all_thread "$num_cores"
for ((i=0; i<num_cores; i++)); do
    echo "Starting thread $i"
    python3 readjson.py --all_thread "$num_cores" --thread_id "$i" &
done

wait