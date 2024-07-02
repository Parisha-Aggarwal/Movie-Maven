import streamlit as st
import pickle
import pandas as pd

import base64


# @st.cache(allow_output_mutation=True)
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image:  url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('movie.jpg')
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # extracting the index of the movie entered by the user
    distances = similarity[movie_index]  # distances will be the array of distances of that movie with other movies. We have to sort it also.
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # enumerate function is used to save the index of the movie after it is sorted. Lambda function is used to sort on the basis of distances.

    l=[]
    for i in movies_list:
        l.append(movies.iloc[i[0]].title)
    return l


movies_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movies of your choice !')
movie_name = st.selectbox(
    'Enter the movie name',
    movies['title'].values)


if st.button('Recommend'):
    recommendations = recommend(movie_name)
    for i in recommendations:
        st.write(i)