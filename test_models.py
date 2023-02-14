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
        self.ticket.set_date("2025/1/1")

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

    def test_admin_card_owner(self):
        self.assertRaises(AssertionError,self.admin.set_card_owner,self.ticket,"new user id")

        self.assertEqual(self.card_credit.get_id(),self.user.get_id())
        new_user = User("mmd","mmd zade",75,"mmdzade1325@yahoo.com")
        self.admin.set_card_owner(self.card_credit,new_user.get_id())
        self.assertEqual(self.card_credit.get_id(),new_user.get_id())

    def test_admin_card_balance(self):
        self.assertRaises(AssertionError,self.admin.set_card_balance,self.ticket,"new user id")

        self.assertRaises(TypeError,self.admin.set_card_balance,self.card_one_way,500)
        self.assertRaises(ValueError,self.admin.set_card_balance,self.card_credit,-5)

        self.admin.set_card_balance(self.card_credit,50000)
        self.assertEqual(self.card_credit.get_balance(),50000)

    def test_admin_card_epire_date(self):
        self.assertRaises(AssertionError,self.admin.set_card_expire_date,self.ticket,"new user id")

        self.assertRaises(TypeError,self.admin.set_card_expire_date,self.card_one_way,"2023/6/6")
        self.assertRaises(TypeError,self.admin.set_card_expire_date,self.card_credit,"2023/6/6")

        self.admin.set_card_expire_date(self.card_term_credit,"2025/1/5")
        self.assertEqual(self.card_term_credit.get_expire_date(),datetime(2025,1,5))

    def test_admin_ticket_origin(self):
        self.assertRaises(AssertionError,self.admin.set_ticket_origin,self.card_credit,"Tehran")

        self.admin.set_ticket_origin(self.ticket,"Anzali")
        self.assertEqual(self.ticket.origin,"Anzali")

    def test_admin_ticket_destination(self):
        self.assertRaises(AssertionError,self.admin.set_ticket_destination,self.card_credit,"Tehran")

        self.admin.set_ticket_destination(self.ticket,"Anzali")
        self.assertEqual(self.ticket.destination,"Anzali")

    def test_admin_ticket_owner(self):
        self.assertRaises(AssertionError,self.admin.set_ticket_owner,self.card_credit,"new user id")

        self.admin.set_ticket_owner(self.ticket,"mmd")
        self.assertEqual(self.ticket.get_id(),"mmd")

    def test_admin_ticket_price(self):
        self.assertRaises(AssertionError,self.admin.set_ticket_price,self.card_credit,50)

        self.admin.set_ticket_price(self.ticket,24)
        self.assertEqual(self.ticket.price,24)

        self.assertRaises(ValueError,self.admin.set_ticket_price,self.ticket,"aa")
        self.assertRaises(ValueError,self.admin.set_ticket_price,self.ticket,-9)

    def test_admin_ticket_date(self):
        self.assertRaises(AssertionError,self.admin.set_ticket_price,self.card_credit,"2024/5/7")

        self.admin.set_ticket_date(self.ticket,"2020/8/4")
        self.assertEqual(self.ticket.date,datetime(2020,8,4))

        self.assertRaises(ValueError,self.admin.set_ticket_date,self.ticket,"2025-10-6")
        self.assertRaises(ValueError,self.admin.set_ticket_date,self.ticket,"yoooo")

if __name__ == "__main__":
    unittest.main()