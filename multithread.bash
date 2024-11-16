#!/bin/bash

num_cores=$(nproc)
num_cores=8
dataset_type="val"
python3 dataset_preprocess/_1_split_annotation.py --all_thread "$num_cores" --dataset_type "$dataset_type"
for ((i=0; i<num_cores; i++)); do
    echo "Starting thread $i"
    python3 dataset_preprocess/_2_readjson.py --all_thread "$num_cores" --thread_id "$i" --dataset_type "$dataset_type" &
done

wait

python3 dataset_preprocess/_3_merge_annotation.py --dataset_type "$dataset_type"