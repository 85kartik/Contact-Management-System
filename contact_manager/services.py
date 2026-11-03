# services.py
# This file manages contacts and handles JSON file persistence.

import json
import os

try:
    from contact_manager.models import Contact
    from contact_manager.utils import validate_email, validate_phone, format_phone
except ImportError:
    from models import Contact
    from utils import validate_email, validate_phone, format_phone

# Resolve path to contacts.json in project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILENAME = os.path.join(ROOT_DIR, "contacts.json")


class ContactService:
    def __init__(self, filename=FILENAME):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def save_contacts(self):
        """Saves current contacts list to contacts.json."""
        data = []
        for c in self.contacts:
            data.append(c.to_dict())

        try:
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            print(f"Error saving contacts to file: {e}")

    def load_contacts(self):
        """Loads contacts safely from contacts.json handling file errors."""
        self.contacts = []
        try:
            with open(self.filename, "r") as f:
                content = f.read().strip()
                if not content:
                    return
                data = json.loads(content)
                if not isinstance(data, list):
                    return
                for item in data:
                    if isinstance(item, dict) and "name" in item:
                        try:
                            c = Contact(
                                item.get("name", ""),
                                item.get("email", ""),
                                item.get("phone", ""),
                                item.get("address", ""),
                            )
                            self.contacts.append(c)
                        except ValueError:
                            # Skip malformed/invalid contact entries safely
                            pass
        except FileNotFoundError:
            # File does not exist yet; start with an empty contact list
            self.contacts = []
        except json.JSONDecodeError:
            # File is corrupted or empty JSON; start with empty list
            self.contacts = []

    def add_contact(self, name, email, phone, address):
        """Validates input, checks duplicates, creates Contact and saves."""
        name = str(name).strip()
        email = str(email).strip()
        phone = str(phone).strip()
        address = str(address).strip()

        if not name:
            print("Error: Name cannot be empty!")
            return False

        # Prevent duplicate email addresses
        for c in self.contacts:
            if c.email.lower() == email.lower():
                print("Error: A contact with this email already exists!")
                return False

        if not validate_phone(phone):
            print("Error: Phone number must be exactly 10 digits!")
            return False

        if not validate_email(email):
            print("Error: Invalid email! Must contain valid format (e.g. user@example.com)")
            return False

        phone = format_phone(phone)

        try:
            new_contact = Contact(name, email, phone, address)
        except ValueError as e:
            print(f"Error: {e}")
            return False

        self.contacts.append(new_contact)
        self.save_contacts()
        print("Contact added and saved successfully!")
        return True

    def display_all_contacts(self):
        """Displays all contacts stored in the system."""
        if len(self.contacts) == 0:
            print("No contacts to display.")
            return

        print(f"\n--- All Contacts (Total: {len(self.contacts)}) ---")
        for contact in self.contacts:
            contact.display_contact()

    def search_contact(self, name):
        """Searches for contacts by name or phone."""
        query = str(name).strip().lower()
        if not query:
            print("Error: Search query cannot be empty.")
            return

        found = False
        for contact in self.contacts:
            if query in contact.name.lower() or query in contact.phone:
                contact.display_contact()
                found = True

        if not found:
            print("No contact found.")

    def update_contact(self, name):
        """
        Updates an existing contact's phone, email, or address.
        Validates new inputs and prevents duplicate email addresses before saving.
        """
        name = str(name).strip()
        if not name:
            print("Error: Name cannot be empty.")
            return False

        target = None
        for contact in self.contacts:
            if contact.name.lower() == name.lower() or name.lower() in contact.name.lower():
                target = contact
                break

        if not target:
            print("Contact not found.")
            return False

        print(f"\nUpdating contact: {target.name}")
        new_phone = input("Enter new phone (or press Enter to skip): ").strip()
        new_email = input("Enter new email (or press Enter to skip): ").strip()
        new_address = input("Enter new address (or press Enter to skip): ").strip()

        # 1. Validate new phone if provided
        if new_phone:
            if not validate_phone(new_phone):
                print("Error: Phone number must be exactly 10 digits! Update canceled.")
                return False

        # 2. Validate new email if provided
        if new_email:
            if not validate_email(new_email):
                print("Error: Invalid email format! Update canceled.")
                return False

            # 3. Prevent duplicate email across other contacts
            for other in self.contacts:
                if other != target and other.email.lower() == new_email.lower():
                    print("Error: Another contact already has this email address! Update canceled.")
                    return False

        # 4. Apply updates only after all validations pass
        if new_phone:
            target.phone = format_phone(new_phone)
        if new_email:
            target.email = new_email
        if new_address:
            target.address = new_address

        self.save_contacts()
        print("Contact updated and saved successfully!")
        return True

    def delete_contact(self, name):
        """Deletes a contact by matching name."""
        query = str(name).strip().lower()
        if not query:
            print("Error: Name cannot be empty.")
            return False

        target = None
        for contact in self.contacts:
            if contact.name.lower() == query or query in contact.name.lower():
                target = contact
                break

        if target:
            self.contacts.remove(target)
            self.save_contacts()
            print("Contact deleted and file updated successfully!")
            return True

        print("Contact not found.")
        return False
