import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_movie_card(movie_id):
   api_url = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=acf81b3943e77919437f27b6148ea056'.format(movie_id))
   json_data = api_url.json()
   image_path = "https://image.tmdb.org/t/p/original/" + json_data['poster_path']
   return image_path
   

def get_recommendation(movie_title):
  index = movies_df[movies_df['title']==movie_title].index[0]
  similarity_scores = similarity[index]
  movies_list = list(enumerate(similarity_scores))
  top_10 = sorted(movies_list,reverse= True, key = lambda x:x[1])[1:11]
  recommendations = []
  movie_cards = []
  for i in top_10:
    poster_id = movies_df.iloc[i[0]].movie_id
    movie_cards.append(get_movie_card(poster_id))
    recommendations.append(movies_df.iloc[i[0]].title)
  return movie_cards,recommendations 
logo_url = "/home/navaal-iqbal/vscode/Recommender System/data/cinema (1).png"
st.image(logo_url, width=100)
st.title('Movie Recommendation System')
movies  = pickle.load(open('data/movies.pkl','rb'))
similarity= pickle.load(open('data/similarity.pkl','rb'))
movies_df = pd.DataFrame(movies)
selection= st.selectbox(
   "",
   movies_df['title'],
   index=None,
   placeholder="Enter movie name..",
)

if st.button("Recommend", type='primary'):
    images, recommendations = get_recommendation(selection)
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

# Distribute images across columns
    for i, img_url in enumerate(images):
       with columns[i % 5]:
          st.image(img_url, caption=recommendations[i], use_column_width=True)

