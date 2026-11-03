# main.py
# This is the main file that runs the program.

from contact_manager.services import ContactService


def main():
    service = ContactService()

    while True:
        print("\n--- Contact Management System ---")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter choice (1-6): ")

        # 1. Add Contact
        if choice == "1":
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            phone = input("Enter Phone (10 digits): ")
            address = input("Enter Address: ")
            service.add_contact(name, email, phone, address)

        # 2. View All Contacts
        elif choice == "2":
            service.display_all_contacts()

        # 3. Search Contact
        elif choice == "3":
            name = input("Enter Name to search: ")
            service.search_contact(name)

        # 4. Update Contact
        elif choice == "4":
            name = input("Enter Name to update: ")
            service.update_contact(name)

        # 5. Delete Contact
        elif choice == "5":
            name = input("Enter Name to delete: ")
            service.delete_contact(name)

        # 6. Exit
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice! Please choose 1 to 6.")


# Start the program
if __name__ == "__main__":
    main()
