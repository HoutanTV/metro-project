import uuid
from datetime import datetime,timedelta
import random
import os
import pickle

class User:
    def __init__(self, first_name, last_name, age : int, email):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self._id = str(uuid.uuid4())
        print("Save your id but don't show it to anyone:",self._id)

    def get_id(self):
        return self._id


class BankAccount:
    WAGE_AMOUNT = 0  # کارمزد
    MIN_BALANCE = 10000  # حداقل موجودی

    class MinBalanceError(Exception):
        pass

    def __init__(self, owner: User, initial_balance: int = 0) -> None:
        self.__owner = owner  # صاحب حساب
        self.__balance = initial_balance  # موجودی حساب

    def __check_minimum_balance(self, amount_to_withdraw):  # چک کردن حداقل موجودی
        return (self.__balance - amount_to_withdraw) >= self.MIN_BALANCE

    def set_owner(self, owner):  # تغییر صاحب حساب
        self.__owner = owner

    def get_owner(self):  # مشاهده صاحب حساب
        return self.__owner

    def withdraw(self, amount):  # برداشت وجه
        if not self.__check_minimum_balance(amount):
            raise BankAccount.MinBalanceError("NOT Enough balance to withdraw!")
        self.__balance -= amount
        self.__balance -= self.WAGE_AMOUNT   # برداشت کارمزد

    def deposit(self, amount):  # واریز وجه
        self.__balance += amount

    def get_balance(self):  # مشاهده موجودی
        self.__balance -= self.WAGE_AMOUNT   # برداشت کارمزد
        return self.__balance

    def transfer(self, target_account, amount: int):  # انتقال وجه
        self.withdraw(amount)  # برداشت از حساب خود
        target_account.deposit(amount)  # واریز به حساب مقصد

    @classmethod
    def change_wage(cls, new_amount):
        cls.WAGE_AMOUNT = max(new_amount, 0)   # حداقل مقدار برابر صفر است

    @classmethod
    def change_min_balance(cls, new_amount):  # حداقل مقدار برابر صفر است
        cls.MIN_BALANCE = max(new_amount, 0)


class Card:
    def __init__(self,type,user_id,expire_date=datetime.now(),balance=0, bankaccount=""):

        self.type = type
        if self.type not in ["One Way","Credit","Term Credit"]:
            raise ValueError

        if self.type == "One Way":
            self._owner = user_id
            self.used = False
        elif self.type == "Credit":
            assert isinstance(bankaccount,BankAccount),"enter a valid bank account"
            if balance < 0:
                raise ValueError
            bankaccount.withdraw(balance)
            self._owner = user_id
            self._balance = balance
        elif self.type == "Term Credit":
            assert isinstance(bankaccount, BankAccount),"enter a valid bank account"
            bankaccount.withdraw(balance)
            self._owner = user_id
            self._balance = balance
            date_expire = datetime.strptime(expire_date, "%Y/%m/%d")
            self._expire_date = date_expire
        self.id = str(uuid.uuid4())
        print("Save your id but don't show it to anyone:",self.id)


    def deposit(self, bank_account:BankAccount, amount:float):
        assert isinstance(bank_account,BankAccount),"enter a valid bank account"
        if amount < 0:
            raise ValueError

        if self.type == "One Way":
            raise TypeError

        elif self.type == "Credit":
            bank_account.withdraw(amount)
            self._balance += amount
            return self._balance

        elif self.type == "Term Credit":
            assert self._expire_date >= datetime.now() ,"your card is expired"
            bank_account.withdraw(amount)
            self._balance += amount
            return self._balance

    def withdraw(self,amount:float):
        if self.type == "Term Credit":
            assert self._expire_date > datetime.now(),"card is expired"

        if amount < 0:
            raise ValueError

        assert self._balance - amount >= 0,"Not enough balance"
        self._balance -= amount
        return self._balance

    def use_card(self):
        self.used = True

    def get_id(self):
        return self._owner

    def set_id(self,new_owner):
        self._owner = new_owner

    def get_balance(self):
        return self._balance

    def set_balance(self,new_balance):
        self._balance = new_balance

    def set_expire_date(self,new_date):
        end_date = datetime.strptime(new_date, "%Y/%m/%d")
        self._expire_date = end_date

    def get_expire_date(self):
        return self._expire_date

    def __str__(self):
        if self.type == "One Way":
            return f"Type:{self.type}\nHolder:{self._owner}\nCard Id:{self.id}"
        elif self.type == "Credit":
            return f"Type:{self.type}\nHolder:{self._owner}\nBalance:{self._balance}\nCard Id:{self.id}"
        elif self.type == "Term Credit":
            return f"Type:{self.type}\nHolder:{self._owner}\nBalance:{self._balance}\nExpire Date:{self._expire_date}\nCard Id:{self.id}"


class Ticket:
    def __init__(self,origin,destination,date):
        self.origin = origin
        self.destination = destination
        self._owner = "Metro"
        self.price = random.randint(5,10)
        # generates a random date between now and given date
        self._set_date(date)
        self.id = str(uuid.uuid4())

    def _set_date(self,date):
        start_date = datetime.now()
        end_date = datetime.strptime(date, "%Y/%m/%d")

        num_days = (end_date - start_date).days
        rand_days = random.randint(0, num_days+1)
        random_date = start_date + timedelta(days=rand_days)
        self.date = random_date

    def buy_ticket(self, user_id, card):
        assert self.date > datetime.now(),"ticket is out of date"
        assert isinstance(card,Card)
        if card.type == "One Way":
            if not card.used:
                card.use_card()
                self._owner = user_id
                return self._owner
            else:
                raise AssertionError
        else:
            assert card.get_id() == user_id,"user id and card owner doesn't match"
            card.withdraw(self.price)
            self._owner = user_id
            return self._owner

    def get_id(self):
        return self._owner

    def set_origin(self,new_origin):
        self.origin = new_origin

    def set_destination(self,new_destination):
        self.destination = new_destination

    def set_owner(self,new_owner):
        self._owner = new_owner

    def set_price(self,new_price):
        if new_price < 0 :
            raise ValueError
        self.price = new_price

    def set_date(self,date):
        new_date = datetime.strptime(date, "%Y/%m/%d")
        self.date = new_date

    @staticmethod
    def show_tickets():
        temp_dict = {}
        if os.path.exists("./tickets.pickle"):
            with open("tickets.pickle", "rb") as u:
                temp_dict = pickle.load(u)

            print("Available tickets:")
            for ticket_id in temp_dict:
                if temp_dict[ticket_id].date > datetime.now():
                    print(ticket_id,temp_dict[ticket_id])

        else:
            print("no ticket exists")

    def __str__(self):
        return f"Origin:{self.origin}\nDestination:{self.destination}\nOwner:{self._owner}\nPrice:{self.price}\nDate:{self.date}"


class SuperUser(User):

    def __init__(self, first_name, last_name, age: int, email):
        super().__init__(first_name, last_name, age, email)

    @staticmethod
    def set_card_owner(card,new_owner):
        assert isinstance(card,Card),"enter a valid card"
        card.set_id(new_owner)

    @staticmethod
    def set_card_balance(card,new_balance:float):
        assert isinstance(card,Card),"enter a valid card"
        if card.type in ["Credit","Term Credit"]:
            if new_balance < 0:
                raise ValueError
            card.set_balance(new_balance)
        else:
            raise TypeError

    @staticmethod
    def set_card_expire_date(card,new_date):
        assert isinstance(card, Card), "enter a valid card"
        if card.type == "Term Credit":
            card.set_expire_date(new_date)
        else:
            raise TypeError

    @staticmethod
    def set_ticket_origin(ticket,new_origin):
        assert isinstance(ticket,Ticket),"please enter a valid ticket"
        ticket.set_origin(new_origin)

    @staticmethod
    def set_ticket_destination(ticket,new_destination):
        assert isinstance(ticket,Ticket),"please enter a valid ticket"
        ticket.set_destination(new_destination)

    @staticmethod
    def set_ticket_owner(ticket,user_id):
        assert isinstance(ticket,Ticket),"please enter a valid ticket"
        ticket.set_owner(user_id)

    @staticmethod
    def set_ticket_price(ticket,price: float):
        assert isinstance(ticket,Ticket),"please enter a valid ticket"
        price = float(price)
        ticket.set_price(price)

    @staticmethod
    def set_ticket_date(ticket,new_date):
        assert isinstance(ticket, Ticket), "please enter a valid ticket"
        ticket.set_date(new_date)

def update_database(item,user=""):
    temp_dict = {}

    if isinstance(item, SuperUser):
        if os.path.exists("./admins.pickle"):
            with open("admins.pickle", "rb") as u:
                temp_dict = pickle.load(u)

            with open("admins.pickle", "wb") as u:
                temp_dict[item.get_id()] = item
                pickle.dump(temp_dict, u)

        else:
            with open("admins.pickle", "wb") as u:
                temp_dict[item.get_id()] = item
                pickle.dump(temp_dict, u)

    elif isinstance(item, User):
        if os.path.exists("./users.pickle"):
            with open("users.pickle", "rb") as u:
                temp_dict = pickle.load(u)

            with open("users.pickle", "wb") as u:
                temp_dict[item.get_id()] = item
                pickle.dump(temp_dict, u)
        else:
            with open("users.pickle", "wb") as u:
                temp_dict[item.get_id()] = item
                pickle.dump(temp_dict, u)

    elif isinstance(item, BankAccount):
        if os.path.exists("./bankaccount.pickle"):
            with open("bankaccount.pickle", "rb") as u:
                temp_dict = pickle.load(u)

            with open("bankaccount.pickle", "wb") as u:
                temp_dict[user.get_id()] = item
                pickle.dump(temp_dict, u)
        else:
            with open("bankaccount.pickle", "wb") as u:
                temp_dict[user.get_id()] = item
                pickle.dump(temp_dict, u)

    elif isinstance(item, Card):
        if os.path.exists("./cards.pickle"):
            with open("cards.pickle", "rb") as u:
                temp_dict = pickle.load(u)

            with open("cards.pickle", "wb") as u:
                temp_dict[item.id] = item
                pickle.dump(temp_dict, u)

        else:
            with open("cards.pickle", "wb") as u:
                temp_dict[item.id] = item
                pickle.dump(temp_dict, u)

    elif isinstance(item, Ticket):
        if os.path.exists("./tickets.pickle"):
            with open("tickets.pickle", "rb") as u:
                temp_dict = pickle.load(u)

            with open("tickets.pickle", "wb") as u:
                temp_dict[item.id] = item
                pickle.dump(temp_dict, u)

        else:
            with open("tickets.pickle", "wb") as u:
                temp_dict[item.id] = item
                pickle.dump(temp_dict, u)
    else:
        print("incorrect item to be updated")
