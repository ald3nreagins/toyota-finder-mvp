import os
from dotenv import load_dotenv
import openai

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#This code creates the car image based on the user prompt that is in the app.py file. The code returns the image to the user 
def generate_car_image(car, user_prompt=""):
    description = (
        f"A {car['color_options'].split('|')[0]} Toyota {car['model']}, "
        f"a {car['type']} with {car['horsepower']} horsepower. {user_prompt}"
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        n=1,
        size="512x512"
    )

    return response.data[0].url
