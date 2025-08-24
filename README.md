# Car Price Prediction
- This project predicts the price of a car based on its specifications such as:
    - Company
    - Model
    - Year of Manufacture
    - Odometer Reading
    - Fuel Type
    - Transmission
    - RTO (Registration)

- A **machine learning model** was trained using a Pipeline that included preprocessing with One-Hot Encoding, hyperparameter tuning via GridSearchCV, and model training with **CatBoost** to achieve accurate predictions.

- To make the system more realistic, the predicted price is adjusted with a penalty score based on the ***car damage detection model (YOLO)*** that identifies dents, scratches, and paint damage from uploaded images.

- The car damage detection model (YOLO) generates a damage score based on the severity of detected issues, which is then used to **penalize** the predicted car price from the ML model, ensuring more reliable and realistic valuations.

---

## Features
- **Car Price Prediction** using a Machine Learning Pipeline with One-Hot Encoding, GridSearchCV for hyperparameter tuning, and CatBoost for accurate results.  
- **Car Damage Detection** using YOLO to identify **Scratches, Dents, and Paint Damage** from uploaded images or videos.  
- **Car Quality/Damage Score** generation based on detected damages, used to adjust the predicted price for more realistic valuations.  
- **Penalty Integration**: The final price is penalized according to the severity of the detected damage, ensuring fair and practical pricing.  
- **Streamlit UI** for seamless interaction – upload images/videos, input car details, and get predictions instantly.  
- **Multi-Modal Input Support**: Works with both **Images & Videos** for damage detection.  
- **Scalable Integration**: Can be easily extended for dealership platforms, resale marketplaces, or insurance use cases.  


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
3. Enter Car Details
```
    - Fill in the required fields:
    - Company
    - Model
    - Year of Manufacture
    - Odometer Reading
    - Fuel Type
    - Transmission
    - RTO (Region)
```
- **Get Final Price Prediction** 
```
The ML model (CatBoost) predicts the base price.
The Car Damage Score is used to adjust/penalize the price.
The final output is a realistic car resale value displayed on the UI.
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
- **YOLOv8 (Ultralytics)** – Detect car damages (scratches, dents, etc.) from images and videos
- **CatBoost** – Predict car price based on specs and image-derived features
- **Streamlit** – Web interface for uploading car specs and images, and displaying predictions
- **OpenCV & Pillow** – Image/video processing and annotation
- **Python** – Backend logic and model integration

  
## Future Improvements 
- Include insurance claim estimation based on detected damages and car value.
- Expand training dataset to include more car models, years, and diverse damage scenarios for better generalization.
- Add real-time webcam support for instant car assessment.

### ***DEMO***
- []()
- [video for detection](https://www.linkedin.com/posts/sarthak-tyagi-a18812226_machinelearning-yolo-computervision-activity-7361832762640617474-uKed?utm_source=share&utm_medium=member_desktop&rcm=ACoAADi3pDQBy3-nsVgSm0LYdQdC_W0qjLWiwoo)
- [Scoring those detection](https://www.linkedin.com/posts/sarthak-tyagi-a18812226_machinelearning-yolo-computervision-activity-7361835658560069633-DCAs?utm_source=share&utm_medium=member_desktop&rcm=ACoAADi3pDQBy3-nsVgSm0LYdQdC_W0qjLWiwoo)
-[the complete project](https://www.linkedin.com/posts/sarthak-tyagi-a18812226_machinelearning-computervision-deeplearning-ugcPost-7365096350364925953-m6in?utm_source=share&utm_medium=member_desktop&rcm=ACoAADi3pDQBy3-nsVgSm0LYdQdC_W0qjLWiwoo)

## Author
***Sarthak Tyagi***
- Machine Learning Engineer | Computer Vision Enthusiast
- [LinkedIn]([www.linkedin.com/in/sarthak-tyagi-a18812226](https://www.linkedin.com/in/sarthak-tyagi-a18812226/))
