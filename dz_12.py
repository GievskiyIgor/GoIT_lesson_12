from PhoneBook_classes import *
from collections import UserDict
from datetime import datetime
import re
import csv

# ************************* CLASSES  *************************
class Field ():
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self)
 
class Name (Field):
    pass
    
class Phone (Field):
    def __init__(self, value=None):
        self.value = value
        
    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self, value):
        if value is None:
            self._value = value
        else:
            self._value = self.number_phone(value)
        
    def number_phone(self, phone:str):
        if not re.match(r"^\+[\d]{12}$", phone):
                raise ValueError
        return phone

class Birthday (Field):
    def __init__(self, value) -> None:
        # super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value (self):
        return self.__value.strftime('%d-%m-%Y')
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            raise ValueError('"dd-mm-yyyy" - birthday format')    
    
    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


class Record ():
    def __init__(self, name:Name, phone:Phone = None, birthday:Birthday = None):
        self.name = name
        self.phones = [phone] if phone else [] 
        self.birthday = birthday
    
    # Добавление телефона из адресной книги
    def add_phone(self, phone:Phone):
        self.phones.append(phone)

    # Удаление телефона из адресной книги
    def remove_record(self, phone:Phone):
        # self.phones.remove(phone)
        for i, p in enumerate(self.phones):
            if p.value == phone.value:
                self.phones.pop(i)
                return f"Phone {phone} deleted successfully"
        return f'Contact has no phone {phone}'  
    
    # Изменение телефона в адресной книги
    def change_phone(self, old_phone:Phone, new_phone:Phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone.value:
                self.phones[i] = new_phone
                return f'Phone {old_phone} change to {new_phone}'
        return f'Contact has no phone {old_phone}'   
    
    # день рождения
    def set_birthday(self, birthday):
        self.birthday = birthday

    def get_birthday (self):    
        return self.birthday.value if self.birthday else None
    
    def days_to_birthday(self):
        
        if self.birthday:
            dateB = self.birthday
            today = datetime.date.today()
            current_year_dateB = datetime.date(today.year, dateB.month, dateB.day)

            if current_year_dateB < today:
                current_year_dateB = datetime.date(today.year+1, dateB.month, dateB.day)

            delta =current_year_dateB - today    
            return delta.days
        
        return None
    
    def __str__(self):
        result = ''
        phones = ", ".join([str(phone) for phone in self.phones])
    
        if self.birthday:
            result += f"{self.name}: {phones}. Birthday: {self.birthday}\n"
        else:
            result += f"{self.name}: {phones}"
        return result
   
class AddressBook(UserDict):
    index = 0
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def write_csv(self, user_contacts):
        
        try:
            with open (csv_file, 'w', newline ='') as f:
                fieldnames = ['Name','Phones','Birthday']
                writer = csv.DictWriter(f, fieldnames = fieldnames)
                writer.writeheader()
                for name in user_contacts.data:
                    record = user_contacts.data[name]
                # for record in  user_contacts:
                    name = record.name.value
                    phones = [phone.value for phone in record.phones]
                    B_day = record.birthday
                    writer.writerow({'Name': name, 'Phones': phones, "Birthday": B_day})
        except:
            return user_contacts

    # чтение контактов 
    def read_csv(self, reader):
        for row in reader:
            try:
                record = Record(Name(row['Name'])) 
                csv_phones = [Phone(phone) for phone in eval(row['Phones'])] if row['Phones'] !='[]' else None
                csv_birthday = Birthday(row['Birthday']) if row['Birthday'] != '' else None

                if len(csv_phones) > 1:
                    record.add_phones(csv_phones)
                elif len(csv_phones) == 1:
                    record.add_phone(next(iter(csv_phones)))
                if csv_birthday:    
                    record.birthday(csv_birthday.value) 
                user_contacts.add_record(record) 
            except (FileNotFoundError, AttributeError, KeyError, TypeError):
                user_contacts
        return user_contacts

    def __iter__(self):
        if len(self) > 0:
            self.keys_list = sorted(self.data.keys())
            return self

    def __next__(self):
        if self.index >=len(self.keys_list):
            raise StopIteration
        else:
            name =self.keys_list[self.index]
            self.index +=1
            return self[name]

    def iterator(self, n=2):
        self.keys_list = sorted(self.data.keys())
        if self.index < len(self.keys_list):
            yield from [self[name] for name in self.keys_list[self.index:self.index+n]]
            self.index +=n
        else:
            self.index = 0
            self.keys_list =[]
# ************************* CLASSES  *************************
user_contacts = AddressBook()
# user_contacts = {}
# запись контактов 
def write_csv(csv_file, user_contacts):
        
        try:
            with open (csv_file, 'w', newline ='') as f:
                fieldnames = ['Name','Phones','Birthday']
                writer = csv.DictWriter(f, fieldnames = fieldnames)
                writer.writeheader()
                for name in user_contacts.data:
                    record = user_contacts.data[name]
                # for record in  user_contacts:
                    name = record.name.value
                    phones = [phone.value for phone in record.phones]
                    B_day = record.birthday
                    writer.writerow({'Name': name, 'Phones': phones, "Birthday": B_day})
        except:
            return user_contacts

# # # чтение контактов 
# def read_csv(csv_file):

#     with open (csv_file, 'a+', newline='') as f:
#         f.seek(0)
#         reader = csv.DictReader(f)
#         user_contacts = {}

#         for row in reader:
#             try:
#                 record = Record(Name(row['Name'])) 
#                 csv_phones = [Phone(phone) for phone in eval(row['Phones'])] if row['Phones'] !='[]' else None
#                 csv_birthday = Birthday(row['Birthday']) if row['Birthday'] != '' else None

#                 if len(csv_phones) > 1:
#                     record.add_phones(csv_phones)
#                 elif len(csv_phones) ==1:
#                     record.add_phone(next(iter(csv_phones)))
#                 if csv_birthday:    
#                     record.birthday(csv_birthday) 
#                 # user_contacts.add_record(record) 
#                 user_contacts[record.name] = record
#             except (FileNotFoundError, AttributeError, KeyError, TypeError):
#                 user_contacts
#     return user_contacts


def user_help ():
   return """
          Phone book commands:
          1. hello
          2. add 'Name' 'phone number" 'birthday' - (Igor +380989709609 28-05-1982) 
          3. change 'Name' 'phone number1' 'phone number1'  - (Igor +380989709609 +380990509393)
          4. phone 'Name'
          5. remove 'Name' 'phone number'  - (Igor +380989709609') 
          6. show all
          7. b_day 'Name' - number of days until birthday Name
          8. good bye, close, exit
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

    return wrapper

# Greetings
@input_error
def user_hello(*args):
    return "How can I help you?"

# Add добавление номера в адресную книгу
@input_error
def user_add(*args, **kwargs):
    user_contacts = kwargs['contacts']
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[2]) if len(args) > 2 else None
    
    try:
        rec:Record = user_contacts.get(name.value)
    except AttributeError:
        rec = None

    if not rec:
        if not birthday:
            birthday = None

        rec = Record(name, phone, birthday)
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
    name = Name(args[0])
    record = user_contacts[name.value]
   
    return f"The phone number for {name} is {record.phones}", user_contacts
    

# Show all  вся адресная книга
@input_error
def user_show_all(*args, **kwargs):
    user_contacts = kwargs['contacts']
    all = ""
    
    if len(user_contacts) == 0:
        return "Phone book is empty", user_contacts
    else:
        for name in user_contacts.data:
           record = user_contacts.data[name]
           #rec = Record(record.name.value, birthday=record.birthday.value)
           rec = Record(record.name.value)
           days_birthday = rec.days_to_birthday(rec.birthday) if rec.birthday != None else None
           print(f"{record.name.value}: {', '.join(str(phone) for phone in record.phones)}. Dirthday {record.birthday.value}. Days birthday - {days_birthday}")
        #  for name, phone in user_contacts.items():
        #     all += f"{name}: {phone}\n"
        # return all
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
    'phone': user_phone, # Телефон
    'show all': user_show_all, # Список контактов
    'remove': remove_phone, # удаление из адресной книги
    'b_bay': birthday_to_days, 
    'good bye': user_exit, # выход
    'close': user_exit,
    'exit': user_exit,
    'help': user_help, # помощь
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
    # user_contacts = AddressBook(read_csv(csv_file))
    # contacts = read_csv(csv_file)
    with open (csv_file, 'r', newline='') as f:
        f.seek(0)
        reader = csv.DictReader(f)
        contacts = user_contacts.read_csv(reader)
    
    while True:
        user_input = input("Enter a command: ")
        command, data = command_handler(user_input)
        result, contacts = command(*data, contacts = contacts)
        print(result)
        if command == user_exit:
            write_csv(csv_file, contacts)
            break

        if not command:
            print("Command is not supported. Try again.")
            continue
        
      


if __name__ == "__main__":

    csv_file = 'user_contacts.csv'
    main(csv_file)
    