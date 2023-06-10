import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
from digi.xbee.devices import XBeeDevice
from digi.xbee.models.address import XBee64BitAddress
import time

class XBeeThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.xbee = None

    def run(self):
        self.xbee = XBeeDevice(self.port, 115200)
        try:
            self.xbee.open()
            while True:
                xbee_message = self.xbee.read_data()
                if xbee_message is not None:
                    source_address = xbee_message.remote_device.get_64bit_addr()
                    data = xbee_message.data.decode('utf-8').strip()
                    self.data_received.emit(data)
        finally:
            if self.xbee is not None and self.xbee.is_open():
                self.xbee.close()

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

        self.xbee_thread = XBeeThread("COM7")  # Replace "COM7" with your XBee's port
        self.xbee_thread.data_received.connect(self.update_table_rows)
        self.xbee_thread.start()

    def update_table_rows(self, data):
        chunks = data.split(",")
        if chunks[0] == "start" and chunks[-1] == "stop":
            values = chunks[1:-1]
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
