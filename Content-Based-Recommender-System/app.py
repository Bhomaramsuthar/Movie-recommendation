import streamlit as st
import pickle
import requests
import os
import gc

st.set_page_config(layout="wide", page_title="Movie Recommender")

st.header('Movie Recommender System')

# --- LOAD DATA ---
current_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_data():
    try:
        # Load the Answer Key (Dictionary)
        dict_path = os.path.join(current_dir, 'similarity_dict.pkl')
        if not os.path.exists(dict_path):
            return None
        return pickle.load(open(dict_path, 'rb'))
    except:
        return None

similarity_dict = load_data()

if similarity_dict is None:
    st.error("Error: Please make sure 'similarity_dict.pkl' is in the folder.")
    st.stop()

# --- POSTER FETCHER ---
def fetch_poster(movie_id):
    api_key = "cd76cf2795eb1690d74cf60297624f65"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        # Timeout is crucial so the app doesn't freeze waiting for images
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('poster_path'):
                return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
    except:
        pass
    return "https://via.placeholder.com/185x278?text=No+Image"

# --- UI SECTION ---
movie_list = sorted(similarity_dict.keys())
selected_movie = st.selectbox("Type or select a movie", movie_list)

# 1. Create a placeholder container for the results
# This reserves a specific area on the screen.
results_container = st.container()

if st.button('Show Recommendation'):
    
    # 2. CLEAR PREVIOUS RESULTS (The Fix)
    # This forces the browser to dump the old images from memory immediately.
    results_container.empty()
    
    with st.spinner('Thinking...'):
        recommendations = similarity_dict.get(selected_movie, [])
        
        # 3. Draw new results inside the container
        with results_container:
            cols = st.columns(5)
            for i in range(min(5, len(recommendations))):
                name = recommendations[i][0]
                m_id = recommendations[i][1]
                poster = fetch_poster(m_id)
                
                with cols[i]:
                    # Use 'width="stretch"' for mobile stability
                    st.image(poster, caption=name, width="stretch")
            
    # Force python to clear backend memory too
    gc.collect()