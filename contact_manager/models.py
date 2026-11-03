# models.py
# This file contains the Contact class with validation.

try:
    from contact_manager.utils import validate_email, validate_phone
except ImportError:
    from utils import validate_email, validate_phone


class Contact:
    """
    Contact class representing a single contact.
    Validates email and phone upon creation to prevent invalid instances.
    """

    def __init__(self, name, email, phone, address=""):
        if not name or not str(name).strip():
            raise ValueError("Contact name cannot be empty.")
        if not validate_phone(phone):
            raise ValueError("Phone number must be exactly 10 digits.")
        if not validate_email(email):
            raise ValueError("Invalid email format.")

        self.name = str(name).strip()
        self.email = str(email).strip()
        self.phone = str(phone).strip()
        self.address = str(address).strip() if address else ""

    # Display contact details
    def display_contact(self):
        print("Name   :", self.name)
        print("Email  :", self.email)
        print("Phone  :", self.phone)
        print("Address:", self.address)
        print("-" * 30)

    # Convert to dictionary for JSON persistence
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }
