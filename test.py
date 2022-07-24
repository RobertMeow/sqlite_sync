from engine import HandlerDB, ClientDriver

if __name__ == '__main__':
    DB = ClientDriver(HandlerDB('file.db').config)
    DB.save("CREATE TABLE meow (test INT)")
    DB.save("INSERT INTO meow VALUES (1)")
    print(DB.receive("SELECT * FROM meow"))
