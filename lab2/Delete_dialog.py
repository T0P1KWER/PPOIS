import tkinter as tk
from tkinter import ttk, messagebox


class DeleteDialog:
    def __init__(self, parent):
        self.result_conditions = None
        self.top = tk.Toplevel(parent)
        self.top.title("Удаление записей")
        self.top.geometry("450x380")
        self.top.resizable(False, False)

        self.top.transient(parent)
        self.top.grab_set()

        ttk.Label(self.top, text="Введите условия для удаления:", font=("Arial", 12, "bold")).grid(row=0, column=0,
                                                                                                   columnspan=2,
                                                                                                   pady=10, padx=10,
                                                                                                   sticky="w")

        ttk.Label(self.top, text="Имя питомца:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_name = ttk.Entry(self.top, width=30)
        self.entry_name.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.top, text="Дата рождения\n(ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_birth = ttk.Entry(self.top, width=30)
        self.entry_birth.grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(self.top, text="(оставьте пустым, если не нужно)", font=("Arial", 8), foreground="gray").grid(row=3,
                                                                                                                column=1,
                                                                                                                sticky="w",
                                                                                                                padx=10)

        ttk.Separator(self.top, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10, padx=10)

        ttk.Label(self.top, text="Дата приема\n(ГГГГ-ММ-ДД):").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.entry_visit = ttk.Entry(self.top, width=30)
        self.entry_visit.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.top, text="ФИО Ветеринара:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.entry_vet = ttk.Entry(self.top, width=30)
        self.entry_vet.grid(row=6, column=1, padx=10, pady=5)

        ttk.Separator(self.top, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky='ew', pady=10, padx=10)

        ttk.Label(self.top, text="Фраза из диагноза:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        self.entry_diag = ttk.Entry(self.top, width=30)
        self.entry_diag.grid(row=8, column=1, padx=10, pady=5)
        ttk.Label(self.top, text="(часть текста)", font=("Arial", 8), foreground="gray").grid(row=9, column=1,
                                                                                              sticky="w", padx=10)

        btn_frame = ttk.Frame(self.top)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="🗑️ Удалить найденные", command=self.on_delete).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.top.destroy).pack(side=tk.LEFT, padx=10)

        self.entry_name.focus()

    def on_delete(self):
        name_val = self.entry_name.get().strip()
        birth_val = self.entry_birth.get().strip()
        visit_val = self.entry_visit.get().strip()
        vet_val = self.entry_vet.get().strip()
        diag_val = self.entry_diag.get().strip()

        conditions = {
            'name': name_val if name_val else None,
            'birth_date': birth_val if birth_val else None,
            'visit_date': visit_val if visit_val else None,
            'vet_name': vet_val if vet_val else None,
            'diagnosis_phrase': diag_val if diag_val else None
        }

        if not any([conditions['name'], conditions['birth_date'], conditions['visit_date'], conditions['vet_name'],
                    conditions['diagnosis_phrase']]):
            messagebox.showwarning("Внимание", "Заполните хотя бы одно поле для удаления!")
            return

        self.result_conditions = conditions
        self.top.destroy()

    def get_conditions(self):
        return self.result_conditions