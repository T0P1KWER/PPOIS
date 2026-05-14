import tkinter as tk
from tkinter import ttk, messagebox


class Front:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("Ветеринарная клиника")
        self.root.geometry("1000x700")

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        actions_menu = tk.Menu(menubar, tearoff=0)
        actions_menu.add_command(label="Добавить питомца", command=controller.on_add_pet)
        actions_menu.add_command(label="Поиск", command=controller.on_search)
        actions_menu.add_command(label="Удалить", command=controller.on_delete)
        menubar.add_cascade(label="Действия", menu=actions_menu)
        toolbar = ttk.Frame(root, padding=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        btn_add = ttk.Button(toolbar, text="➕ Добавить", command=controller.on_add_pet)
        btn_add.pack(side=tk.LEFT, padx=5)
        btn_search = ttk.Button(toolbar, text="🔍 Поиск", command=controller.on_search)
        btn_search.pack(side=tk.LEFT, padx=5)
        btn_delete = ttk.Button(toolbar, text="🗑️ Удалить", command=controller.on_delete)
        btn_delete.pack(side=tk.LEFT, padx=5)
        columns = ("name", "birth", "visit", "vet", "diagnosis")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
        self.tree.heading("name", text="Имя питомца")
        self.tree.heading("birth", text="Дата рождения")
        self.tree.heading("visit", text="Дата приема")
        self.tree.heading("vet", text="Ветеринар")
        self.tree.heading("diagnosis", text="Диагноз")
        self.tree.column("name", width=150, anchor=tk.CENTER)
        self.tree.column("birth", width=100, anchor=tk.CENTER)
        self.tree.column("visit", width=100, anchor=tk.CENTER)
        self.tree.column("vet", width=150, anchor=tk.CENTER)
        self.tree.column("diagnosis", width=200, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.add_record_to_table("Барсик", "12.05.2020", "10.10.2023", "Иванов И.И.", "Здоров")

    def add_record_to_table(self, name, birth, visit, vet, diagnosis):
        self.tree.insert("" , tk.END, values=(name, birth, visit, vet, diagnosis))

    def show_message(self, title, message):
        messagebox.showinfo(title, message)


class Controller:
    def __init__(self, root):
        self.root = root
        self.view = Front(root, self)
        self.data = []


    def on_add_pet(self):
        self.view.show_message("Добавление", "Открываем окно добавления питомца...")

        self.view.add_record_to_table("Новый Кот", "01.01.2024", "20.10.2024", "Петров П.П.", "Осмотр")

    def on_search(self):
        self.view.show_message("Поиск", "Открываем окно поиска...")

    def on_delete(self):
        self.view.show_message("Удаление", "Открываем окно удаления...")

