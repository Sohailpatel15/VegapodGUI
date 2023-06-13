import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLCDNumber, QLabel, QPushButton, \
    QComboBox
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time

device = XBeeDevice("COM7", 115200)  # Replace 'COM6' with the appropriate port name
device.open()

# remote_device_address = XBee64BitAddress.from_hex_string("13A20041F44E12")  # change
# remote_device = RemoteXBeeDevice(device, remote_device_address)

baud_rate = 115200

data1 = [0, 0, 0, 0]


class XBeeThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.xbee = None

    def run(self):
        self.xbee = device
        try:
            # self.xbee.open()
            while True:
                start_time = time.time()  # Get the current time
                xbee_message = None
                while xbee_message is None:
                    xbee_message = self.xbee.read_data(1000)  # Increase the timeout value to allow for broadcast messages
                    if xbee_message is not None:
                        break  # Exit the inner loop if data is received
                    if time.time() - start_time > 10:  # Adjust the timeout value as needed (in seconds)
                        break  # Exit the inner loop if the timeout is reached
                if xbee_message is not None:
                    source_address = xbee_message.remote_device.get_64bit_addr()
                    data = xbee_message.data.decode('utf-8').strip()
                    self.data_received.emit(data)
        finally:
            if self.xbee is not None and self.xbee.is_open():
                self.xbee.close()


# 13A200   41F41035
class SendThread(QThread):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        send_array(self.data)


def send_array(array):
    string_array = [str(value) for value in array]
    start_string = "".join(string_array)
    print(start_string)
    try:
        device.send_data_broadcast(start_string.encode())
    except Exception as e:
        print(f"Error occurred while sending data: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VEGAPOD Hyperloop")
        self.setGeometry(0, 0, 1059, 463)

        self.table1 = QTableWidget(self)
        self.table1.setGeometry(10, 20, 231, 311)
        self.table1.setColumnCount(1)
        self.table1.setRowCount(9)
        self.table1.setHorizontalHeaderLabels(["sensor 1 to 9"])
        self.table1.setVerticalHeaderLabels(
            ["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7", "Sensor 8",
             "Sensor 9"])

        self.table2 = QTableWidget(self)
        self.table2.setGeometry(250, 20, 231, 311)
        self.table2.setColumnCount(1)
        self.table2.setRowCount(9)
        self.table2.setHorizontalHeaderLabels(["sensor 10 to 18"])
        self.table2.setVerticalHeaderLabels(
            ["Sensor 10", "Sensor 11", "Sensor 12", "Sensor 13", "Sensor 14", "Sensor 15", "Sensor 16", "Sensor 17",
             "Sensor 18"])

        self.table3 = QTableWidget(self)
        self.table3.setGeometry(490, 20, 231, 311)
        self.table3.setColumnCount(1)
        self.table3.setRowCount(9)
        self.table3.setHorizontalHeaderLabels(["sensor 19 to 27"])
        self.table3.setVerticalHeaderLabels(
            ["Voltage", "Current", "AVG Voltage", "Max Cell Voltage", "Min Cell Voltage", "AVG Cell Temp",
             "Max Cell Temp", "Min Cell Temp", "Extra"])

        self.table4 = QTableWidget(self)
        self.table4.setGeometry(10, 340, 231, 81)
        self.table4.setColumnCount(1)
        self.table4.setRowCount(2)
        self.table4.setHorizontalHeaderLabels(["sensor 28 to 29"])
        self.table4.setVerticalHeaderLabels(["Distance 1", "Distance 2"])

        self.table5 = QTableWidget(self)
        self.table5.setGeometry(250, 340, 231, 81)
        self.table5.setColumnCount(1)
        self.table5.setRowCount(2)
        self.table5.setHorizontalHeaderLabels(["sensor 30 to 31"])
        self.table5.setVerticalHeaderLabels(["Pressure 1", "Pressure 2"])  # Add vertical labels

        self.table6 = QTableWidget(self)
        self.table6.setGeometry(490, 340, 231, 81)
        self.table6.setColumnCount(1)
        self.table6.setRowCount(2)
        self.table6.setHorizontalHeaderLabels(["sensor 32 to 33"])
        self.table6.setVerticalHeaderLabels(["Temperature 1", "Temperature 2"])  # Add vertical labels

        self.table7 = QTableWidget(self)
        self.table7.setGeometry(730, 20, 191, 141)
        self.table7.setColumnCount(1)
        self.table7.setRowCount(4)
        self.table7.setHorizontalHeaderLabels(["sensor 34 to 37"])
        self.table7.setVerticalHeaderLabels(["Status", "Voltage", "Current", "Temperature"])  # Add vertical labels

        self.lcd1 = QLCDNumber(self)
        self.lcd1.setGeometry(730, 170, 121, 41)

        self.lcd2 = QLCDNumber(self)
        self.lcd2.setGeometry(730, 220, 121, 41)

        self.lcd3 = QLCDNumber(self)
        self.lcd3.setGeometry(730, 270, 121, 41)

        self.Label1 = QLabel(self)
        self.Label1.setGeometry(860, 180, 31, 21)
        self.Label1.setText('SPEED')

        self.Label2 = QLabel(self)
        self.Label2.setGeometry(860, 230, 81, 21)
        self.Label2.setText('ACCELERATION')

        self.Label3 = QLabel(self)
        self.Label3.setGeometry(860, 280, 51, 21)
        self.Label3.setText('DISTANCE')

        self.button1 = QPushButton(self)
        self.button1.setGeometry(730, 330, 101, 41)
        self.button1.clicked.connect(self.button1_clicked)
        self.button1.setText('START')

        self.button2 = QPushButton(self)
        self.button2.setGeometry(840, 330, 101, 41)
        self.button2.clicked.connect(self.button2_clicked)
        self.button2.setText('BRAKE E')

        self.button3 = QPushButton(self)
        self.button3.setGeometry(950, 330, 101, 41)
        self.button3.clicked.connect(self.button3_clicked)
        self.button3.setText('BRAKE D')

        self.button4 = QPushButton(self)
        self.button4.setGeometry(730, 380, 101, 41)
        self.button4.clicked.connect(self.button4_clicked)
        self.button4.setText('LIM ON')

        self.button5 = QPushButton(self)
        self.button5.setGeometry(840, 380, 101, 41)
        self.button5.clicked.connect(self.button5_clicked)
        self.button5.setText('LIM OFF')

        self.button6 = QPushButton(self)
        self.button6.setGeometry(950, 380, 101, 41)
        self.button6.clicked.connect(self.button6_clicked)
        self.button6.setText('STOP')

        self.spin1 = QComboBox(self)
        self.spin1.setGeometry(940, 20, 101, 41)
        self.spin1.addItem("0")
        self.spin1.addItem("1")
        self.spin1.addItem("2")
        self.spin1.addItem("2")
        self.spin1.addItem("3")
        self.spin1.addItem("4")
        self.spin1.addItem("5")
        self.spin1.addItem("6")
        self.spin1.addItem("7")
        self.spin1.addItem("8")
        self.spin1.addItem("9")
        self.spin1.currentIndexChanged.connect(self.update_selection1)

        self.selected_item1 = 0

        self.spin2 = QComboBox(self)
        self.spin2.setGeometry(940, 70, 101, 41)
        self.spin2.addItem("0")
        self.spin2.addItem("1")
        self.spin2.addItem("2")
        self.spin2.addItem("3")
        self.spin2.addItem("4")
        self.spin2.addItem("5")
        self.spin2.addItem("6")
        self.spin2.addItem("7")
        self.spin2.addItem("8")
        self.spin2.addItem("9")
        self.spin2.currentIndexChanged.connect(self.update_selection2)

        self.selected_item2 = 0

        self.xbee_thread = XBeeThread("COM7")  # Replace "COM7" with your XBee's port
        self.xbee_thread.data_received.connect(self.update_table_rows)
        self.xbee_thread.start()

        self.send_thread = SendThread(data1)
        self.send_thread.start()

    def update_selection1(self, index):
        self.selected_item1 = self.spin1.currentText()

    def update_selection2(self, index):
        self.selected_item2 = self.spin2.currentText()

    def button1_clicked(self):
        data1[0] = 1
        data1[1] = 1
        data1[2] = self.selected_item1
        data1[3] = self.selected_item2
        self.send_thread.data = data1

    def button2_clicked(self):
        data1[0] = 0
        self.send_thread.data = data1

    def button3_clicked(self):
        data1[0] = 1
        data1[2] = self.selected_item1
        data1[3] = self.selected_item2
        self.send_thread.data = data1

    def button4_clicked(self):
        data1[1] = 0
        data1[2] = self.selected_item1
        self.send_thread.data = data1

    def button5_clicked(self):
        data1[2] = self.selected_item1
        self.send_thread.data = data1

    def button6_clicked(self):
        data1[0] = 0
        data1[1] = 0
        data1[2] = self.selected_item1
        data1[3] = self.selected_item2

    send_array(data1)

    def update_table_rows(self, data):
        chunks = data.split(",")
        if chunks[0] == "start" and chunks[-1] == "stop":
            values = chunks[1:-1]
            for i in range(min(len(values), 40)):
                item = QTableWidgetItem(values[i])
                if i < 9:
                    self.table1.setItem(i, 0, item)
                elif i < 18:
                    self.table2.setItem(i - 9, 0, item)
                elif i < 27:
                    self.table3.setItem(i - 18, 0, item)
                elif i < 29:
                    self.table4.setItem(i - 27, 0, item)
                elif i < 31:
                    self.table5.setItem(i - 29, 0, item)
                elif i < 33:
                    self.table6.setItem(i - 31, 0, item)
                elif i < 37:
                    self.table7.setItem(i - 33, 0, item)

            if len(values) >= 38:
                self.lcd1.display(int(values[37]))
            if len(values) >= 39:
                self.lcd2.display(int(values[38]))
            if len(values) >= 40:
                self.lcd3.display(int(values[39]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    timer = QTimer()
    timer.timeout.connect
    timer.start(200)
    timer.timeout.connect(lambda: send_array(data1))
    window.show()
    sys.exit(app.exec_())