import streamlit as st
import pickle
import requests
import os
import gc  # Garbage collection to free up memory
from sklearn.metrics.pairwise import cosine_similarity

# 1. PAGE CONFIG (Must be first)
st.set_page_config(layout="wide", page_title="Movie Recommender")

st.header('Movie Recommender System')

# --- 2. LOAD DATA (Lightweight Version) ---
current_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_data():
    try:
        # Load the Movie List
        movies_path = os.path.join(current_dir, 'movie_list.pkl')
        movies = pickle.load(open(movies_path, 'rb'))
        
        # Load the Vectors (Not the massive similarity matrix)
        vectors_path = os.path.join(current_dir, 'vectors.pkl')
        vectors = pickle.load(open(vectors_path, 'rb'))
        
        return movies, vectors
    except Exception as e:
        st.error(f"Error loading files. Please make sure 'vectors.pkl' exists. Details: {e}")
        return None, None

movies, vectors = load_data()

if movies is None:
    st.stop()

# --- 3. ROBUST POSTER FETCHER ---
def fetch_poster(movie_id):
    # Your API Key
    api_key = "cd76cf2795eb1690d74cf60297624f65"
    
    # Use w185 (Mobile-Optimized Size) instead of w500
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    fallback = "https://via.placeholder.com/185x278?text=No+Image"
    
    try:
        # Timeout set to 3 seconds to prevent hanging
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
        else:
            return fallback
    except:
        return fallback

# --- 4. RECOMMENDATION LOGIC (On-the-Fly) ---
def recommend(movie):
    # 1. Find the index of the movie
    movie_index = movies[movies['title'] == movie].index[0]
    
    # 2. CALCULATE SIMILARITY NOW (Lazy Loading)
    # Instead of loading a 500MB matrix, we calculate just this 1 row instantly.
    # This uses almost 0 RAM.
    similarity_scores = cosine_similarity(vectors[movie_index], vectors).flatten()
    
    # 3. Sort results
    distances = sorted(list(enumerate(similarity_scores)), reverse=True, key=lambda x: x[1])
    
    names = []
    posters = []
    
    # 4. Fetch top 5
    for i in distances[1:6]:
        # Handle different column names for ID
        if 'movie_id' in movies.columns:
            m_id = movies.iloc[i[0]].movie_id
        elif 'id' in movies.columns:
            m_id = movies.iloc[i[0]].id
        else:
            m_id = movies.iloc[i[0]].values[0]
            
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(m_id))
        
    # Force memory cleanup
    gc.collect()
    
    return names, posters

# --- 5. UI ---
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie", movie_list)

if st.button('Show Recommendation'):
    with st.spinner('Thinking...'):
        names, posters = recommend(selected_movie)
        
        # Use Columns with "use_container_width" for best responsiveness
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i], caption=names[i], use_container_width=True)