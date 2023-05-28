from getpass import getpass
from random import SystemRandom

import bcrypt
from consolemenu.console_menu import ConsoleMenu
from consolemenu.items import FunctionItem
from sqlitedict import SqliteDict

db_file = 'passwords.sqlite3'
encoding = 'utf-8'
random = SystemRandom()


class Passwords:
    def __init__(self):
        try:
            self.db = SqliteDict(db_file, autocommit=True)
        except Exception as e:
            print('Error:', e)

    def add_password(self, pw_hint, pw_hash):
        self.db[pw_hint] = pw_hash

    def password_exists(self, pw_hint):
        return self.db.get(pw_hint) is not None

    def delete_password(self, pw_hint):
        del self.db[pw_hint]

    def get_passwords(self):
        return list(self.db.keys())

    def get_count(self):
        return len(self.get_passwords())

    def check_password(self, pw_hint, password):
        return bcrypt.checkpw(password, self.db.get(pw_hint))


passwords = Passwords()


def print_title(s):
    border = "=" * (len(s) + 2)
    print(border)
    print(" " + s)
    print(border)


def action_add_password():
    print_title("Add or change password")
    pw_hint = input("Password hint: ")
    if pw_hint.strip() == '':
        print("Bad input")
        print("")
        input()
        return
    if passwords.password_exists(pw_hint) and input(
            'Password with hint "{}" already exists. Change password? (y/N) '.format(pw_hint)) != 'y':
        return
    pw_hash = bcrypt.hashpw(getpass().encode(encoding), bcrypt.gensalt())
    passwords.add_password(pw_hint, pw_hash)


def list_passwords():
    print_title("Passwords (hints)")
    for pw_hint in passwords.get_passwords():
        print(pw_hint)


def action_list_passwords():
    list_passwords()
    print("")
    input()


def action_delete_password():
    list_passwords()
    print("")
    pw_hint = input('Which password would you like to delete? (Enter password hint) ')
    if not passwords.password_exists(pw_hint):
        print("Password doesn't exist")
        print("")
        input()
        return
    passwords.delete_password(pw_hint)


def quiz_password(pw_hint):
    print("Hint: {}".format(pw_hint))
    correct = False
    password = None
    while not correct:
        password = getpass("Password (leave empty to give up): ")
        if password != '' and not passwords.check_password(pw_hint, password.encode(encoding)):
            print("Incorrect, please try again")
        else:
            correct = True
    if password != '':
        print('Correct!')


def action_quiz_passwords():
    if passwords.get_count() == 0:
        print("No passwords")
        input()
    shuffled_passwords = passwords.get_passwords()
    random.shuffle(shuffled_passwords)
    for pw_hint in shuffled_passwords:
        print("")
        quiz_password(pw_hint)
    print("")
    print("Quiz complete!")
    input()


def show_menu():
    menu = ConsoleMenu("Password Quiz")
    menu.append_item(FunctionItem("Start quiz", action_quiz_passwords))
    menu.append_item(FunctionItem("List passwords", action_list_passwords))
    menu.append_item(FunctionItem("Add or change password", action_add_password))
    menu.append_item(FunctionItem("Delete password", action_delete_password))
    menu.show()


if __name__ == '__main__':
    show_menu()
