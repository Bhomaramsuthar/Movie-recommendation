# 🎬 Movie Recommender System

A Content-Based Movie Recommendation System built with Python and Streamlit. It recommends similar movies based on metadata (tags, genres, cast, crew) and fetches real-time movie posters using the TMDB API.

🔗 **Live Demo:** [Click here to view the App](https://movie-recommendation-cosine-similarity.streamlit.app/)  
*(Note: The app is hosted on Streamlit's free tier. If it is "sleeping," please click 'Wake Up' and wait ~45 seconds for it to load.)*

---

## 🚀 Features
* **Content-Based Filtering:** Uses Cosine Similarity to find movies with similar tags, genres, and descriptions.
* **Smart Search:** Select any movie from a database of 5,000+ films.
* **Live Posters:** Fetches high-quality movie posters dynamically via the TMDB API.
* **Robust Deployment:** Optimized with `joblib` compression to handle large similarity matrices within GitHub's file limits.
* **Responsive UI:** Built with Streamlit for a clean, interactive user experience.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend:** Python, Pandas, Numpy
* **Machine Learning:** Scikit-learn (CountVectorizer, Cosine Similarity)
* **API:** The Movie Database (TMDB) API
* **Deployment:** Streamlit Cloud

## 🧠 How It Works
1.  **Data Preprocessing:** The system combines movie genres, keywords, cast, and crew into a single "tags" column.
2.  **Vectorization:** Uses `CountVectorizer` to convert text tags into numerical vectors.
3.  **Similarity Calculation:** Calculates the Cosine Similarity between these vectors to determine which movies are closest to each other in multi-dimensional space.
4.  **Recommendation:** When a user selects a movie, the system retrieves the top 5 closest vectors (movies) and displays them.

## 📦 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Bhomaramsuthar/Movie-recommendation.git](https://github.com/Bhomaramsuthar/Movie-recommendation.git)
    cd Movie-recommendation
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure
├── app.py # Main application logic <br>
├── movie_list.pkl # Pre-processed movie dataframe <br>
├── similarity_compressed.pkl # Compressed similarity matrix (Joblib) <br>
├── requirements.txt # Project dependencies <br>
├── .gitignore # Files excluded from Git <br>
└── README.md # Project documentation<br>


---

### 📬 Contact
Created by **Bhomaram Suthar** - [LinkedIn Profile](https://www.linkedin.com/in/bhomaram-suthar-651a672a6/)