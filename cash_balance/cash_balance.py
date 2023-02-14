import re

class CashBalance:
    def __init__(self) -> None:
        pass

    def get_current_cash_balance(self, cash_balance_dict):
        cash_balance = 0
        for key, value in cash_balance_dict.items():
            cash_balance += int(key) * int(value)
        return cash_balance

    def verify_cash(self, price, pay_amount):
        diff = self.expense(self, price, pay_amount)
        # Whether pay_amount is higher than price.
        if diff < 0:
            print('Actually, you can\'t buy it.')
            return
        spend_dict = self.calc_num_of_each_cash(self, pay_amount)
        change_dict = self.calc_num_of_each_cash(self, diff)
        print('Price: ¥' + str(price) + '\n\nPayed: ¥' + str(pay_amount))
        verified_spend_dict = self.arrange_cash_dict(self, spend_dict)
        print('Change: ¥' + str(diff))
        verified_change_dict = self.arrange_cash_dict(self, change_dict)
        spend_and_change_dict = [verified_spend_dict, verified_change_dict]
        return spend_and_change_dict

    def arrange_cash_dict(self, cash_dict):
        for key, value in cash_dict.items():
            if value > 0:
                print(' ¥' + str(key).rjust(4) + ': ' + str(value))
        print('Is it collect? y/n')
        response = input()
        if response == 'y':
            return cash_dict
        elif response == 'n':
            print('Which cash do you break?')
            response = input()
            regex = r'(5|10|50|100|500|1000|5000)'
            if bool(re.fullmatch(regex, response)):
                if response == '5000' and cash_dict['5000'] > 0:
                    cash_dict['5000'] -= 1
                    cash_dict['1000'] += 5
                elif response == '1000' and cash_dict['1000'] > 0:
                    cash_dict['1000'] -= 1
                    cash_dict['500'] += 2
                elif response == '500' and cash_dict['500'] > 0:
                    cash_dict['500'] -= 1
                    cash_dict['100'] += 5
                elif response == '100' and cash_dict['100'] > 0:
                    cash_dict['100'] -= 1
                    cash_dict['50'] += 2
                elif response == '50' and cash_dict['50'] > 0:
                    cash_dict['50'] -= 1
                    cash_dict['10'] += 5
                elif response == '10' and cash_dict['10'] > 0:
                    cash_dict['10'] -= 1
                    cash_dict['5'] += 2
                elif response == '5' and cash_dict['5'] > 0:
                    cash_dict['5'] -= 1
                    cash_dict['1'] += 5
            else:
                print('Please retry.')

            self.arrange_cash_dict(self, cash_dict)

    def manage(self, cash, spend, change):
        new_cash_balance = cash
        cash_balance = 0
        for x in cash:
            cash[x] = cash[x] - spend[x]
            cash[x] = cash[x] + change[x]
            # print(x + '円: ' + str(cash[x]) + '枚')
            cash_balance = cash_balance + int(x) * cash[x]
            new_cash_balance[x] = cash[x]
        print('現金残高: ' + str(cash_balance) + '円')
        return new_cash_balance

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

    def test(self, num):
        if num < 10:
            print('not yet..')
            num += 1
            self.test(self, num)
        else:
            return 'ok'

    def test2(self):
        self.test(self)
 
