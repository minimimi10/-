import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

FILENAME = "favorites.json"

# ---------- Работа с JSON ----------
def load_favorites():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []

def save_favorites(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

favorites = load_favorites()

# ---------- Поиск ----------
def search_users():
    query = entry.get().strip()

    if not query:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым")
        return

    url = f"https://api.github.com/search/users?q={query}"
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("Ошибка", "Ошибка API")
        return

    users = response.json()["items"]

    listbox.delete(0, tk.END)

    for user in users:
        listbox.insert(tk.END, user["login"])

# ---------- Добавление в избранное ----------
def add_to_favorites():
    selected = listbox.curselection()

    if not selected:
        return

    user = listbox.get(selected[0])

    if user not in favorites:
        favorites.append(user)
        save_favorites(favorites)
        messagebox.showinfo("Успех", f"{user} добавлен в избранное")
    else:
        messagebox.showinfo("Инфо", "Пользователь уже в избранном")

# ---------- Показ избранного ----------
def show_favorites():
    listbox.delete(0, tk.END)
    for user in favorites:
        listbox.insert(tk.END, user)

# ---------- GUI ----------
root = tk.Tk()
root.title("GitHub User Finder")

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

btn_search = tk.Button(root, text="Поиск", command=search_users)
btn_search.pack()

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

btn_add = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_add.pack()

btn_show = tk.Button(root, text="Показать избранное", command=show_favorites)
btn_show.pack()

root.mainloop()
