import sys
import os
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QRadioButton, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl
from save_bd_results import write_sqlite


class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.translate_players = {"  ": 'X', "   ": 'O', "": ""}
        """два пробела - сходил x, 3 пробела - сходил o, пустота - никто не сходил"""

    def initUI(self):
        """ориентир на X и O, но отображаться будут картинки на экране"""
        self.setGeometry(400, 300, 280, 495)
        self.setFixedSize(280, 495)
        self.fon_label = QLabel(self)
        self.fon_label.resize(280, 500)
        self.button_grid = []
        self.fon_label.setPixmap(QPixmap("assets/files_for_tic_tac/fon_tic_tac.png"))
        self.setWindowTitle('Крестики-нолики')

        self.label_x = QLabel(self)
        self.label_x.setPixmap(QPixmap("assets/files_for_tic_tac/motota.png"))
        self.label_x.resize(75, 75)
        self.label_x.move(25, 0)

        self.label_o = QLabel(self)
        self.label_o.setPixmap(QPixmap("assets/files_for_tic_tac/sahareg.png"))
        self.label_o.resize(75, 75)
        self.label_o.move(179, 0)

        self.btn_info_tic_tac = QPushButton(self)
        self.btn_info_tic_tac.setStyleSheet("background-image : url(assets/files_for_tic_tac/information.png);")
        self.btn_info_tic_tac.resize(120, 27)
        self.btn_info_tic_tac.move(82, 464)
        self.btn_info_tic_tac.clicked.connect(self.check_information)

        self.x = QRadioButton(self)
        self.x.toggle()
        self.x.move(115, 10)
        self.x.clicked.connect(self.replace_going)

        self.o = QRadioButton(self)
        self.o.move(155, 10)
        self.o.clicked.connect(self.replace_going)

        self.add_buttom()

        self.result = QLabel(self)
        self.result.move(135, 385)

        self.new_game = QPushButton(self)
        self.new_game.move(90, 342)
        self.new_game.resize(100, 40)
        self.new_game.clicked.connect(self.make_new_game)
        self.new_game.setStyleSheet("background-image : url(assets/files_for_tic_tac/restart.png);")

        self.GO_X = True
        self.GO_O = False

        self.label_winner = QLabel(self)

    def replace_going(self):
        """выбор того, кто будет первый ходить"""
        self.make_sound('assets/files_for_tic_tac/sound_click.mp3')
        if self.x.isChecked():
            self.x.toggle()
            self.GO_X = True
            self.GO_O = False
        else:
            self.o.toggle()
            self.GO_X = False
            self.GO_O = True
        self.make_new_game()

    def add_buttom(self):
        """добавление всех кнопок в списки"""
        for i in range(3):
            string = []
            for j in range(3):
                string.append(QPushButton(self))
                string[j].resize(80, 80)
                string[j].move(i * 80 + 22, j * 80 + 103)
                string[j].clicked.connect(self.action)
                string[j].setStyleSheet(r"background-image : url(assets/files_for_tic_tac/valera.jpg);")
            self.button_grid.append(string)

    def load_image_result(self):
        """загрузка результата изображения и добавления результата в БД"""
        self.label_winner.move(105, 389)
        self.label_winner.resize(74, 72)
        if self.result.text() == "Выиграл X!":
            self.label_winner.setPixmap(QPixmap("assets/files_for_tic_tac/motota_winner.png"))
            write_sqlite('Крестики-нолики', 'Мотота')
            self.make_sound('assets/files_for_tic_tac/winner_sound.mp3')
        elif self.result.text() == 'Выиграл O!':
            self.label_winner.setPixmap(QPixmap("assets/files_for_tic_tac/sahareg_winner.png"))
            self.make_sound('assets/files_for_tic_tac/winner_sound.mp3')
            write_sqlite('Крестики-нолики', "Сахареж")
        else:
            self.label_winner.setPixmap(QPixmap("assets/files_for_tic_tac/draw_tic_tac.png"))
            write_sqlite('Крестики-нолики', "Ничья")
            self.make_sound('assets/files_for_tic_tac/draw_sound.mp3')
        self.result.clear()

    def action(self):
        """
        Данная функция блокирует выбор первого хода, проверяет корректность хода,
        Воспроизводит звук и проверяет конец игры
        """

        self.x.setEnabled(False)
        self.o.setEnabled(False)
        if not self.sender().text():
            self.make_sound('assets/files_for_tic_tac/sound_click.mp3')
            if self.GO_X:
                self.sender().setText("  ")
                self.GO_X = False
                self.GO_O = True
                self.sender().setStyleSheet("background-image : url(assets/files_for_tic_tac/motota.png);")
            else:
                self.GO_O = False
                self.GO_X = True
                self.sender().setText("   ")
                self.sender().setStyleSheet("background-image : url(assets/files_for_tic_tac/sahareg.png);")
            self.check_end_game()
        else:
            self.make_sound('assets/files_for_tic_tac/ben_no.mp3')

    def check_end_game(self):
        check_matrix = []
        for i in range(len(self.button_grid)):
            line = []
            for j in range(len(self.button_grid[i])):
                line.append(self.translate_players[self.button_grid[i][j].text()])
            check_matrix.append(line)
        string = "".join(check_matrix[0]) + "".join(check_matrix[1]) + "".join(check_matrix[2])
        if "".join(check_matrix[0]).count("X") == 3 or "".join(check_matrix[1]).count("X") == 3 or \
                "".join(check_matrix[2]).count("X") == 3:
            self.result.setText("Выиграл X!")
        elif "".join(check_matrix[0]).count("O") == 3 or "".join(check_matrix[1]).count("O") == 3 or \
                "".join(check_matrix[2]).count("O") == 3:
            self.result.setText("Выиграл O!")

        elif check_matrix[0][0] == "X" and check_matrix[1][0] == "X" and check_matrix[2][0] == "X":
            self.result.setText("Выиграл X!")
        elif check_matrix[0][1] == "X" and check_matrix[1][1] == "X" and check_matrix[2][1] == "X":
            self.result.setText("Выиграл X!")
        elif check_matrix[0][2] == "X" and check_matrix[1][2] == "X" and check_matrix[2][2] == "X":
            self.result.setText("Выиграл X!")

        elif check_matrix[0][0] == "O" and check_matrix[1][0] == "O" and check_matrix[2][0] == "O":
            self.result.setText("Выиграл O!")
        elif check_matrix[0][1] == "O" and check_matrix[1][1] == "O" and check_matrix[2][1] == "O":
            self.result.setText("Выиграл O!")
        elif check_matrix[0][2] == "O" and check_matrix[1][2] == "O" and check_matrix[2][2] == "O":
            self.result.setText("Выиграл O!")

        elif check_matrix[0][0] == "X" and check_matrix[1][1] == "X" and check_matrix[2][2] == "X":
            self.result.setText("Выиграл X!")
        elif check_matrix[0][0] == "O" and check_matrix[1][1] == "O" and check_matrix[2][2] == "O":
            self.result.setText("Выиграл O!")

        elif check_matrix[0][2] == "X" and check_matrix[1][1] == "X" and check_matrix[2][0] == "X":
            self.result.setText("Выиграл X!")
        elif check_matrix[0][2] == "O" and check_matrix[1][1] == "O" and check_matrix[2][0] == "O":
            self.result.setText("Выиграл O!")

        elif string.count("O") + string.count("X") == 9:
            self.result.setText("Ничья!")

        if self.result.text():
            for i in range(len(self.button_grid)):
                for j in range(len(self.button_grid[i])):
                    self.button_grid[i][j].setEnabled(False)
            self.load_image_result()

    def make_new_game(self):
        self.x.setEnabled(True)
        self.o.setEnabled(True)
        self.result.clear()
        self.label_winner.resize(0, 0)
        if self.x.isChecked():
            self.GO_X = True
            self.GO_O = False
        else:
            self.GO_O = True
            self.GO_X = False
        for i in range(len(self.button_grid)):
            for j in range(len(self.button_grid[i])):
                self.button_grid[i][j].setStyleSheet(r"background-image : url(assets/files_for_tic_tac/valera.jpg);")
                self.button_grid[i][j].setText("")
                self.button_grid[i][j].setEnabled(True)

    def check_information(self):
        self.information_tic_tac = InformationTicTac()
        self.information_tic_tac.show()

    def make_sound(self, sound_file):
        self.player = QMediaPlayer()
        full_file_path = os.path.join(os.getcwd(), sound_file)
        url = QUrl().fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


class InformationTicTac(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(674, 402, 280, 294)
        self.setFixedSize(280, 294)
        self.setWindowTitle('Информация')
        self.info_label = QLabel(self)
        self.info_label.setPixmap(QPixmap("assets/files_for_tic_tac/hint_tic_tac.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    tt = TicTacToe()
    tt.show()
    sys.exit(app.exec())
