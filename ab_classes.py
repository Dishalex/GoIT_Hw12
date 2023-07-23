from collections import UserDict
from datetime import datetime, date
import re


class PhoneError(Exception):
    pass


class BirthdayError(Exception):
    pass


class Name_Error(Exception):
    pass


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not re.match(r'^\+38\d{10}$', value):
            raise PhoneError()
        self.__value = value


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) < 3:
            raise Name_Error("Name must be not less then 3 symbols")
        self.__value = value


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise BirthdayError()

    def __repr__(self):
        return self.__value

    def __str__(self):
        if self.__value:
            return self.__value.strftime("%d-%m-%Y")
        else:
            return ''


class Record():
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f'Contact {self.name} was updated with phone {phone}.'
        return f'Phone "{phone}" is already belong to contact with name "{self.name}".'

    def change_phone(self, old_p: Phone, new_p: Phone):
        for indx, p in enumerate(self.phones):
            if old_p.value == p.value:
                self.phones[indx] = new_p
                return f'Contacts "{self.name}" phone "{old_p}" changed to "{new_p}".'
        return f'Contact "{self.name}" has no phone "{old_p}" to change.'

    def del_phone(self, phone_to_remove: Phone):
        for indx, p in enumerate(self.phones):
            if phone_to_remove.value == p.value:
                del self.phones[indx]
                return f'Contacts "{self.name}" phone "{phone_to_remove}" was removed".'
        return f'Contact "{self.name}" has no phone "{phone_to_remove}" to remove.'

    def get_day_to_bd(self):
        if not self.birthday:
            return ''
        b_date = self.birthday.__repr__().date()
        t_date = date.today()
        b_day = date(year=t_date.year, month=b_date.month, day=b_date.day)
        if b_day < t_date:
            b_day = b_day.replace(year=t_date.year+1)
        return ', ' + str((b_day-t_date).days) + ' days to bday'

    def __str__(self) -> str:
        if self.birthday:
            return f"{self.name}: {', '.join(str(p) for p in self.phones)}{self.get_day_to_bd()}"
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        if record.birthday:
            return f"Contact {record.name} {', '.join(str(p) for p in record.phones)} with birthday {record.birthday} was added"
        else:
            return f"Contact {record} was added"

    def iterator(self, n=3):
        result = []
        count = 0
        for i in self.values():
            result.append(str(i))
            count += 1
            if count >= n:
                yield '\n'.join(result)
                count = 0
                result = []
        if result:
            yield '\n'.join(result)

    def __str__(self) -> str:
        if self.data:
            return '\n'.join(str(r) for r in self.values()) + '\n' + '...the end of phone book.'
        return 'Address book is empty'
