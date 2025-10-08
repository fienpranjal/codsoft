import json
import os

class ContactManager:
    def __init__(self):
        self.file = "contacts.json"
        self.contacts = self.load_contacts()
    
    def load_contacts(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_contacts(self):
        with open(self.file, 'w') as f:
            json.dump(self.contacts, f, indent=2)
    
    def add_contact(self):
        name = input("Name: ").strip()
        if name in self.contacts:
            print("Contact already exists!")
            return
        
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()
        address = input("Address: ").strip()
        
        self.contacts[name] = {
            "phone": phone,
            "email": email,
            "address": address
        }
        self.save_contacts()
        print("Contact added successfully!")
    
    def view_contacts(self):
        if not self.contacts:
            print("No contacts found.")
            return
        
        print("\n--- Contact List ---")
        for name, details in self.contacts.items():
            print(f"{name}: {details['phone']}")
    
    def search_contact(self):
        query = input("Search by name or phone: ").strip().lower()
        found = []
        
        for name, details in self.contacts.items():
            if query in name.lower() or query in details['phone']:
                found.append((name, details))
        
        if found:
            print("\n--- Search Results ---")
            for name, details in found:
                print(f"Name: {name}")
                print(f"Phone: {details['phone']}")
                print(f"Email: {details['email']}")
                print(f"Address: {details['address']}")
                print("-" * 20)
        else:
            print("No contacts found.")
    
    def update_contact(self):
        name = input("Enter contact name to update: ").strip()
        if name not in self.contacts:
            print("Contact not found!")
            return
        
        print(f"Current details for {name}:")
        details = self.contacts[name]
        print(f"Phone: {details['phone']}")
        print(f"Email: {details['email']}")
        print(f"Address: {details['address']}")
        
        phone = input(f"New phone ({details['phone']}): ").strip()
        email = input(f"New email ({details['email']}): ").strip()
        address = input(f"New address ({details['address']}): ").strip()
        
        self.contacts[name] = {
            "phone": phone or details['phone'],
            "email": email or details['email'],
            "address": address or details['address']
        }
        self.save_contacts()
        print("Contact updated successfully!")
    
    def delete_contact(self):
        name = input("Enter contact name to delete: ").strip()
        if name not in self.contacts:
            print("Contact not found!")
            return
        
        confirm = input(f"Delete {name}? (y/n): ").strip().lower()
        if confirm == 'y':
            del self.contacts[name]
            self.save_contacts()
            print("Contact deleted successfully!")
    
    def run(self):
        while True:
            print("\n--- Contact Manager ---")
            print("1. Add Contact")
            print("2. View Contacts")
            print("3. Search Contact")
            print("4. Update Contact")
            print("5. Delete Contact")
            print("6. Exit")
            
            choice = input("Choose option (1-6): ").strip()
            
            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.view_contacts()
            elif choice == '3':
                self.search_contact()
            elif choice == '4':
                self.update_contact()
            elif choice == '5':
                self.delete_contact()
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid option!")

if __name__ == "__main__":
    ContactManager().run()