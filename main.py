from ultralytics import YOLO
import cv2
import math

# 1. Load trained YOLO model
model = YOLO("my_model.pt")  # replace with your trained model path

# 2. Define severity weights
severity_weights = {
    "scratch": 1,
    "paint damage": 2,
    "dent": 3
}

# 3. Scoring function (area + detection count penalty)
def get_car_score(results, image_width, image_height, c=5, k=5):
    total_area = image_width * image_height
    raw_damage = 0
    detections_list = []

    for r in results:
        boxes = r.boxes
        names = model.names  
        
        for box in boxes:
            cls_id = int(box.cls.item())
            cls_name = names[cls_id]
            conf = float(box.conf.item())
            
            if cls_name in severity_weights:
                weight = severity_weights[cls_name]
                
                # Bounding box size
                x1, y1, x2, y2 = box.xyxy[0]
                box_area = float((x2 - x1) * (y2 - y1))
                area_pct = box_area / total_area
                
                detections_list.append((cls_name, conf, box_area))
                
                # Area × weight × confidence
                raw_damage += area_pct * weight * conf

    # Penalty for having many detections
    total_detections = len(detections_list)
    count_penalty = 1 + (total_detections / k)
    raw_damage *= count_penalty

    # Convert damage to score 
    score = 100 * math.exp(-c * raw_damage)
    return round(score, 2)



