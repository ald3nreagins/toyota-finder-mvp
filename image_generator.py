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
        f"Create a highly detailed, photorealistic concept car inspired by Toyota, "
        f"based on the following description: '{user_prompt}'. "
        f"The car should reflect innovative design elements, combining features like {car['type']}, "
        f"with approximately {car['horsepower']} horsepower, and {car['color_options'].split('|')[0]} color. "
        f"Include both exterior and interior views showing modern dashboard, seating, and steering wheel. "
        f"The image should be ultra-realistic, indistinguishable from a real photograph, "
        f"with natural lighting, sharp details, and lifelike textures. "
        f"Rendered in professional automotive photography style, against a clean, minimalistic background."
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        n=1,
        size="1024x1024",
        quality="standard"
    )

    return response.data[0].url


car = {
    "model": "Toyota Camry",
    "type": "Sedan",
    "horsepower": 203,
    "color_options": "Red|Blue|Black|White",
    "price": 25000,
    "Miles Per Gallon": 28,
    "Drive Type": "FWD",
    "Transmission": "Automatic",
    "Fuel Type": "Gasoline"
}
user_prompt = "I want a car that is sporty, has a sleek design, and is good for city driving."
list_prompts = [
    (
        f"A highly detailed, photorealistic image of a {car['color_options'].split('|')[0]} Toyota {car['model']}, "
        f"a {car['type']} with {car['horsepower']} horsepower, "
        f"showing both exterior and interior views with visible dashboard, leather seats, and steering wheel, "
        f"captured in professional automotive photography style with sharp focus and realistic lighting. "
        f"Background is a clean urban street. "
        f"{user_prompt}"
    )
]

