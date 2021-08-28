import sqlite3


# 作るテーブル
# USERS
#
#

class Users:
    def __init__(self):
        self.con = sqlite3.connect("db/sample.db")
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            mac_addr text PRIMARY KEY,
            hard_mac_addr text,
            name text,
            score integer,
            rank integer,
            hand text
        )""")
        self.con.commit()
        cur.close()

    def cursor(self) -> sqlite3.Cursor:
        return self.con.cursor()

    def register(self, mac_addr: str, name: str) -> bool:
        cur = self.cursor()
        row = cur.execute(
            "SELECT * FROM users WHERE mac_addr = ?", (mac_addr,))
        count = len(row.fetchall())
        if count == 0:
            cur.execute(
                """INSERT INTO users (mac_addr, name) VALUES(?, ?)""", (mac_addr, name))
            self.con.commit()
            cur.close()
            return True
        return False

    def pairing(self, mac_addr: str, phrase: str) -> bool:
        cur = self.cursor()
        row = cur.execute(
            "SELECT * FROM users WHERE mac_addr = ?", (mac_addr,))
        count = len(row.fetchall())
        if count == 0:
            row = cur.execute(
                "SELECT mac_addr FROM hard_devices WHERE phrase = ?", (phrase,))
            result = row.fetchall()
            if len(result) == 1:
                hard_mac_addr: str = result[0]
                cur.execute("INSERT INTO users (mac_addr, hard_mac_addr) VALUES(?, ?)", (mac_addr, hard_mac_addr))
