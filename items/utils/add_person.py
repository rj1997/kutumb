import uuid
import json
import os

class Person:
    def __init__(self, name, details=None) -> None:
        self.id = str(uuid.uuid4())  # Generate a unique ID
        self.name = name
        self.details = details if details else {}

    def add_detail(self, key, value):
        self.details[key] = value

    def save_to_json(self):
        folder = "nodes"
        os.makedirs(folder, exist_ok=True)  # Ensure the folder exists
        file_path = os.path.join(folder, f"{self.id}.json")
        with open(file_path, "w") as file:
            json.dump({"id": self.id, "name": self.name, "details": self.details}, file, indent=4)

def create_person():
    name = input("Enter name: ").strip()
    details = {}
    
    add_details = input("Do you want to add details? (yes/no): ").strip().lower()
    if add_details == "yes":
        city = input("Enter city: ").strip()
        gender = input("Enter gender (M/F): ").strip()
        details["city"] = city
        details["gender"] = gender

    
    person = Person(name, details)
    person.save_to_json()
    print(f"Person created with ID: {person.id}")

if __name__ == "__main__":
    create_person()
