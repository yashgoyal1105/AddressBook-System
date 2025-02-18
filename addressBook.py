import logging

"""
Simple Address Book Program
This script collects contact details from the user, logs them to a file, and displays them.
"""

logging.basicConfig(filename='contacts.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Collects contact details from the user, logs them, and displays them.
    Handles exceptions to ensure smooth execution.
    """
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
        
        logging.info(f"Contact Saved -\n First Name: {first_name},\n Last Name: {last_name},\n Address: {address},\n City: {city},\n State: {state},\n Zip Code: {zip_code},\n Phone Number: {phone_number},\n Email: {email}")
        
        print("\nContact Saved!")
        print("---------------------------")
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Address:", address)
        print("City:", city)
        print("State:", state)
        print("Zip Code:", zip_code)
        print("Phone Number:", phone_number)
        print("Email:", email)
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print("An error occurred while saving contact details. Please try again.")

if __name__ == "__main__":
    main()
