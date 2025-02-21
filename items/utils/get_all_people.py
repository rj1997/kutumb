import os
import json

def get_node_details(filename):
    with open('nodes/' + filename, "r") as file:
        node = json.load(file)
    return (node["name"], node["details"]["gender"], node["details"]["city"])

for filename in os.listdir('nodes/'):
    node_details = get_node_details(filename)
    print(node_details[0],'|',node_details[1],'|',node_details[2])



