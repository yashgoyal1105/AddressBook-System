import logging

logging.basicConfig(
    filename='contacts.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

CONTACTS_FILE = "address_books.txt"

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
        Initializes an empty address book and loads contacts from a file.

        Args:
            name (str): The name of the address book.
        """
        self.name = name
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        """
        Loads contacts for this address book from the main file.
        """
        try:
            self.contacts = []
            current_book = ""
            current_contact = {}

            try:
                with open(CONTACTS_FILE, 'r') as file:
                    for line in file:
                        line = line.strip()

                        # Check for bookName
                        if line.endswith(':') and not line.startswith('first_name:'):
                            current_book = line.rstrip(':')
                            continue

                        # current book
                        if current_book == self.name:
                            if line.startswith('first_name:'):
                                if current_contact:
                                    self.contacts.append(current_contact.copy())
                                current_contact = {}

                            if ':' in line:
                                key, value = line.split(':', 1)
                                key = key.strip()
                                value = value.strip().rstrip(',')
                                current_contact[key] = value

                    # Add the last contact if it belongs to current book
                    if current_contact and current_book == self.name:
                        self.contacts.append(current_contact.copy())

            except FileNotFoundError:
                logging.info("No existing contacts file found")
        except Exception as e:
            logging.error(f"Error loading contacts: {str(e)}")

    @staticmethod
    def save_all_books(address_books):
        """
        Saves all address books to a single file.

        Args:
            address_books (dict): Dictionary containing all address books.
        """
        try:
            with open(CONTACTS_FILE, 'w') as file:
                file.write("AddressBooks:\n")
                file.write("_________________________\n")

                for book_name, book in address_books.items():
                    file.write(f"{book_name}:\n")
                    for contact in book.contacts:
                        file.write("--------------------------------\n")
                        file.write(f"first_name: {contact['first_name']},\n")
                        file.write(f"last_name: {contact['last_name']},\n")
                        file.write(f"address: {contact['address']},\n")
                        file.write(f"city: {contact['city']},\n")
                        file.write(f"state: {contact['state']},\n")
                        file.write(f"zip_code: {contact['zip_code']},\n")
                        file.write(f"phone_number: {contact['phone_number']},\n")
                        file.write(f"email: {contact['email']}\n")
                    file.write("----------------------------------\n")

            logging.info("All address books saved to file")
        except Exception as e:
            logging.error(f"Error saving contacts: {str(e)}")
            print("Error saving contacts to file.")

    def add_contact(self, contact):
        """
        Adds a contact to the address book and logs the details.

        Args:
            contact (ContactPerson): Contact object to be added.
        """
        if any(existing_contact["first_name"] == contact.details["first_name"] and
               existing_contact["last_name"] == contact.details["last_name"]
               for existing_contact in self.contacts):
            print("Duplicate entry found. Contact not added.")
            logging.warning(f"Duplicate entry attempt in {self.name} - {contact.details}")
        else:
            self.contacts.append(contact.details)
            logging.info(f"Contact added to {self.name} - {contact.details}")
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
            print(f"\n{self.name}:")
            for contact in self.contacts:
                print("--------------------------------")
                print(f"first_name: {contact['first_name']},")
                print(f"last_name: {contact['last_name']},")
                print(f"address: {contact['address']},")
                print(f"city: {contact['city']},")
                print(f"state: {contact['state']},")
                print(f"zip_code: {contact['zip_code']},")
                print(f"phone_number: {contact['phone_number']},")
                print(f"email: {contact['email']}")
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
                new_details["first_name"] = first_name
                new_details["last_name"] = last_name
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

    def sort_contacts_by_city(self):
        """
        Sorts the contacts alphabetically by city.
        """
        self.contacts.sort(key=lambda x: x["city"])
        print("\nContacts sorted alphabetically by city.")

def main():
    """
    Main function to manage multiple address books.
    """
    address_books = {}

    # Load existing address books
    try:
        with open(CONTACTS_FILE, 'r') as file:
            current_book = None
            for line in file:
                line = line.strip()
                if line.endswith(':') and not line.startswith('first_name:'):
                    current_book = line.rstrip(':')
                    if current_book != "AddressBooks" and current_book not in address_books:
                        address_books[current_book] = AddressBook(current_book)
    except FileNotFoundError:
        pass

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
            while True:
                print(f"\n{book_name} Menu:")
                print("1) Add Contact")
                print("2) Display Contacts")
                print("3) Edit Contact")
                print("4) Delete Contact")
                print("5) Sort Contacts by Name")
                print("6) Sort Contacts by City")
                print("7) Go Back")
                choice = input("Enter your choice: ")

                if choice == "1":
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
                            contact = ContactPerson(first_name, last_name, address, city,
                                                 state, zip_code, phone_number, email)
                            address_book.add_contact(contact)
                            AddressBook.save_all_books(address_books)
                    except ValueError:
                        print("Please enter a valid number.")
                    except Exception as e:
                        print(f"An error occurred: {str(e)}")

                elif choice == "2":
                    address_book.display_contacts()

                elif choice == "3":
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
                        if address_book.edit_contact(first_name, last_name, new_details):
                            AddressBook.save_all_books(address_books)
                    except Exception as e:
                        print(f"An error occurred: {str(e)}")

                elif choice == "4":
                    first_name = input("Enter First Name to Delete: ")
                    last_name = input("Enter Last Name to Delete: ")
                    if address_book.delete_contact(first_name, last_name):
                        AddressBook.save_all_books(address_books)

                elif choice == "5":
                    address_book.sort_contacts_by_name()
                    AddressBook.save_all_books(address_books)

                elif choice == "6":
                    address_book.sort_contacts_by_city()
                    AddressBook.save_all_books(address_books)

                elif choice == "7":
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

        elif main_choice == "5":
            for address_book in address_books.values():
                address_book.sort_contacts_by_name()
            AddressBook.save_all_books(address_books)
            print("All address books sorted by name.")

        elif main_choice == "6":
            for address_book in address_books.values():
                address_book.sort_contacts_by_city()
            AddressBook.save_all_books(address_books)
            print("All address books sorted by city.")

        elif main_choice == "7":
            print("Exiting Program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
