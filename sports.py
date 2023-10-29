import csv
import sys
import io
from PyQt5 import uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


def get_first_data():
    """чтение из файла csv для первой таблицы"""
    with open('assets/files_for_sports/first_sports_achievemnt.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        data = []
        for elem in reader:
            data.append(elem)
        return data


def get_second_data():
    """чтение из файла csv для второй таблицы"""
    with open('assets/files_for_sports/arm.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        data = []
        for elem in reader:
            data.append(elem)
        return data


template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>sports</class>
 <widget class="QMainWindow" name="sports">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>640</width>
    <height>240</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>640</width>
    <height>240</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>640</width>
    <height>240</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTableWidget" name="first_table">
    <property name="geometry">
     <rect>
      <x>5</x>
      <y>20</y>
      <width>259</width>
      <height>181</height>
     </rect>
    </property>
   </widget>
   <widget class="QTableWidget" name="second_table">
    <property name="geometry">
     <rect>
      <x>320</x>
      <y>20</y>
      <width>319</width>
      <height>181</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>110</x>
      <y>0</y>
      <width>47</width>
      <height>13</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(255,255,255)</string>
    </property>
    <property name="text">
     <string>обычные</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>450</x>
      <y>-5</y>
      <width>191</width>
      <height>21</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(255,255,255)</string>
    </property>
    <property name="text">
     <string>армрестлинг</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>640</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class SportsInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.setWindowTitle("Sports Room")
        self.setFixedSize(640, 220)
        self.setStyleSheet("background-image : url(assets/files_for_sports/giri.jpg);")
        self.load_table_first()
        self.load_table_second()

    def load_table_first(self):
        """занесение в первую таблицу данных"""
        self.first_data = get_first_data()
        self.header = self.first_data[0]
        self.first_data = self.first_data[1:]
        self.first_table.setColumnCount(len(self.first_data[0]))
        self.first_table.setHorizontalHeaderLabels(self.header)
        self.first_table.setRowCount(0)
        for i, row in enumerate(self.first_data):
            self.first_table.setRowCount(
                self.first_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.first_table.setItem(i, j, QTableWidgetItem(str(elem)))
            for e in range(self.first_table.columnCount()):
                self.first_table.item(i, e).setBackground(QColor(255, 255, 255))
        self.first_table.resizeColumnsToContents()
        self.first_table.setStyleSheet("color: rgb(255, 0, 255)")

    def load_table_second(self):
        """занесение во вторую таблицу данных"""
        self.second_data = get_second_data()
        self.header = self.second_data[0]
        self.second_data = self.second_data[1:]
        self.second_table.setColumnCount(len(self.second_data[0]))
        self.second_table.setHorizontalHeaderLabels(self.header)
        self.second_table.setRowCount(0)
        for i, row in enumerate(self.second_data):
            self.second_table.setRowCount(
                self.second_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.second_table.setItem(i, j, QTableWidgetItem(str(elem)))
            for e in range(self.second_table.columnCount()):
                self.second_table.item(i, e).setBackground(QColor(255, 255, 255))
        self.second_table.resizeColumnsToContents()
        self.second_table.setStyleSheet("color: rgb(255, 0, 255)")


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SportsInfo()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
