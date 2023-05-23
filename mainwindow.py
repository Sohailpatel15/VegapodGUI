import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLCDNumber, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
import serial 

class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = 'COM5'

    def run(self):
        ser = serial.Serial(self.port, 9600)
        while True:
            if ser.in_waiting > 0:
                try:
                    data = ser.readline().decode('utf-8').strip()
                    self.data_received.emit(data)
                except UnicodeDecodeError:
                    pass

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

        self.table2 = QTableWidget(self)
        self.table2.setGeometry(250, 20, 231, 311)
        self.table2.setColumnCount(1)
        self.table2.setRowCount(9)
        self.table2.setHorizontalHeaderLabels(["sensor 10 to 18"])

        self.table3 = QTableWidget(self)
        self.table3.setGeometry(490, 20, 231, 311)
        self.table3.setColumnCount(1)
        self.table3.setRowCount(9)
        self.table3.setHorizontalHeaderLabels(["sensor 19 to 27"])

        self.table4 = QTableWidget(self)
        self.table4.setGeometry(10, 340, 231, 81)
        self.table4.setColumnCount(1)
        self.table4.setRowCount(2)
        self.table4.setHorizontalHeaderLabels(["sensor 28 to 29"])

        self.table5 = QTableWidget(self)
        self.table5.setGeometry(250, 340, 231, 81)
        self.table5.setColumnCount(1)
        self.table5.setRowCount(2)
        self.table5.setHorizontalHeaderLabels(["sensor 30 to 31"])

        self.table6 = QTableWidget(self)
        self.table6.setGeometry(490, 340, 231, 81)
        self.table6.setColumnCount(1)
        self.table6.setRowCount(2)
        self.table6.setHorizontalHeaderLabels(["sensor 32 to 33"])

        self.table7 = QTableWidget(self)
        self.table7.setGeometry(730, 20, 191, 141)
        self.table7.setColumnCount(1)
        self.table7.setRowCount(4)
        self.table7.setHorizontalHeaderLabels(["sensor 34 to 37"])

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


        self.serial_thread = SerialThread("COM5")  # Replace "COM1" with your Arduino's port
        self.serial_thread.data_received.connect(self.update_table_rows)
        self.serial_thread.start()

    def update_table_rows(self, data):
        if data.startswith("START") and data.endswith("STOP"):
            values = data[6:-5].split(",")
            if len(values) == 40:
                for i in range(9):
                    item = QTableWidgetItem(values[i])
                    self.table1.setItem(i, 0, item)
                for i in range(9, 18):
                    item = QTableWidgetItem(values[i])
                    self.table2.setItem(i - 9, 0, item)
                for i in range(18, 27):
                    item = QTableWidgetItem(values[i])
                    self.table3.setItem(i - 18, 0, item)
                for i in range(27, 29):
                    item = QTableWidgetItem(values[i])
                    self.table4.setItem(i - 27, 0, item)
                for i in range(29, 31):
                    item = QTableWidgetItem(values[i])
                    self.table5.setItem(i - 29, 0, item)
                for i in range(31, 33):
                    item = QTableWidgetItem(values[i])
                    self.table6.setItem(i - 31, 0, item)
                for i in range(33, 37):
                    item = QTableWidgetItem(values[i])
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
    window.show()
    sys.exit(app.exec_())