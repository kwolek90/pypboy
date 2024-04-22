import config
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import math

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    config.GPIO_AVAILABLE = True
except Exception as e:
    print("GPIO UNAVAILABLE (%s)" % e)
    config.GPIO_AVAILABLE = False



class PipBoy(QMainWindow):
    def __init__(self):
        super().__init__()
        self.size = QSize(config.WIDTH, config.HEIGHT)
        self.setFixedSize(self.size)
        self.setWindowTitle("PypBoy")
        self.pages = QStackedWidget()
        self.subPages = QStackedWidget()

        self.bottom_menu = ["Status", "Items", "Map", "Notes", "Radio", "Skills"]
        self.left_menu = ["Antidotes", "Poisons", "Antibiotics", "Genetics"]

        self.selected_subMenu = 3
        self.selected_botMenu = 3

        self.preparePage()
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            print("Killing")
            self.deleteLater()
        elif event.key() == Qt.Key_Enter:
            self.proceed()
        elif event.key() == Qt.Key_Up:
            self.selected_subMenu = max(0, self.selected_subMenu - 1)
            self.preparePage()
            print(self.selected_subMenu)
        elif event.key() == Qt.Key_Down:
            self.selected_subMenu = min(len(self.left_menu) - 1, self.selected_subMenu + 1)
            self.preparePage()
            print(self.selected_subMenu)
        elif event.key() == Qt.Key_Right:
            self.selected_botMenu = min(len(self.bottom_menu) - 1, self.selected_botMenu + 1)
            self.preparePage()
            print(self.selected_botMenu)
        elif event.key() == Qt.Key_Left:
            self.selected_botMenu = max(0, self.selected_botMenu - 1)
            self.preparePage()
            print(self.selected_botMenu)
        event.accept()

    def prepareMainLabel(self):
        label = QLabel("PipBoy 3000", self)
        label.move(0, 0)
        label.resize(self.size)
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        label.setStyleSheet("color: green")
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        return label

    def prepareLeftMenu(self):
        i = 0
        lmenu = QVBoxLayout()

        for menu_item in self.left_menu:
            lmenu.addWidget(
                self.prepareLabel(
                    menu_item,
                    20,
                    40 + i,
                    menu_item == self.left_menu[self.selected_subMenu]))
            i += 14
        return lmenu

    def preparePage(self):
        vbox = QVBoxLayout()

        header = QHBoxLayout()
        main = QHBoxLayout()
        footer = QHBoxLayout()
        i = 20
        for menu_item in self.bottom_menu:
            footer.addWidget(self.prepareLabel(menu_item, i, self.size.height() - 20,
                                               menu_item == self.bottom_menu[self.selected_botMenu]))
            i += 14 * len(menu_item)

        lmenu = self.prepareLeftMenu()

        main.addLayout(lmenu)

        vbox.addLayout(header)
        vbox.addLayout(main)
        vbox.addLayout(footer)

        if not self.selected_botMenu:
            label2 = self.prepareGif()
            vbox.addWidget(label2)

        self.setLayout(vbox)
        self.update()


    def prepareLabel(self, text, x_position, y_position, selected=False):
        label = QLabel(text, self)
        label.move(x_position, y_position)
        label.resize(QSize(10*len(text), 14))
        style = "color: green;"
        if selected:
            style += "border-width: 1;border-style: solid; border-color:green;"
            print(text)
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        return label

    def prepareGif(self):
        movie = QMovie("images/vault_boy_walking.gif")
        label2 = QLabel("", self)
        label2.move(0, 0)
        label2.resize(self.size)
        label2.setMovie(movie)
        label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        movie.start()
        return label2


if __name__ == "__main__":
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Background, Qt.black)
    app.setPalette(palette)

    window = PipBoy()
    sys.exit(app.exec())

