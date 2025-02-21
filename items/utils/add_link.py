import uuid
import json
import os

class Link:
    def __init__(self, link_from, link_to, link_relation) -> None:
        self.id = str(uuid.uuid4())  # Generate a unique ID
        self.link_from = link_from
        self.link_to = link_to
        self.link_relation = link_relation

    def save_to_json(self):
        file_path = "links.json"
        
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                links = json.load(file)
        else:
            links = []
        
        links.append({
            "id" : str(uuid.uuid4()),
            "link_from": self.link_from,
            "link_to": self.link_to,
            "link_relation": self.link_relation
        })
        
        with open(file_path, "w") as file:
            json.dump(links, file, indent=4)

def list_people():
    folder = "nodes"
    if not os.path.exists(folder):
        return []
    
    people = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        with open(file_path, "r") as file:
            person_data = json.load(file)
            people.append((
                person_data["id"],
                person_data["name"] + ' | ' + person_data["details"]["city"]
            ))
    return people

def select_person():
    people = list_people()
    if not people:
        print("No people available.")
        return None
    
    for index, person in enumerate(people):
        print(str(index+1) + '.',person[1])
    
    choice = int(input("Select a person by number: ")) - 1
    return people[choice][0] if 0 <= choice < len(people) else None

def create_link():
    print("Select link_from person:")
    link_from = select_person()
    if not link_from:
        return
    
    print("Select link_to person:")
    link_to = select_person()
    if not link_to:
        return
    
    link_relation = input("Enter relation (e.g., parent, sibling, spouse): ").strip()
    link = Link(link_from, link_to, link_relation)
    link.save_to_json()
    print("Link created successfully.")

if __name__ == "__main__":
    create_link()
