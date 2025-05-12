import random
import string
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Path to the JSON file
PASSWORDS_FILE = "saved_passwords.json"

def generate_password(length, use_lowercase=True, use_uppercase=True, use_numbers=True, use_special=True):
    """Generate a random password based on specified criteria."""
    # Define character sets
    lowercase_chars = string.ascii_lowercase if use_lowercase else ""
    uppercase_chars = string.ascii_uppercase if use_uppercase else ""
    number_chars = string.digits if use_numbers else ""
    special_chars = string.punctuation if use_special else ""
    
    # Combine all enabled character sets
    all_chars = lowercase_chars + uppercase_chars + number_chars + special_chars
    
    # Ensure at least one character set is selected
    if not all_chars:
        return None
    
    # Generate password
    password = "".join(random.choice(all_chars) for _ in range(length))
    
    return password

def load_passwords():
    """Load saved passwords from JSON file"""
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_password(password, description=""):
    """Save a password to the JSON file"""
    passwords = load_passwords()
    
    # Create new password entry
    new_entry = {
        "password": password,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add to list and save
    passwords.append(new_entry)
    
    with open(PASSWORDS_FILE, 'w') as file:
        json.dump(passwords, file, indent=4)
    
    return True

@app.route('/')
def index():
    """Main page with password generator"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate a password based on form inputs"""
    try:
        # Get parameters from form
        length = int(request.form.get('length', 12))
        use_lowercase = 'lowercase' in request.form
        use_uppercase = 'uppercase' in request.form
        use_numbers = 'numbers' in request.form
        use_special = 'special' in request.form
        
        # Generate password
        password = generate_password(length, use_lowercase, use_uppercase, use_numbers, use_special)
        
        if not password:
            return jsonify({"error": "Please select at least one character type"}), 400
        
        return jsonify({"password": password})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/save', methods=['POST'])
def save():
    """Save a password to JSON file"""
    try:
        data = request.get_json()
        password = data.get('password')
        description = data.get('description', '')
        
        if not password:
            return jsonify({"error": "No password provided"}), 400
        
        save_password(password, description)
        return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/passwords')
def view_passwords():
    """View all saved passwords"""
    passwords = load_passwords()
    return render_template('passwords.html', passwords=passwords)

if __name__ == '__main__':
    app.run(debug=True) 