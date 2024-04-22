import config
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

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

        self.bottom_menu = ["status", "items", "map", "notes", "radio", "skills"]
        self.left_menu = ["Antidotes", "Poisons", "Antibiotics", "Genetics"]

        header = QHBoxLayout()
        main = QHBoxLayout()
        footer = QHBoxLayout()
        i=20
        for menu_item in self.bottom_menu:
            footer.addWidget(self.prepareLabel(menu_item, i, self.size.height()-20, QSize(10 * len(menu_item), 10)))
            i+=10 * len(menu_item)

        lmenu = QVBoxLayout()
        i=0
        for menu_item in self.left_menu:
            lmenu.addWidget(self.prepareLabel(menu_item, 20, 40 + i, QSize(10*len(menu_item), 10)))
            i+=10

        main.addLayout(lmenu)

        vbox = QVBoxLayout()
        vbox.addLayout(header)
        vbox.addLayout(main)
        vbox.addLayout(footer)

        # label = self.prepareLabel()
        # vbox.addWidget(label)

        label2 = self.prepareGif()
        vbox.addWidget(label2)

        self.setLayout(vbox)
        self.show()

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

    def prepareLabel(self, text, x_position, y_position, size):
        label = QLabel(text, self)
        label.move(x_position, y_position)
        label.resize(size)
        label.setStyleSheet("color: green")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
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

