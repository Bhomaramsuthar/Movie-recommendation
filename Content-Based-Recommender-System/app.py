import streamlit as st
import pickle
import requests
import os

st.set_page_config(layout="wide", page_title="Movie Recommender")

st.header('Movie Recommender System')

# --- LOAD DATA ---
current_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_data():
    # Load the Answer Key (Tiny Dictionary)
    dict_path = os.path.join(current_dir, 'similarity_dict.pkl')
    similarity_dict = pickle.load(open(dict_path, 'rb'))
    return similarity_dict

similarity_dict = load_data()

if similarity_dict is None:
    st.error("Error: 'similarity_dict.pkl' not found.")
    st.stop()

# --- POSTER FETCHER ---
def fetch_poster(movie_id):
    api_key = "cd76cf2795eb1690d74cf60297624f65"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('poster_path'):
                return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
    except:
        pass
    return "https://via.placeholder.com/185x278?text=No+Image"

# --- UI ---
# Get movie list directly from the dictionary keys
movie_list = sorted(similarity_dict.keys())
selected_movie = st.selectbox("Type or select a movie", movie_list)

if st.button('Show Recommendation'):
    with st.spinner('Thinking...'):
        
        # 1. Look up answer instantly (O(1) complexity)
        # The dict already has [(Title, ID), (Title, ID)...]
        recommendations = similarity_dict.get(selected_movie, [])
        
        # 2. Fetch Posters
        cols = st.columns(5)
        for i in range(min(5, len(recommendations))):
            name = recommendations[i][0]
            m_id = recommendations[i][1]
            poster = fetch_poster(m_id)
            
            with cols[i]:
                st.image(poster, caption=name, width="stretch")