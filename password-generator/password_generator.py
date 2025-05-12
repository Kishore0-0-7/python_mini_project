import random
import string

def generate_password(length, use_lowercase=True, use_uppercase=True, use_numbers=True, use_special=True):
    """
    Generate a random password based on specified criteria.
    
    Args:
        length (int): Length of the password to generate
        use_lowercase (bool): Include lowercase letters
        use_uppercase (bool): Include uppercase letters
        use_numbers (bool): Include numbers
        use_special (bool): Include special characters
    
    Returns:
        str: Generated password
    """
    # Define character sets
    lowercase_chars = string.ascii_lowercase if use_lowercase else ""
    uppercase_chars = string.ascii_uppercase if use_uppercase else ""
    number_chars = string.digits if use_numbers else ""
    special_chars = string.punctuation if use_special else ""
    
    # Combine all enabled character sets
    all_chars = lowercase_chars + uppercase_chars + number_chars + special_chars
    
    # Ensure at least one character set is selected
    if not all_chars:
        print("Error: At least one character set must be selected")
        return None
    
    # Generate password
    password = "".join(random.choice(all_chars) for _ in range(length))
    
    return password

def main():
    print("==== Password Generator ====")
    
    # Get password length from user
    while True:
        try:
            length = int(input("Enter the desired password length: "))
            if length <= 0:
                print("Please enter a positive number")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Get complexity preferences
    use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
    use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_numbers = input("Include numbers? (y/n): ").lower() == 'y'
    use_special = input("Include special characters? (y/n): ").lower() == 'y'
    
    # Generate and display password
    password = generate_password(length, use_lowercase, use_uppercase, use_numbers, use_special)
    
    if password:
        print("\nGenerated Password:", password)
    else:
        print("\nPassword generation failed. Please select at least one character set.")

if __name__ == "__main__":
    main() 