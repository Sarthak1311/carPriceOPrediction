import streamlit as st
import tempfile
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image
import pickle
import pandas as pd
from main import get_car_score  # Your scoring function

# ----------------- Load Models -----------------
# YOLO model for damage detection
yolo_model = YOLO("my_model.pt")

# ML pipeline for price prediction
with open("models/car_price_pipeline.pkl", "rb") as f:
    pipe = pickle.load(f)

# Model encoding dict
with open("models/model_mean.pkl", "rb") as f:
    model_mean = pickle.load(f)


st.title("Car Price Prediction with Damage Adjustment")
st.write("Upload an image/video of a car and fill the details to predict adjusted resale price.")

# file uploader
uploaded_file = st.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])

damage_score = None

if uploaded_file is not None:
    file_type = uploaded_file.type

    # Image handling
    if file_type.startswith("image"):
        image = Image.open(uploaded_file)
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        h, w = img_cv.shape[:2]

        results = yolo_model(img_cv)
        annotated_frame = results[0].plot()

        damage_score = get_car_score(results, w, h)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Original Image", use_container_width=True)
        with col2:
            st.image(annotated_frame, caption=f"Damage Score: {damage_score}/100", channels="BGR", use_container_width=True)

    # Video handling
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
            results = yolo_model(frame)
            annotated_frame = results[0].plot()
            damage_score = get_car_score(results, w, h)

            col1, col2 = st.columns(2)
            with col1:
                stframe1.image(frame, channels="BGR", use_container_width=True)
            with col2:
                stframe2.image(annotated_frame, caption=f"Score: {damage_score}/100", channels="BGR", use_container_width=True)

        cap.release()

# ----------------- Car Details Form -----------------
company_models = {
    'Mahindra':['Scorpio', 'XUV300', 'Bolero', 'Thar', 'XUV500', 'XUV700','SCORPIO-N', 'XUV 3XO', 'Kuv100'],
    'Tata':['Harrier', 'Safari', 'NEXON', 'ALTROZ', 'Tiago', 'TIGOR', 'PUNCH','Curvv', 'TIAGO NRG'],
    'KIA':['CARENS', 'SONET', 'SELTOS', 'CARNIVAL'],
    'Other':['X3', 'XC 60', 'S60', 'DISCOVERY SPORT', 'A3', 'MU-X','D-Max V Cross', 'Q5', 'Q7', 'RANGE ROVER VELAR', 'Cooper', 'Z4','5 Series', 'XJ L', 'Spark'],
    'Mercedes':['Benz E Class', 'Benz CLS Class', 'Benz GLC COUPE','Benz GLC CLASS', 'Benz GL Class', 'Benz Maybach S Class','Benz S Class', 'Benz GLA Class', 'Benz C Class'],
    'Toyota':['Fortuner', 'Innova Crysta', 'Etios', 'Etios Liva', 'Camry','Corolla Altis', 'YARIS', 'Glanza', 'URBAN CRUISER'],
    'Renault':['Duster', 'Kwid', 'TRIBER', 'Kiger'],
    'Jeep':['Compass', 'MERIDIAN', 'WRANGLER'],
    'Hyundai':['VENUE', 'Creta', 'Verna', 'Tucson', 'GRAND I10 NIOS','NEW SANTRO', 'Elite i20', 'Grand i10', 'AURA', 'i10',
               'i20 Active', 'Eon', 'New Elantra', 'EXTER', 'NEW I20', 'ALCAZAR','Xcent', 'i20', 'VENUE N LINE', 'Santro Xing', 'Accent'],
    'Maruti':['Vitara Brezza', 'Dzire', 'Celerio', 'BREZZA', 'Baleno', 'FRONX','Alto', 'Alto 800', 'Swift', 'Ertiga', 'Wagon R 1.0',
              'New Wagon-R', 'Ciaz', 'Alto K10', 'IGNIS', 'Swift Dzire', 'XL6','Ritz', 'JIMNY', 'Eeco', 'S PRESSO', 'Zen Estilo'],
    'MG':['HECTOR PLUS', 'HECTOR', 'ASTOR'],
    'Skoda':['Rapid', 'KUSHAQ', 'Superb', 'SLAVIA', 'Karoq', 'Octavia'],
    'Honda':['CRV', 'City', 'Amaze', 'WR-V', 'BR-V', 'Mobilio', 'Brio', 'Jazz','ELEVATE'],
    'Nissan':['MAGNITE', 'Kicks'],
    'Ford':['New Figo', 'Ecosport'],
    'Volkswagen':['TAIGUN', 'VIRTUS', 'Polo', 'Vento'],
    'Datsun':['Redi Go', 'Go']
}

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)

company = col1.selectbox("Company", list(company_models.keys()))
models_for_company = company_models.get(company, [])
model = col2.selectbox("Model", models_for_company)

fuel = col3.selectbox("Fuel Type", ['Diesel', 'Petrol', 'CNG'])
transmission = col4.selectbox("Transmission", ['Manual', 'Auto'])
State = col5.selectbox("State",['DL', 'HR', 'UP', 'OTH'])
yom = col6.number_input("Year of Manufacture", 1990, 2025, 2015)
odo = col7.number_input("Odometer (in kms)", 0, 500000, 30000)
carage = 2025 - yom
col8.write(f"Car Age: {carage} years")

# Encode model
overall_mean = sum(model_mean.values()) / len(model_mean)
model_enc_value = model_mean.get(model, overall_mean)

# Prepare dataframe
input_data = pd.DataFrame([[company, model_enc_value, fuel, transmission, State, carage, odo]],
                          columns=["Company", "Model_Enc", "Fuel", "Transmission", "State", "carAge", "Odometer"])

#  Predict Price 
if st.button("Predict Adjusted Price"):
    base_price = pipe.predict(input_data)[0]

    if damage_score is None:
        st.warning("⚠️ Please upload an image or video to calculate damage score.")
    else:
        # penalty logic
        if damage_score >= 75:
            final_price = base_price
        else:
            penalty_factor = (2/3) + (damage_score / 75) * (1/3)  
            final_price = base_price * penalty_factor

        st.success(f"💰 Estimated Car Price (after damage adjustment): ₹{final_price:,.2f}")
        st.info(f"Base Price (no damage considered): ₹{base_price:,.2f}")
        st.info(f"Damage Score: {damage_score}/100")
