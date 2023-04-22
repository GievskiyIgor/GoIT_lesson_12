from PhoneBook_classes import *

# user_contacts = AddressBook()

def user_help ():
      return """
          Phone book commands:
          1. hello
          2. add 'Name' 'phone" 'birthday' - (Igor +380989709609 28-05-1982) 
          3. change 'Name' 'phone 1' 'phone 2'  - (Igor +380989709609 +380990509393)
          4. search  - enter search string
          5. remove 'Name' 'phone'  - (Igor +380989709609') 
          6. show all
          7. good bye, close, exit
          """
 
# Decorator input errors
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"This contact {' '.join(args)} doesn't exist in the phone book"
        except ValueError:
            return "The entered name and phone number do not match the given parameter. For help, type 'help'"
        except IndexError:
            return "Type all params for command. For help, type 'help'"
        except TypeError:
             raise TypeError
            # return "Type all params for command. For help, type 'help'"
    return wrapper

def user_help1 (*args, **kwargs):
      user_contacts = kwargs['contacts']
      return """
          Phone book commands:
          1. hello
          2. add 'Name' 'phone" 'birthday' - (Igor +380989709609 28-05-1982) 
          3. change 'Name' 'phone 1' 'phone 2'  - (Igor +380989709609 +380990509393)
          4. search  - enter search string
          5. remove 'Name' 'phone'  - (Igor +380989709609') 
          6. show all
          7. good bye, close, exit
          """, user_contacts

# Greetings
@input_error
def user_hello(*args, **kwargs):
    user_contacts = kwargs['contacts']
    return "How can I help you?",  user_contacts

# Add добавление номера в адресную книгу
@input_error
def user_add(*args, **kwargs):
    user_contacts = kwargs['contacts']
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[2]) if len(args) > 2 else None
    
    try:
        rec = user_contacts.get(name.value)
    except AttributeError:
        rec = None

    if not rec:
        if not birthday:
            birthday = None

        rec: Record = Record(name, phone, birthday)
        user_contacts.add_record(rec)
        return f"{name} : {phone}, {birthday} has been added to the phone book", user_contacts    
    
    rec.add_phone(phone)
    return f"Phone {phone} add to contact {name}", user_contacts
    #  ****

# Change  изменение номера в адресной книги
@input_error
def user_change(*args, **kwargs):
    user_contacts = kwargs['contacts']
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    
    rec = user_contacts.get(name.value)
    
    if rec:
        return rec.change_phone(old_phone, new_phone), user_contacts
    
    return f'Phone book has no contact {name}', user_contacts

    
# Contact phone number
@input_error
def user_phone(*args, **kwargs):
    user_contacts = kwargs['contacts']
    # name = Name(args[0])
    # record = user_contacts.[name.value]
    record = user_contacts.search(args[0])
   
    return record, user_contacts
    # return f"The phone number for {name} is {record.phones}", user_contacts
    

# Show all  вся адресная книга
@input_error
def user_show_all(*args, **kwargs):
    user_contacts = kwargs['contacts']
    all = ""
    
    if len(user_contacts) == 0:
        return "Phone book is empty", user_contacts
    else:
        for name in user_contacts.data:
           rec: Record = user_contacts.data[name]
           bd = str(rec.birthday.value.strftime("%d.%m.%Y")) if rec.birthday else ""
           birthday_day = f"Birthday {bd}." if rec.birthday else ""
           days_birthday = f"Days birthday - {rec.days_to_birthday() }."  if rec.birthday != None else "" 
           
           print(f"{rec.name.value}: {', '.join(str(phone) for phone in rec.phones)}. {birthday_day} {days_birthday}")
        
        return all, user_contacts
# 
@input_error
def remove_phone(*args, **kwargs):
    user_contacts = kwargs['contacts']
    name = Name(args[0])
    phone = Phone(args[1])
    
    rec:Record = user_contacts[name.value]
    return rec.remove_record(phone), user_contacts
 
@input_error
def birthday_to_days(*args, **kwargs):
    user_contacts = kwargs['contacts']
    name =Name(args[0])

    rec:Record = user_contacts.get(name.value)

    if rec:
        birthday = rec.birthday.value
        today = datetime.date.today()
        current_year_birthday = datetime.date(today.year, birthday.month, birthday.day)

    if current_year_birthday < today:
        current_year_birthday = datetime.date(today.year + 1 , birthday.month, birthday.day)
        delta = current_year_birthday - today
        return delta.days
    else:    
         print('No record found for '+ name)   

# Exit
def user_exit(*args, **kwargs): 
    user_contacts = kwargs['contacts']
    return "Good bye!\n", user_contacts

COMMANDS = {
    'hello': user_hello, # приветствие
    'add': user_add, # Добавление
    'change': user_change, # Изменение
    'search': user_phone, # Поиск, больше 3 символов
    'show all': user_show_all, # Список контактов
    'remove': remove_phone, # удаление из адресной книги
    'good bye': user_exit, # выход
    'close': user_exit,
    'exit': user_exit,
    'help': user_help1, # помощь
}
 
# Command processing
def command_handler(user_input: str):
    for cmd in COMMANDS:
        if user_input.startswith(cmd):
            return COMMANDS[cmd], user_input.replace(cmd, '').strip().split()
    return None, []

# ********
def main(csv_file):
    
    print(user_help())
    user_contacts = AddressBook()
    user_contacts.read_csv(csv_file)
    
    while True:
        user_input = input("Enter a command: ")
        command, data = command_handler(user_input)
        result, contacts = command(*data, contacts = user_contacts)
        print(result)
        if command == user_exit:
            contacts.save_csv(csv_file)
            break

        if not command:
            print("Command is not supported. Try again.")
            continue
        
      


if __name__ == "__main__":

    csv_file = 'user_contacts.csv'
    main(csv_file)
    