import tkinter as tk
from tkinter import ttk


class start_dialog:
    def __init__(self, parent):
        self.selected_file = None
        self.top = tk.Toplevel(parent)
        self.top.title("Выбор базы данных")
        self.top.geometry("400x200")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()
        lbl = ttk.Label(self.top, text="Выберите файл для работы:", font=("Arial", 12))
        lbl.pack(pady=20)
        btn_frame = ttk.Frame(self.top)
        btn_frame.pack(pady=10)
        btn1 = ttk.Button(btn_frame, text="data1",
                          command=lambda: self.select("data1.xml"), width=30)
        btn1.pack(pady=5)
        btn2 = ttk.Button(btn_frame, text="data2",
                          command=lambda: self.select("data2.xml"), width=30)
        btn2.pack(pady=5)
        self.status_lbl = ttk.Label(self.top, text="", foreground="green")
        self.status_lbl.pack(pady=10)

    def select(self, filename):
        self.selected_file = filename
        self.status_lbl.config(text=f"Выбрано: {filename}")
        self.top.after(500, self.top.destroy)

    def get_file(self):
        return self.selected_file