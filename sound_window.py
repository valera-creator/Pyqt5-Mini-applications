import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl


class Sounds(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 459, 352)
        self.setFixedSize(459, 352)
        self.setWindowTitle('Звуковая комната')
        self.fon_label = QLabel(self)
        self.fon_label.resize(459, 352)
        self.fon_label.setPixmap(QPixmap('assets/files_for_sounds_window/fon.png'))

        self.btn_select_sound = QPushButton(self)
        self.btn_select_sound.resize(193, 85)
        self.btn_select_sound.move(131, 133)
        self.btn_select_sound.setStyleSheet("background-image : url(assets/files_for_sounds_window/select_sound.jpg);")
        self.btn_select_sound.clicked.connect(self.get_namefiles)

        self.all_sounds = {'неработающий звук (не нажимать)': 'assets/files_for_sounds_window/scrim2.wav',
                           'Валера ломает силовой аппарат': 'assets/files_for_sounds_window/ha.wav',
                           'нам задали выучить изложение': 'assets/files_for_sounds_window/learn_presentation.wav',
                           'мы кароче приложили карту к этой фигне': 'assets/files_for_sounds_window/fignia.wav',
                           'файлы, файлы, файлы': 'assets/files_for_sounds_window/files_files_files.wav',
                           'ну я то аморал, я и не забрал': 'assets/files_for_sounds_window/amoral.wav',
                           'Payday 2 - No Mercy': 'assets/files_for_sounds_window/no_mercy.wav',
                           'Payday 2 Official Soundtrack - Left In The Cold (Assault)':
                               "assets/files_for_sounds_window/payday2_track.wav",
                           'Funk_Tribu': "assets/files_for_sounds_window/Funk_Tribu.mp3",
                           'дэбил': 'assets/files_for_sounds_window/debil.wav',
                           'непонятный звук Валеры': 'assets/files_for_sounds_window/incomprehensibility1.wav',
                           'непонятные звуки Валеры в больнице после перелома': 'assets/files_for_sounds_window/hospital.wav',
                           'девочка танцует одна': 'assets/files_for_sounds_window/enveel.mp3',
                           'Ella & Парнишка - Мы умрем где-то посреди ночи (tiktok remix)':
                               'assets/files_for_sounds_window/silence_ellipsis.mp3',
                           'agressive fonk: gqtis - POOR': 'assets/files_for_sounds_window/gqtis-POOR.mp3',
                           'agressive fonk: zxcursed - supernxva': 'assets/files_for_sounds_window/zxcursed-supernxva.wav',
                           'agressive fonk: ANTIQUE - HERE I COME': 'assets/files_for_sounds_window/here_i_come.mp3',
                           'agressive fonk: $werve x $pidxrs808 - BALADINHA SINISTRA ':
                               'assets/files_for_sounds_window/baladinha.mp3',
                           'DEVILNOTCRY - ImpulsesHardstyle': 'assets/files_for_sounds_window/DEVILNOTCRY-ImpulsesHardstyle.mp3',
                           'да, тоже заметил?': 'assets/files_for_sounds_window/yes.wav',
                           'чето я не могу': 'assets/files_for_sounds_window/ne_mogy.wav',
                           'встань в мид': 'assets/files_for_sounds_window/mid.wav',
                           'ты же так хотела, чтобы я покинул тело (my remix)': 'assets/files_for_sounds_window/telo.wav',
                           'MORGENSHTERN: а мы все дальше живем': 'assets/files_for_sounds_window/life.wav',
                           'discord': 'assets/files_for_sounds_window/ds.wav',
                           'странный звук мототы': 'assets/files_for_sounds_window/detei.wav',
                           'весь кросовок промочил': 'assets/files_for_sounds_window/puddle.wav',
                           'бен взял трубку': 'assets/files_for_sounds_window/ben.mp3',
                           'бен говорит yes': 'assets/files_for_sounds_window/ben_yes.mp3',
                           'бен говорит no': 'assets/files_for_sounds_window/ben_no.mp3',
                           'выключить аудио': ''}

    def get_namefiles(self):
        name_sound, ok_pressed = QInputDialog.getItem(
            self, "Выбор звука", "Выберите звук",
            list(self.all_sounds.keys()), 0, False)
        if ok_pressed:
            self.make_sound(name_sound)

    def make_sound(self, name):
        self.player = QMediaPlayer()
        full_file_path = os.path.join(os.getcwd(), self.all_sounds[name])
        url = QUrl().fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def closeEvent(self, event):
        self.player = QMediaPlayer()
        self.player.stop()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sounds = Sounds()
    sys.excepthook = except_hook
    sounds.show()
    sys.exit(app.exec())
