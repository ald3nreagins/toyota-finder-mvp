import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_car_image(car, user_prompt=""):
    description = (
        f"A {car['color_options'].split('|')[0]} Toyota {car['model']}, "
        f"a {car['type']} with {car['horsepower']} horsepower. {user_prompt}"
    )

    response = openai.Image.create(
        model="dall-e-3",
        prompt=description,
        n=1,
        size="512x512"
    )

    return response['data'][0]['url']
