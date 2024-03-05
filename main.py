#Импорт зависимостей
import numpy as np # для матриц
import pandas as pd # для создания таблиц
import difflib # для поиска более похожего значения
from sklearn.feature_extraction.text import TfidfVectorizer # преобразование тект данных в числовые значения (векторы-признаков)
from sklearn.metrics.pairwise import cosine_similarity # Косинусное сходство

#Мы вводим название фильма, при помощи библиотеки дифлиб находим самое похожий по названию фильм,
# далее превращаем его в вектор и по косиносному сходству определяем рекомендации

#Обработка данных
movies_data = pd.read_csv('movies.csv')
selected_features = ['genres','keywords','tagline','cast','director']

for feature in selected_features:
  movies_data[feature] = movies_data[feature].fillna('')

all_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(all_features)

similarity = cosine_similarity(feature_vectors)

movie_name = input(' Enter your favourite movie name : ')
list_of_all_titles = movies_data['title'].tolist()
find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
close_match = find_close_match[0]
index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
similarity_score = list(enumerate(similarity[index_of_the_movie]))
sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True)
print('Movies suggested for you : \n')
i = 1
for movie in sorted_similar_movies:
  index = movie[0]
  title_from_index = movies_data[movies_data.index==index]['title'].values[0]
  if (i<11):
    print(i, '.',title_from_index)
    i+=1

    """<script type="text/javascript">
        async function display_movie() {
            let movie = document.getElementById('location').value;
            let res = await eel.movie_rec(movie)();
            document.querySelector('.info').innerHTML = res; // Обращение к элементу с классом "info"
        }

        document.getElementById('show').addEventListener('click', function() {
            display_movie();
        });
    </script>"""