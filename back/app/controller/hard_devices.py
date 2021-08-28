import sqlite3

# from pathlib import Path

# try:
#     from controller.libs import get_back_path
# except ModuleNotFoundError:
#     from libs import get_back_path

from libs.get_path import get_back_path

class HardDevices:
    def __init__(self):
        path = get_back_path() / "db/sample.db"
        self.con = sqlite3.connect(path)
        cur = self.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS hard_devices (
            mac_addr text PRIMARY KEY,
            phrase text
        )""")
        self.con.commit()
        cur.close()

    def cursor(self) -> sqlite3.Cursor:
        return self.con.cursor()

    def set_sample(self):
        "直接叩いてほしい"
        cur = self.cursor()
        items = [("mac1", "ABCDE"), ("mac2", "BCDEF"), ("mac3", "CDERG")]
        cur.executemany(
            "INSERT INTO hard_devices (mac_addr, phrase) VALUES(?, ?)", items)
        self.con.commit()
        cur.close()


if __name__ == '__main__':
    HardDevices().set_sample()
