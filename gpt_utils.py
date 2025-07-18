import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()  # Uses OPENAI_API_KEY from env

def get_top_matches(
    df,
    car_type,
    color,
    min_hp,
    drive_type,
    budget,
    fuel_type,
    transmission_type,
    mpg,
    user_prompt,
    num_results=1
):
    # Filter dataset
    filtered = df[
        (df['type'] == car_type) &
        (df['horsepower'] >= min_hp) &
        (df['color_options'].str.contains(color, case=False, na=False)) &
        (df['Drive Type'] == drive_type) &
        (df['price'] <= budget) &
        (df['Fuel Type'] == fuel_type) &
        (df['Transmission'] == transmission_type) &
        (df['Miles Per Gallon'] >= mpg)
    ]

    car_data = filtered.to_dict(orient='records')
    if not car_data:
        return []

    # Build GPT prompt
    prompt = f"""
    Based on the user's preferences and the following list of Toyota cars, return the {num_results} best matching models.

    User description: "{user_prompt}"

    Available cars:
    {car_data}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant helping customers find their ideal Toyota cars."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message.content
        response_text_lower = response_text.lower()

        matched = []
        for car in car_data:
            tokens = car["model"].lower().split()
            if all(token in response_text_lower for token in tokens):
                matched.append(car)

        # Fallback: if GPT returns nothing recognizable, just return top N from filtered
        if not matched:
            return car_data[:num_results]

        return matched[:num_results]

    except Exception as e:
        print(f"❌ GPT failed: {e}")
        return car_data[:num_results]
