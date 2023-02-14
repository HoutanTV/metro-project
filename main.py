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
                                            bank_balance = float(input("please enter your balance carefully "
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
                                        except TypeError:
                                            print("wrong input for balance")
                                            input("press enter to continue")

                                elif login_input == "2":
                                    os.system("cls")
                                    print('''
1.buy a card
2.your available cards
                                    
                                    ''')
                                    card_input = input(">>")
                                    if card_input == "1":
                                        os.system("cls")
                                        print('''
please enter which type of card do you want
1.One Way
2.Credit
3.Term Credit
''')
                                        card_type = input(">>")
                                        if card_type == "1":
                                            os.system("cls")
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
                                                input("press enter to continue")
                                        elif card_type == "2":
                                            os.system("cls")
                                            if temp_bank == "":
                                                print("please login to your bank account first")
                                                input("press enter to continue")
                                            else:
                                                try:
                                                    cc_balance = float(input("please enter the balance of your card: "))
                                                    if cc_balance < 0 :
                                                        raise ValueError
                                                    temp_bank.withdraw(cc_balance)
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
                                                except TypeError:
                                                    print("wrong input for balance")
                                                    input("press enter to continue")

                                        elif card_type == "3":
                                            os.system("cls")
                                            if temp_bank == "":
                                                print("please login to your bank account first")
                                                input("press enter to continue")
                                            else:
                                                try:
                                                    cc_balance = float(input("please enter the balance of your card"))
                                                    if cc_balance < 0 :
                                                        raise ValueError
                                                    temp_bank.withdraw(cc_balance)
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
                                                except TypeError:
                                                    print("wrong input for balance")
                                                    input("press enter to continue")

                                    elif card_input == "2":
                                       os.system("cls")
                                       available_cc = 0
                                       if os.path.exists("./cards.pickle"):
                                            with open("cards.pickle","rb") as u:
                                                cards_dict = pickle.load(u)

                                            for card in cards_dict:
                                                if cards_dict[card].get_id() == temp_user.get_id():
                                                    print(cards_dict[card])
                                                    available_cc += 1
                                            if available_cc == 0:
                                                print("you have no cards to show")
                                            input("press enter to continue")
                                       else:
                                           print("there is no card to show")
                                           input("press enter to continue")



                                elif login_input == "3":
                                    os.system("cls")
                                    print('''
1.buy ticket
2.see your tickets                                    
                                    
                                    ''')
                                    ticket_input = input(">>")
                                    if ticket_input == "1":
                                        os.system("cls")
                                        try:
                                            origin = input("please enter your origin: ")
                                            destination = input("please enter your destination: ")
                                            date = input("please enter the date in this format "
                                                                "YYYY/MM/DD: ")
                                            for i in range(4):
                                                update_database(Ticket(origin,destination,date))

                                            with open("tickets.pickle","rb") as u:
                                                ticket_dict = pickle.load(u)
                                            print("available tickets:")
                                            for ticket_id in ticket_dict:
                                                if ticket_dict[ticket_id].origin == origin and ticket_dict[ticket_id].destination == destination and ticket_dict[ticket_id].date > datetime.now():
                                                    print(ticket_id,":",ticket_dict[ticket_id])
                                            choosen_ticket = input("to buy one of these tickets enter it's id: ")
                                            user_ticket = ticket_dict[choosen_ticket]

                                            user_card_id = input("enter your card id: ")
                                            if os.path.exists("./cards.pickle"):
                                                with open("cards.pickle", "rb") as u:
                                                    cards_dict = pickle.load(u)
                                                if user_card_id in cards_dict:
                                                    if cards_dict[user_card_id].get_id() == temp_user.get_id():
                                                        try:
                                                            user_card = cards_dict[user_card_id]
                                                            user_ticket.buy_ticket(temp_user.get_id(),user_card)
                                                            update_database(user_ticket)
                                                            print("ticket successfuly bought")
                                                            input("press enter to continue")
                                                        except AssertionError:
                                                            print("not enough balance in your card")
                                                            input("press enter to continue")
                                                    else:
                                                        print("validation failed")
                                                        input("press enter to continue")

                                                else:
                                                    print("card id doesn't exist")
                                                    input("press enter to continue")

                                            else:
                                                print("there is no card saved please create one!!")
                                                input("press enter to continue")
                                        except ValueError:
                                            print("invalid date")
                                        except AssertionError:
                                            print("Your one time card had been used")

                                    elif ticket_input == "2":
                                        os.system("cls")
                                        user_ticket_num = 0
                                        if os.path.exists("./tickets.pickle"):
                                            with open("tickets.pickle","rb") as u:
                                                ticket_dict = pickle.load(u)
                                            for ticket_id in ticket_dict:
                                                if ticket_dict[ticket_id].get_id() == temp_user.get_id():
                                                    print(ticket_dict[ticket_id])
                                                    user_ticket_num += 1
                                            if user_ticket_num == 0:
                                                print("you have no tickets to show")
                                            input("press enter to continue")
                                        else:
                                            print("there is no tickets to show you")
                                            input("press enter to continue")


                                elif login_input == "4":
                                    break
                        else:
                            print("validation failed")
                            input("press enter to continue")
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
                    assert age >= 18,"you should have at list 18 years old"
                    email = input("please enter email: ")

                    new_user = User(fname,lname,age,email)
                    update_database(new_user)

                    print("user created now you can login to your account")
                    input("press enter to continue")
                except ValueError:
                    print("incorrect input")
                    input("press enter to continue")
                except AssertionError:
                    print("you should be older")
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
                os.system("cls")
                email = input("please enter your email: ")
                admin_id = input("please enter your id: ")
                try:
                    with open("admins.pickle", "rb") as u:
                        admin_dict = pickle.load(u)
                    if admin_id in admin_dict:
                        if admin_dict[admin_id].email == email:
                            print("login successful")
                            input("press enter to continue")
                            temp_admin = admin_dict[admin_id]
                            while True:
                                os.system("cls")
                                print('''
1.cards
2.tickets
3.exit
                                
                                
                                ''')

                                admin_choice = input(">>")
                                if admin_choice == "1":
                                    os.system("cls")


                                    if os.path.exists("./cards.pickle"):
                                        print('''
1.add a card
2.delete a card
3.edit a card                         
                                        
                                        ''')
                                        sudo_card = input("please select an option:")

                                        try:
                                            with open("cards.pickle", "rb") as u:
                                                cc_dict = pickle.load(u)
                                        except FileNotFoundError:
                                            print("there is no card saved you can only add cards")
                                            if sudo_card in ["1","2"]:
                                                print("please select an another option")
                                                input("please press enter to continue")
                                                continue

                                        if sudo_card == "1":
                                            os.system("cls")
                                            cc_type = input("1:One Way, 2:Credit, 3:Term Credit >> ")
                                            user_id = input("please enter the owner id:")
                                            if cc_type == "1":
                                                new_cc = Card("One Way",user_id)
                                                update_database(new_cc)
                                                print("card saved successfuly")
                                                input("press enter to continue")
                                            elif cc_type == "2":
                                                try:
                                                    cc_balance = float(input("please enter the balance of card: "))
                                                    new_cc = Card("Credit",user_id,balance=cc_balance)
                                                    update_database(new_cc)
                                                    print("card saved successfuly")
                                                    input("press enter to continue")
                                                except TypeError:
                                                    print("wrong input for balance")
                                                    input("press enter to continue")
                                            elif cc_type == "3":
                                                try:
                                                    cc_balance = float(input("please enter the balance of card: "))
                                                    cc_ex_date = input("please enter the expire date in this format "
                                                                        "YYYY/MM/DD: ")
                                                    new_cc = Card("Credit", user_id, balance=cc_balance, expire_date=cc_ex_date)
                                                    update_database(new_cc)
                                                    print("card saved successfuly")
                                                    input("press enter to continue")
                                                except ValueError:
                                                    print("invalid date")
                                                    input("press enter to continue")
                                                except TypeError:
                                                    print("wrong input for balance")
                                                    input("press enter to continue")

                                        elif sudo_card == "2":
                                            os.system("cls")
                                            try:
                                                cc_id = input("please enter the id of card: ")
                                                del cc_dict[cc_id]
                                                print("card deleted")
                                                input("press enter to continue")
                                            except KeyError:
                                                print("card id is wrong")
                                                input("press enter to continue")
                                        elif sudo_card == "3":
                                            os.system("cls")
                                            try:
                                                cc_id = input("please enter the id of card: ")
                                                print('''
1.change card owner
2.change card balance
3.change expire date      
                                                ''')
                                                change_option = input(">>")
                                                if change_option == "1":
                                                    new_owner = input("please enter the id of new owner: ")
                                                    new_cc = cc_dict[cc_id]
                                                    temp_admin.set_card_owner(new_cc,new_owner)
                                                    update_database(new_cc)
                                                elif change_option == "2":
                                                    try:
                                                        new_balance = int(input("please enter new balance"))
                                                        new_cc = cc_dict[cc_id]
                                                        temp_admin.set_card_balance(new_cc,new_balance)
                                                        update_database(new_cc)
                                                    except AssertionError:
                                                        print("invalid balance given")
                                                elif change_option == "3":
                                                    try:
                                                        new_date = input("please enter the new date in the form of "
                                                                         "YYYY/MM/DD: ")
                                                        new_cc = cc_dict[cc_id]
                                                        temp_admin.set_card_expire_date(new_cc,new_date)
                                                        update_database(new_cc)
                                                    except ValueError:
                                                        print("incorrect date")
                                            except KeyError:
                                                print("incorrect id")
                                                input("press enter to continue")


                                    else:
                                        print('''
there is no cards saved you can only add cards
1.add a card                                        
                                        ''')

                                        if sudo_card == "1":
                                            os.system("cls")
                                            cc_type = input("1:One Way, 2:Credit, 3:Term Credit >> ")
                                            user_id = input("please enter the user id:")
                                            if cc_type == "1":
                                                new_cc = Card("One Way", user_id)
                                                update_database(new_cc)
                                                print("card saved successfuly")
                                                input("press enter to continue")
                                            elif cc_type == "2":
                                                cc_balance = input("please enter the balance of card: ")
                                                new_cc = Card("Credit", user_id, balance=cc_balance)
                                                update_database(new_cc)
                                            elif cc_type == "3":
                                                try:
                                                    cc_balance = input("please enter the balance of card: ")
                                                    cc_ex_date = input("please enter the expire date in this format "
                                                                       "YYYY/MM/DD: ")
                                                    new_cc = Card("Credit", user_id, balance=cc_balance,
                                                                  expire_date=cc_ex_date)
                                                    update_database(new_cc)
                                                except ValueError:
                                                    print("invalid date")
                                                    input("press enter to continue")
                                elif admin_choice == "2":
                                    while True:
                                        os.system("cls")
                                        print('''
1.add a ticket
2.delete a ticket
3.edit a ticket


                                                                    ''')

                                        sudo_ticket = input("please select an option:")
                                        try:
                                            with open("tickets.pickle", "rb") as u:
                                                ticket_dict = pickle.load(u)
                                        except FileNotFoundError:
                                            print("there is no ticket saved you can only add cards")
                                            if sudo_card in ["1", "2"]:
                                                print("please select an another option")
                                                input("please press enter to continue")
                                                continue
                                        if sudo_ticket == "1":
                                            os.system("cls")
                                            try:
                                                origin = input("please enter your origin: ")
                                                destination = input("please enter your destination: ")
                                                date = input("please enter the expire date in this format "
                                                                            "YYYY/MM/DD: ")
                                                update_database(Ticket(origin,destination,date))
                                                print("ticket successfuly saved")
                                                input("please press enter to continue")
                                            except ValueError:
                                                print("please enter the date in the given format!!")
                                                input("press any key to continue")

                                        elif sudo_ticket == "2":
                                            os.system("cls")
                                            ticket_id = input("please enter the id of card: ")
                                            del ticket_dict[ticket_id]
                                            print("card deleted")
                                            input("press enter to continue")

                                        elif sudo_ticket == "3":
                                            try:
                                                os.system("cls")
                                                print('''
1.change owner
2.change origin
3.change destination
4.change price
5.change date
                                                
                                                ''')
                                                change_option = input("please enter an option: ")
                                                if change_option == "1":
                                                    ticket_id = input("please enter ticket id: ")
                                                    changed_ticket = ticket_dict[ticket_id]
                                                    new_owner = input("please enter the new owner id: ")
                                                    temp_admin.set_ticket_owner(changed_ticket,new_owner)
                                                    update_database(changed_ticket)
                                                    print("owner changed successfuly")
                                                    input("press enter to continue")

                                                elif change_option == "2":
                                                    ticket_id = input("please enter ticket id: ")
                                                    changed_ticket = ticket_dict[ticket_id]
                                                    new_origin = input("please enter the new origin: ")
                                                    temp_admin.set_ticket_origin(changed_ticket,new_origin)
                                                    update_database(changed_ticket)
                                                    print("origin changed successfuly")
                                                    input("press enter to continue")

                                                elif change_option == "3":
                                                    ticket_id = input("please enter ticket id: ")
                                                    changed_ticket = ticket_dict[ticket_id]
                                                    new_destination = input("please enter the new destination: ")
                                                    temp_admin.set_ticket_destination(changed_ticket, new_destination)
                                                    update_database(changed_ticket)
                                                    print("destination changed successfuly")
                                                    input("press enter to continue")

                                                elif change_option == "4":
                                                    try:
                                                        ticket_id = input("please enter ticket id: ")
                                                        changed_ticket = ticket_dict[ticket_id]
                                                        new_price = input("please enter the new price: ")
                                                        temp_admin.set_ticket_price(changed_ticket, new_price)
                                                        update_database(changed_ticket)
                                                        print("destination changed successfuly")
                                                        input("press enter to continue")
                                                    except ValueError:
                                                        print("incorrect input for price")
                                                        input("press enter to continue")

                                                elif change_option == "5":
                                                    try:
                                                        ticket_id = input("please enter ticket id: ")
                                                        changed_ticket = ticket_dict[ticket_id]
                                                        new_date = input("please enter the date in this format "
                                                                            "YYYY/MM/DD: ")
                                                        temp_admin.set_ticket_date(changed_ticket, new_date)
                                                        update_database(changed_ticket)
                                                        print("destination changed successfuly")
                                                        input("press enter to continue")
                                                    except ValueError:
                                                        print("incorrect input for price")
                                                        input("press enter to continue")

                                            except KeyError:
                                                print("incorrect id")
                                                input("press enter to continue")

                                elif admin_choice == "3":
                                    break
                        else:
                            print("validation failed")
                    else:
                        print("admin id not found")
                except FileNotFoundError:
                    print("there is no admin please create one")

            elif admin_input == "2":
                os.system("cls")
                try:
                    fname = input("please enter your first name: ")
                    if not fname.isalpha():
                        raise ValueError
                    lname = input("please enter your last name: ")
                    if not lname.isalpha():
                        raise ValueError
                    age = int(input("please enter your age: "))
                    assert age >= 18, "you should have at list 18 years old"
                    email = input("please enter email: ")

                    new_admin = SuperUser(fname, lname, age, email)
                    update_database(new_admin)
                    print("admin created now you can login to your account")
                    input("press enter to continue")
                except ValueError:
                    print("incorrect input")
                    input("press enter to continue")
                except AssertionError:
                    print("you should be older")
                    input("press enter to continue")
            elif admin_input == "3":
                break

    elif menu_input == "3":
        break
