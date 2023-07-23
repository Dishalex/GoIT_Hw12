from ab_classes import AddressBook, Name, Phone, Record, Birthday, BirthdayError, PhoneError, Name_Error
address_book = AddressBook()

def input_error(func):
    def wrapper(*args):
        try:
            return func(args)
        except PhoneError:
            return "Phone number must be in the format +380XXXXXXXXX"
        except Name_Error:
            return "Name must be not less then 3 symbols"
        except BirthdayError:
            return "Birthday must be in format dd-mm-yyyy"
        except IndexError:   
            if func.__name__ == 'add_command':
                return 'Please specify contact name and phone after command'
            elif func.__name__ == 'change_command':
                return 'Please specify contact name, old phone and new phone after command'
            elif func.__name__ == 'delete_phone_command':
                return 'Please specify contact name and phone after command'
            elif func.__name__ == 'show_command':
                return 'Please specify contact name after command'
            return 'Please try again'
        except Exception as err:
            return err
    return wrapper


@input_error
def add_command(args: tuple[str]) -> str:
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    try:
        args[2]
        try:
            b_day = Birthday(args[2])
            rec = Record(name, phone, b_day)
            return address_book.add_record(rec)
        except Exception as err:
            return err
    except Exception:
        pass
    rec = Record(name, phone)
        
    return address_book.add_record(rec)

@input_error
def change_command(args: tuple[str]) -> str:
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        old_p = Phone(args[1])
        new_p = Phone(args[2])
        return rec.change_phone(old_p, new_p)
    return f'No contact with name "{name}" in address book'

@input_error
def delete_phone_command(args: tuple[str]) -> str:
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        phone_to_delete = Phone(args[1])
        return rec.del_phone(phone_to_delete)
    return f'No contact with name "{name}" in address book'

@input_error
def show_command(args: tuple[str]) -> str:
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec
    else:
        return f'No contact with name "{name}" in address book'

@input_error
def show_all_command(*args) -> str:
    try:
        n = 0
        k = int(args[0])
        for rec in address_book.iterator(k):
            print(f'Рage {n}')
            print(rec)
            n += 1
        return 'End of records'
    except Exception:
        pass  
    return address_book

def no_command():
    return 'Unknown command'


def exit_command():
    return 'Good bye!'


def hello_command() -> str:
    return 'How can I help you?'


COMMANDS = {
    add_command: ('add', '+', 'додати'),
    delete_phone_command: ('delete', '-', 'видалити', 'del'),
    change_command: ('change', 'змінити'),
    exit_command: ('close', 'exit', 'вийти' 'закрити', 'bye'),
    hello_command: ('hello', 'привіт'),
    show_command: ('phone', 'show', 'contact', 'телефон', 'контакт'),
    show_all_command: ('show_all', 'all', 'всі', 'книга')
    }
        
def parser(text: str) -> tuple[callable, list[str]]:
    command, *data = text.strip().split() 
    for cmd, kwds in COMMANDS.items():
        if command.lower() in kwds: #спробував відмовитися від .startswith(), оскільки цей метод не достатньо специфічний.
                                    #як наслідок не спиймаються команди довше ніж 1 слово
            return cmd, data
    return no_command, []


def main():
    print("I am at your service, my lord!")
    while True:
        user_input = input('>>> ')
        command, data = parser(user_input)
        result = command(*data)
        print(result)
        if command == exit_command:
            break


if __name__ == "__main__":
    main()
