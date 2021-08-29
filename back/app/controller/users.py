import sqlite3

try:
    from controller.libs import get_back_path
except ModuleNotFoundError:
    from libs import get_back_path

from libs.phrase import score

# 作るテーブル
# USERS
#
# mac_addr text PRIMARY KEY,
# hard_mac_addr text,
# name text,
# score integer,
# rank integer,
# hand text
# phrase text


class Users:
    def __init__(self):
        path = get_back_path()
        self.con = sqlite3.connect(path / "db/sample.db")
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            mac_addr text PRIMARY KEY,
            hard_mac_addr text,
            name text,
            score integer default 0,
            rank integer,
            hand text,
            phrase text,
            is_sending integer default 0
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
            "SELECT mac_addr FROM hard_devices WHERE phrase = ?", (phrase,))
        result = row.fetchall()
        if len(result) == 1:
            hard_mac_addr: str = result[0][0]
            # print(hard_mac_addr)
            cur.execute(
                "UPDATE users SET hard_mac_addr = ?  WHERE mac_addr = ?", (hard_mac_addr, mac_addr))
            self.con.commit()
            row = cur.execute(
                "SELECT * FROM users WHERE hard_mac_addr = ?", (hard_mac_addr,))
            count = len(row.fetchall())
            if count == 1:
                # ハードウェアMACアドレスが一致したらTrue
                return True
        cur.close()
        return False

    def start_phrase(self, mac_addr: str):
        cur = self.cursor()
        cur.execute(
            "UPDATE users SET is_sending = 1 WHERE hard_mac_addr = ?", (mac_addr,))
        self.con.commit()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE hard_mac_addr = ?", (mac_addr,))
        is_sending: int = row.fetchone()
        is_sending = is_sending[0] if isinstance(
            is_sending, tuple) else is_sending
        self.con.commit()
        cur.close()

    def stop_phrase(self, mac_addr: str):
        cur = self.cursor()
        cur.execute(
            "UPDATE users SET is_sending = 0 WHERE mac_addr = ?", (mac_addr,))
        self.con.commit()
        cur.close()

    def is_sending(self, mac_addr: str) -> int:
        cur = self.cursor()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE mac_addr = ?", (mac_addr,))
        is_sending = row.fetchone()
        is_sending = is_sending[0] if isinstance(
            is_sending, tuple) else is_sending
        cur.close()
        return is_sending if is_sending else 0

    def is_sending_h(self, hard_mac_addr: str) -> int:
        cur = self.cursor()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE hard_mac_addr = ?", (hard_mac_addr,))
        flag = row.fetchone()
        cur.close()
        return flag if flag else 0

    def set_phrase_and_score(self, mac_addr: str, phrase: str):
        _score, _hand = score(phrase)
        cur = self.cursor()
        cur.execute("UPDATE users SET phrase = ?, score = ?, hand = ? WHERE hard_mac_addr = ?",
                    (phrase, _score, _hand, mac_addr,))
        self.con.commit()
        cur.close()

    def get_ranking(self, mac_addr: str):
        cur = self.cursor()
        row = cur.execute("""
        SELECT mac_addr, name, score, hand, 
            (SELECT COUNT(*) + 1 
            FROM users users2 
            WHERE users2.score > users1.score) rnk
        FROM users users1 
        WHERE rnk <= 10 
        ORDER BY score
        """)
        result = [item + (mac_addr == item[0],) for item in row.fetchall()]
        print(result)
        cur.close()
        return result

    def get_me(self, mac_addr: str):
        cur = self.cursor()
        row = cur.execute("""
        SELECT mac_addr, name, score, hand, 
            (SELECT COUNT(*) + 1 
            FROM users users2 
            WHERE users2.score > users1.score) rnk
        FROM users users1 
        WHERE mac_addr = ?""", (mac_addr,))
        result = row.fetchone()
        cur.close()
        return result
