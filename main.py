import logging
import os
import sys
import threading

import yaml
from PyQt5.QtCore import QTime, QTimer, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton, QVBoxLayout, QWidget, QLCDNumber)


def get_configuartions():
    """Fetch configurations from config file

    Returns:
        dict: configurations of the app
    """
    path = os.path.join(os.getcwd(), "config.yml")
    with open(path, mode="r") as config_file:
        data = yaml.load(config_file, Loader=yaml.FullLoader)
    return data[0]["App_Configuration"]


class MyGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.conf = get_configuartions()
        # set the title
        self.setWindowTitle(self.conf["Title"])
        # setting the size of window
        self.setFixedWidth(self.conf["window_width"])
        self.setFixedHeight(self.conf["window_height"])
        # Set logo
        self.setWindowIcon(QIcon(self.conf["logo_path"]))

        self.lcd_time = QLCDNumber(self)
        self.lcd_time.setSegmentStyle(QLCDNumber.Filled)  # Outline Filled Flat
        self.lcd_time.setDigitCount(8)

        self.timer = QTimer(self)
        self.lbl = QLabel(self)
        # Shutdown call2action button
        self.shutdown_btn = QPushButton(parent=self, text="Shutdown?")
        self.shutdown_btn.clicked.connect(self.shutdown_button_clicked)

        self.how_many_mins = QLabel("In how many minutes?:")
        self.how_many_mins_textbox = QLineEdit()
        self.how_many_mins_textbox.textChanged.connect(self.how_many_mins_textbox_validation_form)
        self.how_many_mins_textbox.setPlaceholderText("Number of mins")

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd_time)
        vbox.addWidget(self.lbl)
        vbox.addWidget(self.how_many_mins)
        vbox.addWidget(self.how_many_mins_textbox)
        vbox.addWidget(self.shutdown_btn)
        self.setLayout(vbox)

        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.num_seconds = 0
        self.show()

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm:ss")
        if (time.second() % 2) == 0:
            text = text[0:2] + " " + text[3:5] + " " + text[6:]
        self.lcd_time.display(text)
        self.num_seconds += 1
        if self.num_seconds == 5:
            self.num_seconds = 0

    def showLabel(self, text_label):
        self.lbl.setText(text_label)

    def how_many_mins_textbox_validation_form(self):
        """
        Validation form for user entry, displays error/no error
        """
        num_of_minutes = self.how_many_mins_textbox.text().strip()
        if len(num_of_minutes) == 0:
            self.how_many_mins_textbox.setStyleSheet("border: 0px solid red;")
        elif num_of_minutes.isdigit():
            self.how_many_mins_textbox.setStyleSheet("border: 1px solid green;")
        else:
            self.how_many_mins_textbox.setStyleSheet("border: 1px solid red;")

    def shutdown_button_clicked(self):
        num_of_minutes = self.how_many_mins_textbox.text().strip()
        if len(num_of_minutes) > 0 and num_of_minutes.isdigit():
            seconds = int(num_of_minutes) * 60
            os.system(f"shutdown -s -t {seconds}")
        else:
            QMessageBox.about(
                self,
                "Warning",
                "Please enter a valid amount of minutes",
            )


def main():
    app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
    gui = MyGui()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Configure Logging
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s: %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    main()
