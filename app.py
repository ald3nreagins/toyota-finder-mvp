import streamlit as st
import pandas as pd
from gpt_utils import get_top_matches #This uses a GPT tool to find the best matches based on input parameters
from image_generator import generate_car_image #This imports an image generating LLM that will allow the code to build an image from the user input prompt

st.title("Find Your Ideal Toyota") #This sets the title to the argument 

df = pd.read_csv("cars.csv") #This links the Toyota Database to the  through a dataframe

car_type = st.selectbox("Select car type", df["type"].unique()) 
color = st.selectbox("Preferred color", sorted({c for x in df["color_options"] for c in x.split("|")})) #I am watching a video on Python set comprehension, this creates a dropdown select box that has all different color options in the database
min_hp = st.slider("Minimum horsepower", 100, 500, 150) #Creates a slider from 100 to 500 with 150 being the default hp provided, this is for the hp minimum btw
#These lines allow you too set the you to create the filters for which people want to choose their car
user_prompt = st.text_area("What do you want in your car?") #This creates a text area where the user inputs the things they want in their car

if st.button("Find Cars"):
    top_cars = get_top_matches(df, car_type, color, min_hp, user_prompt) #Watching video on this. This uses the AI to scrape what the user input car type, color, and minimum horsepower, it finds the top car by connecting to the Toyota DB

    if top_cars:
        for i, car in enumerate(top_cars):
            st.subheader(car["model"])
            st.write(f"Type: {car['type']} | {car['horsepower']} HP | ${car['price']}") #Loops through the dataframe of top cars created by the LLM and then returns with the model, type, horsepower, and price

            button_key = f"gen_img_{i}" #creates image based on the input of LLM

            if st.button(f"Generate image of {car['model']}", key=button_key): #creates picture of every car returned by code that maches the preferences of the user
                with st.spinner("Generating image..."):
                    try:
                        img_url = generate_car_image(car, user_prompt)
                        st.image(img_url, caption=f"{car['model']} (AI-generated)")
                    except Exception as e:
                        st.error(f"Image generation failed: {e}")
    else:
        st.warning("No cars matched. Try adjusting your filters or prompt.") #This returns explains that no cars were found in the database

