import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Path to the JSON file
CONTACTS_FILE = "contacts.json"

def load_contacts():
    """Load saved contacts from JSON file"""
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_contacts(contacts):
    """Save contacts to the JSON file"""
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)
    return True

def add_contact(name, phone, email="", address=""):
    """Add a new contact to the JSON file"""
    contacts = load_contacts()
    
    # Create new contact entry with a unique ID
    new_id = 1
    if contacts:
        new_id = max(contact.get("id", 0) for contact in contacts) + 1
    
    new_contact = {
        "id": new_id,
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add to list and save
    contacts.append(new_contact)
    save_contacts(contacts)
    
    return True

def update_contact(contact_id, name, phone, email="", address=""):
    """Update an existing contact"""
    contacts = load_contacts()
    
    for contact in contacts:
        if contact["id"] == contact_id:
            contact["name"] = name
            contact["phone"] = phone
            contact["email"] = email
            contact["address"] = address
            contact["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    
    save_contacts(contacts)
    return True

def delete_contact(contact_id):
    """Delete a contact by ID"""
    contacts = load_contacts()
    contacts = [contact for contact in contacts if contact["id"] != contact_id]
    save_contacts(contacts)
    return True

@app.route('/')
def index():
    """Main page with contact list"""
    contacts = load_contacts()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add new contact page"""
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email', '')
        address = request.form.get('address', '')
        
        if not name or not phone:
            return render_template('add.html', error="Name and phone are required fields")
        
        add_contact(name, phone, email, address)
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit(contact_id):
    """Edit existing contact"""
    contacts = load_contacts()
    contact = next((c for c in contacts if c["id"] == contact_id), None)
    
    if not contact:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email', '')
        address = request.form.get('address', '')
        
        if not name or not phone:
            return render_template('edit.html', contact=contact, error="Name and phone are required fields")
        
        update_contact(contact_id, name, phone, email, address)
        return redirect(url_for('index'))
    
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:contact_id>')
def delete(contact_id):
    """Delete a contact"""
    delete_contact(contact_id)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    """Search for contacts"""
    query = request.args.get('q', '').lower()
    contacts = load_contacts()
    
    if query:
        filtered_contacts = []
        for contact in contacts:
            if (query in contact['name'].lower() or 
                query in contact['phone'].lower() or 
                query in contact.get('email', '').lower()):
                filtered_contacts.append(contact)
        contacts = filtered_contacts
    
    return render_template('index.html', contacts=contacts, search_query=query)

if __name__ == '__main__':
    app.run(debug=True) 