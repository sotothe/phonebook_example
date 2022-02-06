import json
import pickle
import yaml

STORAGE = 'yaml'
contacts = []

def add():
    contacts.append(dict(
        firstname=input('firstname: '),
        lastname=input('lastname: '),
        nickname=input('nickname: '),
        phone=input('phone: '),
        email=input('email: ') or '-',
    ))
    save()

def view(lst=None):
    if lst == None:
        lst = contacts
    if len(lst) == 0:
        print('Nothing to show!')
    else:
        keys = 'firstname lastname nickname phone email'.split()
        print(' NO ', *[i.upper().center(12) for i in keys])
        for idx,contact in enumerate(lst):
            print(str(idx+1).ljust(4) ,*[contact.get(i).capitalize().center(12) for i in keys])

def find(only_one=False, msg='Who do you look for? '):
    x = input(msg)
    result = []
    for contact in contacts:
        if x in ' '.join(contact.values()):
            result.append(contact)
    view(result)
    if only_one:
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            n = int(input('Which one? '))
            return result[n-1]

def delete():
    x = find(only_one=True, msg='Who do you want to delete? ')
    if x == None:
        return
    contacts.remove(x)
    save()
    print(f"{x.get('firstname')} {x.get('lastname')} has been deleted.")

def edit():
    x = find(only_one=True, msg='Who do you want to edit? ')
    if x == None:
        return
    contacts.remove(x)
    contacts.append(dict(
        firstname=input(f"firstname ({x.get('firstname')}): ").strip() or x.get('firstname'),
        lastname=input(f"lastname ({x.get('lastname')}): ").strip() or x.get('lastname'),
        nickname=input(f"nickname ({x.get('nickname')}): ").strip() or x.get('nickname'),
        phone=input(f"phone ({x.get('phone')}): ").strip() or x.get('phone'),
        email=input(f"email ({x.get('email')}): ").strip() or x.get('email'),
    ))
    save()
    print(f"{x.get('firstname')} {x.get('lastname')} has been edited.")
    
def help():
    print('''
    a, add
    e, edit
    v, view
    f, find
    d, delete
    x, exit
    ''')

def menu():
    while True:
        dict(
            a=add, add=add,
            e=edit, edit=edit,
            v=view, view=view,
            f=find, find=find,
            d=delete, delete=delete,
            x=exit, exit=exit,
        ).get(input('What to do? '), help)()

def sort():
    contacts.sort(key=lambda x:x['firstname']+x['lastname']+x['nickname'], reverse=False)

def save():
    sort()
    if STORAGE == 'text':
        with open('data.txt', 'w') as f:
            f.write(str(contacts))
    elif STORAGE == 'json':
        with open('data.json', 'w') as f:
            json.dump(contacts, f, indent=4)
    elif STORAGE == 'pickle':
        with open('data.pkl', 'wb') as f:
            pickle.dump(contacts, f)
    elif STORAGE == 'yaml':
        with open('data.yml', 'w') as f:
            yaml.safe_dump(contacts, f)

def load():
    global contacts
    try:
        if STORAGE == 'text':
            with open('data.txt', 'r') as f:
                contacts = eval(f.read())
        elif STORAGE == 'json':
            with open('data.json', 'r') as f:
                contacts = json.load(f)
        elif STORAGE == 'pickle':
            with open('data.pkl', 'rb') as f:
                contacts = pickle.load(f)
        elif STORAGE == 'yaml':
            with open('data.yml', 'r') as f:
                contacts = yaml.safe_load(f)
    except FileNotFoundError:
        pass

load()
menu()
