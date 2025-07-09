import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()
client = OpenAI()  # Uses OPENAI_API_KEY from env

# This code creates the car image based on the user prompt that is in the app.py file.
# The code returns the image URL to the user.
def generate_car_image(car, user_prompt=""):
    description = (
        f"A {car['color_options'].split('|')[0]} Toyota {car['model']}, "
        f"a {car['type']} with {car['horsepower']} horsepower. {user_prompt}"
    )
    response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        n=1,
        size="1024x1024",
        quality="standard"
    )

    return response.data[0].url
