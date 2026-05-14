import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class AddPetDialog:
    def __init__(self, parent):
        self.result = None

        self.top = tk.Toplevel(parent)
        self.top.title("Добавить питомца")
        self.top.geometry("400x320")
        self.top.resizable(False, False)

        self.top.transient(parent)
        self.top.grab_set()

        ttk.Label(self.top, text="Имя питомца:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_name = ttk.Entry(self.top, width=30)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.top, text="Дата рождения\n(ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_birth = ttk.Entry(self.top, width=30)
        self.entry_birth.grid(row=1, column=1, padx=10, pady=5)
        self.entry_birth.insert(0, date.today().strftime('%Y-%m-%d'))

        ttk.Label(self.top, text="Дата приема\n(ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_visit = ttk.Entry(self.top, width=30)
        self.entry_visit.grid(row=2, column=1, padx=10, pady=5)
        self.entry_visit.insert(0, date.today().strftime('%Y-%m-%d'))

        ttk.Label(self.top, text="Ветеринар:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entry_vet = ttk.Entry(self.top, width=30)
        self.entry_vet.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.top, text="Диагноз:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entry_diag = ttk.Entry(self.top, width=30)
        self.entry_diag.grid(row=4, column=1, padx=10, pady=5)

        btn_frame = ttk.Frame(self.top)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.top.destroy).pack(side=tk.LEFT, padx=10)

        self.entry_name.focus()

    def on_ok(self):
        name = self.entry_name.get().strip()
        birth_str = self.entry_birth.get().strip()
        visit_str = self.entry_visit.get().strip()

        if not name:
            messagebox.showwarning("Ошибка", "Введите имя питомца!")
            return

        self.result = {
            'name': name,
            'birthday': birth_str,
            'last_visit_date': visit_str,
            'vet_name': self.entry_vet.get().strip(),
            'diagnosis': self.entry_diag.get().strip()
        }
        self.top.destroy()

    def get_result(self):
        return self.result