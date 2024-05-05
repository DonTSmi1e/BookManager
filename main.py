import customtkinter
from CTkTable import *

from config import *
from db import Database

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

db = Database(DATABASE)

db.get_books()

class BookDetailsWindow(customtkinter.CTkToplevel):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, **kwargs)
        self.book_list_frame = master
        self.data = data

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.title(f"\"{self.data[1]}\"")
        self.geometry("500x300")
        self.resizable(False, False)

        self.info_label = customtkinter.CTkLabel(self, text=f"{self.data[2]}, {self.data[3]}", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.info_label.grid(row=0, column=0)

        self.details_textbox = customtkinter.CTkTextbox(self, width=400)
        self.details_textbox.grid(row=1, column=0, columnspan=2)
        self.details_textbox.insert("0.0", self.data[4])
        self.details_textbox.configure(state="disabled")

        self.delete_button = customtkinter.CTkButton(self, text="Удалить", command=self.delete_button_callback)
        self.delete_button.grid(row=2, column=0)

    def delete_button_callback(self):
        db.delete_book(self.data[0])
        self.book_list_frame.update_table()
        self.destroy()

class AddBookWindow(customtkinter.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = master

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.title("Добавить книгу")
        self.geometry("400x400")
        self.resizable(False, False)

        customtkinter.CTkLabel(self, text="Название: ").grid(row=0, column=0)
        self.name_entry = customtkinter.CTkEntry(self)
        self.name_entry.grid(row=0, column=1)

        customtkinter.CTkLabel(self, text="Автор: ").grid(row=1, column=0)
        self.author_entry = customtkinter.CTkEntry(self)
        self.author_entry.grid(row=1, column=1)

        customtkinter.CTkLabel(self, text="Жанр: ").grid(row=2, column=0)
        self.genre_combo = customtkinter.CTkComboBox(self, values=db.get_genres())
        self.genre_combo.grid(row=2, column=1)
        self.genre_combo.set("")

        customtkinter.CTkLabel(self, text="Описание: ").grid(row=3, column=0)
        self.details_textbox = customtkinter.CTkTextbox(self)
        self.details_textbox.grid(row=3, column=1)

        self.add_button = customtkinter.CTkButton(self, text="Добавить", command=self.add_button_callback)
        self.add_button.grid(row=4, column=0, columnspan=2)

        self.info_label = customtkinter.CTkLabel(self, text="")
        self.info_label.grid(row=5, column=0, columnspan=2)

    def add_button_callback(self):
        data = (
            self.name_entry.get(),
            self.author_entry.get(),
            self.genre_combo.get(),
            self.details_textbox.get("0.0", "end")
        )

        if   len(data[0]) == 0: self.info_label.configure(text="Введите название книги")
        elif len(data[1]) == 0: self.info_label.configure(text="Введите автора книги")
        elif len(data[2]) == 0: self.info_label.configure(text="Введите жанр книги")
        elif len(data[3]) == 0: self.info_label.configure(text="Введите описание книги")
        else:
            db.create_book(data[0], data[1], data[2], data[3])
            self.app.book_list_frame.update_table()
            self.destroy()

class BookListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = master

        self.table = CTkTable(self, command=self.book_click_handler)
        self.table.pack(expand=True)

        self.update_table()

    def update_table(self, keyword: str = ""):
        keyword = keyword.lower()
        books = [[ "ID", "Название", "Автор", "Жанр" ]]

        for data in db.get_books():
            if keyword in data[1].lower() or keyword in data[2].lower() or keyword in data[3].lower():
                books.append([ data[0], data[1], data[2], data[3] ])

        self.table.columns = 4
        self.table.rows = len(books)
        self.table.update_values(books)

    def book_click_handler(self, event):
        if event["row"] > 0:
            self.app.open_toplevel_window(BookDetailsWindow(self, data=db.get_book(self.table.get_row(event["row"])[0])))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.label = customtkinter.CTkLabel(self.sidebar, text=WINDOW_TITLE, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.add_book_button = customtkinter.CTkButton(self.sidebar, text="Добавить", command=self.add_book_button_callback)
        self.add_book_button.grid(row=1, column=0, padx=20, pady=20)

        self.search_entry = customtkinter.CTkEntry(self.sidebar, placeholder_text="Название/автор")
        self.search_entry.grid(row=2, column=0, padx=20, pady=10)

        self.search_button = customtkinter.CTkButton(self.sidebar, text="Поиск", command=self.search_button_callback)
        self.search_button.grid(row=3, column=0, padx=20, pady=2)

        self.search_label = customtkinter.CTkLabel(self.sidebar, text="")
        self.search_label.grid(row=4, column=0, padx=20, pady=2)

        self.book_list_frame = BookListFrame(self, width=1280, height=1280, corner_radius=0)
        self.book_list_frame.grid(row=0, column=1)

        self.toplevel_window = None

    def add_book_button_callback(self):
        self.open_toplevel_window(AddBookWindow(self))

    def search_button_callback(self):
        keyword = self.search_entry.get()
        self.book_list_frame.update_table(keyword)
        self.search_label.configure(text=f"Поиск по {keyword}" if keyword else "")

    def open_toplevel_window(self, window):
        if self.toplevel_window:
            self.toplevel_window.destroy()

        self.toplevel_window = window
        self.toplevel_window.after(100, self.toplevel_window.lift)

app = App()
app.mainloop()
