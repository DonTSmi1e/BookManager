import sqlite3

class Database:
    def __init__(self, file_name: str):
        """An object with functions for interacting with the book database"""
        self.file_name = file_name

        self.execute("""
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                details TEXT NOT NULL
            )
        """, commit=True)

    def execute(self, query: str, parameters: tuple = (), commit: bool = False):
        """An auxiliary function that executes an SQL query to a database"""
        with sqlite3.connect(self.file_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query, parameters)
            if commit: connection.commit()

        return cursor

    def create_book(self, name: str, author: str, genre: str, details: str):
        """Creates a book in the database, returns nothing"""
        self.execute("""
            INSERT INTO Books (
                name,
                author,
                genre,
                details
            ) VALUES (?, ?, ?, ?)
        """, (name, author, genre, details), commit=True)

    def get_books(self):
        """Returns a LIST with LISTS containing book data"""
        books = self.execute("SELECT * FROM Books").fetchall()
        return books

    def get_book(self, book_id: int):
        """Returns a LIST containing book data"""
        book = self.execute(f"SELECT * FROM Books WHERE id={book_id}").fetchone()
        return book

    def delete_book(self, book_id: int):
        """DELETE book"""
        self.execute(f"DELETE FROM Books WHERE id={book_id}", commit=True)
