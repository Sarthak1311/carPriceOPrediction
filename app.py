import streamlit as st
import tempfile
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image
from main import get_car_score  # Import your scoring function

# Load YOLO model
model = YOLO("my_model.pt")

st.title("Car Damage Detection & Scoring")
st.write("Upload an image or video of a car to detect dents, scratches, and paint damage, and calculate a quality score.")

uploaded_file = st.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])

if uploaded_file is not None:
    file_type = uploaded_file.type

    # Handle Image
    if file_type.startswith("image"):
        image = Image.open(uploaded_file)
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        h, w = img_cv.shape[:2]

        # YOLO detection
        results = model(img_cv)
        annotated_frame = results[0].plot()

        # Calculate score
        score = get_car_score(results, w, h)

        # Display
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Original Image", use_container_width=True)
        with col2:
            st.image(annotated_frame, caption=f"Detection Results\nCar Score: {score}/100", channels="BGR", use_container_width=True)

    # Handle Video
    elif file_type.startswith("video"):
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        cap = cv2.VideoCapture(tfile.name)
        stframe1 = st.empty()
        stframe2 = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            h, w = frame.shape[:2]
            results = model(frame)
            annotated_frame = results[0].plot()

            # Calculate score
            score = get_car_score(results, w, h)

            # Display side-by-side
            col1, col2 = st.columns(2)
            with col1:
                stframe1.image(frame, channels="BGR", use_container_width=True)
            with col2:
                stframe2.image(annotated_frame, caption=f"Score: {score}/100", channels="BGR", use_container_width=True)

        cap.release()
