import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
import serial

class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = '/dev/ttys004'

    def run(self):
        ser = serial.Serial(self.port, 115200)
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
        self.setWindowTitle("Sensor Tables")
        self.setGeometry(0, 0, 760, 705)

        self.table1 = QTableWidget(self)
        self.table1.setGeometry(140, 10, 181, 651)
        self.table1.setColumnCount(1)
        self.table1.setRowCount(20)
        self.table1.setHorizontalHeaderLabels(["sensor1 to 20"])

        self.table2 = QTableWidget(self)
        self.table2.setGeometry(400, 10, 181, 651)
        self.table2.setColumnCount(1)
        self.table2.setRowCount(20)
        self.table2.setHorizontalHeaderLabels(["sensor21 to 40"])

        self.serial_thread = SerialThread("COM1")  # Replace "COM1" with your Arduino's port
        self.serial_thread.data_received.connect(self.update_table_rows)
        self.serial_thread.start()

    def update_table_rows(self, data):
        if data.startswith("START") and data.endswith("STOP"):
            values = data[6:-5].split(",")
            if len(values) == 40:
                for i in range(20):
                    item = QTableWidgetItem(values[i])
                    self.table1.setItem(i, 0, item)
                for i in range(20, 40):
                    item = QTableWidgetItem(values[i])
                    self.table2.setItem(i - 20, 0, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
