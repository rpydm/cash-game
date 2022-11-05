import csv
import sqlite3
with sqlite3.connect('cola.db') as conn:

  class Moneytree(object):
    def __init__(self):
      self.cur = conn.cursor()

    def create(self):
      table = "transaction"
      schema_lang = f"""CREATE TABLE IF NOT EXISTS {table}(
          id          INTEGER PRIMARY KEY AUTOINCREMENT
        , date        TEXT    DEFAULT NULL
        , amount      INTEGER DEFAULT NULL
        , currency    TEXT    DEFAULT NULL
        , summary     TEXT    DEFAULT NULL
        , memo        TEXT    DEFAULT NULL
        , receipt     TEXT    DEFAULT NULL
        , category    TEXT    DEFAULT NULL
        , account     TEXT    DEFAULT NULL
        , account_num TEXT    DEFAULT NULL
        , cost        TEXT    DEFAULT NULL
        , created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
        , updated_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
      )"""
      
      self.cur.execute(schema_lang)  # SQL実行
      with open('全ての口座-2021-01-01-2022-10-31.csv','r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['date'], i['amount'], i['currency'], i['summary'], i['memo'], i['receipt'], i['account'], i['account_num'], i['cost']) for i in dr]

      self.cur.executemany("INSERT INTO transaction (date, amount, currency, summary, memo, receipt, category, account, account_num, cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
      conn.commit()

    def insert(self):
      lang = [("Fortran", 1957), ("Python", 1991), ("Go", 2009)]

      self.cur.executemany('INSERT INTO lang(name, year) VALUES(?, ?)', lang)
      conn.commit()

    def select_all(self):
      self.cur.execute('SELECT * FROM transaction')
      print(self.cur.fetchall())
      conn.commit()

    def add_column(self):
      self.cur.execute("""ALTER TABLE user ADD COLUMN created_at[date]""")
      conn.commit()

    def delete(self):
      self.cur.execute("""DELETE FROM user WHERE id = 1""")

    def show_schema(self):
      self.cur.execute("""PRAGMA table_info(lang)""")
      print(self.cur.fetchall())

  class Budget(object):
    def __init__(self) -> None:
      self.cur = conn.cursor()

    def create(self):
      table = "budget"
      schema_lang = f"""CREATE TABLE IF NOT EXISTS {table}(
          id INTEGER PRIMARY KEY AUTOINCREMENT
        , date TEXT NOT NULL
        , amount INTEGER NOT NULL DEFAULT 0
        , currency TEXT
        , summary TEXT
        , memo TEXT
        , receipt TEXT
        , category TEXT
        , account TEXT
        , account_num TEXT
        , cost TEXT
        , created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        , updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
      )"""
      
      self.cur.execute(schema_lang)  # SQL実行
      conn.commit()
      
  class Category(object):
    def __init__(self):
      self.cur = conn.cursor()
      
    def create(self):
      table = "category"
      schema_lang = f"""CREATE TABLE IF NOT EXISTS {table}(
          id INTEGER PRIMARY KEY AUTOINCREMENT
        , name TEXT NOT NULL
        , created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        , updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
      )"""
      
      self.cur.execute(schema_lang)  # SQL実行
      conn.commit()

mt = Moneytree()
# mt.create()
mt.select_all()