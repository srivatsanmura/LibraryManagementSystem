# validation.py

import re

class ValidationError(Exception):
    """Custom exception for all validation-related issues."""
    pass

def validate_book_id(book_id):
    # Example rule: BOOK IDs like B101, B202, BK001 etc.
    pattern = r'^[A-Za-z]{1,3}\d{2,5}$'
    if not re.match(pattern, book_id):
        raise ValidationError("Invalid Book ID. Use letters followed by digits (e.g., B101, BK202).")

def validate_member_id(member_id):
    # Example rule: Member IDs like M001, MEM32 etc.
    pattern = r'^[A-Za-z]{1,4}\d{2,5}$'
    if not re.match(pattern, member_id):
        raise ValidationError("Invalid Member ID format. Use letters followed by digits (e.g., M001).")

def validate_name(name):
    if not name.strip():
        raise ValidationError("Name cannot be empty.")
    if not re.match(r"^[A-Za-z\s.]+$", name):
        raise ValidationError("Name should contain only alphabets and spaces.")

def validate_age(age):
    if not (1 <= age <= 120):
        raise ValidationError("Age must be between 1 and 120.")

def validate_contact(contact):
    # Very simple Indian mobile number validator
    pattern = r'^[6-9]\d{9}$'
    if not re.match(pattern, contact):
        raise ValidationError("Invalid contact number. Use 10-digit Indian mobile numbers starting with 6-9.")

def validate_genre(genre):
    if not genre.strip():
        raise ValidationError("Genre cannot be empty.")

def validate_author(author):
    if not author.strip():
        raise ValidationError("Author cannot be empty.")

def validate_title(title):
    if not title.strip():
        raise ValidationError("Title cannot be empty.")

## Map of to-be-validated elements and their validators with messages
## format: "element" : (prompt, validator)
elementValidatorMap = {
    "book_id": ("Book ID :", validate_book_id),
    "member_id": ("Member ID :", validate_member_id),
    "name": ("Name :", validate_name),
    "age": ("Age :", validate_age),
    "contact": ("Contact :", validate_contact),
    "genre": ("Genre :", validate_genre),
    "author": ("Author :", validate_author),
    "title": ("Title :", validate_title)
}

# Helper function that simplifies user interaction and validation
def get_valid_input(element, isInteger=False):
    if elementValidatorMap.get(element):
        prompt, validator = elementValidatorMap.get(element)
        while True:
            value = input(prompt).strip() if not isInteger else int(input(prompt).strip())
            try:
                if validator:
                    #validator(value, *args) if args else validator(value) ## enable when arg is needed for validator
                    validator(value)
                return value
            except ValidationError as e:
                print(f"Invalid input: {e}")
    else:
        raise ValueError(f"Missing configuration for {element=}")