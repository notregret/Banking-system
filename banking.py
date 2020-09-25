# Write your code here
from random import *
from luhn import *
import sqlite3


class Bank_Sys:

    def initializedb(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS card(\n'
                         '        id INTEGER NULL PRIMARY KEY AUTOINCREMENT,\n'
                         '        number TEXT NOT NULL UNIQUE,\n'
                         '        pin TEXT,\n'
                         '        balance INTEGER DEFAULT 0\n'
                         '        );')
        self.conn.commit()

    def __init__(self):
        self.balance = int()
        self.initializedb()
        self.do_it()

    def Balance(self):
        self.cur.execute(f'SELECT number FROM card WHERE number = "{self.enter_number}"')
        if self.cur.fetchone() is None:
            print('a zapisi to net')
        else:
            for value in self.cur.execute(f'SELECT balance FROM card WHERE number = "{self.enter_number}"'):
                print(value[0])


    def add(self):
        balance = int(input('How much?\n'))
        self.cur.execute(f'SELECT number FROM card WHERE number = "{self.enter_number}"')
        if self.cur.fetchone() is None:
            print('a zapisi to net')
        else:
            self.cur.execute(f'UPDATE card SET balance = {balance} WHERE number ="{self.enter_number}"')
            self.conn.commit()

    def do_it(self) -> None:
        while True:
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
            choice: str = input()
            if choice == '1':
                self.create()
            elif choice == '2':
                self.verification()
            elif choice == '0':
                print('Bye!')
                quit()

    def verification(self) -> None:
        self.enter_number: str = input("Enter your card number:")
        enter_pin: str = input("Enter your PIN:")
        self.cur.execute(f"SELECT number FROM card WHERE number = '{self.enter_number}'")
        if self.cur.fetchone() is None:
            print("Wrong number")
        else:
            self.cur.execute(f"SELECT pin FROM card WHERE pin = '{enter_pin}'")
            if self.cur.fetchone() is None:
                print("Wrong pin")
            else:
                print("You have successfully logged in!")
                self.menu()

    def transfer(self):
        transfer_number: str = input('Enter number\n')
        if self.enter_number == transfer_number:
            print('You cant transfer money to the same account')
        else:
            if verify(transfer_number) is True:
                self.cur.execute(f'SELECT number FROM card WHERE number ="{transfer_number}"')
                if self.cur.fetchone() is None:
                    print('Such a card does not exist.')
                else:
                    transfer_money = str(input('How much u want transf\n'))
                    if int(transfer_money) < self.balance:
                        print('u have not enough money')
                    else:
                        print('All is ok')
                        self.cur.execute('UPDATE card SET balance = (balance + ?) WHERE number LIKE (?)', (transfer_money, transfer_number))
                        self.conn.commit()
                        self.cur.execute('UPDATE card SET balance = (balance - ?) WHERE number LIKE (?)', (transfer_money, self.enter_number))
                        self.conn.commit()
            else:
                print('Wrong number')
                self.transfer()

    def close(self):
        self.cur.execute(f"DELETE FROM card where number ='{self.enter_number}'")
        self.conn.commit()
        print('Your acc was deleted')
        self.do_it()

    def menu(self) -> None:
        while True:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
            v2choice: str = input()
            if v2choice == '1':
                self.Balance()
            elif v2choice == '2':
                self.add()
            elif v2choice == '3':
                self.transfer()
            elif v2choice == '4':
                self.close()
            elif v2choice == '5':
                self.do_it()
            elif v2choice == '0':
                print('Bye')
                quit()

    def create(self) -> None:
        self.pin = randrange(1000, 9999)
        self.number = str(append('400000' + ''.join([str(p) for p in sample(range(9), 9)])))
        self.cur.execute(f"INSERT OR IGNORE INTO card(id, number, pin) VALUES (?, ?, ?)", (None, self.number, self.pin))
        self.conn.commit()
        print('Your card has been created')
        print(f'Your card number:\n{self.number}')
        print(f'Your card PIN:\n{self.pin}')

Bank_Sys()
