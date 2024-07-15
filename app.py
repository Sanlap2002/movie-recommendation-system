import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3N2Y2ZjBlMGYzOWRmNTk0YmQwMzVkNjA4MWY4YWQyYiIsIm5iZiI6MTcyMDk2NTc2NC4zMTI2MjMsInN1YiI6IjY2OTNkNzBkOTk5ODY3NGE2ZmE3YmQwYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DYiLZp3mQ9Y8AWk6SWojkB8zgs_a5yFKsGDoptZqG_U"
    }

    response = requests.get(url, headers=headers)

    data=response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend_movies(movie):
    ## Once we get the movie name we have to locate the movie ,for that we need to have the index and the below line fetches the index
    movie_index=movies[movies['title']==movie].index[0]
    similarities=distances[movie_index]
    ## We can sort the the rows but by that we will lose the index positions as distances[0] contains cosine similarity of all the indices with other indices
    movies_list=sorted(list(enumerate(similarities)),reverse=True,key=lambda x:x[1])[1:6]
    recommended=[]
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended,recommended_movie_posters



st.title('Movie Recommendation System')
st.header('We might have what you are looking for..')

movies_list=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_list)
distances=pickle.load(open('similarities.pkl','rb'))
 
selected = st.selectbox('Search bar',
 movies.title.values)
if st.button("Recommend"):
  names,posters=recommend_movies(selected)
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

#st.write("You selected:", option)