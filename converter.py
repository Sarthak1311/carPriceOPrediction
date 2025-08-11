import json
import os
from PIL import Image


# Class mapping 
class_map = {
    "scratch": 0,
    "dent": 1,
    "no damage": 2,
    "paint damage": 3
}

# Paths
images_dir = "/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/allImage"
json_dir = "/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/alljson"
labels_out_dir = "/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/all"    # folder to save YOLO labels
os.makedirs(labels_out_dir, exist_ok=True)


for json_file in os.listdir(json_dir):
    if not json_file.endswith(".json"):
        continue

    json_path = os.path.join(json_dir, json_file)
    with open(json_path, "r") as f:
        data = json.load(f)

    # Match image by filename (ignore JSON's imagePath)
    img_name = os.path.splitext(json_file)[0]
    possible_exts = [".jpg", ".jpeg", ".png"]
    image_path = None
    for ext in possible_exts:
        candidate = os.path.join(images_dir, img_name + ext)
        if os.path.exists(candidate):
            image_path = candidate
            break

    if image_path is None:
        print(f"Image for {json_file} not found. Skipping.")
        continue

    # Open image to get width/height
    img = Image.open(image_path)
    w, h = img.size

    label_lines = []
    for shape in data["shapes"]:
        label_name = shape["label"].lower().strip()
        if label_name not in class_map:
            print(f" Unknown label '{label_name}' in {json_file}, skipping.")
            continue

        points = shape["points"]
        norm_points = []
        for x, y in points:
            norm_points.append(round(x / w, 6))
            norm_points.append(round(y / h, 6))

        class_id = class_map[label_name]
        line = f"{class_id} " + " ".join(map(str, norm_points))
        label_lines.append(line)

    # Save YOLO label file
    txt_filename = img_name + ".txt"
    with open(os.path.join(labels_out_dir, txt_filename), "w") as out_f:
        out_f.write("\n".join(label_lines))

print("✅ Conversion complete! YOLOv8 labels are in:", labels_out_dir)
