import json
import gc
import numpy as np
import imageio.v2 as imageio
import os
import tqdm
import shutil
from sklearn.cluster import MeanShift
from sklearn.neighbors import KNeighborsClassifier
import argparse
from PIL import Image, ImageDraw

def visualize_image_with_annotations(image, annotation):
    fixations = annotation["fixations"]
    path_to_image = path_t0_image_dir + image["file_name"]
    annotationed_image_path = annotationed_image_dir+image["file_name"]
    if os.path.exists(annotationed_image_path):
        image_IMAGEIO = imageio.imread(annotationed_image_path)
    else:
        image_IMAGEIO = imageio.imread(path_to_image)
    image_array = np.array(image_IMAGEIO)
    fixations = np.array(fixations)
    for fixation in fixations:
        x, y = fixation
        x = x-1
        y = y-1
        image_array[x, y] = [255, 0, 0]
    imageio.imwrite(annotationed_image_path, image_array)
    pass

def draw_circle(image_path,save_path, fixations):
    image_pil = Image.open(image_path)
    
    draw = ImageDraw.Draw(image_pil)
    
    num_fixations = len(fixations)
    for i, fixation in enumerate(fixations):
        if len(fixation) == 2:
            x, y = fixation
            radius = 5
        elif len(fixation) == 3:
            x, y, radius = fixation
        # 计算颜色渐变，从蓝色 (0, 0, 255) 到红色 (255, 0, 0)
        r = int(255 * (i / num_fixations))
        b = 255 - r
        color = (r, 0, b)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=color, width=2)
    #create lines between fixations
    for i in range(num_fixations-1):
        if len(fixations[i]) == 2:
            x1, y1 = fixations[i]
        elif len(fixations[i]) == 3:
            x1, y1, _ = fixations[i]
        if len(fixations[i+1]) == 2:
            x2, y2 = fixations[i+1]
        elif len(fixations[i+1]) == 3:
            x2, y2, _ = fixations[i+1]
        draw.line((x1, y1, x2, y2), fill=(255, 0, 0), width=2)

    image_pil.save(save_path)

def mean_shift_fixations(fixations):
    fixations = np.array(fixations)
    mean_shift = MeanShift(bandwidth=10)
    mean_shift.fit(fixations)
    cluster_centers = mean_shift.cluster_centers_
    labels = mean_shift.labels_
    unique_labels, counts = np.unique(labels, return_counts=True)
    cluster_sizes_dict = dict(zip(unique_labels, counts))
    cluster_sizes = [cluster_sizes_dict[i] for i in range(len(cluster_centers))]


    #arrange the cluster centers
    knn = KNeighborsClassifier(n_neighbors=1)
    labels = np.arange(len(fixations))
    knn.fit(fixations,labels)
    near_index = knn.predict(cluster_centers)
    #sort the cluster centers by the near_index
    cluster_centers = cluster_centers[near_index.argsort()]
    cluster_sizes = np.array(cluster_sizes)[near_index.argsort()]

    #merge 2 numpy arrays
    cluster_centers = np.column_stack((cluster_centers, cluster_sizes))
    

    return cluster_centers


if __name__ == "__main__":
    #get parsed parameter
    parser = argparse.ArgumentParser(description="shift annotations.")
    parser.add_argument('--all_thread', type=int, default=1, help='the number of all thread runingg parallel')
    parser.add_argument('--thread_id', type=int, default=0, help='the id of thread')
    parser.add_argument('--dataset_type', type=str, default="train", help='train or val')
    args = parser.parse_args()
    mode = args.dataset_type
    if mode == "train":
        path_to_json = "fixations_train2014.json"
        path_t0_image_dir = "train/"
        annotationed_image_dir = "annotationed_images/"
        path_to_anno_dir = "anno/"
        path_to_unshifted_template = "fixations_train2014_anno_{}.json"
        path_to_shifted_template = "fixations_train2014_shift_{}.json"
    elif mode == "val":
        path_to_json = "fixations_val2014.json"
        path_t0_image_dir = "val/"
        annotationed_image_dir = "annotationed_images/"
        path_to_anno_dir = "anno_val/"
        path_to_unshifted_template = "fixations_val2014_anno_{}.json"
        path_to_shifted_template = "fixations_val2014_shift_{}.json"


    path = path_to_anno_dir+path_to_unshifted_template.format(args.thread_id)
    with open(path, 'r') as f:
        data = json.load(f)

    for annotation in tqdm.tqdm(data):
        shifted_fixations = mean_shift_fixations(annotation["fixations"])
        # draw_circle(
        #     path_t0_image_dir+image_dict[annotation["image_id"]]["file_name"], 
        #     "origin_"+image_dict[annotation["image_id"]]["file_name"], 
        #     annotation["fixations"])
        # draw_circle(
        #     path_t0_image_dir+image_dict[annotation["image_id"]]["file_name"], 
        #     "shifted_"+image_dict[annotation["image_id"]]["file_name"], 
        #     shifted_fixations)
        #convert to 2d list
        shifted_fixations = shifted_fixations.tolist()
        annotation["fixations"] = shifted_fixations


    with open(path_to_anno_dir+path_to_shifted_template.format(args.thread_id), 'w') as f:
        json.dump(data, f)
                # visualize_image_with_annotations(image_dict[key], annotation)
