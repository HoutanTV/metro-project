import uuid
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, phone, email) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self._id = str(uuid.uuid4())

    def get_id(self):
        return self._id


class BankAccount:
    WAGE_AMOUNT = 600  # کارمزد
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
    def __init__(self,type,user_id,expire_date=datetime.now(),balance=0):

        self.type = type
        if self.type == "One Way":
            self.owner = user_id
        elif self.type == "Credit":
            self.owner = user_id
            self.balance = balance
        elif self.type == "Term Credit":
            self.owner = user_id
            self.balance = balance
            self.expire_date = expire_date

    def add_balance(self,bank_account:BankAccount,amount:int):
        assert isinstance(bank_account,BankAccount)
        assert isinstance(amount,int)

        if self.type == "One Way":
            return TypeError

        elif self.type == "Credit":
            bank_account.withdraw(amount)
            self.balance += amount
            return self.balance

        elif self.type == "Term Credit":
            assert self.expire_date >= datetime.now() ,"your card is expired"
            bank_account.withdraw(amount)
            self.balance += amount
            return self.balance

    def withdraw(self,amount:int):
        assert isinstance(amount,int)
        assert self.balance - amount >= 0,"Not enough balance"
        self.balance -= amount
        return self.balance