from entities import *
import pickle

# Decorators
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please(10 digits)."
        except KeyError:
            return "Contact doesn't exists in your contact list."
        except IndexError:
            return "Enter the argument for the command."
        except SyntaxError as e:
            return e

    return inner

# Handlers
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = 'Contact added.'
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook) -> str:
    name, phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(phone, new_phone)
        return "Contact changed."
    raise SyntaxError(f"Give name, phone and new number of the contact.")

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        phones = ", ".join([phone.value for phone in record.phones ])
        return phones
    raise KeyError()

@input_error
def add_birthday(args, book: AddressBook) -> str:
    name, date, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return f"Birthday added to Contact: {name}"
    raise KeyError(f"Contact {name} not found.")

@input_error
def show_birthday(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record: return f"{name}'s birthday is {record.birthday} "
    raise KeyError(f"Contact {name} not found.")

@input_error
def birthdays(book: AddressBook):
    for contact in book.get_upcoming_birthdays():
        print(f"Don't forget to wish {contact['name']} a happy birthday on {contact['congratulation_date']}")

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()