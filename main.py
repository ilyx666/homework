import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from tkinter import ttk

# Настройка окна
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Вход/Регистрация")
        self.geometry("400x250")
        self.create_db()
        self.create_widgets()

    def create_db(self):
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Имя пользователя")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Пароль", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Войти", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = ctk.CTkButton(self, text="Зарегистрироваться", command=self.register)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = self.cursor.fetchone()
        if result:
            self.destroy()
            app = LibraryApp()
            app.mainloop()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Успех", "Пользователь зарегистрирован")
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует")

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Библиотека")
        self.geometry("800x500")
        self.create_widgets()
        self.create_db()
        self.load_data()

    def create_widgets(self):
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=10)

        self.title_entry = ctk.CTkEntry(entry_frame, placeholder_text="Название книги", width=150)
        self.title_entry.grid(row=0, column=0, padx=5)

        self.author_entry = ctk.CTkEntry(entry_frame, placeholder_text="Автор", width=150)
        self.author_entry.grid(row=0, column=1, padx=5)

        self.year_entry = ctk.CTkEntry(entry_frame, placeholder_text="Год", width=100)
        self.year_entry.grid(row=0, column=2, padx=5)

        self.add_button = ctk.CTkButton(entry_frame, text="Добавить", command=self.add_book)
        self.add_button.grid(row=0, column=3, padx=5)

        self.update_button = ctk.CTkButton(entry_frame, text="Обновить", command=self.update_book)
        self.update_button.grid(row=0, column=4, padx=5)

        self.delete_button = ctk.CTkButton(entry_frame, text="Удалить", command=self.delete_book)
        self.delete_button.grid(row=0, column=5, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Название", "Автор", "Год"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Год", text="Год")
        self.tree.column("ID", width=30)
        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.fill_form_from_selection)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

    def create_db(self):
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER
            )
        """)
        self.conn.commit()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()

        if not title or not author or not year.isdigit():
            messagebox.showerror("Ошибка", "Проверьте правильность ввода данных")
            return

        self.cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, int(year)))
        self.conn.commit()
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT id, title, author, year FROM books")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def fill_form_from_selection(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        self.selected_id = values[0]
        self.title_entry.delete(0, ctk.END)
        self.title_entry.insert(0, values[1])
        self.author_entry.delete(0, ctk.END)
        self.author_entry.insert(0, values[2])
        self.year_entry.delete(0, ctk.END)
        self.year_entry.insert(0, values[3])

    def update_book(self):
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Выбор записи", "Сначала выберите запись для обновления")
            return

        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()

        if not title or not author or not year.isdigit():
            messagebox.showerror("Ошибка", "Проверьте правильность ввода данных")
            return

        self.cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?",
                            (title, author, int(year), self.selected_id))
        self.conn.commit()
        self.load_data()

    def delete_book(self):
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("Выбор записи", "Сначала выберите запись для удаления")
            return

        confirm = messagebox.askyesno("Удаление", "Вы уверены, что хотите удалить запись?")
        if confirm:
            self.cursor.execute("DELETE FROM books WHERE id = ?", (self.selected_id,))
            self.conn.commit()
            self.load_data()
            self.selected_id = None

if __name__ == '__main__':
    login = LoginWindow()
    login.mainloop()
