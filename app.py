import streamlit as st
import pickle
import requests
import pandas as pd
import urllib.request
import gdown


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=1b287d5b39bbb4f0506e1aac120693f1&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movies_id))
    return recommended_movies, recommended_movie_posters


movies_dict = pickle.load(open('movie_dict.pkl.', 'rb'))
file_id = '1xugIC10orCX3Kx_M7lRLzxU9V5rg0NWM'

# URL to download the file
url = f'https://drive.google.com/uc?id={file_id}'

try:
    # Download the file using gdown
    gdown.download(url, 'similarity.pkl', quiet=False)

    # Now you can load the binary data as a pickle
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)

except Exception as e:
    st.write(f"An error occurred: {e}")
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')
selected_movies_name = st.selectbox(
    'how would you like to be contacted?',
    movies['title'].values)
if st.button('Recommend'):
    names, posters = recommend(selected_movies_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
colored_text = """
    <div style='color: blue;font-weight: bold'>
        In contributions of 3.
    </div>
    <br>
    <div style='color:White;font-weight:bold'>
    Anurag
    <br>
    Awnish
    <br>
    Adil
"""

st.markdown(colored_text, unsafe_allow_html=True)
