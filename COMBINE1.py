import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLCDNumber, QLabel, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import serial

com_port = "/dev/ttys005" #data sending
baud_rate = 9600
ser = serial.Serial(com_port, baud_rate)

data = [1, 0, 0, 0]



class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = "/dev/ttys003" #data receiving


    def run(self):
        ser = serial.Serial(self.port, 9600)
        while True:
            if ser.in_waiting > 0:
                try:
                    data = ser.readline().decode('utf-8').strip()
                    self.data_received.emit(data)
                except UnicodeDecodeError:
                    pass
def send_array(array):
    array_string = ",".join(str(element) for element in array)
    ser.write(array_string.encode() + b"\n")

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
        self.table1.setVerticalHeaderLabels(["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7", "Sensor 8", "Sensor 9"])

        self.table2 = QTableWidget(self)
        self.table2.setGeometry(250, 20, 231, 311)
        self.table2.setColumnCount(1)
        self.table2.setRowCount(9)
        self.table2.setHorizontalHeaderLabels(["sensor 10 to 18"])
        self.table2.setVerticalHeaderLabels(["Sensor 10", "Sensor 11", "Sensor 12", "Sensor 13", "Sensor 14", "Sensor 15", "Sensor 16", "Sensor 17", "Sensor 18"])

        self.table3 = QTableWidget(self)
        self.table3.setGeometry(490, 20, 231, 311)
        self.table3.setColumnCount(1)
        self.table3.setRowCount(9)
        self.table3.setHorizontalHeaderLabels(["sensor 19 to 27"])
        self.table3.setVerticalHeaderLabels(["Voltage", "Current", "AVG Voltage", "Max Cell Voltage", "Min Cell Voltage", "AVG Cell Temp", "Max Cell Temp", "Min Cell Temp", "Extra"])

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

        self.serial_thread = SerialThread("/dev/ttys003")  # Replace
        self.serial_thread.data_received.connect(self.update_table_rows)
        self.serial_thread.start()

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

    def update_table_rows(self, data):
        if data.startswith("START") and data.endswith("STOP"):
            values = data[6:-5].split(",")
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
    timer = QTimer()
    timer.timeout.connect(lambda: send_array(data))
    timer.start(100)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
