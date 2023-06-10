import sys
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

device = XBeeDevice("COM6", 115200)  # Replace 'COM6' with the appropriate port name
device.open()

remote_device_address = XBee64BitAddress.from_hex_string("13A20041F41035")
remote_device = RemoteXBeeDevice(device, remote_device_address)

data = [1, 0, 0, 0]

def send_array(array):
    string_array = [str(value) for value in data]
    start_string =  ",".join(string_array)
    print(start_string)
    device.send_data(remote_device, start_string.encode())

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create four buttons and connect them to their respective functions
        button1 = QPushButton("START")
        button1.clicked.connect(self.button1_clicked)
        layout.addWidget(button1)

        button2 = QPushButton("BRAKE ON")
        button2.clicked.connect(self.button2_clicked)
        layout.addWidget(button2)

        button3 = QPushButton("BRAKE OFF")
        button3.clicked.connect(self.button3_clicked)
        layout.addWidget(button3)

        button4 = QPushButton("LIM ON")
        button4.clicked.connect(self.button4_clicked)
        layout.addWidget(button4)

        button5 = QPushButton("LIM OFF")
        button5.clicked.connect(self.button5_clicked)
        layout.addWidget(button5)

        button6 = QPushButton("STOP")
        button6.clicked.connect(self.button6_clicked)
        layout.addWidget(button6)

        self.setLayout(layout)

    def button1_clicked(self):
        data[0] = 0
        data[1] = 1
        data[2] = 255
        data[3] = 255

    def button2_clicked(self):
        data[0] = 1

    def button3_clicked(self):
        data[0] = 0
        data[2] = 255
        data[3] = 255

    def button4_clicked(self):
        data[1] = 1
        data[2] = 255
        data[3] = 255

    def button5_clicked(self):
        data[1] = 0

    def button6_clicked(self):
        data[0] = 1
        data[1] = 0
        data[2] = 0
        data[3] = 0

    send_array(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()

    timer = QTimer()
    timer.timeout.connect(lambda: send_array(data))
    timer.start(100)

    window.show()

    sys.exit(app.exec_())