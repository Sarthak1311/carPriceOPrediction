# carPriceOPrediction
# the first pahse --->  Car Damage Detection & Scoring System

This project uses **YOLOv8** and **Streamlit** to detect car damages such as scratches, dents, and paint damage.  
It then calculates a **Car Quality Score (0–100)** based on the severity and number of damages.  
This score can be further used for **car price prediction** or insurance-related applications.

---

## 📌 Features
- Detects **Scratches**, **Dents**, and **Paint Damage** on cars.
- Generates a **Car Quality Score** (higher = better condition).
- Supports **both Images & Videos**.
- **Streamlit UI** for easy interaction.
- Can be integrated with **car price prediction models**.

---
## Usage
1. Run Streamlit App
   - streamlit run app.py
2. Upload Car Image/Video
```
  Upload an image (.jpg, .png) or video (.mp4, .avi).
  The app will:
  Detect damages
  Annotate the car with bounding boxes
  Display the Car Score (/100)
```
📊 **Scoring Logic**
  - Each type of damage is given a severity weight:
  - Scratch → 1
  - Paint Damage → 2
  - Dent → 3
### The score calculation considers:
  - Number of damages
  - Bounding box size relative to car
  - Model confidence
  - Finally, the Car Quality Score is:
  - Score = 100 - Normalized_Damage_Value
    ```
    So:
    100 = No Damage (Perfect Condition)
    0 = Severe Damage (Worst Condition)
    ```
### Example Output
1. Image Example:
  - Input: Car with multiple dents
  - Output:
    - Annotated Image with boxes
    - Car Score: 62/100
2. Video Example:
  - Real-time damage detection on uploaded car videos
  - Frame-by-frame scoring


 ***Tech Stack***
- YOLOv8 (Ultralytics) – Damage detection
- Streamlit – Web UI
- OpenCV & Pillow – Image/Video handling
- Python – Backend logic

  
## Future Improvements 
- Integrate with Car Price Prediction Model.
- Improve scoring with damage severity classification.
- Add insurance claim estimation.
- Train on larger & more diverse dataset.

### ***DEMO***
- [video for detection](https://www.linkedin.com/posts/sarthak-tyagi-a18812226_machinelearning-yolo-computervision-activity-7361832762640617474-uKed?utm_source=share&utm_medium=member_desktop&rcm=ACoAADi3pDQBy3-nsVgSm0LYdQdC_W0qjLWiwoo)
- [Scoring those detection](https://www.linkedin.com/posts/sarthak-tyagi-a18812226_machinelearning-yolo-computervision-activity-7361835658560069633-DCAs?utm_source=share&utm_medium=member_desktop&rcm=ACoAADi3pDQBy3-nsVgSm0LYdQdC_W0qjLWiwoo)

## Author
***Sarthak Tyagi***
- Machine Learning Engineer | Computer Vision Enthusiast
- [LinkedIn]([www.linkedin.com/in/sarthak-tyagi-a18812226](https://www.linkedin.com/in/sarthak-tyagi-a18812226/))
