import json
from datetime import datetime

#####################
## Define Book class
##### A simple class to store the attributes of a book
##### static method to create a Book object from a dictionary
class Book:
    def __init__(self, book_id, title, author, genre, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "available": self.available
        }

    @staticmethod
    def from_dict(data):
        return Book(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            available=data["available"]
        )

#####################
## Define Member  class
##### A simple class to store the attributes of a Member
##### static method to create a Member object from a dictionary
class Member:
    def __init__(self, member_id, name, age, contact, borrowed_books=None):
        self.member_id = member_id
        self.name = name
        self.age = age
        self.contact = contact
        self.borrowed_books = borrowed_books or []

    def add_borrowed_book(self, bookid, borrowed_on=datetime.now().strftime("%Y-%m-%d")):
        borrowed_book = {
            "book_id": book_id,
            "borrowed_on": borrowed_on
        }
        self.borrowed_books.append(borrowed_book)

    def remove_borrowed_book(self, bookid):
        # Check if member actually borrowed this book
        active_record = None
        for entry in self.borrowed_books:
            if entry["book_id"] == book_id:
                active_record = entry
                break

        if not active_record:
            raise ValueError("This member did not borrow the specified book.")

        # Remove from member's active borrow list
        self.borrowed_books.remove(active_record)

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "age": self.age,
            "contact": self.contact,
            "borrowed_books": self.borrowed_books  # simple list of dicts
        }

    @staticmethod
    def from_dict(data):
        return Member(
            member_id=data["member_id"],
            name=data["name"],
            age=data["age"],
            contact=data["contact"],
            borrowed_books=data.get("borrowed_books", [])
        )

#####################
## Define BorrowRecord class
##### A simple class to store the attributes of a BorrowRecord
##### static method to create a BorrowRecord object from a dictionary
class BorrowRecord:
    def __init__(self, member_id, book_id, borrowed_on=datetime.now().strftime("%Y-%m-%d"), returned_on=None):
        self.member_id = member_id
        self.book_id = book_id
        self.borrowed_on = borrowed_on
        self.returned_on = returned_on

    def closeRecord(self, returned_on):
        self.returned_on = returned_on

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "book_id": self.book_id,
            "borrowed_on": self.borrowed_on,
            "returned_on": self.returned_on
        }

    @staticmethod
    def from_dict(data):
        return BorrowRecord(
            member_id=data["member_id"],
            book_id=data["book_id"],
            borrowed_on=data["borrowed_on"],
            returned_on=data["returned_on"]
        )


#####################
## Define Library class
##### This is the master class that ties all the above classes
#####
class Library:
    def __init__(self, books=None, members=None, borrow_history=None):
        self.books = books or []
        self.members = members or []
        self.borrow_history = borrow_history or []

    # --------------------------------------------
    # JSON Persistence
    # --------------------------------------------
    def save_to_json(self, filename="library_data.json"):
        data = {
            "books": [b.to_dict() for b in self.books],
            "members": [m.to_dict() for m in self.members],
            "borrow_history": [r.to_dict() for r in self.borrow_history]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_from_json(filename="library_data.json"):
        from classes import Book, Member, BorrowRecord  # adjust import if needed
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return Library()

        books = [Book.from_dict(b) for b in data.get("books", [])]
        members = [Member.from_dict(m) for m in data.get("members", [])]
        history = [BorrowRecord.from_dict(r) for r in data.get("borrow_history", [])]

        return Library(books, members, history)

    # --------------------------------------------
    # Helper Lookups
    # --------------------------------------------
    def find_book_by_id(self, book_id):
        return next((b for b in self.books if b.book_id == book_id), None)

    def find_member_by_id(self, member_id):
        return next((m for m in self.members if m.member_id == member_id), None)

    # --------------------------------------------
    # Book Operations
    # --------------------------------------------
    def add_book(self, book):
        if self.find_book_by_id(book.book_id):
            raise ValueError("Book ID already exists.")
        self.books.append(book)

    def search_books(self, title=None, author=None):
        results = self.books
        if title:
            results = [b for b in results if title.lower() in b.title.lower()]
        if author:
            results = [b for b in results if author.lower() in b.author.lower()]
        return results

    def get_available_books_by_genre(self, genre):
        return [
            b for b in self.books
            if b.genre.lower() == genre.lower() and b.available
        ]

    # --------------------------------------------
    # Member Operations
    # --------------------------------------------
    def add_member(self, member):
        if self.find_member_by_id(member.member_id):
            raise ValueError("Member ID already exists.")
        self.members.append(member)

    # --------------------------------------------
    # Borrow Operations
    # --------------------------------------------
    def borrow_book(self, member_id, book_id):
        member = self.find_member_by_id(member_id)
        if not member:
            raise ValueError("Member does not exist.")

        book = self.find_book_by_id(book_id)
        if not book:
            raise ValueError("Book does not exist.")

        if not book.available:
            raise ValueError("Book is already borrowed.")

        # Mark book unavailable
        book.available = False

        # Add to member's active borrow list
        member.add_borrowed_book(book_id=book_id)

        # Add to borrow history log
        record = BorrowRecord(member_id=member_id, book_id=book_id)
        self.borrow_history.append(record)

    # --------------------------------------------
    # Return Operation
    # --------------------------------------------
    def return_book(self, member_id, book_id):
        member = self.find_member_by_id(member_id)
        if not member:
            raise ValueError("Member does not exist.")

        book = self.find_book_by_id(book_id)
        if not book:
            raise ValueError("Book does not exist.")

        # Mark book available again
        book.available = True

        # Update borrow history record where returned_on is None
        for record in reversed(self.borrow_history):
            if record.book_id == book_id and record.member_id == member_id and record.returned_on is None:
                record.returned_on = datetime.now().strftime("%Y-%m-%d")
                break

    # --------------------------------------------
    # Reports
    # --------------------------------------------
    def list_members_with_borrows(self):
        return [m for m in self.members if len(m.borrowed_books) > 0]

    def most_popular_genre(self):
        if not self.borrow_history:
            return None

        # Count only based on borrow events, not availability
        genre_counts = {}
        for record in self.borrow_history:
            book = self.find_book_by_id(record.book_id)
            if book:
                genre_counts[book.genre] = genre_counts.get(book.genre, 0) + 1

        # Find genre with max count
        return max(genre_counts, key=genre_counts.get)
