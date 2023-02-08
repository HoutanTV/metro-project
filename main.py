from models import *

while True:
    os.system('cls')

    print("Welcome to the metro!!")

    print('''
1.Enter as a user
2.Enter as an admin
3.Exit
    ''')
    menu_input = input(">> ")

    if menu_input == "1":
        os.system('cls')
        while True:

            print('''
1.login
2.register
3.Exit
            ''')
            user_input = input(">> ")
            if user_input == "1":
                os.system("cls")
                email = input("please enter your email: ")
                user_id = input("please enter your id: ")
                users_dict = {}
                try:
                    with open("users.pickle","rb") as u:
                        users_dict = pickle.load(u)
                    if user_id in users_dict:
                        if users_dict[user_id].email == email:
                            print("login successful")
                            input("press enter to continue")
                            temp_user = users_dict[user_id]
                            temp_bank = ""
                            while True:
                                os.system("cls")
                                print('''
1.Enter your bank account
2.Card
3.Ticket gate
4.Exit
''')
                                login_input = input(">>")
                                if login_input == "1":
                                    os.system("cls")
                                    print('''
1.login to see your balance
2.register
Or press enter to go back
                                                ''')
                                    bankacc_input = input(">>")
                                    if bankacc_input == "1":
                                        os.system("cls")
                                        if os.path.exists("./bankaccount.pickle"):
                                            with open("bankaccount.pickle","rb") as u:
                                                bank_dict = pickle.load(u)
                                            if temp_user.get_id() in bank_dict:
                                                temp_bank = bank_dict[temp_user.get_id()]
                                                print(f"your balance is {temp_bank.get_balance()}")
                                                input("press enter to continue")
                                            else:
                                                print("you don't have a bank account")
                                                input("press enter to continue")
                                        else:
                                            print("there is no bank account")
                                    elif bankacc_input == "2":
                                        os.system("cls")
                                        try:
                                            bank_balance = int(input("please enter your balance carefully "
                                                                 "you can't change it further: "))
                                            if bank_balance < 0:
                                                raise ValueError
                                            validation = input("please enter your id for validation: ")
                                            if validation == user_id:
                                                if os.path.exists("./bankaccount.pickle"):
                                                    with open("bankaccount.pickle","rb") as u:
                                                        bank_dict = pickle.load(u)
                                                    if temp_user.get_id() not in bank_dict:
                                                        bankacc = BankAccount(temp_user,bank_balance)
                                                        update_database(bankacc,temp_user)
                                                        print("bank account created now you can login to it!")
                                                        input("press enter to continue")
                                                    else:
                                                        print("your bank account exists")
                                                        input("press enter to continue")
                                                else:
                                                    bankacc = BankAccount(temp_user, bank_balance)
                                                    update_database(bankacc,temp_user)
                                                    print("bank account created now you can login to it!")
                                                    input("press enter to continue")
                                            else:
                                                print("validation failed")
                                                input("press enter to continue")
                                        except ValueError:
                                            print("wrong inputs!!")
                                            input("press enter to continue")

                                elif login_input == "2":
                                    print('''
1.buy a card
2.your available cards
                                    
                                    ''')
                                    card_input = input(">>")
                                    if card_input == "1":
                                        print('''
please enter which type of card do you want
1.One Way
2.Credit
3.Term Credit
''')
                                        card_type = input(">>")
                                        if card_type == "1":
                                            print("The price of an one way card is 6$\nYes or no")
                                            answer = input(">>").lower()
                                            if answer == "yes":
                                                if temp_bank == "":
                                                    print("please login to your bank account first")
                                                    input("press enter to continue")
                                                else:
                                                    try:
                                                        temp_bank.withdraw(6)
                                                        update_database(temp_bank,temp_user)
                                                        bought_card = Card("One Way",temp_user.get_id())
                                                        update_database(bought_card)
                                                        print("card successfuly bought")
                                                        input("press enter to continue")
                                                        break

                                                    except BankAccount.MinBalanceError:
                                                        print("not enough balance")

                                            elif answer == "no":
                                                pass
                                            else:
                                                print("you should say yes or no")
                                        # elif card_type == "2":
                                        #     cc_balance = input("please enter your balance")
                                        #     cc = Card("Credit",temp_user.get_id(),balance=cc_balance,bankaccount=temp_bank)
                                                pass
                                        elif card_type == "2":
                                            if temp_bank == "":
                                                print("please login to your bank account first")
                                                input("press enter to continue")
                                            else:
                                                try:
                                                    cc_balance = int(input("please enter the balance of your card"))
                                                    if cc_balance < 0 :
                                                        raise ValueError
                                                    new_cc = Card("Credit",temp_user.get_id(),
                                                                  balance=cc_balance,bankaccount=temp_bank)
                                                    update_database(new_cc)
                                                    update_database(temp_bank,temp_user)
                                                    print("card successfuly bought")
                                                    input("press enter to continue")
                                                    break
                                                except BankAccount.MinBalanceError:
                                                    print("not enough balance")
                                                    input("press enter to continue")

                                                except ValueError:
                                                    print("wrong input")
                                                    input("press enter to continue")

                                        elif card_type == "3":
                                            if temp_bank == "":
                                                print("please login to your bank account first")
                                                input("press enter to continue")
                                            else:
                                                try:
                                                    cc_balance = int(input("please enter the balance of your card"))
                                                    if cc_balance < 0 :
                                                        raise ValueError
                                                    expire_date = input("please enter the expire date in this format "
                                                                        "YYYY/MM/DD: ")
                                                    new_cc = Card("Credit",temp_user.get_id(),
                                                                  balance=cc_balance,bankaccount=temp_bank,
                                                                  expire_date=expire_date)
                                                    update_database(new_cc)
                                                    update_database(temp_bank,temp_user)
                                                    print("card successfuly bought")
                                                    input("press enter to continue")
                                                    break
                                                except BankAccount.MinBalanceError:
                                                    print("not enough balance")
                                                    input("press enter to continue")

                                                except ValueError:
                                                    print("wrong input")
                                                    input("press enter to continue")

                                    elif card_input == "2":
                                       if os.path.exists("./cards.pickle"):
                                            with open("cards.pickle","rb") as u:
                                                cards_dict = pickle.load(u)
                                            for card in cards_dict:
                                                if cards_dict[card].get_id() == temp_user.get_id():
                                                    print(cards_dict[card])
                                                    input("press enter to continue")
                                       else:
                                           print("there is no card to show")
                                           input("press enter to continue")



                                elif login_input == "3":
                                    print('''
1.buy ticket
2.see your tickets                                    
                                    
                                    ''')
                                    ticket_input = input(">>")
                                    if ticket_input == "1":
                                        pass
                                    elif ticket_input == "2":
                                        pass

                                elif login_input == "4":
                                    break
                        else:
                            print("validation failed")
                    if user_id not in users_dict:
                        print("user not found")
                        input("press enter to continue")
                except FileNotFoundError:
                    print("no user have been created so far")
                    input("press enter to continue")

            elif user_input == "2":
                os.system("cls")
                try:
                    fname = input("please enter your first name: ")
                    if not fname.isalpha():
                        raise ValueError
                    lname = input("please enter your last name: ")
                    if not lname.isalpha():
                        raise ValueError
                    age = int(input("please enter your age: "))
                    email = input("please enter email: ")

                    new_user = User(fname,lname,age,email)
                    update_database(new_user)

                    print("user created now you can login to your account")
                    input("press enter to continue")
                except ValueError:
                    print("incorrect input")
                    input("press enter to continue")

            elif user_input == "3":
                break

    elif menu_input == "2":
        os.system('cls')
        while True:

            print('''
1.login
2.register
3.Exit
                    ''')
            admin_input = input(">>")
            if admin_input == "1":
                pass
            elif admin_input == "2":
                pass
            elif admin_input == "3":
                break

    elif menu_input == "3":
        break