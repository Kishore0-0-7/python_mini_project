# Password Generator

This repository contains both command-line and web-based applications for generating secure, random passwords.

## Command-Line Password Generators

### Simple Password Generator

The `simple_password_generator.py` file contains a basic password generator that:
- Prompts the user to specify the desired length of the password
- Generates a password of the specified length using a combination of lowercase letters, uppercase letters, digits, and special characters
- Displays the generated password on the screen

#### Usage

```bash
python simple_password_generator.py
```

### Advanced Password Generator

The `password_generator.py` file contains a more advanced password generator with additional features:
- Allows users to specify password length
- Lets users choose which character types to include (lowercase, uppercase, numbers, special characters)
- Provides input validation
- Ensures at least one character type is selected

#### Usage

```bash
python password_generator.py
```

## Web-Based Password Generator

The web application provides a user-friendly interface for generating and managing passwords.

### Features

- Generate secure passwords with customizable length and character types
- Copy generated passwords to clipboard
- Save passwords with descriptions for future reference
- View all saved passwords
- Password masking for security

### Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

### How It Works

The web application stores saved passwords in a JSON file (`saved_passwords.json`) with the following structure:

```json
[
  {
    "password": "generated_password",
    "description": "user_description",
    "created_at": "timestamp"
  }
]
```

## Requirements

- Python 3.x
- Flask (for web version)
- Web browser (for web version) 