
import streamlit as st
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

from gpt_utils import get_top_matches
from image_generator import generate_car_image

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/ald3nreagins/toyota-finder-mvp/main/white%20background.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Find Your Ideal Toyota")

# Safety check for API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OpenAI API Key. Please check your .env or environment.")
    st.stop()
st.write(f"Key check: {api_key[:5]}***")
st.write("Session state:", st.session_state)
# Load and clean data
df = pd.read_csv("Expanded_Toyota_Car_Dataset.csv")
df = df.drop_duplicates(subset=['model'])

# --- Inputs
car_type = st.selectbox("Select car type", df["type"].unique())
color = st.selectbox("Preferred color", sorted({c for x in df["color_options"] for c in x.split("|")}))
min_hp = st.slider("Minimum horsepower", 100, 500, 150)
drive_type = st.selectbox("Select drive type", df["Drive Type"].unique())
budget = st.slider("Budget Maximum", 18000, 70000, 25000)
transmission_type = st.selectbox("Select transmission type", df["Transmission"].unique())
fuel_type = st.selectbox("Select fuel type", df["Fuel Type"].unique())
mpg = st.slider("Miles per Gallon", 20, 50, 25)
user_prompt = st.text_area("What do you want in your car?")

# --- State defaults
if "top_cars" not in st.session_state:
    st.session_state.top_cars = []
if "generate_image" not in st.session_state:
    st.session_state.generate_image = False
if "selected_car" not in st.session_state:
    st.session_state.selected_car = None

# --- Find Cars
if st.button("Find Cars"):
    try:
        top_cars = get_top_matches(df, car_type, color, min_hp, drive_type, budget, fuel_type, transmission_type, mpg, user_prompt)
        st.session_state.top_cars = top_cars
        st.session_state.generate_image = False
        st.session_state.selected_car = None
    except Exception as e:
        st.error(f"Error finding cars: {e}")

# --- Show Found Cars
for i, car in enumerate(st.session_state.top_cars):
    st.subheader(car["model"])
    st.write(f"Type: {car['type']} | {car['horsepower']} HP | {car['Miles Per Gallon']} MPG | ${car['price']}")
    button_key = f"gen_img_{i}"
    if st.button(f"Generate image of {car['model']}", key=button_key):
        st.session_state.selected_car = car
        st.session_state.generate_image = True

# --- Generate Image
if st.session_state.generate_image and st.session_state.selected_car:
    car = st.session_state.selected_car
    with st.spinner("Generating image..."):
        try:
            img_url = generate_car_image(car, user_prompt)
            st.image(img_url, caption=f"{car['model']} (AI-generated)")
        except Exception as e:
            st.error(f"Image generation failed: {e}")
