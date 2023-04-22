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
        # return self.__value.strftime('%d-%m-%Y')
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            raise ValueError('Wrong DATE format. Please enter the DATE in the format - dd-mm-yyyy')    
    
    def __str__(self) -> str:
        return str(self.value.strftime('%d-%m-%Y'))

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
            dateB = self.birthday.value
            today = datetime.today()
            # current_year_dateB = datetime.date(today.year, dateB.month, dateB.day)
            current_year_dateB = dateB.replace(year=today.year)

            if current_year_dateB < today:
                current_year_dateB = datetime.date(today.year+1, dateB.month, dateB.day)

            delta =current_year_dateB - today    
            return delta.days
        
        return None
    
    def __str__(self):
        
        result = ''
        phones = ", ".join([str(phone) for phone in self.phones])
                
        if self.birthday:
            # date_bd = self.birthday.strftime("%m/%d/%Y, %H:%M:%S")
            result += f"{self.name}: {phones}. Birthday: {self.birthday}\n"
        else:
            result += f"{self.name}: {phones}"
        return result
   
class AddressBook(UserDict):
    index = 0
    
    fieldnames = ['Name','Phones','Birthday']
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def save_csv(self, csv_file):
        
        try:
            with open (csv_file, 'w', newline ='') as f:
                writer = csv.DictWriter(f, fieldnames = self.fieldnames)
                writer.writeheader()
                for name in self.data:
                    record = self.data[name]
                # for record in  user_contacts:
                    name = record.name.value
                    phones = [phone.value for phone in record.phones]
                    B_day = record.birthday
                    writer.writerow({'Name': name, 'Phones': phones, "Birthday": B_day})
        except:
            return ...

    
    def read_csv(self, csv_file):
        try:
            with  open (csv_file, 'r', newline ='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                
                    csv_name = Name(row['Name'])
                    # csv_phones = [Phone(phone) for phone in eval(row['Phones'])] if row['Phones'] !='[]' else None
                    # csv_birthday = Birthday(row['Birthday']) if row['Birthday'] != '' else None
                    csv_phones = [Phone(phone) for phone in eval(row['Phones'])] if row['Phones'] else None
                    csv_birthday = Birthday(row['Birthday']) if row['Birthday'] else None

                    rec = Record(csv_name, birthday=csv_birthday)
                    for phone in csv_phones:
                        rec.add_phone(phone)
                    
                    self.add_record(rec)
                
        except (FileNotFoundError, AttributeError, KeyError, TypeError):
            pass
        
    def search(self, param):
        if len(param) < 3:
            return 
        
        result = []
        
        for rec in self.data.values():
            if param in str (rec):
                result.append(str(rec))  

        str_result = '\n'.join(result)    
        return f"{str_result}"

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