import json

class Book:
    def __init__(self, book_id, title, author, year, status="в наличии"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __repr__(self):
        return f"{self.book_id}: {self.title} by {self.author} ({self.year}) - {self.status}"

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                books = json.load(file)
                return [Book(**book) for book in books]
        except FileNotFoundError:
            return []

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {book_id}.")

    def remove_book(self, book_id):
        book = next((book for book in self.books if book.book_id == book_id), None)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, **kwargs):
        results = self.books
        for key, value in kwargs.items():
            if key in ["title", "author", "year"]:
                results = [book for book in results if str(getattr(book, key)) == str(value)]
        return results

    def display_books(self):
        for book in self.books:
            print(book)

    def update_status(self, book_id, status):
        book = next((book for book in self.books if book.book_id == book_id), None)
        if book:
            book.status = status
            self.save_books()
            print(f"Статус книги с ID {book_id} обновлен на '{status}'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

def main():
    library = Library()

    while True:
        print("\n1. Добавить книгу")
        print("\n2. Удалить книгу")
        print("\n3. Поиск книги")
        print("\n4. Отображение всех книг")
        print("\n5. Изменение статуса книги")
        print("\n6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)
        elif choice == "3":
            search_by = input("Искать по (title, author, year): ")
            search_value = input(f"Введите значение для поиска по {search_by}: ")
            results = library.search_books(**{search_by: search_value})
            for book in results:
                print(book)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            status = input("Введите новый статус (в наличии, выдана): ")
            library.update_status(book_id, status)
        elif choice == "6":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
