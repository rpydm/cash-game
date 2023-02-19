import sqlite3

class CashBalanceDml:
    def select_all_cash_balance(self, cur):
        cur.execute(f'SELECT * FROM cash_balance_jpy')
        fields = cur.fetchall()
        cash = {}
        cash["10000"] = fields[0][1]
        cash["5000"] = fields[0][2]
        cash["1000"] = fields[0][3]
        cash["500"] = fields[0][4]
        cash["100"] = fields[0][5]
        cash["50"] = fields[0][6]
        cash["10"] = fields[0][7]
        cash["5"] = fields[0][8]
        cash["1"] = fields[0][9]
        return cash

    def update_cash_balance(self, cur, con, cash):
        columns = ""
        columns = columns + 'bill_10k = ' + str(cash["10000"]) + ','
        columns = columns + 'bill_5k = ' + str(cash["5000"]) + ','
        columns = columns + 'bill_1k = ' + str(cash["1000"]) + ','
        columns = columns + 'bill_1k = ' + str(cash["1000"]) + ','
        columns = columns + 'coin_500 = ' + str(cash["500"]) + ','
        columns = columns + 'coin_100 = ' + str(cash["100"]) + ','
        columns = columns + 'coin_50 = ' + str(cash["50"]) + ','
        columns = columns + 'coin_10 = ' + str(cash["10"]) + ','
        columns = columns + 'coin_5 = ' + str(cash["5"]) + ','
        columns = columns + 'coin_1 = ' + str(cash["1"]) + ','
        columns = columns + 'updated_at = datetime(\'now\', \'localtime\')'
        sql_update_query = f"UPDATE cash_balance_jpy SET {columns} WHERE id = 1"
        try:
            cur.execute(sql_update_query)
            print('Do you commit? y/n')
            res = input()
            if res == 'y':
                con.commit()
                print(sql_update_query + '\nhas executed.')
            else:
                con.rollback()
        except sqlite3.Error as error:
            print('Failed to insert sqlite table', error)
        # finally:
        #     if con:
        #         con.close()
        #         print('The SQLite connection is closed')

    def get_columns(self, cur, table, str_flg = 0):
        cur.execute(f"PRAGMA table_info({table})")
        desc = cur.fetchall()
        columns = [fields[1] for fields in desc]
        if str_flg == 1:
            column_str = ''
            for column in columns:
                column_str += column + ','
            return column_str[:-1]
        return columns
