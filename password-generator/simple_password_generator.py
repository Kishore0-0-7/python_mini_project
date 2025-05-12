import random
import string

def generate_password(length):
    """
    Generate a random password of specified length using a combination of
    lowercase letters, uppercase letters, digits, and special characters.
    
    Args:
        length (int): Length of the password to generate
    
    Returns:
        str: Generated password
    """
    # Define character sets
    all_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    
    # Generate password
    password = "".join(random.choice(all_chars) for _ in range(length))
    
    return password

def main():
    print("==== Password Generator ====")
    
    # Get password length from user
    while True:
        try:
            length = int(input("Enter the desired length of the password: "))
            if length <= 0:
                print("Please enter a positive number")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Generate and display password
    password = generate_password(length)
    print("\nGenerated Password:", password)

if __name__ == "__main__":
    main() 