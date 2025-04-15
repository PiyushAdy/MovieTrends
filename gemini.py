import os
import google.generativeai as genai
from helpers import * 

genai.configure(api_key=os.environ["GEMINI_API_KEY"])



# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

def Interpret_HTML(Html_data,data_type):
    prompt=f"""
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

