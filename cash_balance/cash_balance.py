import re
from datetime import date

class CashBalance:
    def __init__(self) -> None:
        pass

    def verify_date_input(self):
        is_regex_matched_res = False
        while is_regex_matched_res == False:
            print('Enter date value')
            res = input()
            regex = r'(^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$)'
            res = re.split("\D", res)
            res[1] = res[1].zfill(2)
            res[2] = res[2].zfill(2)
            res = "-".join(res)
            is_regex_matched_res = bool(re.fullmatch(regex, res))
        return res

    def verify_amount_input(self, value):
        print('Enter ' + value + ' value')
        res = input()
        regex = r'(^[0-9]+$)'
        while bool(re.fullmatch(regex, res)) == False:
            print('Please retry')
            res = input()
            res = re.sub("\D", '', res)
        return int(res)

    def get_current_cash_balance(self, cash_balance_dict):
        cash_balance = 0
        for key, value in cash_balance_dict.items():
            cash_balance += int(key) * int(value)
        return cash_balance

    def get_cash_balance_str(self, cash_dict):
        cash_balance_str = ''
        for key, value in cash_dict.items():
            if value == 0:
                continue
            cash_balance_str += ' ¥' + str(key).rjust(5) + ': ' + str(value) + "\n"
        return cash_balance_str

    def verify_cash(self, amount):
        cash_dict = self.calc_num_of_each_cash(self, amount)
        verified_cash_dict = self.arrange_cash_dict(self, cash_dict)
        return verified_cash_dict

    def arrange_cash_dict(self, cash_dict):
        response = ''
        while response != 'y':
            cash_balance_str = self.get_cash_balance_str(self, cash_dict)
            print(cash_balance_str)
            print('Is it collect? y/n')
            response = input()
            if response == 'y':
                break
            elif response != 'n':
                continue
            print('Which cash do you break?')
            response = input()
            regex = r'(5|10|50|100|500|1000|5000|10000)'
            if bool(re.fullmatch(regex, response)) == False:
                print('Please retry.')
                continue
            if response == '10000' and cash_dict["10000"] > 0:
                cash_dict["10000"] -= 1
                cash_dict["5000"] += 2
            elif response == '5000' and cash_dict["5000"] > 0:
                cash_dict["5000"] -= 1
                cash_dict["1000"] += 5
            elif response == '1000' and cash_dict["1000"] > 0:
                cash_dict["1000"] -= 1
                cash_dict["500"] += 2
            elif response == '500' and cash_dict['500'] > 0:
                cash_dict["500"] -= 1
                cash_dict["100"] += 5
            elif response == '100' and cash_dict["100"] > 0:
                cash_dict["100"] -= 1
                cash_dict["50"] += 2
            elif response == '50' and cash_dict["50"] > 0:
                cash_dict["50"] -= 1
                cash_dict["10"] += 5
            elif response == '10' and cash_dict["10"] > 0:
                cash_dict["10"] -= 1
                cash_dict["5"] += 2
            elif response == '5' and cash_dict["5"] > 0:
                cash_dict["5"] -= 1
                cash_dict["1"] += 5
        return cash_dict

    def manage(self, cash_balance, spend, change):
        for x in cash_balance:
            cash_balance[x] += change[x]
            cash_balance[x] -= spend[x]
        return cash_balance

    def calc_num_of_each_cash(self, amount):
        bill10000 = amount // 10000
        bill5000 = amount % 10000 // 5000
        bill1000 = amount % 5000 // 1000
        coin = amount % 1000
        coin500 = coin // 500
        coin100 = coin % 500 // 100
        coin50 = coin % 100 // 50
        coin10 = coin % 50 // 10
        coin5 = coin % 10 // 5
        coin1 = coin % 5 // 1
        cash = {
            "10000" : bill10000, "5000" : bill5000, "1000" : bill1000,
            "500" : coin500, "100" : coin100, "50" : coin50,
            "10" : coin10, "5" : coin5, "1" : coin1
        }
        return cash

    def prepare_columns_for_cash_expenses_receipt(self, cbd, cur):
        # Create the cash_expenses_receipt record
        table = 'cash_expenses_receipt'
        cash_expenses_receipt_columns = cbd.get_columns(cbd, cur, table)
        cash_expenses_receipt_columns.remove("id")
        cash_expenses_receipt_columns.remove("created_at")
        cash_expenses_receipt_columns.remove("updated_at")
        cash_expenses_receipt_columns = ",".join(cash_expenses_receipt_columns)
        return cash_expenses_receipt_columns

    def prepare_values_for_cash_expenses_receipt(self):
        # Requirement of date
        trans_date = date.today()
        print(str(trans_date) + "\nDo you edit the date? y/n")
        res = input()
        if res != 'n':
            print('Ok, enter date')
            trans_date = self.verify_date_input(self)
        print('Now you can leave a note about transaction.')
        # Requirement of note
        note = input()
        # Requirement of category
        print('And then enter category.')
        category = input()
        # Demand price and pay amount
        price = self.verify_amount_input(self, 'price')
        pay_amount = self.verify_amount_input(self, 'pay amount')
        # Whether pay_amount is higher than price.
        change = pay_amount - price
        if change < 0:
            print('Actually, you can\'t buy it.')
            return
        cash_expenses_receipt_values = {
            "user_id" : ['int', 1],
            "trans_date" : ['str', trans_date], 
            "price" : ['int', price], 
            "pay_amount" : ['int', pay_amount], 
            "change" : ['int', change],
            "cash_balance_jpy_id" : ['int', 1],
            "currency" : ['str', 'JPY'],
            "note" : ['str', note], 
            "category" : ['str', category]
        }
        return cash_expenses_receipt_values

    def register_cash_record(self, cbd, con, cur, pay_amount, change):
        # Determine base information
        pay_amount_dict = self.verify_cash(self, pay_amount)
        if 0 < change:
            print('Change: ' + str(change))
            change_dict = self.verify_cash(self, change)
        else:
            change_dict = self.calc_num_of_each_cash(self, change)
        # Show cash balance before registered
        cash_balance_dict = cbd.select_all_cash_balance(cbd, cur)
        cash_balance_int = self.get_current_cash_balance(self, cash_balance_dict)
        print("Before purchase\nCash balance: ¥" + str(cash_balance_int))
        cash_balance_str = self.get_cash_balance_str(self, cash_balance_dict)
        print(cash_balance_str)
        # Show cash balance after registered
        managed_cash_balance_dict = self.manage(self, cash_balance_dict, pay_amount_dict, change_dict)
        managed_cash_balance_int = self.get_current_cash_balance(self, managed_cash_balance_dict)
        print("After purchase\nCash balance: ¥" + str(managed_cash_balance_int))
        cash_balance_str = self.get_cash_balance_str(self, managed_cash_balance_dict)
        print(cash_balance_str)
        # Update cash_balance_jpyTBL
        cbd.update_cash_balance(cbd, cur, con, managed_cash_balance_dict)
        cash_balance_dict = cbd.select_all_cash_balance(cbd, cur)
        cash_balance_int = self.get_current_cash_balance(self, cash_balance_dict)
        print("Record updated\nNew cash balance: ¥" + str(cash_balance_int))
