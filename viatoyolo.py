# via_to_yolov8_seg.py
import json, os
from PIL import Image

# ---- CONFIG ----
via_json = "via_region_data.json"    # or car-damage-train.json
images_dir = "dataset/images/all"    # folder containing all images from VIA
out_labels_dir = "dataset/labels/all" # where .txt label files will be written
# map textual region attribute to class id you want in training
# adjust to your dataset: many of your regions use "damage" as name
class_map = {
    "scratch": 0,
    "dent": 1,
    "damage": 0,    # if you want to treat unlabeled "damage" as scratch (or change to single class)
    "unknown": 2
}
os.makedirs(out_labels_dir, exist_ok=True)

with open(via_json, "r") as f:
    data = json.load(f)

def get_label_name(region_attr):
    # tries several keys that might exist in VIA
    for k in ("name","label","type"):
        if k in region_attr and region_attr[k]:
            return region_attr[k]
    return "damage"

for key, entry in data.items():
    filename = entry.get("filename")
    if not filename:
        continue
    img_path = os.path.join(images_dir, filename)
    if not os.path.exists(img_path):
        print("MISSING image:", img_path)
        continue
    w,h = Image.open(img_path).size
    lines = []
    for region in entry.get("regions", []):
        sa = region.get("shape_attributes", {})
        if sa.get("name") != "polygon":
            continue
        xs = sa.get("all_points_x", [])
        ys = sa.get("all_points_y", [])
        if len(xs) < 3:
            continue
        ra = region.get("region_attributes", {})
        lname = get_label_name(ra)
        cls_id = class_map.get(lname, class_map.get("damage", 0))
        # normalize coords by width/height
        coords = []
        for x,y in zip(xs, ys):
            coords.append(f"{x/ w:.6f}")
            coords.append(f"{y/ h:.6f}")
        line = str(cls_id) + " " + " ".join(coords)
        lines.append(line)
    # write label file (same base name but .txt)
    if lines:
        out_path = os.path.join(out_labels_dir, os.path.splitext(filename)[0] + ".txt")
        with open(out_path, "w") as out:
            out.write("\n".join(lines))
