import os
from dotenv import load_dotenv
import openai

# Load .env
load_dotenv()

# New client-based API usage
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_top_matches(df, car_type, color, min_hp, user_prompt): #This is code provides the tools for the GPT to find match the cars to the database
    filtered = df[
        (df['type'] == car_type) &
        (df['horsepower'] >= min_hp) &
        (df['color_options'].str.contains(color))
    ]

    car_data = filtered.to_dict(orient='records') #This is the cars that match filtered to be in alphabetical order by the columns of records

    #This is the prompt that is output to the AI so that it can make a match
    prompt = f"""
    Based on the user's description and the following list of Toyota cars, return the 10 best matching models.

    Description: "{user_prompt}"


    #This creates a dictionary with the car data, probably nested with all the different specs. Then the LLM responds with the 10 best matches based on the user prompt matching to car database
    Cars:
    {car_data}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Toyota assistant helping customers find cars."},
            {"role": "user", "content": prompt}
        ]
    )

    response_text = response.choices[0].message.content

    matched = []
    for car in car_data:
        if car["model"] in response_text:
            matched.append(car)
    return matched[:10]

    
