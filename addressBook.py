import logging
import csv

logging.basicConfig(
    filename='contacts.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

CONTACTS_FILE = "address_books.csv"

class ContactPerson:
    """
    Represents a contact person with personal details.
    """

    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, email):
        """
        Initializes a ContactPerson object with provided details.

        Args:
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
        Initializes an empty address book and loads contacts from a CSV file.

        Args:
            name (str): The name of the address book.
        """
        self.name = name
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        """
        Loads contacts for this address book from the CSV file.
        """
        try:
            self.contacts = FileManager.load_address_book(self.name)
        except Exception as e:
            logging.error(f"Error loading contacts: {str(e)}")

    def save_contacts(self):
        """
        Saves the current address book's contacts to the CSV file.
        """
        try:
            FileManager.save_address_book(self.name, self.contacts)
        except Exception as e:
            logging.error(f"Error saving contacts: {str(e)}")

    def add_contact(self, contact):
        """
        Adds a contact to the address book and logs the details.

        Args:
            contact (ContactPerson): Contact object to be added.
        """
        if not any(existing_contact["first_name"] == contact.details["first_name"] and
                    existing_contact["last_name"] == contact.details["last_name"]
                    for existing_contact in self.contacts):
            self.contacts.append(contact.details)
            logging.info(f"Contact added to {self.name} - {contact.details}")
            print("\nContact Saved!")
            self.save_contacts()
        else:
            print("Duplicate entry found. Contact not added.")
            logging.warning(f"Duplicate entry attempt in {self.name} - {contact.details}")

    def display_contacts(self):
        """
        Displays all contacts in the address book.
        """
        if not self.contacts:
            print(f"No contacts found in {self.name}.")
        else:
            print(f"\n{self.name}:")
            for contact in self.contacts:
                print("--------------------------------")
                for key, value in contact.items():
                    print(f"{key}: {value}")
            print("----------------------------------")

    def edit_contact(self, first_name, last_name, new_details):
        """
        Edits an existing contact using their first and last name.

        Args:
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
                self.save_contacts()
                return True
        print("Contact not found.")
        return False

    def delete_contact(self, first_name, last_name):
        """
        Deletes a contact from the address book using their first and last name.

        Args:
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
                self.save_contacts()
                return True
        print("Contact not found.")
        return False

    def search_by_city_or_state(self, city=None, state=None):
        """
        Searches for contacts by city or state.

        Args:
            city (str, optional): City to search for. Defaults to None.
            state (str, optional): State to search for. Defaults to None.

        Returns:
            list: List of contacts matching the search criteria.
        """
        results = []
        for contact in self.contacts:
            if (city and contact["city"].lower() == city.lower()) or \
               (state and contact["state"].lower() == state.lower()):
                results.append(contact)
        return results

    def count_contacts_by_city(self):
        """
        Counts the number of contacts by city.

        Returns:
            dict: Dictionary with city names as keys and contact counts as values.
        """
        city_count = {}
        for contact in self.contacts:
            city = contact["city"]
            city_count[city] = city_count.get(city, 0) + 1
        return city_count

    def sort_contacts_by_name(self):
        """
        Sorts the contacts alphabetically by first name, then last name.
        """
        self.contacts.sort(key=lambda x: (x["first_name"], x["last_name"]))
        print("\nContacts sorted alphabetically by name.")
        self.save_contacts()

    def sort_contacts_by_city(self):
        """
        Sorts the contacts alphabetically by city.
        """
        self.contacts.sort(key=lambda x: x["city"])
        print("\nContacts sorted alphabetically by city.")
        self.save_contacts()

class FileManager:
    """
    Handles file operations for address books.
    """

    @staticmethod
    def load_address_book(book_name):
        """
        Loads an address book from the CSV file.

        Args:
            book_name (str): The name of the address book to load.

        Returns:
            list: List of contacts for the specified address book.
        """
        contacts = []
        try:
            with open(CONTACTS_FILE, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['book_name'] == book_name:
                        contacts.append(row)
        except FileNotFoundError:
            logging.info("No existing contacts file found")
        return contacts

    @staticmethod
    def save_address_book(book_name, contacts):
        """
        Saves an address book to the CSV file.

        Args:
            book_name (str): The name of the address book to save.
            contacts (list): List of contacts to save.
        """
        try:
            temp_file = "temp_address_books.csv"
            with open(temp_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["book_name", "first_name", "last_name", "address", "city", "state", "zip_code", "phone_number", "email"])
                writer.writeheader()
                for contact in contacts:
                    contact["book_name"] = book_name
                    writer.writerow(contact)

            # Replace the original file with the temp file
            import os
            os.replace(temp_file, CONTACTS_FILE)

            logging.info("Address book saved to file")
        except Exception as e:
            logging.error(f"Error saving contacts: {str(e)}")
            print("Error saving contacts to file.")

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
        print("5) Sort Contacts by Name")
        print("6) Sort Contacts by City")
        print("7) Exit")
        main_choice = input("Enter your choice: ")

        if main_choice == "1":
            book_name = input("Enter Address Book Name: ")
            if book_name not in address_books:
                address_books[book_name] = AddressBook(book_name)
                print(f"Address Book '{book_name}' created!")

            address_book = address_books[book_name]
            manage_address_book(address_book)

        elif main_choice == "2":
            display_address_books(address_books)

        elif main_choice == "3":
            search_contacts(address_books)

        elif main_choice == "4":
            count_contacts_by_city(address_books)

        elif main_choice == "5":
            sort_contacts_by_name(address_books)

        elif main_choice == "6":
            sort_contacts_by_city(address_books)

        elif main_choice == "7":
            print("Exiting Program.")
            break
        else:
            print("Invalid choice, please try again.")

def manage_address_book(address_book):
    """
    Manages operations within a selected address book.

    Args:
        address_book (AddressBook): The address book to manage.
    """
    while True:
        print(f"\n{address_book.name} Menu:")
        print("1) Add Contact")
        print("2) Display Contacts")
        print("3) Edit Contact")
        print("4) Delete Contact")
        print("5) Sort Contacts by Name")
        print("6) Sort Contacts by City")
        print("7) Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact(address_book)
        elif choice == "2":
            address_book.display_contacts()
        elif choice == "3":
            edit_contact(address_book)
        elif choice == "4":
            delete_contact(address_book)
        elif choice == "5":
            address_book.sort_contacts_by_name()
        elif choice == "6":
            address_book.sort_contacts_by_city()
        elif choice == "7":
            break
        else:
            print("Invalid choice, please try again.")

def display_address_books(address_books):
    """
    Displays all available address books.

    Args:
        address_books (dict): Dictionary containing all address books.
    """
    if not address_books:
        print("No Address Books available.")
    else:
        print("\nAvailable Address Books:")
        for name in address_books:
            print(f"- {name}")

def search_contacts(address_books):
    """
    Searches for contacts by city or state across all address books.

    Args:
        address_books (dict): Dictionary containing all address books.
    """
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

def count_contacts_by_city(address_books):
    """
    Counts contacts by city across all address books.

    Args:
        address_books (dict): Dictionary containing all address books.
    """
    city_count = {}
    for address_book in address_books.values():
        counts = address_book.count_contacts_by_city()
        for city, count in counts.items():
            city_count[city] = city_count.get(city, 0) + count

    if city_count:
        print("\nContact Count by City:")
        print("---------------------------")
        for city, count in city_count.items():
            print(f"{city}: {count}")
        print("---------------------------")
    else:
        print("No contacts found in any city.")

def sort_contacts_by_name(address_books):
    """
    Sorts contacts by name across all address books.

    Args:
        address_books (dict): Dictionary containing all address books.
    """
    for address_book in address_books.values():
        address_book.sort_contacts_by_name()
    print("All address books sorted by name.")

def sort_contacts_by_city(address_books):
    """
    Sorts contacts by city across all address books.

    Args:
        address_books (dict): Dictionary containing all address books.
    """
    for address_book in address_books.values():
        address_book.sort_contacts_by_city()
    print("All address books sorted by city.")

def add_contact(address_book):
    """
    Adds a new contact to the address book.

    Args:
        address_book (AddressBook): The address book to add the contact to.
    """
    try:
        number_of_times = int(input("How many contacts do you want to add: "))
        for _ in range(number_of_times):
            print("\nEnter Contact Details:")
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
    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def edit_contact(address_book):
    """
    Edits an existing contact in the address book.

    Args:
        address_book (AddressBook): The address book containing the contact to edit.
    """
    print("Enter Contact Name to Edit:")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    try:
        print("Enter New Details:")
        new_address = input("New Address: ")
        new_city = input("New City: ")
        new_state = input("New State: ")
        new_zip_code = input("New Zip Code: ")
        new_phone_number = input("New Phone Number: ")
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
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def delete_contact(address_book):
    """
    Deletes a contact from the address book.

    Args:
        address_book (AddressBook): The address book containing the contact to delete.
    """
    first_name = input("Enter First Name to Delete: ")
    last_name = input("Enter Last Name to Delete: ")
    address_book.delete_contact(first_name, last_name)

if __name__ == "__main__":
    main()
