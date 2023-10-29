import sys
import os
from random import choice
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl, QTimer
from save_bd_results import write_sqlite


class RussianRoulette(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 319)
        self.setFixedSize(500, 310)
        self.setWindowTitle('Русская рулетка')
        self.fon_label = QLabel(self)
        self.fon_label.resize(500, 319)
        self.fon_label.setPixmap(QPixmap('assets/files_for_roulette/fon_roulette.jpg'))

        self.btn_killer = QPushButton(self)
        self.btn_killer.move(150, 14)
        self.btn_killer.resize(200, 102)
        self.btn_killer.setStyleSheet("background-image : url(assets/files_for_roulette/pistol.png);")
        self.btn_killer.clicked.connect(self.start_animation_kill)

        self.btn_info_roulette = QPushButton(self)
        self.btn_info_roulette.move(190, 279)
        self.btn_info_roulette.resize(120, 27)
        self.btn_info_roulette.clicked.connect(self.check_information)
        self.btn_info_roulette.setStyleSheet("background-image : url(assets/files_for_roulette/information.png);")

        self.label_motota_live = QLabel(self)
        self.label_motota_live.setPixmap(QPixmap('assets/files_for_roulette/motota.png'))
        self.label_motota_live.move(171, 124)

        self.label_sahareg_live = QLabel(self)
        self.label_sahareg_live.setPixmap(QPixmap("assets/files_for_roulette/sahareg.png"))
        self.label_sahareg_live.move(251, 124)

        self.label_sahareg_live.setPixmap(QPixmap("assets/files_for_roulette/sahareg.png"))
        self.label_motota_live.setPixmap(QPixmap('assets/files_for_roulette/motota.png'))

    def make_sound_shot(self):
        self.player = QMediaPlayer()
        full_file_path = os.path.join(os.getcwd(), 'assets/files_for_roulette/pistol_sound.mp3')
        url = QUrl().fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def start_animation_kill(self):
        """воспроизведение звука и временный показ убитого игрока, запись в БД"""
        self.make_sound_shot()
        self.timer = QTimer()
        killed = choice(["мотота", 'сахареж'])
        if killed == 'мотота':
            self.label_motota_live.setPixmap(QPixmap("assets/files_for_roulette/killed_motota.png"))
            write_sqlite('Русская рулетка', 'Сахареж')
        else:
            self.label_sahareg_live.setPixmap(QPixmap("assets/files_for_roulette/killed_sahareg.png"))
            write_sqlite('Русская рулетка', 'Мотота')
        self.timer.singleShot(500, self.make_standart_image)

    def make_standart_image(self):
        self.label_motota_live.setPixmap(QPixmap('assets/files_for_roulette/motota.png'))
        self.label_sahareg_live.setPixmap(QPixmap("assets/files_for_roulette/sahareg.png"))

    def check_information(self):
        self.information = InformationRoulette()
        self.information.show()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


class InformationRoulette(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 300, 300, 300)
        self.setFixedSize(300, 300)
        self.setWindowTitle('Информация')
        self.info_label = QLabel(self)
        self.info_label.setPixmap(QPixmap("assets/files_for_roulette/hint_roulette.jpg"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    roulette = RussianRoulette()
    sys.excepthook = except_hook
    roulette.show()
    sys.exit(app.exec())
