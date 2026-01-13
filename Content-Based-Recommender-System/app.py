import streamlit as st
import pickle
import pandas as pd
import requests
import os
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.header('Movie Recommender System')

# --- 1. LOAD DATA ---
current_dir = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(current_dir, 'movie_list.pkl')
movies = pickle.load(open(movies_path, 'rb'))

if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

# Auto-fix tags if they are lists
if isinstance(movies['tags'].iloc[0], list):
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))

# --- 2. CACHING (FIXES SPEED) ---
# @st.cache_resource tells Streamlit: "Run this ONCE and save the result in memory."
# Next time you click, it loads instantly.
@st.cache_resource
def calculate_similarity_matrix(df):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(df['tags']).toarray()
    return cosine_similarity(vector)

# Calculate once, reuse forever
similarity = calculate_similarity_matrix(movies)

# --- 3. POSTER FUNCTION (FIXES IMAGES) ---
def fetch_poster(movie_id):
    api_key = "YOUR_NEW_API_KEY_HERE"  # <--- PASTE YOUR KEY AGAIN
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    # Try to fetch the poster 3 times before failing
    for attempt in range(3):
        try:
            # timeout=10 means wait 10 seconds for a response
            data = requests.get(url, timeout=10)
            data.raise_for_status() # Check if we got a 404 or 500 error
            data = data.json()
            
            if 'poster_path' in data and data['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"
                
        except requests.exceptions.RequestException as e:
            # If it failed, wait 1 second and try again
            time.sleep(1)
            continue
            
    # If all 3 attempts fail, return the error image
    return "https://via.placeholder.com/500x750?text=Connection+Error"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_names = []
    recommended_posters = []
    
    for i in distances[1:6]:
        # Handle IDs
        if 'movie_id' in movies.columns:
            movie_id = movies.iloc[i[0]].movie_id
        else:
            movie_id = movies.iloc[i[0]].id
            
        recommended_names.append(movies.iloc[i[0]].title)
        
        # Fetch the poster
        poster_url = fetch_poster(movie_id)
        recommended_posters.append(poster_url)
        
        # Wait 0.1 seconds to be polite to the API (Prevents getting blocked)
        time.sleep(0.1)

    return recommended_names, recommended_posters

# --- 4. UI ---
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie", movie_list)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Using a loop is cleaner
    cols = [col1, col2, col3, col4, col5]
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])