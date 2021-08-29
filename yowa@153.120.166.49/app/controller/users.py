import sqlite3

# from pathlib import Path

try:
    from controller.libs import get_back_path
except ModuleNotFoundError:
    from libs import get_back_path

# from libs.get_path import get_back_path

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
            score integer,
            rank integer,
            hand text,
            phrase text,
            is_sending bool
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
                """INSERT INTO users (mac_addr, name, score, is_sending) VALUES(?, ?, 0, false)""", (mac_addr, name))
            self.con.commit()
            cur.close()
            return True
        return False

    def pairing(self, mac_addr: str, phrase: str) -> bool:
        cur = self.cursor()
        # row = cur.execute(
        #     "SELECT * FROM users WHERE mac_addr = ?", (mac_addr,))
        # count = len(row.fetchall())
        # if count == 0:
        row = cur.execute(
            "SELECT mac_addr FROM hard_devices WHERE phrase = ?", (phrase,))
        result = row.fetchall()
        if len(result) == 1:
            hard_mac_addr: str = result[0][0]
            print(hard_mac_addr)
            cur.execute(
                "UPDATE users SET hard_mac_addr = ?  WHERE mac_addr = ?", (hard_mac_addr, mac_addr))
            self.con.commit()
            row = cur.execute(
                "SELECT * FROM users WHERE hard_mac_addr = ?", (hard_mac_addr,))
            count = len(row.fetchall())
            print(count)
            if count == 1:
                # ハードウェアMACアドレスが一致したらTrue
                return True
        cur.close()
        return False

    def start_phrase(self, mac_addr: str) -> bool:
        cur = self.cursor()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE mac_addr = ?", (mac_addr,))
        is_sending: bool = row.fetchone()[0]
        if not is_sending:
            cur.execute(
                "UPDATE users SET is_sending = true WHERE mac_addr = ?", (mac_addr,))
            self.con.commit()
        cur.close()

    def stop_phrase(self, mac_addr: str):
        cur = self.cursor()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE mac_addr = ?", (mac_addr,))
        is_sending: bool = row.fetchone()
        if is_sending:
            cur.execute(
                "UPDATE users SET is_sending = false WHERE mac_addr = ?", (mac_addr,))
            self.con.commit()
        cur.close()

    def is_sending(self, mac_addr: str) -> bool:
        cur = self.cursor()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE mac_addr = ?", (mac_addr,))
        is_sending: bool = row.fetchone()
        cur.close()
        return is_sending if is_sending else False

    def set_phrase_and_score(self, mac_addr: str, phrase: str):
        _score = score(phrase)
        cur = self.cursor()
        cur.execute("UPDATE users SET phrase = ?, score = ? WHERE mac_addr = ?",
                    (phrase, _score, mac_addr,))
        self.con.commit()
        cur.close()

    def set_rank(self):
        pass
