import streamlit as st
import pandas as pd
import pickle
from huggingface_hub import hf_hub_download

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ==========================================
# Load Data
# ==========================================
@st.cache_resource
def load_data():

    # Load movie dictionary
    with open("movies_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)

    # Download similarity matrix from Hugging Face
    similarity_path = hf_hub_download(
        repo_id="Amrritt/movie-recommender-model",
        filename="similarity.pkl"
    )

    with open(similarity_path, "rb") as f:
        similarity = pickle.load(f)

    movies = pd.DataFrame(movies_dict)

    return movies, similarity


movies, similarity = load_data()

# ==========================================
# Recommendation Function
# ==========================================
def recommend(movie):

    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []

    for i in distances[1:6]:
        recommended_movies.append(
            movies.iloc[i[0]].title
        )

    return recommended_movies


# ==========================================
# Sidebar
# ==========================================
st.sidebar.title("🎬 Movie Recommender")

st.sidebar.markdown("### 📌 Project Information")

st.sidebar.info(
"""
This application recommends **5 similar movies**
using a **Content-Based Recommendation System**.

It compares movie features using
**Cosine Similarity**.
"""
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Dataset")

st.sidebar.metric("Total Movies", len(movies))

st.sidebar.markdown("---")

st.sidebar.markdown("### 🛠 Tech Stack")

st.sidebar.markdown("""
- Python
- Pandas
- Scikit-learn
- Streamlit
- Hugging Face
""")

st.sidebar.markdown("---")

st.sidebar.success("Developed by **Amrit Raj**")

# ==========================================
# Main Page
# ==========================================

st.title("🎬 Movie Recommendation System")

st.markdown(
"""
Discover movies similar to your favorite ones using a
**Machine Learning Content-Based Recommendation System**.

Simply choose a movie below and click **Recommend**.
"""
)

st.markdown("---")

# ==========================================
# Movie Selection
# ==========================================

selected_movie = st.selectbox(
    "🎥 Select a Movie",
    movies["title"].values
)

# ==========================================
# Recommend Button
# ==========================================

if st.button("🚀 Recommend Movies", use_container_width=True):

    recommendations = recommend(selected_movie)

    st.success("Top 5 Recommendations")

    for i, movie in enumerate(recommendations, start=1):
        st.write(f"**{i}. {movie}**")

# ==========================================
# About Project
# ==========================================

st.markdown("---")

st.subheader("📖 About this Project")

st.write(
"""
This project demonstrates a **Content-Based Movie Recommendation System**
built using **Machine Learning**.

The recommendation engine analyzes movie features such as genres,
keywords, cast, and crew, then calculates **Cosine Similarity**
to identify movies that are most similar to the selected movie.

The similarity matrix is hosted on **Hugging Face**, making the
GitHub repository lightweight while enabling fast deployment.
"""
)

st.markdown("---")

st.caption(
"© 2026 Amrit Raj | IIT Bhubaneswar | Robotics & AI"
)