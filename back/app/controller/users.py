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
            is_sending integer
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
            # print(hard_mac_addr)
            cur.execute(
                "UPDATE users SET hard_mac_addr = ?  WHERE mac_addr = ?", (hard_mac_addr, mac_addr))
            self.con.commit()
            row = cur.execute(
                "SELECT * FROM users WHERE hard_mac_addr = ?", (hard_mac_addr,))
            count = len(row.fetchall())
            # print(count)
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
        print(f'{mac_addr=}')
        row = cur.execute(
            "SELECT is_sending FROM users WHERE hard_mac_addr = ?", (mac_addr,))
        is_sending: int = row.fetchone()
        is_sending = is_sending[0] if isinstance(is_sending, tuple) else is_sending
        self.con.commit()
        # if is_sending is None:
        #     is_sending = 1
        print(f'l090: {is_sending=}')
        cur.close()

    def stop_phrase(self, mac_addr: str):
        cur = self.cursor()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE mac_addr = ?", (mac_addr,))
        is_sending: bool = row.fetchone()[0]
        print(f'l102: {is_sending=}')
        # if is_sending:
        cur.execute(
            "UPDATE users SET is_sending = 0 WHERE mac_addr = ?", (mac_addr,))
        self.con.commit()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE mac_addr = ?", (mac_addr,))
        is_sending: bool = row.fetchone()[0]
        print(f'l112: {is_sending=}')
        cur.close()

    def is_sending(self, mac_addr: str) -> int:
        cur = self.cursor()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE mac_addr = ?", (mac_addr,))
        # is_sending: bool = x[0] if isinstance(
        #     x := row.fetchone(), (tuple, list)) else x if x else False
        is_sending = row.fetchone()
        is_sending = is_sending[0] if isinstance(is_sending, tuple) else is_sending
        cur.close()
        return is_sending if is_sending else 0

    def is_sending_h(self, hard_mac_addr: str) -> int:
        cur = self.cursor()
        row = cur.execute(
            "SELECT is_sending FROM users WHERE hard_mac_addr = ?", (hard_mac_addr,))
        # is_sending: bool = x[0] if isinstance(
        #     x := row.fetchone(), (tuple, list)) else x if x else False
        flag = row.fetchone()
        cur.close()
        return flag if flag else 0

    def set_phrase_and_score(self, mac_addr: str, phrase: str):
        # print(mac_addr)
        _score, _hand = score(phrase)
        # print(_score)
        cur = self.cursor()
        cur.execute("UPDATE users SET phrase = ?, score = ?, hand = ? WHERE hard_mac_addr = ?",
                    (phrase, _score, _hand, mac_addr,))
        self.con.commit()
        cur.close()

    def get_ranking(self, mac_addr: str):
        cur = self.cursor()
        row = cur.execute("""SELECT view 
        FROM (mac_addr, name, score, hand, RANK() OVER(ORDER BY score DESC) as rank_result FROM users) as view
        WHERE rank_result <= 10""")
        result = [item + (mac_addr == item[0],) for item in row.fetchall()]
        print(result)
        cur.close()
        return result

    def get_me(self, mac_addr: str):
        cur = self.cursor()
        row = cur.execute("""SELECT view 
        FROM (mac_addr, name, score, hand, RANK() OVER(ORDER BY score DESC ) as rank_result, true FROM users) as view
        WHERE mac_addr = ?""", (mac_addr,))
        result = row.fetchone()
        cur.close()
        print(result)
        return result
