from collections import UserDict

class Field:
    """
    Базовий клас для полів запису.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Клас для зберігання імені контакту. Обов'язкове поле.
    """
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    """
    Клас для зберігання номера телефону з валідацією.
    """
    def __init__(self, value):
        if not self._validate_phone(value):
            raise ValueError("Phone number must have exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def _validate_phone(value):
        return value.isdigit() and len(value) == 10


class Record:
    """
    Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """
        Додає телефон до списку телефонів запису.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Видаляє телефон зі списку телефонів запису.
        """
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        """
        Редагує існуючий телефон у записі.
        """
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            self.phones.remove(phone_to_edit)
            self.add_phone(new_phone)

    def find_phone(self, phone):
        """
        Пошук телефону у списку телефонів запису.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    """
    Клас для зберігання та управління записами адресної книги.
    """
    def add_record(self, record):
        """
        Додає запис до книги.
        """
        self.data[record.name.value] = record

    def find(self, name):
        """
        Знаходить запис у книзі за ім'ям.
        """
        return self.data.get(name)

    def delete(self, name):
        """
        Видаляє запис з книги за ім'ям.
        """
        if name in self.data:
            del self.data[name]


# Приклад використання
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print("Jane deleted.")

    # Перевірка після видалення
    for name, record in book.data.items():
        print(record)
