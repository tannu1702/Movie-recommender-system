import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_posters(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?language=en-US&api_key=d4f861a2b13bfc284b60d7a825ddad93'.format(movie_id)
    ,timeout=10)
    data = response.json()
    print(data)
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_posters(movie_id))

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(
    'Choose a movie',
    movies['title'].values
)

if st.button('Recommend'):

   names,posters  = recommend(selected_movie_name)

   col1, col2, col3, col4 ,col5  = st.columns(5)

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
