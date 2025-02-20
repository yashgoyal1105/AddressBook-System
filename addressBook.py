import logging
from collections import defaultdict

logging.basicConfig(
    filename='contacts.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
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

        Returns:
            str: Formatted string containing contact details.
        """
        return str(self.details)

class AddressBook:
    """
    Manages a collection of contacts.
    """
    def __init__(self, name):
        """
        Initializes an empty address book.

        Parameters:
            name (str): The name of the address book.
        """
        self.name = name
        self.contacts = []

    def add_contact(self, contact):
        """
        Adds a contact to the address book and logs the details.

        Parameters:
            contact (ContactPerson): Contact object to be added.
        """
        # Check for duplicate entry
        if any(existing_contact["first_name"] == contact.details["first_name"] and
               existing_contact["last_name"] == contact.details["last_name"]
               for existing_contact in self.contacts):
            print("Duplicate entry found. Contact not added.")
            logging.warning(f"Duplicate entry attempt in {self.name} - {contact.details}")
        else:
            self.contacts.append(contact.details)
            logging.info(f"Contact Saved in {self.name} - {contact.details}")
            print("\nContact Saved!")
            print("---------------------------")
            print(contact.details)

    def display_contacts(self):
        """
        Displays all contacts in the address book.
        """
        if not self.contacts:
            print(f"No contacts found in {self.name}.")
        else:
            print(f"\nContacts in {self.name}:")
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
                logging.info(f"Contact Updated in {self.name} - {contact}")
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
                logging.info(f"Contact Deleted in {self.name} - {contact}")
                print("\nContact Deleted!")
                return True
        print("Contact not found.")
        return False

    def search_by_city_or_state(self, city=None, state=None):
        """
        Searches for contacts by city or state.

        Parameters:
            city (str): City to search for.
            state (str): State to search for.

        Returns:
            list: List of contacts matching the search criteria.
        """
        results = []
        for contact in self.contacts:
            if (city and contact["city"].lower() == city.lower()) or (state and contact["state"].lower() == state.lower()):
                results.append(contact)
        return results

    def count_contacts_by_city(self):
        """
        Counts the number of contacts by city.

        Returns:
            dict: Dictionary with city names as keys and contact counts as values.
        """
        city_count = defaultdict(int)
        for contact in self.contacts:
            city_count[contact["city"]] += 1
        return dict(city_count)

def main():
    """
    Main function to manage multiple address books.
    """
    address_books = {}

    while True:
        print("\nMain Menu:")
        print("1) Create or Select Address Book")
        print("2) Display Address Books")
        print("3) Search Contacts by City or State")
        print("4) Count Contacts by City")
        print("5) Exit")
        main_choice = input("Enter your choice: ")

        if main_choice == "1":
            book_name = input("Enter Address Book Name: ")
            if book_name not in address_books:
                address_books[book_name] = AddressBook(book_name)
                print(f"Address Book '{book_name}' created!")

            address_book = address_books[book_name]
            while True:
                print(f"\n{book_name} Menu:")
                print("1) Add Contact")
                print("2) Display Contacts")
                print("3) Edit Contact")
                print("4) Delete Contact")
                print("5) Go Back")
                choice = input("Enter your choice: ")

                if choice == "1":
                    number_of_times = int(input("How many contacts do you want to add: "))
                    for _ in range(number_of_times):
                        try:
                            print("\nEnter Contact Details:")
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
                    break
                else:
                    print("Invalid choice, please try again.")

        elif main_choice == "2":
            if not address_books:
                print("No Address Books available.")
            else:
                print("\nAvailable Address Books:")
                for name in address_books:
                    print(f"- {name}")

        elif main_choice == "3":
            city = input("Enter City to search (or leave blank): ")
            state = input("Enter State to search (or leave blank): ")
            results = []
            for address_book in address_books.values():
                results.extend(address_book.search_by_city_or_state(city, state))

            if results:
                print("\nSearch Results:")
                print("---------------------------")
                for result in results:
                    print(result)
                    print("---------------------------")
            else:
                print("No contacts found in the specified city or state.")

        elif main_choice == "4":
            city_count = defaultdict(int)
            for address_book in address_books.values():
                counts = address_book.count_contacts_by_city()
                for city, count in counts.items():
                    city_count[city] += count

            if city_count:
                print("\nContact Count by City:")
                print("---------------------------")
                for city, count in city_count.items():
                    print(f"{city}: {count}")
                print("---------------------------")
            else:
                print("No contacts found in any city.")

        elif main_choice == "5":
            print("Exiting Program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
