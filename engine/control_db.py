import sqlite3


class Driver:
    __slots__ = ['con', 'sql', 'warp_file']

    def __init__(self, warp_file='resources/data.db'):
        """
        Подключение к базе данных, инициализация
        :param warp_file: Файл или None - memory
        """
        if warp_file is not None:
            self.con = sqlite3.connect(warp_file, check_same_thread=False)
        else:
            self.con = sqlite3.connect(':memory:', check_same_thread=False)
        self.sql = self.con.cursor()
        self.warp_file = warp_file

    def receive(self, query: str):
        try:
            self.sql.execute(query)
            return self.sql.fetchone()[0]
        except Exception as ex:
            print('Ошибка БД:', str(ex), query)

    def receives(self, query: str):
        try:
            self.sql.execute(query)
            return self.sql.fetchall()
        except Exception as ex:
            print('Ошибка БД:', str(ex), query)

    def save(self, q):
        try:
            if q.endswith(';'):
                self.sql.executescript(q)
            else:
                self.sql.execute(q)
            self.con.commit()
        except Exception as ex:
            print('Ошибка БД:', str(ex), q)

    def __del__(self):
        self.con.close()
