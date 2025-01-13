from flask import Flask, jsonify, request , render_template
import numpy as np
import pandas as pd
import pickle
# Create the Flask application
app = Flask(__name__)
# load models
df = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def Recommendation(song):
    try:
        # Check if the song exists in the DataFrame
        if song not in df['song'].values:
            return f"Error: The song '{song}' does not exist in the dataset."
        
        # Find the index of the song
        idx = df[df['song'] == song].index[0]
        
        # Calculate distances and sort them
        distances = sorted(enumerate(similarity[idx]), reverse=False, key=lambda x: x[1])
        
        # Collect the top 20 similar songs
        songs = []
        for i in distances[1:21]: 
            print(df.iloc[i[0]]['song'])
            songs.append(df.iloc[i[0]]['song'])
            
        
        return songs
    except Exception as e:
        return f"An error occurred: {e}"


# Define a route for the home page

@app.route('/', methods=['GET', 'POST'])
def home():
    names = list(df['song'].values)  # List of all songs

    if request.method == "POST":  # Correct method check
        user_song = request.form['names']  # Get the selected song from the form
        songs = Recommendation(user_song)  # Get recommendations based on user song
        return render_template('index.html', songs=songs, user_song=user_song, names=names)

    return render_template('index.html', names=names)  # Render without recommendations if GET request

    


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
