import tkinter as tk
from tkinter import ttk, messagebox


class SearchDialog:
    def __init__(self, parent, all_pets):
        self.parent = parent
        self.all_pets = all_pets
        self.filtered_pets = []

        self.RECORDS_PER_PAGE = 10
        self.current_page = 1
        self.total_pages = 1

        self.top = tk.Toplevel(parent)
        self.top.title("Поиск записей")
        self.top.geometry("700x550")
        self.top.resizable(False, False)

        self.top.transient(parent)
        self.top.grab_set()

        conditions_frame = ttk.LabelFrame(self.top, text="Условия поиска", padding=10)
        conditions_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(conditions_frame, text="Имя:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_name = ttk.Entry(conditions_frame, width=20)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(conditions_frame, text="Дата рожд. (ГГГГ-ММ-ДД):").grid(row=0, column=2, sticky="w", pady=5)
        self.entry_birth = ttk.Entry(conditions_frame, width=15)
        self.entry_birth.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(conditions_frame, text="Дата приема (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_visit = ttk.Entry(conditions_frame, width=15)
        self.entry_visit.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(conditions_frame, text="Ветеринар:").grid(row=1, column=2, sticky="w", pady=5)
        self.entry_vet = ttk.Entry(conditions_frame, width=20)
        self.entry_vet.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(conditions_frame, text="Фраза из диагноза:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_diag = ttk.Entry(conditions_frame, width=40)
        self.entry_diag.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        btn_search = ttk.Button(conditions_frame, text="🔍 Найти", command=self.on_search)
        btn_search.grid(row=3, column=0, columnspan=4, pady=10)
        btn_search.configure(width=20)

        results_frame = ttk.LabelFrame(self.top, text="Результаты", padding=10)
        results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        columns = ("name", "birth", "visit", "vet", "diagnosis")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)

        self.tree.heading("name", text="Имя")
        self.tree.heading("birth", text="Дата рожд.")
        self.tree.heading("visit", text="Дата приема")
        self.tree.heading("vet", text="Ветеринар")
        self.tree.heading("diagnosis", text="Диагноз")

        self.tree.column("name", width=100, anchor=tk.CENTER)
        self.tree.column("birth", width=80, anchor=tk.CENTER)
        self.tree.column("visit", width=80, anchor=tk.CENTER)
        self.tree.column("vet", width=100, anchor=tk.CENTER)
        self.tree.column("diagnosis", width=150, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        page_frame = ttk.Frame(self.top)
        page_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        ttk.Button(page_frame, text="<< Первая", command=lambda: self.change_page(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(page_frame, text="< Пред.", command=lambda: self.change_page(-1)).pack(side=tk.LEFT, padx=2)

        self.lbl_page_info = ttk.Label(page_frame, text="Стр. 1 из 1")
        self.lbl_page_info.pack(side=tk.LEFT, padx=10)

        ttk.Button(page_frame, text="След. >", command=lambda: self.change_page(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(page_frame, text="Последняя >>", command=lambda: self.change_page(9999)).pack(side=tk.LEFT, padx=2)


    def on_search(self):
        name_val = self.entry_name.get().strip().lower()
        birth_val = self.entry_birth.get().strip()
        visit_val = self.entry_visit.get().strip()
        vet_val = self.entry_vet.get().strip().lower()
        diag_val = self.entry_diag.get().strip().lower()

        if not any([name_val, birth_val, visit_val, vet_val, diag_val]):
            messagebox.showwarning("Внимание", "Введите хотя бы одно условие!")
            return

        self.filtered_pets = []
        for pet in self.all_pets:
            match = True
            if name_val and name_val not in pet.name.lower(): match = False
            if birth_val and pet.birthday.strftime('%Y-%m-%d') != birth_val: match = False
            if visit_val and pet.last_visit_date.strftime('%Y-%m-%d') != visit_val: match = False
            if vet_val and vet_val not in pet.vet_name.lower(): match = False
            if diag_val and diag_val not in pet.diagnosis.lower(): match = False

            if match:
                self.filtered_pets.append(pet)

        self.current_page = 1
        self.update_table()

        count = len(self.filtered_pets)
        if count == 0:
            messagebox.showinfo("Результат", "Ничего не найдено.")
        else:
            messagebox.showinfo("Результат", f"Найдено записей: {count}")

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.filtered_pets:
            self.lbl_page_info.config(text="Стр. 0 из 0")
            return

        limit = self.RECORDS_PER_PAGE

        self.total_pages = (len(self.filtered_pets) + limit - 1) // limit

        if self.current_page > self.total_pages: self.current_page = self.total_pages
        if self.current_page < 1: self.current_page = 1

        start_idx = (self.current_page - 1) * limit
        end_idx = start_idx + limit
        page_data = self.filtered_pets[start_idx:end_idx]

        for pet in page_data:
            d = pet.to_dict()
            self.tree.insert("", tk.END,
                             values=(d['name'], d['birthday'], d['last_visit_date'], d['vet_name'], d['diagnosis']))

        self.lbl_page_info.config(
            text=f"Стр. {self.current_page} из {self.total_pages} (Всего: {len(self.filtered_pets)})")

    def change_page(self, direction):
        if not self.filtered_pets: return
        if direction == 1 and self.current_page < self.total_pages:
            self.current_page += 1
        elif direction == -1 and self.current_page > 1:
            self.current_page -= 1
        elif direction == 9999:
            self.current_page = self.total_pages
        else:
            self.current_page = 1
        self.update_table()