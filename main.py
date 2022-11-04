import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
import sqlite3 as sql

main_bd = sql.connect('ProjectDB.db')
cursor = main_bd.cursor()
name = ''
date = ''

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win1.ui', self)  # Загружаем дизайн
        self.calendar = Calendar()
        self.enter_btn.clicked.connect(self.check_input)

    def check_input(self):
        global name
        name = self.put_name_lineEdit.text()
        try:
            if not str(name).isalpha():
                raise ValueError
            self.calendar.show()
            #self.greeting()
            self.close()
            cursor.execute(f'SELECT "имя" from [таблица имен] WHERE "имя" = "{name}";')
            name_list = cursor.fetchall()
            if len(name_list) == 0:
                cursor.execute(f'INSERT INTO [таблица имен] ("имя") VALUES ("{name}");')
                main_bd.commit()
            else:
                self.greeting()
        except ValueError:
            print('ошибка при вводе')


    def greeting(self):
        self.greet = Greeting()


class Greeting(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('greeting.ui', self)
        self.show()
        self.label.setText(f'Привет, {name}!')
        self.continueButton.clicked.connect(self.close)


class Calendar(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('win3.ui', self)  # Загружаем дизайн
        self.diary_btn.clicked.connect(self.open_diary)

    def open_diary(self):
        global date
        date = self.calendarWidget.selectedDate().toString('dd-MM-yyyy')
        self.diary = Diary()
        self.diary.data_label.setText(date)
        self.diary.show()
        self.close()


class Diary(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('win2.ui', self)  # Загружаем дизайн
        self.refresh_data()
        self.add_btn.clicked.connect(self.product)
        self.back_btn.clicked.connect(self.open_calendar_window)
        self.refresh_button.clicked.connect(self.refresh_data)

    def refresh_data(self):
        sum_belki = sum_zhiri = sum_uglevodi = sum_kkal =  0
        cursor.execute(f'SELECT "id имени" from [таблица имен] WHERE "имя" = "{name}";')
        nameid_for_diary = cursor.fetchone()[0]

        a = self.breakfast_table.rowCount()
        for row in range(a-1, -1, -1):
            self.breakfast_table.removeRow(row)
        a = self.lunch_table.rowCount()
        for row in range(a - 1, -1, -1):
            self.lunch_table.removeRow(row)
        a = self.dinner_table.rowCount()
        for row in range(a - 1, -1, -1):
            self.dinner_table.removeRow(row)


        cursor.execute(f'SELECT "id продукта","масса","Б","Ж","У","Ккал" from [дневник] '
                       f'WHERE "id имени" = {nameid_for_diary} and "id времени пищи" = 1 and "дата" = "{date}";')
        breakfast_list = cursor.fetchall()

        for i in breakfast_list:
            cursor.execute(f'SELECT "имя продукта" from [таблица продуктов] WHERE "id продукта" = {i[0]};')
            table_product = cursor.fetchone()[0]
            sum_belki += i[2]
            sum_zhiri += i[3]
            sum_uglevodi += i[4]
            sum_kkal += i[5]
            count = 0
            self.breakfast_table.insertRow(count)
            self.breakfast_table.setItem(count, 0, QTableWidgetItem(table_product))
            self.breakfast_table.setItem(count, 1, QTableWidgetItem(str(i[1])))
            self.breakfast_table.setItem(count, 2, QTableWidgetItem(str(i[5])))
            count+=1
        count = 0


        cursor.execute(f'SELECT "id продукта","масса","Б","Ж","У","Ккал" from [дневник] WHERE '
                       f'("id имени" = {nameid_for_diary} and "id времени пищи" = 2 and "дата" = "{date}");')
        lunch_list = cursor.fetchall()
        for i in lunch_list:
            cursor.execute(f'SELECT "имя продукта" from [таблица продуктов] WHERE "id продукта" = {i[0]};')
            table_product = cursor.fetchone()[0]
            sum_belki += i[2]
            sum_zhiri += i[3]
            sum_uglevodi += i[4]
            sum_kkal += i[5]
            count = 0
            self.lunch_table.insertRow(count)
            self.lunch_table.setItem(count, 0, QTableWidgetItem(str(table_product)))
            self.lunch_table.setItem(count, 1, QTableWidgetItem(str(i[1])))
            self.lunch_table.setItem(count, 2, QTableWidgetItem(str(i[5])))
            count+=1
        count = 0

        cursor.execute(f'SELECT "id продукта","масса","Б","Ж","У","Ккал" from [дневник] WHERE '
                       f'("id имени" = {nameid_for_diary} and "id времени пищи" = 3 and "дата" = "{date}");')
        dinner_list = cursor.fetchall()
        for i in dinner_list:
            cursor.execute(f'SELECT "имя продукта" from [таблица продуктов] WHERE "id продукта" = {i[0]};')
            table_product = cursor.fetchone()[0]
            sum_belki += i[2]
            sum_zhiri += i[3]
            sum_uglevodi += i[4]
            sum_kkal += i[5]
            count = 0
            self.dinner_table.insertRow(count)
            self.dinner_table.setItem(count, 0, QTableWidgetItem(table_product))
            self.dinner_table.setItem(count, 1, QTableWidgetItem(str(i[1])))
            self.dinner_table.setItem(count, 2, QTableWidgetItem(str(i[5])))

        self.proteins_count.display(sum_belki)
        self.fats_count.display(sum_zhiri)
        self.carbohydrates_count.display(sum_uglevodi)
        self.quantity_count.display(sum_kkal)


    def open_calendar_window(self):
        self.calendar = Calendar()
        self.calendar.show()
        self.close()


    def product(self):
        self.product = Add_product()
        self.product.show()


class Add_product(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add.ui', self)
        cursor.execute(f'SELECT "имя продукта" from [таблица продуктов];')
        list_of_data = cursor.fetchall()
        for i in list_of_data:
            self.chooseBox.addItem(i[0])
        self.okey_btn.clicked.connect(self.add_product)

    def add_product(self):
        product = self.chooseBox.currentText() #!
        weight = self.weight_lineEdit.text()
        eat_time = ''
        if self.radio_br.isChecked():
            eat_time = 'завтрак'
        elif self.radio_l.isChecked():
            eat_time = 'обед'
        elif self.radio_d.isChecked():
            eat_time = 'ужин'
        try:
            if not str(product).isalpha() or (eat_time == ''):
                raise ValueError
            weight = float(weight)

            cursor.execute(f'SELECT "Б", "Ж", "У", "Ккал", "Граммовка" from [таблица продуктов] WHERE "имя продукта" = "{product}";')
            list_of_data = cursor.fetchall()
            k = weight / list_of_data[0][4]
            belki = k * list_of_data[0][0]
            zhiri = k * list_of_data[0][1]
            uglevodi = k * list_of_data[0][2]
            kkal = k * list_of_data[0][3]

            cursor.execute(f'SELECT "id имени" from [таблица имен] WHERE "имя" = "{name}";')
            nameid_for_diary = cursor.fetchone()[0]
            cursor.execute(f'SELECT "id" from [таблица времени пищи] WHERE "время приёма" = "{eat_time}";')
            timeid_for_diary = cursor.fetchone()[0]
            cursor.execute(f'SELECT "id продукта" from [таблица продуктов] WHERE "имя продукта" = "{product}";')
            productid_for_diary = cursor.fetchone()[0]

            cursor.execute(f'INSERT INTO дневник ("id имени","дата","id времени пищи","id продукта","масса","Б","Ж","У","Ккал") '
                           f'VALUES ("{nameid_for_diary}", "{date}", "{timeid_for_diary}", "{productid_for_diary}", "{weight}",'
                           f'"{belki}","{zhiri}","{uglevodi}","{kkal}");')
            main_bd.commit()
            self.close()
        except Exception as e:
            print('ошибка при вводе ',e)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
