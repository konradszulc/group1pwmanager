import json
import re
import random
import string

# Caesar cipher encryption and decryption functions (pre-implemented)
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                # Included an additional if-statement to ensure that the decrypting process works properly
                if shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                if shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Password strength checker function (optional)
def is_strong_password(password):
    """
    Must be between 5 and 15 characters, with 1 number, 1 capital and 1 special character
    This is our projects base requirement for a strong password
    """
    special_char = string.punctuation
    strong = False
    chck1 = False
    chck2 = False
    chck3 = False
    chck4 = False

    # Checks for correct length of the password
    if len(password) >= 5 and len(password) <= 15:
        chck1 = True

    # Checks for a number in the password
    for value in password:
        if value.isnumeric():
            chck2 = True
            break
         
    # Checks for one capital letter in the string
    for value in password:
        if value.isupper():
            chck3 = True
            break

    # Checks for at least one special character in the string
    for value in password:
        if value in special_char:
            chck4 = True
            break
    
    # Checks whether all the required conditions are met and returns the result
    if chck1 and chck2 and chck3 and chck4:
        strong = True
        return strong
    else:
        return strong


# Password generator function (optional)
def generate_password(length):
    # We used a preliminary length before using the function, to ensure length will work in further code

    # Set the password as blank to trigger false in strength checker function 
    password = ""

    # Require vars that act as a library of different characters to use in the string
    nums = string.digits
    upper_char = string.ascii_uppercase
    lower_char = string.ascii_lowercase
    special_char = string.punctuation

    # Create a string of all the other characters for password to randomly select
    library_char = nums + special_char + upper_char + lower_char

    # Will consistenly run the password strength checker to ensure the generator produces a proper password eventually
    while is_strong_password(password) == False:

        # Resets the password if while loop performed a False password and create list for shuffle
        password = ""
        password_shuffle = []

        # Guarantees that the password meets the minimum requirements for the password strength checker
        password = random.choice(nums) + random.choice(special_char) + random.choice(upper_char)

        # This loop will run until the desired length is met
        while len(password) < length:
            password += random.choice(library_char)
        
        # Shuffle the characters to randomize the password further, first turning the string into a list, and then back into a string after the shuffle
        for items in password:
            password_shuffle += items

        random.shuffle(password_shuffle)
        
        password = ""
        for items in password_shuffle:
            password += items

    return password

# Initialize empty lists to store encrypted passwords, websites, and usernames
encrypted_passwords = []
websites = []
usernames = []

# Function to add a new password 
def add_password():
    # Inputs from the user 
    website = input("Please enter the name of the website: ")
    username = input("Please enter a username associated with the website: ")
    password = input("Would you like to randomly generate a password? (y/n): ")

    # Depending on whether the user wants to generate a password or enter one of their own
    if password == "y":
        # Forbids the user from entering a length that doesn't fall within the limits
        try:
            length = int(input("Please enter your desired length for the password. The password must be between 5 and 15 characters long (Please use an integer): "))
        except ValueError:
            print("Reminder: make it an integer.")
            length = -1
        while length < 5 or length > 15:
            try:
                length = int(input("That is not a suitable length. The password must be between 5 and 15 characters long: "))
            except ValueError:
                print("Reminder: make it an integer.")
                length = -1
        password = generate_password(length)
        print(f"Password was generated succesfully.")
    # User is prompted to create a password that meets the requirements of the is_strong_password() function
    else:
        password = input("Please enter your desired password. The password must be between 5 and 15 characters long and must contain 1 number, 1 special character and 1 capital letter: ")
        while is_strong_password(password) == False:
            print("That is not a suitable password")
            password = input ("Please try again: ")
        print("That is a suitable password.")
    # Password is encrypted
    e_password = caesar_encrypt(password,3)

    # User inputs are added to their respective lists within the same index
    websites.append(website.lower())
    usernames.append(username)
    encrypted_passwords.append(e_password)
    print(f"{website} was added successfully to the manager alongside your username {username} and password {password} which was encrypted becoming {e_password}")

# Function to retrieve a password 
def get_password():

    website = (input("For which website is the password for: "))
    index = 0
    shared_index = 0
    match = False
    # While loop to check if the requested website is included in the list
    while index < len(websites):
        if website.lower() == websites[index]:
            shared_index = index
            index +=1
            match = True
            password = caesar_decrypt(encrypted_passwords[shared_index],3)
            print(f"Your username is: {usernames[shared_index]} with password: {password}")
        else:
            index += 1
    if match == False:
        print(f"{website} was not found on the list.")

# Function to save passwords to a JSON file 
def save_passwords():
    # Checks if data stored in lists first
    if len(encrypted_passwords) <= 0:
        print("There is no data to store currently, please add passwords to the password manager first.")
    else:
        with open("vault.txt", "a") as pass_file:
            # JSON format, written into vault.txt file
            for i in range(len(encrypted_passwords)):
                x = {
		            "website": websites[i],
		            "username": usernames[i],
		            "password": encrypted_passwords[i]
		        }
                y = json.dumps(x)
                pass_file.write(y + "\n")
            print("Credentials successfully implemented into the vault.txt file.")

# Function to load passwords from a JSON file 

def load_passwords():
    # Converts JSON to list for other functions to run properly
    try:
        with open("vault.txt") as pass_file:
            for row in pass_file:
                convert = json.loads(row)
                website = convert["website"]
                username = convert["username"]
                password = convert["password"]
                # Checks if list already contains datasets
                print("Website: "+ website +", Username: "+ username + ", Password: " + caesar_decrypt(password, 3))
                if website in websites and username in usernames and password in encrypted_passwords:
                    continue
                else:
                    websites.append(website)
                    usernames.append(username)
                    encrypted_passwords.append(password)
            print("Passwords loaded successfully!")
    # Prevents loading passwords when no file exists      
    except FileNotFoundError:
        print ("The file vault.txt was not found.")
                

  # Main method
def main():
# implement user interface 

  while True:
    print("\nPassword Manager Menu:")
    print("1. Add Password")
    print("2. Get Password")
    print("3. Save Passwords")
    print("4. Load Passwords")
    print("5. Quit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_password()
    elif choice == "2":
        get_password()
    elif choice == "3":
        save_passwords()
    elif choice == "4":
        passwords = load_passwords()
        # Changed print statement from template, to better readibility
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")

# Execute the main function when the program is run
if __name__ == "__main__":
    main()
    