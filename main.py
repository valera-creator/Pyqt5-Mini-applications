import sys
from sports import SportsInfo
from russian_roulette import RussianRoulette
from tic_tac import TicTacToe
from sound_window import Sounds
from mini_sea_battle import MiniSeaBattle
from min_padding import MinPadding
from marks import Mark
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from statistic import Statistic


class StartMiniGames(QWidget):
    """главный класс всего приложения, запускающий все мини-приложения"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 800, 720)
        self.setFixedSize(800, 720)
        self.setWindowTitle('Главное меню')

        self.fon1_label = QLabel(self)
        self.fon1_label.resize(800, 720)
        self.fon1_label.move(0, 320)
        self.fon1_label.setPixmap(QPixmap('assets/files_for_main/fon.jpg'))

        self.fon2_label = QLabel(self)
        self.fon2_label.resize(800, 320)
        self.fon2_label.setPixmap(QPixmap('assets/files_for_main/image_of_the_players_and_the_author.png'))

        self.btn_roulette = QPushButton(self)
        self.btn_roulette.resize(100, 100)
        self.btn_roulette.clicked.connect(self.start_roulette)
        self.btn_roulette.move(550, 505)
        self.btn_roulette.setStyleSheet("background-image : url(assets/files_for_main/fon_roulette.png);")

        self.btn_tic_tac = QPushButton(self)
        self.btn_tic_tac.resize(100, 100)
        self.btn_tic_tac.clicked.connect(self.start_tic_tac)
        self.btn_tic_tac.move(350, 345)
        self.btn_tic_tac.setStyleSheet("background-image : url(assets/files_for_main/fon_tic_tac);")

        self.btn_sounds = QPushButton(self)
        self.btn_sounds.resize(100, 100)
        self.btn_sounds.clicked.connect(self.start_sounds)
        self.btn_sounds.move(550, 345)
        self.btn_sounds.setStyleSheet("background-image : url(assets/files_for_main/fon_sounds);")

        self.btn_mini_sea_battle = QPushButton(self)
        self.btn_mini_sea_battle.resize(100, 100)
        self.btn_mini_sea_battle.clicked.connect(self.start_mini_sea_battle)
        self.btn_mini_sea_battle.move(150, 505)
        self.btn_mini_sea_battle.setStyleSheet("background-image : url(assets/files_for_main/fon_mini_sea_battle);")

        self.btn_min_padding = QPushButton(self)
        self.btn_min_padding.resize(100, 100)
        self.btn_min_padding.clicked.connect(self.start_min_padding)
        self.btn_min_padding.move(350, 505)
        self.btn_min_padding.setStyleSheet("background-image : url(assets/files_for_main/fon_min_padding);")

        self.btn_marks = QPushButton(self)
        self.btn_marks.resize(100, 100)
        self.btn_marks.clicked.connect(self.start_marks)
        self.btn_marks.move(150, 345)
        self.btn_marks.setStyleSheet("background-image : url(assets/files_for_main/fon_marks);")

        self.sport_achievemnt = QPushButton(self)
        self.sport_achievemnt.resize(158, 43)
        self.sport_achievemnt.move(0, 666)
        self.sport_achievemnt.setStyleSheet("background-image : url(assets/files_for_main/fon_sports.png);")
        self.sport_achievemnt.clicked.connect(self.check_sport)

        self.btn_statistics = QPushButton(self)
        self.btn_statistics.resize(158, 43)
        self.btn_statistics.setStyleSheet("background-image : url(assets/files_for_main/fon_staticitc.png);")
        self.btn_statistics.move(643, 666)
        self.btn_statistics.clicked.connect(self.check_statistic)

        self.btn_info = QPushButton(self)
        self.btn_info.resize(300, 58)
        self.btn_info.move(250, 655)
        self.btn_info.setStyleSheet("background-image : url(assets/files_for_main/information.png);")
        self.btn_info.clicked.connect(self.check_info)
        self.btn_info.setStyleSheet("background-image : url(assets/files_for_main/information.png);")

    def check_sport(self):
        self.sport = SportsInfo()
        self.sport.show()

    def start_roulette(self):
        self.roulette = RussianRoulette()
        self.roulette.show()

    def start_tic_tac(self):
        self.tic_tac = TicTacToe()
        self.tic_tac.show()

    def start_sounds(self):
        self.sounds = Sounds()
        self.sounds.show()

    def start_mini_sea_battle(self):
        self.sea_battle = MiniSeaBattle()
        self.sea_battle.show()

    def start_min_padding(self):
        self.min_padding_ex = MinPadding()
        self.min_padding_ex.show()

    def start_marks(self):
        self.mark = Mark()
        self.mark.show()

    def check_info(self):
        self.info = InformationMain()
        self.info.show()

    def check_statistic(self):
        self.statistic = Statistic()
        self.statistic.show()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


class InformationMain(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(717, 333, 559, 187)
        self.setFixedSize(559, 187)
        self.setWindowTitle('Информация')
        self.info_label = QLabel(self)
        self.info_label.setPixmap(QPixmap("assets/files_for_main/hint.jpg"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_minigames = StartMiniGames()
    sys.excepthook = except_hook
    start_minigames.show()
    sys.exit(app.exec())
