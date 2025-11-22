# main.py

from libraryClasses import Book, Member, BorrowRecord, Library
from validation import get_valid_input

def pause():
    input("\nPress Enter to continue...")

def menu():
    print("\n===== CITY LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add Book")
    print("2. Add Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. Show Available Books by Genre")
    print("7. List Members Who Borrowed")
    print("8. Most Popular Genre")
    print("9. Save & Exit")
    print("==========================================")
    return input("Enter your choice: ").strip()

def main():
    datafile='/content/library_data.json' # For google colab environment
    library = Library.load_from_json(datafile)

    while True:
        choice = menu()

        # ----------------------------------------
        # 1. Add Book
        # ----------------------------------------
        if choice == "1":
            print("\n--- Add New Book ---")


            try:
                book_id = get_valid_input("book_id")
                title = get_valid_input("title")
                author = get_valid_input("author")
                genre = get_valid_input("genre")

                library.add_book(Book(book_id, title, author, genre))
                library.save_to_json()
                print("Book added successfully.")
            except ValueError as e:
                print(f"Error: {e}")

            pause()

        # ----------------------------------------
        # 2. Add Member
        # ----------------------------------------
        elif choice == "2":
            print("\n--- Add New Member ---")
            try:
                member_id = get_valid_input("member_id")
                name = get_valid_input("name")
                age = get_valid_input("age", isInteger=True)
                contact = get_valid_input("contact")

                library.add_member(Member(member_id, name, age, contact))
                library.save_to_json()
                print("Member added successfully.")
            except ValueError as e:
                print(f"Error: {e}")

            pause()

        # ----------------------------------------
        # 3. Borrow Book
        # ----------------------------------------
        elif choice == "3":
            print("\n--- Borrow Book ---")


            try:
                member_id = get_valid_input("member_id")
                book_id = get_valid_input("book_id")

                library.borrow_book(member_id, book_id)
                library.save_to_json()
                print("Book issued successfully.")
            except ValueError as e:
                print(f"Error: {e}")

            pause()

        # ----------------------------------------
        # 4. Return Book
        # ----------------------------------------
        elif choice == "4":
            print("\n--- Return Book ---")

            try:
                member_id = get_valid_input("member_id")
                book_id = get_valid_input("book_id")

                library.return_book(member_id, book_id)
                library.save_to_json()
                print("Book returned successfully.")
            except ValueError as e:
                print(f"Error: {e}")

            pause()

        # ----------------------------------------
        # 5. Search Books
        # ----------------------------------------
        elif choice == "5":
            print("\n--- Search Books ---")
            title = input("Search by title (or leave blank): ").strip()
            author = input("Search by author (or leave blank): ").strip()

            results = library.search_books(
                title if title else None,
                author if author else None
            )

            if results:
                print("\n--- Search Results ---")
                for book in results:
                    status = "Available" if book.available else "Issued"
                    print(f"{book.book_id} | {book.title} | {book.author} | {status}")
            else:
                print("No books found.")

            pause()

        # ----------------------------------------
        # 6. Available Books by Genre
        # ----------------------------------------
        elif choice == "6":
            print("\n--- Available Books by Genre ---")
            genre = input("Genre: ").strip()

            results = library.get_available_books_by_genre(genre)

            if results:
                print(f"\nAvailable books in '{genre}':")
                for book in results:
                    print(f"{book.book_id} | {book.title} | {book.author}")
            else:
                print("No available books in this genre.")

            pause()

        # ----------------------------------------
        # 7. Members who borrowed books
        # ----------------------------------------
        elif choice == "7":
            print("\n--- Members With Borrowed Books ---")
            members = library.list_members_with_borrows()

            if members:
                for m in members:
                    print(f"{m.member_id} | {m.name} | Borrowed Count: {len(m.borrowed_books)}")
            else:
                print("Currently, no members have borrowed books.")

            pause()

        # ----------------------------------------
        # 8. Most Popular Genre
        # ----------------------------------------
        elif choice == "8":
            genre = library.most_popular_genre()
            if genre:
                print(f"\nMost popular genre: {genre}")
            else:
                print("No borrow history available.")

            pause()

        # ----------------------------------------
        # 9. Save & Exit
        # ----------------------------------------
        elif choice == "9":
            print("Saving data...")
            library.save_to_json()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
            pause()


if __name__ == "__main__":
    main()
