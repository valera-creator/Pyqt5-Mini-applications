import sys
import os
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QRadioButton, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl
from save_bd_results import write_sqlite


class MinPadding(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        """
        расшифровка значений на кнопках
    
        '' - 'чистая клетка'
        '  ' -  'заминировано'
        '   ' - сюда уже сходили
        """

    def initUI(self):
        self.setGeometry(400, 300, 800, 550)
        self.setFixedSize(800, 550)
        self.setWindowTitle("Минер")
        self.first_road = []
        self.second_road = []
        self.fon_label = QLabel(self)
        self.fon_label.resize(800, 550)
        self.fon_label.setPixmap(QPixmap("assets/files_for_min_padding/fon_for_mines.png"))

        self.is_motota_miner = False
        self.is_sahareg_miner = True
        self.end_game = False
        self.is_three_mines = False
        self.cnt_mines = 0

        self.qradio_motota = QRadioButton(self)
        self.qradio_motota.move(30 + 377, 20)
        self.qradio_motota.clicked.connect(self.replace_miner)
        self.label_motota = QLabel(self)
        self.label_motota.move(327, 0)
        self.label_motota.resize(70, 70)
        self.label_motota.setPixmap(QPixmap("assets/files_for_min_padding/motota.png"))

        self.qradio_sahareg = QRadioButton(self)
        self.qradio_sahareg.toggle()
        self.qradio_sahareg.move(355 + 365 - 261, 20)
        self.qradio_sahareg.clicked.connect(self.replace_miner)
        self.label_sahareg = QLabel(self)
        self.label_sahareg.move(380 - 261 + 365, 0)
        self.label_sahareg.resize(70, 70)
        self.label_sahareg.setPixmap(QPixmap("assets/files_for_min_padding/sahareg.png"))

        self.make_buttons(self.first_road, 0)
        self.make_buttons(self.second_road, 110)

        self.label_info_arrange = QLabel(self)
        self.label_info_arrange.resize(80, 21)
        self.label_info_arrange.setPixmap(QPixmap("assets/files_for_min_padding/arrange.png"))
        self.label_info_arrange.move(400, 185)

        self.btn_new_game = QPushButton(self)
        self.btn_new_game.move(220, 315)
        self.btn_new_game.setStyleSheet("background-image : url(assets/files_for_min_padding/min_padding_restart.png);")
        self.btn_new_game.clicked.connect(self.make_new_game)

        self.label_go = QLabel(self)
        self.label_go.setPixmap(QPixmap("assets/files_for_min_padding/lets_go.png"))
        self.label_go.move(400, 78)
        self.label_go.resize(0, 0)

        self.label_kill_miner = QLabel(self)
        self.label_kill_miner.resize(70, 70)
        self.label_kill_miner.move(0, 360)

        self.btn_info = QPushButton(self)
        self.btn_info.setStyleSheet("background-image : url(assets/files_for_min_padding/information.png);")
        self.btn_info.clicked.connect(self.check_info)
        self.btn_info.resize(120, 27)
        self.btn_info.move(210, 375)

        self.label_killed = QLabel(self)
        self.label_killed.resize(80, 80)
        self.label_killed.move(100, 360)

        for i in range(10):
            self.label_valera = QLabel(self)
            self.label_valera.resize(80, 80)
            self.label_valera.setPixmap(QPixmap("assets/files_for_min_padding/valera.jpg"))
            self.label_valera.move(i * 80, 470)

    def replace_miner(self):
        self.make_sound('assets/files_for_min_padding/sound_click.mp3')
        if self.qradio_motota.isChecked():
            self.qradio_motota.toggle()
            self.is_motota_miner = True
            self.is_sahareg_miner = False
        else:
            self.qradio_sahareg.toggle()
            self.is_motota_miner = False
            self.is_sahareg_miner = True
        self.make_new_game()

    def arrenge_mines(self):
        """
        блокировка смены минера
        проверка на корректность расставления мин
        минёрство трех полей
        запрет минить заминированное поле и верхнее|нижнее ему
        """

        self.qradio_sahareg.setEnabled(False)
        self.qradio_motota.setEnabled(False)
        self.make_sound('assets/files_for_min_padding/sound_click.mp3')
        if self.sender().text() == '':
            self.cnt_mines += 1
            self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/mine.png);")
            self.sender().setText("  ")
            if self.sender() in self.first_road:
                self.second_road[self.first_road.index(self.sender())].setText("    ")
            else:
                self.first_road[self.second_road.index(self.sender())].setText("    ")

            if self.cnt_mines == 3:
                self.is_three_mines = True
                self.label_info_arrange.resize(0, 0)
                self.make_sound('assets/files_for_min_padding/bombpl.mp3')
                self.label_go.resize(80, 21)
                man = 'sahareg.png' if self.is_sahareg_miner else 'motota.png'
                for i in range(len(self.first_road)):
                    self.first_road[i].setStyleSheet(f"background-image : url(assets/files_for_min_padding/{man});")
                    self.second_road[i].setStyleSheet(f"background-image : url(assets/files_for_min_padding/{man});")
        else:
            self.make_sound('assets/files_for_min_padding/ben_no.mp3')

    def make_end_game(self):
        self.end_game = True
        self.make_sound('assets/files_for_min_padding/sound_kill_mines.mp3')
        if self.is_motota_miner:
            self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/killed_sahareg.png);")
            write_sqlite('Минер', 'Мотота')
        else:
            self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/killed_motota.png);")
            write_sqlite('Минер', 'Сахареж')
        self.label_go.resize(0, 0)

    def check_road_in_zero(self, main_road, no_main_road):
        """
        проверка самых левых клетки
        main_road - список кнопок дороги, в которую кликнул игрок
        no_main_road - список кнопок второй дороги
        подстройка картинок
        """

        if main_road[0].text() == "  ":
            self.make_end_game()
        else:
            if self.is_motota_miner:
                self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/sahareg.png);")
            else:
                self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/motota.png);")
            self.sender().setText("   ")
            no_main_road[0].setText("   ")

    def check_road_one_eight(self, main_road, no_main_road):
        """
        проверка с 1 по не последнюю клетку
        проверяется совершенность хода в прыдыдущей клетки
        происходит подстройка картинок
        """

        if main_road[main_road.index(self.sender()) - 1].text() != "   " and \
                no_main_road[main_road.index(self.sender()) - 1].text() != "   ":
            self.make_sound('assets/files_for_min_padding/ben_no.mp3')
        elif self.sender().text() == "  ":
            self.make_end_game()
        else:
            self.sender().setText("   ")
            no_main_road[main_road.index(self.sender())].setText("   ")
            if self.is_motota_miner:
                self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/sahareg.png);")
            else:
                self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/motota.png);")

    def check_road_in_end(self, main_road, no_main_road):
        """проверка дошел игрок или взорвался, корректность хода, запись в БД, подстройка картинок"""

        if main_road[8].text() != "   " and no_main_road[8].text() != "   ":
            self.make_sound('assets/files_for_min_padding/ben_no.mp3')
        elif main_road[9].text() != '  ':
            main_road[9].setText("   ")
            no_main_road[9].setText("   ")
            self.label_kill_miner.resize(80, 80)
            self.make_sound('assets/files_for_min_padding/pistol_sound.mp3')
            self.label_killed.resize(80, 80)
            if not self.is_motota_miner:
                self.label_kill_miner.setPixmap(QPixmap('assets/files_for_min_padding/motota.png'))
                self.label_killed.setPixmap(QPixmap('assets/files_for_min_padding/killed_sahareg.png'))
                self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/motota.png);")
                write_sqlite('Минер', 'Мотота')
            else:
                self.label_kill_miner.setPixmap(QPixmap('assets/files_for_min_padding/sahareg.png'))
                self.label_killed.setPixmap(QPixmap('assets/files_for_min_padding/killed_motota.png'))
                self.sender().setStyleSheet("background-image : url(assets/files_for_min_padding/sahareg.png);")
                write_sqlite('Минер', 'Сахареж')
            self.end_game = True
            self.label_go.resize(0, 0)

        else:
            self.make_end_game()

    def check_going(self):
        """вызов функции в зависимости от позиции на которой находится проходящий игрок при корректном ходе"""

        if not self.end_game:
            self.make_sound('assets/files_for_min_padding/sound_click.mp3')
            if self.sender().text() == '   ':
                self.make_sound('assets/files_for_min_padding/ben_no.mp3')
            elif self.sender() in self.first_road and self.first_road.index(self.sender()) == 0:
                self.check_road_in_zero(self.first_road, self.second_road)
            elif self.sender() in self.second_road and self.second_road.index(self.sender()) == 0:
                self.check_road_in_zero(self.second_road, self.first_road)

            elif self.sender() in self.first_road and 1 <= self.first_road.index(self.sender()) <= 8:
                self.check_road_one_eight(self.first_road, self.second_road)
            elif self.sender() in self.second_road and 1 <= self.second_road.index(self.sender()) <= 8:
                self.check_road_one_eight(self.second_road, self.first_road)

            elif self.sender() in self.first_road and self.first_road.index(self.sender()) == 9:
                self.check_road_in_end(self.first_road, self.second_road)
            elif self.sender() in self.second_road and self.second_road.index(self.sender()) == 9:
                self.check_road_in_end(self.second_road, self.first_road)

    def define_action(self):
        """проверка нужно расставить мины или ходить"""
        if not self.is_three_mines:
            self.arrenge_mines()
        else:
            self.check_going()

    def restart_buttons(self):
        """добавление на все кнопки картинки минера"""
        for i in range(len(self.first_road)):
            if self.is_sahareg_miner:
                self.first_road[i].setStyleSheet("background-image : url(assets/files_for_min_padding/sahareg.png);")
                self.second_road[i].setStyleSheet("background-image : url(assets/files_for_min_padding/sahareg.png);")
            else:
                self.first_road[i].setStyleSheet("background-image : url(assets/files_for_min_padding/motota.png);")
                self.second_road[i].setStyleSheet("background-image : url(assets/files_for_min_padding/motota.png);")
            self.second_road[i].setText("")
            self.first_road[i].setText("")

    def make_new_game(self):
        self.qradio_sahareg.setEnabled(True)
        self.qradio_motota.setEnabled(True)
        if self.qradio_motota.isChecked():
            self.is_motota_miner = True
            self.is_sahareg_miner = False
        else:
            self.is_sahareg_miner = True
            self.is_motota_miner = False

        self.is_three_mines = False
        self.cnt_mines = 0
        self.end_game = False
        self.label_info_arrange.resize(80, 21)
        self.label_go.resize(0, 0)
        self.restart_buttons()
        self.label_kill_miner.resize(0, 0)
        self.label_killed.resize(0, 0)

    def make_buttons(self, button_grid, j):
        """
        добавление в переданный список кнопок
        button_grid - переданный список
        j - координаты для расстановки
        """
        for i in range(10):
            button_grid.append(QPushButton(self))
            button_grid[i].resize(80, 80)
            button_grid[i].move(i * 80, 100 + j)
            button_grid[i].clicked.connect(self.define_action)
            if self.is_sahareg_miner:
                button_grid[i].setStyleSheet("background-image : url(assets/files_for_min_padding/sahareg.png);")
            else:
                button_grid[i].setStyleSheet("background-image : url(assets/files_for_min_padding/motota.png);")

    def check_info(self):
        self.info = InformationMinPadding()
        self.info.show()

    def make_sound(self, name_file):
        self.player = QMediaPlayer()
        full_file_path = os.path.join(os.getcwd(), name_file)
        url = QUrl().fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


class InformationMinPadding(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(672, 265, 921, 600)
        self.setFixedSize(921, 600)
        self.setWindowTitle('Информация')
        self.info_label = QLabel(self)
        self.info_label.setPixmap(QPixmap("assets/files_for_min_padding/hint_mines.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    min_padding = MinPadding()
    min_padding.show()
    sys.exit(app.exec())
