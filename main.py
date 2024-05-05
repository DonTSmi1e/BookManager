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

        self.title(f"\"{self.data[1]}\"")
        self.geometry("800x300")

        self.name_label = customtkinter.CTkLabel(self, text=self.data[1], font=customtkinter.CTkFont(size=20, weight="bold"))
        self.name_label.pack(padx=20)

        self.author_label = customtkinter.CTkLabel(self, text=self.data[2], font=customtkinter.CTkFont(size=15, weight="bold"))
        self.author_label.pack(padx=20)

        self.genre_label = customtkinter.CTkLabel(self, text=self.data[3], font=customtkinter.CTkFont(size=15, weight="bold"))
        self.genre_label.pack(padx=20)

        self.details_header_label = customtkinter.CTkLabel(self, text="Описание", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.details_header_label.pack(padx=20, pady=5)

        self.details_label = customtkinter.CTkLabel(self, text=self.data[4])
        self.details_label.pack(padx=20)

        self.delete_button = customtkinter.CTkButton(self, width=350, text="Удалить", command=self.delete_button_callback)
        self.delete_button.pack(padx=20, pady=5)

    def delete_button_callback(self):
        db.delete_book(self.data[0])
        self.book_list_frame.update_table()
        self.destroy()

class AddBookWindow(customtkinter.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = master

        self.title("Добавить книгу")
        self.geometry("400x250")

        self.name_entry = customtkinter.CTkEntry(self, width=350, placeholder_text="Название книги")
        self.name_entry.pack(padx=20, pady=5)

        self.author_entry = customtkinter.CTkEntry(self, width=350, placeholder_text="Автор книги")
        self.author_entry.pack(padx=20, pady=5)

        self.genre_entry = customtkinter.CTkEntry(self, width=350, placeholder_text="Жанр")
        self.genre_entry.pack(padx=20, pady=5)

        self.details_entry = customtkinter.CTkEntry(self, width=350, placeholder_text="Описание")
        self.details_entry.pack(padx=20, pady=5)

        self.add_button = customtkinter.CTkButton(self, width=350, text="Добавить", command=self.add_button_callback)
        self.add_button.pack(padx=20, pady=5)

        self.info_label = customtkinter.CTkLabel(self, text="")
        self.info_label.pack(padx=20, pady=5)

    def add_button_callback(self):
        data = (
            self.name_entry.get(),
            self.author_entry.get(),
            self.genre_entry.get(),
            self.details_entry.get()
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
        books = [[ "ID", "Название", "Автор", "Жанр" ]]

        for data in db.get_books():
            if keyword in data[1] or keyword in data[2]:
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
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

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
