import streamlit as st
import pickle
import pandas as pd
import requests
import joblib
import os
import time

# 1. Page Config (Must be the very first command)
st.set_page_config(layout="wide") 

st.header('Movie Recommender System')

# --- 2. LOAD DATA ---
current_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_data():
    try:
        # Load movie list
        movies_path = os.path.join(current_dir, 'movie_list.pkl')
        movies = pickle.load(open(movies_path, 'rb'))
        
        # Load similarity matrix (Trying compressed first, then normal)
        sim_path_compressed = os.path.join(current_dir, 'similarity_compressed.pkl')
        sim_path_normal = os.path.join(current_dir, 'similarity.pkl')
        
        if os.path.exists(sim_path_compressed):
            similarity = joblib.load(sim_path_compressed)
        else:
            similarity = pickle.load(open(sim_path_normal, 'rb'))
            
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data files: {e}")
        return None, None

movies, similarity = load_data()

if movies is None:
    st.stop()

# --- 3. POSTER FETCHER ---
def fetch_poster(movie_id):
    # Your specific API Key
    api_key = "cd76cf2795eb1690d74cf60297624f65"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    fallback = "https://via.placeholder.com/500x750?text=No+Image"
    
    # Retry logic (3 attempts)
    for _ in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get('poster_path'):
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            else:
                return fallback
                
        except requests.exceptions.RequestException:
            time.sleep(0.2) # Short pause before retry
            continue
            
    return fallback

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    names = []
    posters = []
    
    for i in distances[1:6]:
        # Handle ID column variations
        if 'movie_id' in movies.columns:
            m_id = movies.iloc[i[0]].movie_id
        elif 'id' in movies.columns:
            m_id = movies.iloc[i[0]].id
        else:
            m_id = movies.iloc[i[0]].values[0] # Fallback
            
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(m_id))
        
    return names, posters

# --- 4. UI ---
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie", movie_list)

if st.button('Show Recommendation'):
    with st.spinner('Loading...'):
        names, posters = recommend(selected_movie)
        
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                # FIX: Using 'width="stretch"' to solve the deprecation error
                st.image(posters[i], width="stretch")
                st.caption(names[i])