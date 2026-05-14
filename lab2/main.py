import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys  # Нужно для перезапуска программы

# Импорты
from Pet import Pet
from Add_dialog import AddPetDialog
from Delete_dialog import DeleteDialog
from Search_dialog import SearchDialog
from data1 import XmlDomWriter, XmlSaxReader
from start_dialog import start_dialog


class Front:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Заголовок окна показывает текущий файл
        fname = os.path.basename(controller.current_file) if controller.current_file else "Выбор файла..."
        self.root.title(f"Ветеринарная клиника ({fname})")
        self.root.geometry("1000x700")

        # --- МЕНЮ ---
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Сохранить", command=controller.on_save)
        file_menu.add_command(label="Перезагрузить данные", command=controller.on_load)
        file_menu.add_separator()
        file_menu.add_command(label="🔄 Сменить базу данных (Перезапуск)", command=controller.restart_app)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        actions_menu = tk.Menu(menubar, tearoff=0)
        actions_menu.add_command(label="Добавить", command=controller.on_add_pet)
        actions_menu.add_command(label="Поиск", command=controller.on_search)
        actions_menu.add_command(label="Удалить", command=controller.on_delete)
        menubar.add_cascade(label="Действия", menu=actions_menu)

        # --- КНОПКИ (ПАНЕЛЬ ИНСТРУМЕНТОВ) ---
        toolbar = ttk.Frame(self.root, padding=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="➕ Добавить", command=controller.on_add_pet).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🔍 Поиск", command=controller.on_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🗑️ Удалить", command=controller.on_delete).pack(side=tk.LEFT, padx=5)

        # РАЗДЕЛИТЕЛЬ (вертикальная черта)
        ttk.Separator(toolbar, orient='vertical').pack(side=tk.LEFT, fill='y', padx=10, pady=5)

        # НОВАЯ КНОПКА ПЕРЕЗАПУСКА
        ttk.Button(toolbar, text="выбрать базу данных", command=controller.restart_app).pack(side=tk.LEFT, padx=5)

        # --- ТАБЛИЦА ---
        cols = ("name", "birth", "visit", "vet", "diagnosis")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=20)

        headers = {"name": "Имя питомца", "birth": "Дата рождения", "visit": "Дата приема", "vet": "Ветеринар",
                   "diagnosis": "Диагноз"}
        for col in cols:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=150, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def refresh_table(self, pets):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for pet in pets:
            d = pet.to_dict()
            self.tree.insert("", tk.END,
                             values=(d['name'], d['birthday'], d['last_visit_date'], d['vet_name'], d['diagnosis']))

    def show_message(self, title, msg):
        messagebox.showinfo(title, msg)


class Controller:
    # Явно объявляем атрибуты для IDE
    data = []
    current_file = None

    def __init__(self, root):
        self.root = root
        self.data = []
        self.current_file = None

        # 1. Диалог выбора файла
        dlg = start_dialog(root)
        root.wait_window(dlg.top)

        self.current_file = dlg.get_file()

        if not self.current_file:
            root.quit()
            return

        # 2. Создаем интерфейс
        self.view = Front(root, self)

        # 3. Загружаем данные
        if os.path.exists(self.current_file):
            self.on_load(silent=True)
        else:
            self.view.show_message("Инфо", f"Файл {self.current_file} не найден. Начнем с пустой базы.")

    def restart_app(self):
        """Перезапускает программу заново"""
        answer = messagebox.askyesno("выбрать базу","выбор базы")
        if answer:
            python = sys.executable

            os.execl(python, python, *sys.argv)

    def on_add_pet(self):
        dlg = AddPetDialog(self.root)
        self.root.wait_window(dlg.top)
        res = dlg.get_result()
        if res:
            pet = Pet(res['name'], res['birthday'], res['last_visit_date'], res['vet_name'], res['diagnosis'])
            self.data.append(pet)
            self.view.refresh_table(self.data)
            self.on_save(silent=True)

    def on_search(self):
        dlg = SearchDialog(self.root, self.data)
        self.root.wait_window(dlg.top)

    def on_delete(self):
        dlg = DeleteDialog(self.root)
        self.root.wait_window(dlg.top)
        cond = dlg.get_conditions()

        if not cond:
            return

        keep = []
        count = 0

        # Исправленный цикл
        for p in self.data:
            drop = False
            bs = p.birthday.strftime('%Y-%m-%d')
            vs = p.last_visit_date.strftime('%Y-%m-%d')

            if cond['name'] and cond['name'].lower() in p.name.lower():
                drop = True
            if cond['birth_date'] and cond['birth_date'] == bs:
                drop = True
            if cond['visit_date'] and cond['visit_date'] == vs:
                drop = True
            if cond['vet_name'] and cond['vet_name'].lower() in p.vet_name.lower():
                drop = True
            if cond['diagnosis_phrase'] and cond['diagnosis_phrase'].lower() in p.diagnosis.lower():
                drop = True

            if drop:
                count += 1
            else:
                keep.append(p)

        self.data = keep
        self.view.refresh_table(self.data)
        self.on_save(silent=True)

        msg = f"Удалено записей: {count}" if count > 0 else "Ничего не найдено."
        self.view.show_message("Результат", msg)

    def on_save(self, silent=False):
        if not self.current_file:
            return
        XmlDomWriter(self.current_file).write(self.data)
        if not silent:
            self.view.show_message("OK", f"Данные сохранены в {self.current_file}")

    def on_load(self, silent=False):
        if not self.current_file or not os.path.exists(self.current_file):
            if not silent:
                self.view.show_message("Ошибка", "Файл не найден!")
            return

        pets = XmlSaxReader(self.current_file).read()
        if pets:
            self.data = pets
            self.view.refresh_table(self.data)
            if not silent:
                self.view.show_message("OK", f"Загружено: {len(pets)}")


if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()