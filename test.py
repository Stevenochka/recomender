import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations():
    try:
        movie_name = entry.get()
        if not movie_name:
            messagebox.showinfo("Внимание", "Пожалуйста, введите название фильма.")
            return

        movies_data = pd.read_csv('movies.csv')
        selected_features = ['genres','keywords','tagline','cast','director']

        for feature in selected_features:
            movies_data[feature] = movies_data[feature].fillna('')

        all_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

        vectorizer = TfidfVectorizer()
        feature_vectors = vectorizer.fit_transform(all_features)

        similarity = cosine_similarity(feature_vectors)

        list_of_all_titles = movies_data['title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        if not find_close_match:
            messagebox.showinfo("Информация", "Фильм не найден.")
            return

        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        recommendation_list.delete(0, tk.END)
        i = 1
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies_data[movies_data.index == index]['title'].values[0]
            if i < 11:
                recommendation_list.insert(tk.END, f"{i}. {title_from_index}")
                i += 1
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

# Создание графического интерфейса
root = tk.Tk()
root.title("Рекомендации фильмов")

# Создание элементов интерфейса
label = tk.Label(root, text="Введите название фильма:")
label.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack()

button = tk.Button(root, text="Показать рекомендации", command=get_recommendations)
button.pack(pady=10)

recommendation_list = tk.Listbox(root, width=60, height=10)
recommendation_list.pack()

root.mainloop()
