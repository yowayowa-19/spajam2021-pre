import sqlite3


# 作るテーブル
# USERS
#
#

class Users:
    def __init__(self):
        self.con = sqlite3.connect("users.db")
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
