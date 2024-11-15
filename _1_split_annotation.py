import json 
import argparse
parser = argparse.ArgumentParser(description="shift annotations.")
parser.add_argument('--all_thread', type=int, default=1, help='the number of all thread runingg parallel')
args = parser.parse_args()
path_to_json = "fixations_train2014.json"

with open(path_to_json, 'r') as f:
    data = json.load(f)

annotation = data["annotations"]
anno_dir_path="anno/"
for i in range(args.all_thread):
    with open(anno_dir_path+"fixations_train2014_anno_{}.json".format(i),"w") as f:
        json.dump(annotation[i::args.all_thread],f)
