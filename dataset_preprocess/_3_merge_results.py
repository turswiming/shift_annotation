import json
import os
import numpy
from tqdm import tqdm
path_to_anno_dir = "anno/"
path_to_fixations = "fixations_train2014.json"
path_to_new_fixations = "fixations_train2014_shifted.json"

with open(path_to_fixations, 'r') as f:
    data = json.load(f)

data["annotations"]=[]

for shifted_path in os.listdir(path_to_anno_dir):
    if shifted_path.startswith("fixations_train2014_shift_"):
        path = path_to_anno_dir+shifted_path
        with open(path,"r") as f:
            annos = json.load(f)
            for anno in tqdm(annos):
                fixations = anno["fixations"]
                fixations = numpy.asarray(fixations)
                fixations.astype(numpy.int16)
                fixations = fixations.tolist()
                anno["fixations"] = fixations
                data["annotations"].append(anno)

    else:
        continue
with open(path_to_new_fixations, 'w') as f:
    json.dump(data, f)