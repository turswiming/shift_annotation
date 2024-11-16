import json 
import argparse
import os
parser = argparse.ArgumentParser(description="shift annotations.")
parser.add_argument('--all_thread', type=int, default=1, help='the number of all thread runingg parallel')
parser.add_argument('--dataset_type', type=str, default="train", help='train or val')
args = parser.parse_args()
mode = args.dataset_type
if mode == "train":
    path_to_json = "fixations_train2014.json"
    path_to_fixations_template = "fixations_train2014_anno_{}.json"
    anno_dir_path="anno/"

elif mode == "val":
    path_to_json = "fixations_val2014.json"
    path_to_fixations_template = "fixations_val2014_anno_{}.json"
    anno_dir_path="anno_val/"


with open(path_to_json, 'r') as f:
    data = json.load(f)

annotation = data["annotations"]

if os.path.exists(anno_dir_path) == False:
    os.makedirs(anno_dir_path)

for i in range(args.all_thread):
    with open(anno_dir_path+path_to_fixations_template.format(i),"w") as f:
        json.dump(annotation[i::args.all_thread],f)
