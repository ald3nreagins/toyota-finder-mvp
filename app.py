import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from gpt_utils import get_top_matches
from image_generator import generate_car_image

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Title
st.title("Find Your Ideal Toyota")

# Safety check
if not api_key:
    st.error("Missing OpenAI API Key. Please check your .env file.")
    st.stop()

# Load data
df = pd.read_csv("Expanded_Toyota_Car_Dataset.csv")
df = df.drop_duplicates(subset=['model'])

# --- Input Filters: Dynamically adjust options based on current selections
st.subheader("🔧 Car Preferences")

# Start with full filtered set
filtered_df = df.copy()

# 1. Car type
car_types = sorted(filtered_df["type"].unique())
selected_type = st.selectbox("Car type", car_types)
filtered_df = filtered_df[filtered_df["type"] == selected_type]

# 2. Color (case-insensitive contains)
available_colors = sorted({c.strip() for colors in filtered_df["color_options"] for c in colors.split("|")})
selected_color = st.selectbox("Preferred color", available_colors)
filtered_df = filtered_df[filtered_df["color_options"].str.contains(selected_color, case=False, na=False)]

# 3. Drive type
drive_types = sorted(filtered_df["Drive Type"].unique())
selected_drive = st.selectbox("Drive type", drive_types)
filtered_df = filtered_df[filtered_df["Drive Type"] == selected_drive]

# 4. Transmission
transmissions = sorted(filtered_df["Transmission"].unique())
selected_transmission = st.selectbox("Transmission", transmissions)
filtered_df = filtered_df[filtered_df["Transmission"] == selected_transmission]

# 5. Fuel type
fuel_types = sorted(filtered_df["Fuel Type"].unique())
selected_fuel = st.selectbox("Fuel type", fuel_types)
filtered_df = filtered_df[filtered_df["Fuel Type"] == selected_fuel]

# Safe slider defaults
if not filtered_df.empty:
    hp_min, hp_max = int(filtered_df["horsepower"].min()), int(filtered_df["horsepower"].max())
    mpg_min, mpg_max = int(filtered_df["Miles Per Gallon"].min()), int(filtered_df["Miles Per Gallon"].max())
    price_min, price_max = int(filtered_df["price"].min()), int(filtered_df["price"].max())
else:
    hp_min, hp_max = 0, 1000
    mpg_min, mpg_max = 0, 100
    price_min, price_max = 0, 100000

# 6. Minimum HP
min_hp = st.slider("Minimum horsepower", hp_min, hp_max, 150)

# 7. Minimum MPG
min_mpg = st.slider("Minimum miles per gallon", mpg_min, mpg_max, 25)

# 8. Budget
max_price = st.slider("Budget maximum", price_min, price_max, 30000)

# 9. User description
user_prompt = st.text_area(
    "🧠 What do you want in your car?",
    help="E.g. I want a futuristic Toyota that blends Mercedes luxury and BMW sportiness."
)

# Session state
if "top_cars" not in st.session_state:
    st.session_state.top_cars = []
if "generate_image" not in st.session_state:
    st.session_state.generate_image = False
if "selected_car" not in st.session_state:
    st.session_state.selected_car = None

# --- Button to trigger GPT
if st.button("Find Cars"):
    try:
        top_cars = get_top_matches(
            df,
            selected_type,
            selected_color,
            min_hp,
            selected_drive,
            max_price,
            selected_fuel,
            selected_transmission,
            min_mpg,
            user_prompt
        )
        st.session_state.top_cars = top_cars
        st.session_state.generate_image = False
        st.session_state.selected_car = None
    except Exception as e:
        st.error(f"Error finding cars: {e}")

# --- Show results or info if empty
if not st.session_state.top_cars:
    st.info("No cars matched your filters. Please adjust your preferences.")
else:
    for i, car in enumerate(st.session_state.top_cars):
        st.subheader(car["model"])
        st.write(f"Type: {car['type']} | {car['horsepower']} HP | {car['Miles Per Gallon']} MPG | ${car['price']}")
        if st.button(f"Generate image of {car['model']}", key=f"gen_img_{i}"):
            st.session_state.selected_car = car
            st.session_state.generate_image = True

# --- Generate image
if st.session_state.generate_image and st.session_state.selected_car:
    with st.spinner("Generating AI image..."):
        try:
            img_url = generate_car_image(st.session_state.selected_car, user_prompt)
            st.image(img_url, caption=f"{st.session_state.selected_car['model']} (AI-generated)")
        except Exception as e:
            st.error(f"Image generation failed: {e}")
