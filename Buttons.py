import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
import serial

COM_PORT = '/dev/ttys002'

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.serial_port = serial.Serial(COM_PORT, baudrate=9600)

        self.send_data([0, 1])
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_data_continuously)
        self.timer.timeout.connect(self.send_data_continuously2)
        #self.timer.timeout.connect(self.send_data_continuously0)
        self.timer.start(100)

    def setup_ui(self):
        self.setWindowTitle('Serial Communication')
        self.setGeometry(200, 200, 200, 100)

        layout = QVBoxLayout(self)
        self.button_start = QPushButton('START')
        self.button_start.setCheckable(True)
        self.button_start.clicked.connect(self.send_button_pressed)
        layout.addWidget(self.button_start)

        self.button_change1 = QPushButton('BRAKE E')
        self.button_change1.setCheckable(True)
        self.button_change1.pressed.connect(self.change1_button_pressed)
        self.button_change1.released.connect(self.change_button_released)
        layout.addWidget(self.button_change1)

        self.button_change0 = QPushButton('BRAKE D')
        self.button_change0.setCheckable(True)
        self.button_change0.pressed.connect(self.change0_button_pressed)
        self.button_change0.released.connect(self.change_button_released)
        layout.addWidget(self.button_change0)

        self.button_change01 = QPushButton('LIM ON')
        self.button_change01.setCheckable(True)
        self.button_change01.pressed.connect(self.change01_button_pressed)
        self.button_change01.released.connect(self.change_button_released)
        layout.addWidget(self.button_change01)

        self.button_change00 = QPushButton('LIM OFF')
        self.button_change00.setCheckable(True)
        self.button_change00.pressed.connect(self.change00_button_pressed)
        self.button_change00.released.connect(self.change_button_released)
        layout.addWidget(self.button_change00)

        self.button_change1_pressed = False
        self.button_change0_pressed = False
        self.button_change01_pressed = False
        self.button_change00_pressed = False

    def send_data(self, data):
        data_str = ','.join(str(val) for val in data)
        self.serial_port.write(f'{data_str}\n'.encode())

    # def send_button_pressed0(self):
    #     if self.button_start.isChecked():
    #         self.send_data([0, 1])
    #     else:
    #         self.send_data([1, 0])

    def send_button_pressed(self):
        if self.button_start.isChecked():
            if self.button_change1.isChecked():
                if self.button_change00_pressed.isChecked():
                    self.send_data([1, 0])

                elif self.button_change01_pressed.isChecked():
                     self.send_data([0, 1])

                else:
                    self.send_data([1, 1])
            elif self.button_change0.isChecked():
                if self.button_change00_pressed.isChecked():
                    self.send_data([0, 0])

                elif self.button_change01_pressed.isChecked():
                    self.send_data([0, 1])

                else:
                    self.send_data([0, 1])
            # else:
            #     self.send_data([0, 1])

        else:
            self.send_data([1, 0])

    def send_button_pressed2(self):
        if self.button_start.isChecked():
            if self.button_change01.isChecked():
                if self.button_change1_pressed.isChecked():
                    self.send_data([1, 1])

                elif self.button_change0_pressed.isChecked():
                    self.send_data([0, 1])

                else:
                    self.send_data([0, 1])
            elif self.button_change00.isChecked():
                if self.button_change1_pressed.isChecked():
                    self.send_data([1, 0])

                elif self.button_change0_pressed.isChecked():
                    self.send_data([0, 0])

                else:
                    self.send_data([0, 0])

            # else:
            #     self.send_data([0, 1])

        else:
            self.send_data([1, 0])

    # def send_data_continuously0(self):
    #     if self.button_start.isChecked():
    #         self.send_data([0, 1])
    #     else:
    #         self.send_data([1, 0])


    def send_data_continuously(self):
        if self.button_start.isChecked():
            if self.button_change1.isChecked():
                if self.button_change00.isChecked():
                    self.send_data([1, 0])

                elif self.button_change01.isChecked():
                    self.send_data([1, 1])

                else:
                    self.send_data([1, 1])
            elif self.button_change0.isChecked():
                if self.button_change00.isChecked():
                    self.send_data([0, 0])

                elif self.button_change01.isChecked():
                    self.send_data([0, 1])

                else:
                    self.send_data([0, 1])

            # else:
            #     self.send_data([0, 1])

        else:
            self.send_data([1, 0])

    def send_data_continuously2(self):
        if self.button_start.isChecked():
            if self.button_change01.isChecked():
                if self.button_change1.isChecked():
                    self.send_data([1, 1])

                elif self.button_change0.isChecked():
                    self.send_data([0, 1])

                else:
                    self.send_data([0, 1])
            elif self.button_change00.isChecked():
                if self.button_change1.isChecked():
                    self.send_data([1, 0])

                elif self.button_change0.isChecked():
                    self.send_data([0, 0])

                else:
                    self.send_data([0, 0])

            # else:
            #     self.send_data([0, 1])

        else:
            self.send_data([1, 0])

    def change1_button_pressed(self):
        self.button_change0.setChecked(False)
        self.button_change1_pressed = True

    def change0_button_pressed(self):
        self.button_change1.setChecked(False)
        self.button_change0_pressed = True

    def change01_button_pressed(self):
        self.button_change00.setChecked(False)
        self.button_change01_pressed = True

    def change00_button_pressed(self):
        self.button_change01.setChecked(False)
        self.button_change00_pressed = True

    def change_button_released(self):
        self.button_change1_pressed = False
        self.button_change0_pressed = False

    def closeEvent(self, event):
        self.timer.stop()  # Stop the timer
        self.serial_port.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
