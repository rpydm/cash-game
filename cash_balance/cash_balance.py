import re

class CashBalance:
    def __init__(self) -> None:
        pass

    def input_cash_amount(self, name):
        res = ''
        regex = r'(^[0-9]+$)'
        while bool(re.fullmatch(regex, res)) == False:
            print('Enter amount of ' + name)
            res = input()
            res = re.sub(",", '', res)
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

    def expense(self, price, pay_amount):
        change = pay_amount - price
        return change
