import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QPixmap


def remove_all():
    """очистить файл"""
    f = open('assets/files_for_mark/data.txt', mode='w', encoding='utf8')
    f.close()


class Mark(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 310)
        self.setFixedSize(500, 310)
        self.setWindowTitle('Заметки')
        self.fon_label = QLabel(self)
        self.fon_label.resize(500, 310)
        self.fon_label.setPixmap(QPixmap('assets/files_for_mark/fon_mark.png'))

        self.btn_add_text = QPushButton(self)
        self.btn_add_text.resize(89, 38)
        self.btn_add_text.move(51, 233)
        self.btn_add_text.setStyleSheet("background-image : url(assets/files_for_mark/add_text.png);")
        self.btn_add_text.clicked.connect(self.add_text)

        self.btn_get_text = QPushButton(self)
        self.btn_get_text.resize(89, 38)
        self.btn_get_text.move(151, 233)
        self.btn_get_text.setStyleSheet("background-image : url(assets/files_for_mark/get_text.png);")
        self.btn_get_text.clicked.connect(self.get_text)

        self.btn_remove_text = QPushButton(self)
        self.btn_remove_text.resize(89, 38)
        self.btn_remove_text.move(251, 233)
        self.btn_remove_text.setStyleSheet("background-image : url(assets/files_for_mark/remove_text.png);")
        self.btn_remove_text.clicked.connect(self.remove_text)

        self.btn_remove_all_text = QPushButton(self)
        self.btn_remove_all_text.resize(89, 38)
        self.btn_remove_all_text.move(351, 233)
        self.btn_remove_all_text.setStyleSheet("background-image : url(assets/files_for_mark/remove_all.png);")
        self.btn_remove_all_text.clicked.connect(remove_all)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.resize(500, 35)
        self.lineEdit.move(0, 274)

        self.textEdit = QPlainTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.resize(460, 200)
        self.textEdit.move(20, 0)

        self.btn_info = QPushButton(self)
        self.btn_info.resize(120, 27)
        self.btn_info.setStyleSheet("background-image : url(assets/files_for_mark/information.png);")
        self.btn_info.move(185, 203)
        self.btn_info.clicked.connect(self.get_info)

    def add_text(self):
        """добавление строки в файл"""
        f = open('assets/files_for_mark/data.txt', mode='a', encoding='utf8')
        if self.lineEdit.text():
            f.write(self.lineEdit.text() + "\n")
        f.close()

    def get_text(self):
        """получение текста в окно"""
        self.textEdit.clear()
        f = open('assets/files_for_mark/data.txt', mode='r', encoding='utf8')
        data = [i.strip() for i in f]
        for elem in data:
            self.textEdit.appendPlainText(elem)
        f.close()

    def remove_text(self):
        """Удаление полученной с лайнэдита строки"""
        f = open('assets/files_for_mark/data.txt', mode='r', encoding='utf8')
        data = [i.strip() for i in f]
        if self.lineEdit.text() in data:
            data.remove(self.lineEdit.text())
        f.close()

        f = open('assets/files_for_mark/data.txt', mode='w', encoding='utf8')
        for elem in data:
            f.write(elem + "\n")
        f.close()

    def get_info(self):
        self.information = InformationMarks()
        self.information.show()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


class InformationMarks(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 300, 400, 157)
        self.setFixedSize(400, 157)
        self.setWindowTitle('Информация')
        self.info_label = QLabel(self)
        self.info_label.setPixmap(QPixmap("assets/files_for_mark/hint_marks.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mark = Mark()
    sys.excepthook = except_hook
    mark.show()
    sys.exit(app.exec())
