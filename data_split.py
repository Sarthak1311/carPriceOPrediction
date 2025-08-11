import os
import shutil
import random

# Paths
labels_path = "/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/all"
image_path = "/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/allImage"

# Output dirs
splits = ['train', 'val', 'test']
for s in splits:
    os.makedirs(f"/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/image/{s}", exist_ok=True)
    os.makedirs(f"/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/label/{s}", exist_ok=True)

# Split ratio
train_ratio = 0.7
val_ratio = 0.2

# All image files
files = [f for f in os.listdir(image_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
random.shuffle(files)

train_end = int(train_ratio * len(files))
val_end = train_end + int(val_ratio * len(files))

train_files = files[:train_end]
val_files = files[train_end:val_end]
test_files = files[val_end:]

# Move images + labels
def moving_files(files, split):
    for f in files:
        shutil.copy(os.path.join(image_path, f),
                    f"/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/image/{split}/{f}")
        label_file = os.path.splitext(f)[0] + ".txt"
        if os.path.exists(os.path.join(labels_path, label_file)):
            shutil.copy(os.path.join(labels_path, label_file),
                        f"/Users/sarthaktyagi/Desktop/30days-3oprojects/car_price_prediction/carDamageScore/label/{split}/{label_file}")

moving_files(train_files, "train")
moving_files(val_files, "val")
moving_files(test_files, "test")

print("✅ Dataset split complete!")
print(f"Train: {len(train_files)}, Val: {len(val_files)}, Test: {len(test_files)}")
