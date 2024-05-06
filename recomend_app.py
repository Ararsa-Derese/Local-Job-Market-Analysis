import streamlit as st
import pandas as pd
import numpy as np
import string
import pickle
df1 = pd.read_csv('new.csv', engine ='python')
df1 = df1.dropna()
from sklearn.feature_extraction.text import TfidfVectorizer

tdif = TfidfVectorizer(stop_words='english')

df1['jobdescription'] = df1['jobdescription'].fillna('')

tdif_matrix = tdif.fit_transform(df1['jobdescription'])

tdif_matrix.shape

from sklearn.metrics.pairwise import sigmoid_kernel

cosine_sim = sigmoid_kernel(tdif_matrix, tdif_matrix)
indices = pd.Series(df1.index, index=df1['jobtitle']).drop_duplicates()
def get_recommendations(title, cosine_sim=cosine_sim):
  idx = indices[title]
  sim_scores = list(enumerate(cosine_sim[idx]))
  if isinstance(sim_scores, np.ndarray):
    sim_scores = sim_scores.tolist()

# Check if the elements in sim_scores are arrays or single values
  for item, score in sim_scores:
      if isinstance(score, np.ndarray):
          # Handle if score is an array
          # For example, if you want to take the mean of the array
          score = np.mean(score)
  sim_scores = sorted(sim_scores, key=lambda X: X[1], reverse=True)
  sim_scores = sim_scores[1:16]
  tech_indices = [i[0] for i in sim_scores]
  return df1['jobdescription'].iloc[tech_indices]



st.header('tech jobs recommender')
movies = pd.read_pickle('job_list.pkl')
similarity= pd.read_pickle('similarity.pkl')
toon_list = movies['jobtitle'].values
selected_toon = st.selectbox(
    "Type or select a job from the dropdown",
    toon_list
)


if st.button('Show Recommendation'):
    recommended_toon_names = get_recommendations(selected_toon)
    if recommended_toon_names is None:
        st.write("No Recommendations Found")
    else:
      for i in recommended_toon_names:
          st.subheader(i)
        



