# services.py
# This file manages contacts and saves them to contacts.json.

import json
from models import Contact
from utils import validate_email, validate_phone, format_phone


class ContactService:
    def __init__(self):
        self.contacts = []
        self.load_contacts()  # Load saved contacts when program starts

    # Simple function to save contacts list into contacts.json
    def save_contacts(self):
        data = []
        for c in self.contacts:
            data.append(
                {
                    "name": c.name,
                    "email": c.email,
                    "phone": c.phone,
                    "address": c.address,
                }
            )

        with open("contacts.json", "w") as f:
            json.dump(data, f, indent=4)

    # Simple function to load contacts from contacts.json
    def load_contacts(self):
        try:
            with open("contacts.json", "r") as f:
                data = json.load(f)
                for item in data:
                    # Only load items that have a contact name (skips pure comment objects)
                    if "name" in item:
                        c = Contact(
                            item["name"],
                            item["email"],
                            item["phone"],
                            item["address"],
                        )
                        self.contacts.append(c)
        except:
            self.contacts = []

    # 1. Add Contact
    def add_contact(self, name, email, phone, address):
        if not validate_phone(phone):
            print("Error: Phone number must be 10 digits!")
            return

        if not validate_email(email):
            print("Error: Invalid email! Must contain '@' and '.'")
            return

        phone = format_phone(phone)
        new_contact = Contact(name, email, phone, address)
        self.contacts.append(new_contact)
        self.save_contacts()
        print("Contact added and saved successfully!")

    # 2. View All Contacts
    def display_all_contacts(self):
        if len(self.contacts) == 0:
            print("No contacts to display.")
            return

        print("\n--- All Contacts ---")
        for contact in self.contacts:
            contact.display_contact()

    # 3. Search Contact
    def search_contact(self, name):
        found = False
        for contact in self.contacts:
            if name.lower() in contact.name.lower():
                contact.display_contact()
                found = True

        if not found:
            print("No contact found.")

    # 4. Update Contact
    def update_contact(self, name):
        for contact in self.contacts:
            if name.lower() in contact.name.lower():
                print(f"\nUpdating contact: {contact.name}")
                new_phone = input("Enter new phone (or press Enter to skip): ")
                new_email = input("Enter new email (or press Enter to skip): ")
                new_address = input(
                    "Enter new address (or press Enter to skip): "
                )

                if new_phone != "":
                    contact.phone = format_phone(new_phone)
                if new_email != "":
                    contact.email = new_email
                if new_address != "":
                    contact.address = new_address

                self.save_contacts()
                print("Contact updated and saved successfully!")
                return

        print("Contact not found.")

    # 5. Delete Contact
    def delete_contact(self, name):
        for contact in self.contacts:
            if name.lower() in contact.name.lower():
                self.contacts.remove(contact)
                self.save_contacts()
                print("Contact deleted and file updated successfully!")
                return

        print("Contact not found.")
