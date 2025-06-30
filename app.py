import streamlit as st
import pandas as pd
from gpt_utils import get_top_matches
from image_generator import generate_car_image

st.title("Find Your Ideal Toyota")

df = pd.read_csv("cars.csv")

car_type = st.selectbox("Select car type", df["type"].unique())
color = st.selectbox("Preferred color", sorted({c for x in df["color_options"] for c in x.split("|")}))
min_hp = st.slider("Minimum horsepower", 100, 500, 150)
user_prompt = st.text_area("What do you want in your car?")

if st.button("Find Cars"):
    top_cars = get_top_matches(df, car_type, color, min_hp, user_prompt)
    if top_cars:
        for car in top_cars:
            st.subheader(car["model"])
            st.write(f"Type: {car['type']} | {car['horsepower']} HP | ${car['price']}")
            if st.button(f"Generate image of {car['model']}", key=car["model"]):
                img_url = generate_car_image(car, user_prompt)
                st.image(img_url, caption=f"{car['model']}")
    else:
        st.warning("No cars matched. Try adjusting your filters or prompt.")
