import sqlite3 as sql

main_bd = sql.connect('ProjectDB.db')
cursor = main_bd.cursor()

def clear():
    cursor.execute(f'DROP TABLE IF EXISTS [таблица имен];')
    main_bd.commit()
    cursor.execute(f'DROP TABLE IF EXISTS дневник;')
    main_bd.commit()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS [таблица имен] ([id имени] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "имя" STRING NOT NULL);')
    main_bd.commit()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS дневник (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   f'[id имени] INTEGER NOT NULL REFERENCES [таблица имен] ([id имени]) ON DELETE CASCADE ON UPDATE CASCADE,'
                   f'дата DATE NOT NULL,[id времени пищи] INTEGER NOT NULL REFERENCES [таблица времени пищи] (id) ON DELETE CASCADE ON UPDATE CASCADE,'
                   f'[id продукта] INTEGER NOT NULL REFERENCES [таблица продуктов] ([id продукта]) ON DELETE CASCADE ON UPDATE CASCADE,'
                   f'масса DOUBLE  NOT NULL,Б DOUBLE  NOT NULL, Ж DOUBLE  NOT NULL, У DOUBLE  NOT NULL, Ккал DOUBLE  NOT NULL);')
    main_bd.commit()

if __name__ == '__main__':
    clear()