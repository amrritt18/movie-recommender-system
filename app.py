import streamlit as st
import pandas as pd
import pickle
from huggingface_hub import hf_hub_download

# Load Dataset
@st.cache_resource
def load_data():
    # Load local movie dictionary
    with open("movies_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)

    # Download similarity.pkl from Hugging Face
    similarity_path = hf_hub_download(
        repo_id="Amrritt/movie-recommender-model",
        filename="similarity.pkl"
    )

    with open(similarity_path, "rb") as f:
        similarity = pickle.load(f)

    movies = pd.DataFrame(movies_dict)

    return movies, similarity


movies, similarity = load_data()


# Recommendation Function
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        key=lambda x: x[1],
        reverse=True,
    )

    recommended_movies = []

    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# Streamlit UI
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 Movie Recommender System")
st.write("Select a movie and discover five similar movies using a content-based recommendation system.")

selected_movie = st.selectbox(
    "Choose a Movie",
    movies["title"].values,
)

if st.button("Recommend"):

    recommendations = recommend(selected_movie)

    st.subheader("🎥 Recommended Movies")

    for i, movie in enumerate(recommendations, start=1):
        st.write(f"**{i}. {movie}**")