import sqlite3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTableWidget


class Statistic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 250, 500)
        self.setFixedSize(250, 500)
        self.setWindowTitle("Статистика")
        self.tableWidget = QTableWidget(1, 1, self)
        self.tableWidget.resize(250, 500)
        self.loadTable()

    def loadTable(self):
        """загрузка в таблицу последних 30 игр из БД"""
        self.con = sqlite3.connect("assets/data_for_qt.db")
        self.cur = self.con.cursor()
        self.titles = ["Название игры", "Победитель"]
        data = self.cur.execute("""Select 
                Main_table.Game_num, 
                Game.Name as Game, 
                Players_and_results.Name as Winner 
            from
                Main_table 
            Left Join Players_and_results On Main_table.Winner = Players_and_results.Player_id
            Left Join Game On Main_table.Game_name = Game.game_id""")
        data = list(data)[::-1]
        for i in range(len(data)):
            data[i] = data[i][1:]
        if len(data) > 0:
            self.tableWidget.setColumnCount(len(data[0]))
            self.tableWidget.setHorizontalHeaderLabels(self.titles)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(data):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        else:
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(self.titles)
            self.tableWidget.setRowCount(0)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setStyleSheet("color: rgb(255,0,255)")


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Statistic()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
