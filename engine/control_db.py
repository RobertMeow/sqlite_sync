import sqlite3


class Driver:
    __slots__ = ['con', 'sql', 'warp_file']

    def __init__(self, warp_file):
        self.con = sqlite3.connect(warp_file, check_same_thread=False)
        self.sql = self.con.cursor()
        self.warp_file = warp_file

    def receive(self, query: str):
        try:
            self.sql.execute(query)
            return self.sql.fetchone()[0], True
        except Exception as ex:
            return str(ex), False

    def receives(self, query: str):
        try:
            self.sql.execute(query)
            return self.sql.fetchall(), True
        except Exception as ex:
            return str(ex), False

    def save(self, q):
        try:
            if q.endswith(';'):
                self.sql.executescript(q)
            else:
                self.sql.execute(q)
            return self.con.commit(), True
        except Exception as ex:
            return str(ex), False

    def __del__(self):
        self.con.close()
