import logging

"""
Simple Address Book Program
This script collects contact details from the user, logs them to a file, and displays them.
Using Object-Oriented Concepts to manage relationships between AddressBook and ContactPerson.
"""

# Configure logging
logging.basicConfig(filename='contacts.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ContactPerson:
    """
    Represents a contact person with personal details.
    """
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, email):
        """
        Initializes a ContactPerson object with provided details.
        """
        self.details = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "phone_number": phone_number,
            "email": email
        }
    
    def __str__(self):
        """
        Returns a formatted string representation of the contact details.
        """
        return str(self.details)

class AddressBook:
    """
    Manages a collection of contacts.
    """
    def __init__(self):
        """
        Initializes an empty address book.
        """
        self.contacts = []
    
    def add_contact(self, contact):
        """
        Adds a contact to the address book and logs the details.
        """
        self.contacts.append(contact.details)
        logging.info(f"Contact Saved - {contact.details}")
        print("\nContact Saved!")
        print("---------------------------")
        print(contact.details)
    
    def display_contacts(self):
        """
        Displays all contacts in the address book.
        """
        if not self.contacts:
            print("No contacts found.")
        else:
            print("\nContacts in Address Book:")
            print("---------------------------")
            for contact in self.contacts:
                print(contact)
                print("---------------------------")

def main():
    """
    Provides a menu to add and display contacts.
    """
    address_book = AddressBook()
    while True:
        print("\nAddress Book Menu:")
        print("1) Add Contact")
        print("2) Display Contacts")
        print("3) Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            try:
                print("Enter Contact Details:")
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                address = input("Address: ")
                city = input("City: ")
                state = input("State: ")
                zip_code = input("Zip Code: ")
                phone_number = input("Phone Number: ")
                email = input("Email: ")
                
                contact = ContactPerson(first_name, last_name, address, city, state, zip_code, phone_number, email)
                address_book.add_contact(contact)
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                print("An error occurred while saving contact details. Please try again.")
        
        elif choice == "2":
            address_book.display_contacts()
        
        elif choice == "3":
            print("Exiting Address Book.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
