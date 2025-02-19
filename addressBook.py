import logging
"""
Simple Address Book Program
This script collects contact details from the user, logs them to a file, and displays them using Object-Oriented Concepts.
"""

logging.basicConfig(
    filename='contacts.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ContactPerson:
    """
    Represents a contact person with personal details.
    """
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, email):
        """
        Initializes a ContactPerson object with provided details.
        
        Parameters:
            first_name (str): First name of the contact.
            last_name (str): Last name of the contact.
            address (str): Address of the contact.
            city (str): City of residence.
            state (str): State of residence.
            zip_code (int): Zip code.
            phone_number (int): Contact phone number.
            email (str): Email address of the contact.
        
        Returns:
            None
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
        
        Parameters:
            None
        
        Returns:
            str: Formatted string containing contact details.
        """
        return str(self.details)

class AddressBook:
    """
    Manages a collection of contacts.
    """
    def __init__(self):
        """
        Initializes an empty address book.
        
        Parameters:
            None
        
        Returns:
            None
        """
        self.contacts = []
    
    def add_contact(self, contact):
        """
        Adds a contact to the address book and logs the details.
        
        Parameters:
            contact (ContactPerson): Contact object to be added.
        
        Returns:
            None
        """
        self.contacts.append(contact.details)
        logging.info(f"Contact Saved - {contact.details}")
        print("\nContact Saved!")
        print("---------------------------")
        print(contact.details)
    
    def display_contacts(self):
        """
        Displays all contacts in the address book.
        
        Parameters:
            None
        
        Returns:
            None
        """
        if not self.contacts:
            print("No contacts found.")
        else:
            print("\nContacts in Address Book:")
            print("---------------------------")
            for contact in self.contacts:
                print(contact)
                print("---------------------------")
    
    def edit_contact(self, first_name, last_name, new_details):
        """
        Edits an existing contact using their first and last name.
        
        Parameters:
            first_name (str): First name of the contact to edit.
            last_name (str): Last name of the contact to edit.
            new_details (dict): Dictionary containing updated contact details.
        
        Returns:
            bool: True if contact was updated, False if not found.
        """
        for contact in self.contacts:
            if contact["first_name"] == first_name and contact["last_name"] == last_name:
                contact.update(new_details)
                logging.info(f"Contact Updated - {contact}")
                print("\nContact Updated!")
                print("---------------------------")
                print(contact)
                return True
        print("Contact not found.")
        return False
    
    def delete_contact(self, first_name, last_name):
        """
        Deletes a contact from the address book using their first and last name.
        
        Parameters:
            first_name (str): First name of the contact to delete.
            last_name (str): Last name of the contact to delete.
        
        Returns:
            bool: True if contact was deleted, False if not found.
        """
        for contact in self.contacts:
            if contact["first_name"] == first_name and contact["last_name"] == last_name:
                self.contacts.remove(contact)
                logging.info(f"Contact Deleted - {contact}")
                print("\nContact Deleted!")
                return True
        print("Contact not found.")
        return False

def main():
    """
    Provides a menu to add, edit, display, and delete contacts.
    """
    address_book = AddressBook()
    while True:
        print("\nAddress Book Menu:")
        print("1) Add Contact")
        print("2) Display Contacts")
        print("3) Edit Contact")
        print("4) Delete Contact")
        print("5) Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            try:
                print("Enter Contact Details:")
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                address = input("Address: ")
                city = input("City: ")
                state = input("State: ")
                zip_code = int(input("Zip Code: "))
                phone_number = int(input("Phone Number: "))
                email = input("Email: ")
                
                contact = ContactPerson(first_name, last_name, address, city, state, zip_code, phone_number, email)
                address_book.add_contact(contact)
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                print("An error occurred while saving contact details. Please try again.")
        
        elif choice == "2":
            address_book.display_contacts()
        
        elif choice == "3":
            print("Enter Contact Name to Edit:")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            print("Enter New Details:")
            new_address = input("New Address: ")
            new_city = input("New City: ")
            new_state = input("New State: ")
            new_zip_code = int(input("New Zip Code: "))
            new_phone_number = int(input("New Phone Number: "))
            new_email = input("New Email: ")
            
            new_details = {
                "address": new_address,
                "city": new_city,
                "state": new_state,
                "zip_code": new_zip_code,
                "phone_number": new_phone_number,
                "email": new_email
            }
            address_book.edit_contact(first_name, last_name, new_details)
        
        elif choice == "4":
            print("Enter Contact Name to Delete:")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            address_book.delete_contact(first_name, last_name)
        
        elif choice == "5":
            print("Exiting Address Book.")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()