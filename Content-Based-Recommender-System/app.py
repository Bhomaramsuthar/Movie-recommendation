import streamlit as st
import pickle
import requests
import os
import gc
from sklearn.metrics.pairwise import cosine_similarity

# 1. PAGE CONFIG
st.set_page_config(layout="wide", page_title="Movie Recommender")

st.header('Movie Recommender System')

# --- 2. LOAD DATA ---
current_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_data():
    try:
        # Load Movie List
        movies_path = os.path.join(current_dir, 'movie_list.pkl')
        movies = pickle.load(open(movies_path, 'rb'))
        
        # Load VECTORS (Ensure vectors.pkl is in your folder!)
        vectors_path = os.path.join(current_dir, 'vectors.pkl')
        vectors = pickle.load(open(vectors_path, 'rb'))
        
        return movies, vectors
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return None, None

movies, vectors = load_data()

if movies is None:
    st.stop()

# --- 3. POSTER FETCHER ---
def fetch_poster(movie_id):
    api_key = "cd76cf2795eb1690d74cf60297624f65"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    fallback = "https://via.placeholder.com/185x278?text=No+Image"
    
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
        else:
            return fallback
    except:
        return fallback

# --- 4. RECOMMEND FUNCTION ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    
    # Calculate similarity on the fly (Fast & Low Memory)
    similarity_scores = cosine_similarity(vectors[movie_index], vectors).flatten()
    
    distances = sorted(list(enumerate(similarity_scores)), reverse=True, key=lambda x: x[1])
    
    names = []
    posters = []
    
    for i in distances[1:6]:
        # Handle ID safely
        if 'movie_id' in movies.columns:
            m_id = movies.iloc[i[0]].movie_id
        elif 'id' in movies.columns:
            m_id = movies.iloc[i[0]].id
        else:
            m_id = movies.iloc[i[0]].values[0]
            
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(m_id))
        
    gc.collect()
    return names, posters

# --- 5. UI ---
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie", movie_list)

if st.button('Show Recommendation'):
    with st.spinner('Thinking...'):
        names, posters = recommend(selected_movie)
        
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                # FIX: Replaced 'use_container_width' with 'width="stretch"'
                # This matches exactly what your error logs asked for.
                st.image(posters[i], caption=names[i], width="stretch")