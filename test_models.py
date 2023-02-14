import unittest
from models import *


class Test(unittest.TestCase):
    def setUp(self):
        self.user = User("houtan","tv",18,"houtantv@gmail.com")
        self.bankaccount = BankAccount(self.user,200000)
        self.card_one_way = Card("One Way",self.user.get_id())
        self.card_credit = Card("Credit",self.user.get_id(),balance=500,bankaccount=self.bankaccount)
        self.card_term_credit = Card("Term Credit",self.user.get_id(),expire_date="2023/6/1",balance=500,bankaccount=self.bankaccount)
        self.ticket = Ticket("Tehran","Anzali","2023/3/16")
        self.admin = SuperUser("houtan","tv",18,"houtantv@gmail.com")

    def test_user_get_id(self):
        self.assertIsInstance(self.user.get_id(),str)
        self.assertEqual(len(self.user.get_id()),36)

    def test_Card_deposit(self):
        self.assertRaises(TypeError,self.card_one_way.deposit,self.bankaccount,56)
        self.assertRaises(ValueError,self.card_credit.deposit,self.bankaccount,-5)
        self.assertRaises(ValueError,self.card_term_credit.deposit,self.bankaccount,-5)
        self.assertRaises(TypeError,self.card_credit.deposit,self.bankaccount,"a")
        self.card_term_credit.set_expire_date("2022/1/1")
        self.assertRaises(AssertionError,self.card_term_credit.deposit,self.bankaccount,20)
        self.assertRaises(BankAccount.MinBalanceError,self.card_credit.deposit,self.bankaccount,2000000000)
        self.assertRaises(AssertionError,self.card_credit.deposit,self.ticket,250)

    def test_card_withdraw(self):
        self.assertRaises(ValueError,self.card_credit.withdraw,-5)
        self.assertRaises(AssertionError,self.card_credit.withdraw,5000000)
        self.card_term_credit.set_expire_date("2022/1/1")
        self.assertRaises(AssertionError,self.card_term_credit.withdraw,10)
        self.assertRaises(TypeError,self.card_credit.withdraw,self.bankaccount,"a")

    def test_ticket_buy(self):
        self.ticket.buy_ticket(self.user.get_id(),self.card_one_way)
        self.assertRaises(AssertionError,self.ticket.buy_ticket,self.user.get_id(),self.card_one_way)
        self.card_term_credit.set_expire_date("2023/1/1")
        self.assertRaises(AssertionError,self.ticket.buy_ticket,self.user.get_id(),self.card_term_credit)
        self.card_credit.set_id("mamad")
        self.assertRaises(AssertionError,self.ticket.buy_ticket,self.test_user_get_id(),self.card_credit) #validation
        self.assertRaises(AssertionError,self.ticket.buy_ticket,self.user.get_id(),self.bankaccount)



if __name__ == "__main__":
    unittest.main()