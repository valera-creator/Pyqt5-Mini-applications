import sys
import os
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QRadioButton, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl
from save_bd_results import write_sqlite


def hide_images(button_grid):
    """скрытие кораблей после законченной расстановки в списке button_grid"""
    for i in range(len(button_grid)):
        for j in range(len(button_grid[i])):
            button_grid[i][j].setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/water.png);")


def check_coords(sender, button_grid):
    """возвращение позиций в button_grid, где находится элемент sender"""
    for i in range(len(button_grid)):
        for j in range(len(button_grid[i])):
            if button_grid[i][j] == sender:
                return i, j


def check_ship_in_nearby(i, j, button_grid):
    """
    проверка что рядом нет расставленых кораблей в списке кнопок button_grid от button_grid[i][j]
    при i == -1 и j == -1 нарушается логика проверки, т.к проверяется самый левый и самый правый элемент
    исключение возникает если передали для проверки самый правый или самый нижний элемент в списке
    """
    try:
        if i == -1 or j == -1:
            return True
        return button_grid[i][j].text() == ""
    except IndexError:
        return True


def replace_image(i, j, button_grid):
    """
    изменение 9 картинок, включая там, где был уничтоженный корабль
    если i == -1 или j == -1, то будет нарушена логика проверки, будут задействованы противоположные стороны полей
    если передан самый правый или нижний элемент, то ничего не делать
    """
    try:
        if i == -1 or j == -1:
            pass
        else:
            button_grid[i][j].setText('  ')
            button_grid[i][j].setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/valera.jpg);")
    except IndexError:
        pass


def check_correct_ship(sender, button_grid):
    """проход по матрице и проверка всех значений, что везде пустая клетка"""
    if sender.text():
        return False
    check_i, check_j = check_coords(sender, button_grid)
    for i in range(check_i - 1, check_i + 2):
        for j in range(check_j - 1, check_j + 2):
            if not check_ship_in_nearby(i, j, button_grid):
                return False
    return True


def see_ships(button_grid, image):
    """показать картинку image там, где выжившие корабли в поле button_grid"""
    for i in range(len(button_grid)):
        for j in range(len(button_grid[i])):
            if button_grid[i][j].text() == '   ':
                button_grid[i][j].setStyleSheet(f"background-image : url({image});")


class MiniSeaBattle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        """
        расшифровка значений на кнопках
        
        '' - 'пустая клетка'
        '  ' -  'нельзя ставить корабль, он уже стоит рядом или был уничтожен рядом'
        '   ' - 'стоит корабль'
        '    ' - 'уничтоженный корабль'
        
        """

    def initUI(self):
        self.setGeometry(400, 300, 950, 600)
        self.setFixedSize(950, 600)
        self.motota_button_grid = []
        self.sahareg_button_grid = []
        self.setWindowTitle("Мини-морской бой")
        self.fon_label = QLabel(self)
        self.fon_label.resize(950, 600)
        self.fon_label.setPixmap(QPixmap("assets/files_for_mini_sea_battle/fon_water_ship.png"))

        self.is_motota_now_going = False
        self.is_sahareg_now_going = True

        self.is_four_ship_motota = False
        self.is_four_ship_sahareg = False
        self.cnt_ship_motota = 0
        self.cnt_ship_sahareg = 0

        self.qradio_motota = QRadioButton(self)
        self.qradio_motota.move(80 + 353, 20)
        self.qradio_motota.clicked.connect(self.replace_first_going)
        self.label_motota = QLabel(self)
        self.label_motota.move(353, 0)
        self.label_motota.resize(70, 70)
        self.label_motota.setPixmap(QPixmap("assets/files_for_mini_sea_battle/motota.png"))

        self.qradio_sahareg = QRadioButton(self)
        self.qradio_sahareg.toggle()
        self.qradio_sahareg.move(355 + 365 - 220, 20)
        self.qradio_sahareg.clicked.connect(self.replace_first_going)
        self.label_sahareg = QLabel(self)
        self.label_sahareg.move(380 - 220 + 365, 0)
        self.label_sahareg.resize(70, 70)
        self.label_sahareg.setPixmap(QPixmap("assets/files_for_mini_sea_battle/sahareg.png"))

        self.make_buttons(self.motota_button_grid, 0)
        self.make_buttons(self.sahareg_button_grid, 500)

        self.label_info_motota = QLabel(self)
        self.label_info_motota.resize(80, 21)
        self.label_info_motota.setPixmap(QPixmap("assets/files_for_mini_sea_battle/arrange.png"))
        self.label_info_motota.move(182, 71)

        self.label_info_sahareg = QLabel(self)
        self.label_info_sahareg.resize(80, 21)
        self.label_info_sahareg.setPixmap(QPixmap("assets/files_for_mini_sea_battle/arrange.png"))
        self.label_info_sahareg.move(682, 71)

        self.btn_new_game = QPushButton(self)
        self.btn_new_game.move(420, 500)
        self.btn_new_game.setStyleSheet(
            "background-image : url(assets/files_for_mini_sea_battle/mini_sea_restart.png);")
        self.btn_new_game.clicked.connect(self.make_new_game)

        self.end_game = False

        self.label_shot_him_motota = QLabel(self)
        self.label_shot_him_motota.setPixmap(QPixmap("assets/files_for_mini_sea_battle/shot_him.png"))
        self.label_shot_him_motota.move(682, 68)
        self.label_shot_him_motota.resize(0, 0)
        self.label_shot_him_sahareg = QLabel(self)
        self.label_shot_him_sahareg.setPixmap(QPixmap("assets/files_for_mini_sea_battle/shot_him.png"))
        self.label_shot_him_sahareg.move(182, 68)
        self.label_shot_him_sahareg.resize(0, 0)

        self.label_winner = QLabel(self)
        self.label_winner.resize(70, 70)

        self.btn_info = QPushButton(self)
        self.btn_info.setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/information.png);")
        self.btn_info.clicked.connect(self.check_info)
        self.btn_info.resize(120, 27)
        self.btn_info.move(412, 572)

    def replace_first_going(self):
        self.make_sound('assets/files_for_mini_sea_battle/sound_click.mp3')
        if self.qradio_motota.isChecked():
            self.qradio_motota.toggle()
            self.is_motota_now_going = True
            self.is_sahareg_now_going = False
        else:
            self.qradio_sahareg.toggle()
            self.is_motota_now_going = False
            self.is_sahareg_now_going = True
        self.make_new_game()

    def check_correct_click(self, button_grid):
        """проверка, не кликнул ли игрок в кнопку, находящуюся в button_grid"""
        for elem in button_grid:
            if self.sender() in elem:
                return False
        return True

    def arrange_motota_ship(self):
        """
        функция для расставления кораблей

        Принцип:
        блокировка переключателя первого игрока
        происходит проверка корректности расставления кораблей
        в случае корректной происходит расстановка корабля

        если расставлено 4 корабля, то:
        поднимается флаг расстановки для игрока
        изчезает надпись arrange полем игрока
        скрываются изображения кораблей
        очередь переходит к другому игроку

        если оба игрока расставили корабли, появляется кнопка стрелять в конкретного игрока
        """

        self.qradio_motota.setEnabled(False)
        self.qradio_sahareg.setEnabled(False)
        if self.check_correct_click(self.sahareg_button_grid):
            if check_correct_ship(self.sender(), self.motota_button_grid):
                self.sender().setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/motota.png);")
                self.sender().setText("   ")
                self.make_sound('assets/files_for_mini_sea_battle/sound_click.mp3')
                self.cnt_ship_motota += 1
                if self.cnt_ship_motota == 4:
                    self.label_info_motota.resize(0, 0)
                    self.is_four_ship_motota = True
                    self.is_sahareg_now_going = True
                    self.is_motota_now_going = False
                    hide_images(self.motota_button_grid)
                    if self.is_four_ship_sahareg and self.is_four_ship_motota:
                        self.label_shot_him_sahareg.resize(80, 21)
            else:
                self.make_sound('assets/files_for_mini_sea_battle/ben_no.mp3')
        else:
            self.make_sound('assets/files_for_mini_sea_battle/ben_no.mp3')

    def arrange_sahareg_ship(self):
        """принцип описан в методе arrange_motota_ship"""

        self.qradio_motota.setEnabled(False)
        self.qradio_sahareg.setEnabled(False)
        if self.check_correct_click(self.motota_button_grid):
            if check_correct_ship(self.sender(), self.sahareg_button_grid):
                self.make_sound('assets/files_for_mini_sea_battle/sound_click.mp3')
                self.sender().setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/sahareg.png);")
                self.sender().setText("   ")
                self.cnt_ship_sahareg += 1
                if self.cnt_ship_sahareg == 4:
                    self.label_info_sahareg.resize(0, 0)
                    self.is_four_ship_sahareg = True
                    self.is_sahareg_now_going = False
                    self.is_motota_now_going = True
                    hide_images(self.sahareg_button_grid)
                    if self.is_four_ship_sahareg and self.is_four_ship_motota:
                        self.label_shot_him_motota.resize(80, 21)
            else:
                self.make_sound('assets/files_for_mini_sea_battle/ben_no.mp3')
        else:
            self.make_sound('assets/files_for_mini_sea_battle/ben_no.mp3')

    def make_shot_motota(self):
        """
        проверка корректности хода
        если ход корректен, проверяется промах или попадание
        если промах, на кнопке меняется картинка и текст
        при попадании кнопка и 8 соседних кнопок в матрице меняют картинку и текст
        """

        if self.is_motota_now_going:
            if not self.check_correct_click(self.motota_button_grid):
                return False
            if self.sender().text() != "" and self.sender().text() != "   ":
                return False
            if self.sender().text() == "":
                self.make_sound('assets/files_for_mini_sea_battle/miss_motota.wav')
                self.sender().setText(" ")
                self.sender().setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/water_miss.png);")
                return True
            if self.sender().text() == "   ":
                self.make_sound('assets/files_for_mini_sea_battle/sound_kill_shot.mp3')
                check_i, check_j = check_coords(self.sender(), self.sahareg_button_grid)
                for i in range(check_i - 1, check_i + 2):
                    for j in range(check_j - 1, check_j + 2):
                        replace_image(i, j, self.sahareg_button_grid)
                self.sender().setText("    ")
                self.sender().setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/death_ship.png);")
                self.cnt_ship_sahareg -= 1
                return True

    def make_shot_sahareg(self):
        """принцип описан в методе make_shot_motota"""

        if self.is_sahareg_now_going:
            if not self.check_correct_click(self.sahareg_button_grid):
                return False
            if self.sender().text() != "" and self.sender().text() != "   ":
                return False
            if self.sender().text() == "":
                self.make_sound('assets/files_for_mini_sea_battle/miss_sahareg.wav')
                self.sender().setText(" ")
                self.sender().setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/water_miss.png);")
                return True
            if self.sender().text() == "   ":
                self.make_sound('assets/files_for_mini_sea_battle/sound_kill_shot.mp3')
                check_i, check_j = check_coords(self.sender(), self.motota_button_grid)
                for i in range(check_i - 1, check_i + 2):
                    for j in range(check_j - 1, check_j + 2):
                        replace_image(i, j, self.motota_button_grid)
                self.sender().setText("    ")
                self.sender().setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/death_ship.png);")
                self.cnt_ship_motota -= 1
                return True

    def check_motota_motion(self):
        """
        если корабли не расставлены, то расставлять корабли, иначе ходить
        если ход корректный, проверка на конец игры
        если конец игры, то поднимаем флаг self.end_game, делаем анимацию победы и запись в БД
        """

        if not self.is_four_ship_motota:
            self.arrange_motota_ship()
        else:
            res = self.make_shot_motota()
            if res:
                self.label_shot_him_sahareg.resize(80, 21)
                self.label_shot_him_motota.resize(0, 0)
                self.is_motota_now_going, self.is_sahareg_now_going = \
                    self.is_sahareg_now_going, self.is_motota_now_going
                if self.cnt_ship_sahareg == 0:
                    self.end_game = True
                    see_ships(self.motota_button_grid, "assets/files_for_mini_sea_battle/motota.png")
                    self.label_shot_him_motota.resize(0, 0)
                    self.label_shot_him_sahareg.resize(0, 0)
                    self.label_winner.resize(74, 74)
                    self.label_winner.setPixmap(QPixmap("assets/files_for_mini_sea_battle/motota_winner.png"))
                    self.label_winner.move(184, 18)
                    self.make_sound('assets/files_for_mini_sea_battle/winner_sound.mp3')
                    write_sqlite('Мини-морской бой', 'Мотота')

            else:
                self.make_sound('assets/files_for_mini_sea_battle/ben_no.mp3')

    def check_sahareg_motion(self):
        """принцип описан в методе check_motota_motion"""

        if not self.is_four_ship_sahareg:
            self.arrange_sahareg_ship()
        else:
            res = self.make_shot_sahareg()
            if res:
                self.label_shot_him_motota.resize(80, 21)
                self.label_shot_him_sahareg.resize(0, 0)
                self.is_motota_now_going, self.is_sahareg_now_going = \
                    self.is_sahareg_now_going, self.is_motota_now_going
                if self.cnt_ship_motota == 0:
                    self.end_game = True
                    see_ships(self.sahareg_button_grid, "assets/files_for_mini_sea_battle/sahareg.png")
                    self.label_shot_him_sahareg.resize(0, 0)
                    self.label_shot_him_motota.resize(0, 0)
                    self.label_winner.resize(74, 74)
                    self.label_winner.setPixmap(QPixmap("assets/files_for_mini_sea_battle/sahareg_winner.png"))
                    self.label_winner.move(684, 18)
                    self.make_sound('assets/files_for_mini_sea_battle/winner_sound.mp3')
                    write_sqlite('Мини-морской бой', 'Сахареж')
            else:
                self.make_sound('assets/files_for_mini_sea_battle/ben_no.mp3')

    def define_action(self):
        if not self.end_game:
            if self.is_motota_now_going:
                self.check_motota_motion()
            else:
                self.check_sahareg_motion()

    def make_new_game(self):
        self.qradio_motota.setEnabled(True)
        self.qradio_sahareg.setEnabled(True)
        if self.qradio_motota.isChecked():
            self.is_motota_now_going = True
            self.is_sahareg_now_going = False
        else:
            self.is_sahareg_now_going = True
            self.is_motota_now_going = False
        for i in range(len(self.motota_button_grid)):
            for j in range(len(self.motota_button_grid[i])):
                self.motota_button_grid[i][j].setText("")
                self.motota_button_grid[i][j].setStyleSheet(
                    "background-image : url(assets/files_for_mini_sea_battle/water.png);")
                self.sahareg_button_grid[i][j].setText("")
                self.sahareg_button_grid[i][j].setStyleSheet(
                    "background-image : url(assets/files_for_mini_sea_battle/water.png);")

        self.is_four_ship_motota = False
        self.is_four_ship_sahareg = False
        self.cnt_ship_motota = 0
        self.cnt_ship_sahareg = 0
        self.label_info_motota.resize(80, 21)
        self.label_info_sahareg.resize(80, 21)
        self.label_shot_him_motota.resize(0, 0)
        self.label_shot_him_sahareg.resize(0, 0)
        self.end_game = False
        self.label_winner.resize(0, 0)

    def make_buttons(self, button_grid, col):
        """
        добавление кнопок в переданный список кнопок - button_grid
        col - координаты
        """
        for i in range(5):
            string = []
            for j in range(5):
                string.append(QPushButton(self))
                string[j].resize(80, 80)
                string[j].move(i * 80 + 22 + col, j * 80 + 93)
                string[j].clicked.connect(self.define_action)
                string[j].setStyleSheet("background-image : url(assets/files_for_mini_sea_battle/water.png);")
            button_grid.append(string)

    def check_info(self):
        self.info = InformationSeaBattle()
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


class InformationSeaBattle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(672, 265, 400, 661)
        self.setFixedSize(400, 661)
        self.setWindowTitle('Информация')
        self.info_label = QLabel(self)
        self.info_label.setPixmap(QPixmap("assets/files_for_mini_sea_battle/hint_sea_battle.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    minisea = MiniSeaBattle()
    minisea.show()
    sys.exit(app.exec())
