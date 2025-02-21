import os
import json
import uuid
from collections import deque

FILE_PATH = "links.json"
no_new_links_created = False
total_new_links_created = 0
iteration = 0

def get_node_details(id):
    with open('nodes/' + str(id) + '.json', "r") as file:
        node = json.load(file)
    return node["name"]

def check_already_exist(links, link_from, link_to, link_relation):
    for link in links:
        if link['link_from'] == link_from and link['link_to'] == link_to and link['link_relation'] == link_relation:
            return True
    return False

def list_children(links, node):
    children_list = []
    for link in links:
        if link['link_relation'] == 'parent' and link['link_from'] == node:
            children_list.append(link['link_to'])
    if children_list is []:
        return False, children_list
    else:
        return True, children_list


def add_new_synthetic_link(links, link_from, link_to, link_relation):
    if check_already_exist(links, link_from, link_to, link_relation):
        return False, None, links
    new_link = {
        'id' : str(uuid.uuid4()),
        'is_synthetic_link' : True,
        'link_from': link_from,
        'link_to' : link_to,
        'link_relation' : link_relation
    }
    links.append(new_link)
    print('Created New Link :: From:', get_node_details(new_link['link_from']), 'To:', get_node_details(new_link['link_to']), 'Relation:', new_link['link_relation'])
    return True, new_link, links

if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r") as file:
        links = json.load(file)
else:
    links = []
    
link_queue = deque()
for link in links:
    link_queue.append(link)

while len(link_queue) > 0:
    link = link_queue.popleft()
    print('Visiting Link :: From:', get_node_details(link['link_from']), 'To:', get_node_details(link['link_to']), 'Relation:', link['link_relation'])

    if link['link_relation'] == 'sibling':
        new_link_added, new_link, links = add_new_synthetic_link(links, link['link_to'], link['link_from'], 'sibling')
        if new_link_added:
            link_queue.append(new_link)

    elif link['link_relation'] == 'spouse':
        new_link_added, new_link, links = add_new_synthetic_link(links, link['link_to'], link['link_from'], 'spouse')
        if new_link_added:
            link_queue.append(new_link)
        is_parent, children_list = list_children(links, link['link_to'])
        if is_parent:
            for child in children_list:
                new_link_added, new_link, links = add_new_synthetic_link(links, link['link_from'], child, 'parent')
                if new_link_added:
                    link_queue.append(new_link)

    elif link['link_relation'] == 'parent':
        new_link_added, new_link, links = add_new_synthetic_link(links, link['link_to'], link['link_from'], 'child')
        if new_link_added:
            link_queue.append(new_link)
        for link_item in links:
            if link_item['link_to'] == link['link_to'] and link_item['link_relation'] == 'parent' and link_item['link_from']  != link['link_from']:
                new_link_added, new_link, links = add_new_synthetic_link(links, link['link_from'], link_item['link_from'], 'spouse')
                if new_link_added:
                    link_queue.append(new_link)
            if link_item['link_from'] == link['link_to'] and link_item['link_relation'] == 'sibling':
                new_link_added, new_link, links = add_new_synthetic_link(links, link['link_from'], link_item['link_to'], 'parent')
                if new_link_added:
                    link_queue.append(new_link)

# with open(FILE_PATH, "w") as file:
#     json.dump(links, file, indent=4)

    



