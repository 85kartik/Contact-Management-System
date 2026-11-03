# models.py
# This file contains the Contact class.


class Contact:
    # Constructor to store contact details
    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    # Display contact details
    def display_contact(self):
        print("Name   :", self.name)
        print("Email  :", self.email)
        print("Phone  :", self.phone)
        print("Address:", self.address)
        print("-" * 30)
