import time
from openai import OpenAI
import os 
from flask import Flask, render_template, request

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_KEY)

app = Flask(__name__)



            

def get_movie_recommendations(genre, favorite_movies, preferences):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
   {"role": "system", "content": "You are a professional movie recommender. recommend three movies and make sure you have them all on different lines not just as one blurb of text. "}, 
   {"role": "user", "content": f"Based on the genre '{genre}', favorite movies '{favorite_movies}', and preferences '{preferences}', suggest some movies."}
    ]
)
# Access the message content correctly
    message_content = completion.choices[0].message.content
    movies = [line.strip() for line in message_content.split('\n') if line.strip()]
    return movies

def get_date_ideas(interests, dateType,budget):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
   {"role": "system", "content": "You are a professional date recommender. recommend three dates and make sure you have them all on different lines not just as one blurb of text. "}, 
   {"role": "user", "content": f"Suggest three '{dateType}' dates Based on these interests '{interests}', that match this budget range '{budget}'."}
    ]
)
# Access the message content correctly
    message_content = completion.choices[0].message.content
    dates = [line.strip() for line in message_content.split('\n') if line.strip()]
    return dates


@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/movie_quiz')
def movie_quiz():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def movie_result():
    genre = request.form['genre']
    favorite_movies = request.form['favorite_movies']
    preferences = request.form['preferences']
    recommendations = get_movie_recommendations(genre, favorite_movies, preferences)
    return render_template('result.html', recommendations=recommendations)

@app.route('/date_ideas')
def date_ideas_form():
    return render_template('date_ideas_form.html')

@app.route('/date_ideas_result', methods=['POST'])
def date_ideas_result():
    print(request.form)  # Debug: print all form data
    interests = request.form['interests']
    dateType = request.form['dateType']
    budget = request.form['budget']
    print(f"Interests: {interests}, DateType: {dateType}, Budget: {budget}")  # Debug: print specific form fields
    ideas = get_date_ideas(interests, dateType, budget)
    return render_template('date_ideas_result.html', ideas=ideas)

if __name__ == '__main__':
    app.run(debug=True)