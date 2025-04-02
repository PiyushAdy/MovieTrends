import os
import json
import requests
from helpers import * 

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

class ChatSession:
    def __init__(self, model_name, generation_config):
        self.model_name = model_name
        self.generation_config = generation_config
        self.history = []
        
    def send_message(self, message):
        url = f"{BASE_URL}/models/{self.model_name}:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": self.history + [{"role": "user", "parts": [{"text": message}]}],
            "generationConfig": self.generation_config
        }
        
        response = requests.post(url, json=payload)
        response_json = response.json()
        
        # Extract the text from the response
        try:
            text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            
            # Add the user message and response to history
            self.history.append({"role": "user", "parts": [{"text": message}]})
            self.history.append({"role": "model", "parts": [{"text": text}]})
            
            # Create a simple Response-like object
            class Response:
                def __init__(self, text):
                    self.text = text
            
            return Response(text)
        except (KeyError, IndexError) as e:
            # Handle error cases
            error_msg = response_json.get("error", {}).get("message", "Unknown error occurred")
            print(f"Error: {error_msg}")
            return Response(f"Sorry, I encountered an error: {error_msg}")

def start_chat(model_name, generation_config):
    return ChatSession(model_name, generation_config)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "topP": 0.95,
    "topK": 40,
    "responseMimeType": "text/plain",
}

# Initialize chat session
chat_session = start_chat("gemini-2.0-flash", generation_config)

def Interpret_HTML(Html_data, data_type):
    prompt = f"""
    Interpret the given HTML data for Top 10 movies of a specific {data_type}. provide an ai analysis for the same using following instructions 

    # Instructions
    1. The analyis should be in form of some detailed pointers with a subheading of each point.
    2.The analysis should be done by making some relationships between the given data, also check for relevant trends and patterns in the data .
    3.if you have any additional data of the given movies then feel free to utlize those too for the analysis.
    4.if possible add some explanations for the trends and patterns you have found in the data.
    2. The Response should not contain the provide HTML.
    3.each pointer should look like this 
    <div class="trend-card">
        <h3>Pointer Subheading/h3>
        <p> Pointer Data</p>
    </div>
    where pointer subheading is the subheading of the pointer and pointer data is the data of the pointer . 
    4. Strictly refrain from using any of the following tags: <!DOCTYPE html>, <head>, <title>, <body>
    5. Use related LSI (Latent Semantic Indexing) keywords to enrich the content.
    6. Use friendly and encouraging tone English and follow the Simple friendly and encouraging tone English Wikipedia style guidelines.
    7. Response should strictly not include markdown 
    8. The number of pointers should not exceed 6
    Note: Failure to comply with the specified constraints will make the response invalid.
    Sample Response:
    <div class="trend-card">
        <h3>Rating Distribution</h3>
        <p>Drama films from 2019 showed a higher average rating (8.1) compared to the 5-year industry average (7.4). This indicates exceptional quality in dramatic storytelling for this year.</p>
    </div>
    <div class="trend-card">
        <h3>Audience Engagement</h3>
        <p>Top 10 drama films from 2019 averaged 420,000+ votes per film, representing a 27% increase in audience engagement compared to 2018.</p>
    </div>
    <div class="trend-card">
        <h3>Runtime Analysis</h3>
        <p>The average runtime of critically acclaimed dramas increased to 138 minutes in 2019, continuing the trend toward longer, more deliberate storytelling in the genre.</p>
    </div>

    HTML DATA ::
    {Html_data}
    """
    response = chat_session.send_message(prompt)
    return response.text


# data = Interpret_HTML(get_top10_both("Drama", 2019, HTML=True))
# print(data)