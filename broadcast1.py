import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLCDNumber, QLabel, QPushButton, \
    QComboBox, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import pyqtgraph as pg
import time

device = XBeeDevice("/dev/tty.usbserial-0001", 115200)  # Replace 'COM6' with the appropriate port name
device.open()

# remote_device_address = XBee64BitAddress.from_hex_string("13A20041F44E12")  # change
# remote_device = RemoteXBeeDevice(device, remote_device_address)

baud_rate = 115200

data1 = [0, 0, 0, 0]

x_data = []  # List to store x-axis data
y_data = []  # List to store y-axis data


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

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent)

        # Create a plot widget
        self.plot_widget = pg.PlotWidget()

        # Set the plot title and axis labels
        self.plot_widget.setTitle("Graph Title")
        self.plot_widget.setLabel("left", "Value")
        self.plot_widget.setLabel("bottom", "Time")

        # Create a layout and add the plot widget to it
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def update_graph(self, x_data, y_data):
        # Clear the previous plot
        self.plot_widget.clear()

        # Plot the new data
        self.plot_widget.plot(x_data, y_data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VEGAPOD Hyperloop")
        self.setGeometry(0, 0, 1333, 888)

        self.setStyleSheet("""
                    QMainWindow {
                        background-color: #0E2433;
                    }

                    QTableWidget {
                        background-color: #1C4966;
                        border: 1px solid #1C4966;
                    }

                    QLCDNumber {
                        background-color: #0E2433;
                        color: #444444;
                        border: 1px solid #CCCCCC;
                    }

                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                    }
                    

                    QComboBox {
                        padding: 2px;
                        border: 1px solid gray;
                        border-radius: 4px;
                        background-color: white;
                        color: black;
                    }

                    QLineEdit {
                        background-color: white;
                        color: #296D98;
                        font-size: 16px;
                        border: 1px solid #CCCCCC;
                        padding: 5px;
                    }
                """)


        self.table1 = QTableWidget(self)
        self.table1.setGeometry(10, 420, 281, 421)
        self.table1.setColumnCount(1)
        self.table1.setRowCount(9)
        self.table1.setHorizontalHeaderLabels(["TABLE 1"])
        self.table1.setVerticalHeaderLabels(
            ["SENSOR 1", "SENSOR 2", "SENSOR 3", "SENSOR 4", "SENSOR 5", "SENSOR 6", "SENSOR 7", "SENSOR 8",
             "SENSOR 9"])
        self.table1.horizontalHeader().setDefaultSectionSize(222)
        self.table1.horizontalHeader().setMinimumSectionSize(44)
        self.table1.verticalHeader().setDefaultSectionSize(44)


        self.table2 = QTableWidget(self)
        self.table2.setGeometry(300, 420, 291, 421)
        self.table2.setColumnCount(1)
        self.table2.setRowCount(9)
        self.table2.setHorizontalHeaderLabels(["TABLE 2"])
        self.table2.setVerticalHeaderLabels(
            ["SENSOR 10", "SENSOR 11", "SENSOR 12", "SENSOR 13", "SENSOR 14", "SENSOR 15", "SENSOR 16", "SENSOR 17",
             "SENSOR 18"])
        self.table2.horizontalHeader().setDefaultSectionSize(215)
        self.table2.verticalHeader().setDefaultSectionSize(44)


        self.table3 = QTableWidget(self)
        self.table3.setGeometry(600, 420, 341, 421)
        self.table3.setColumnCount(1)
        self.table3.setRowCount(9)
        self.table3.setHorizontalHeaderLabels(["TABLE 3"])
        self.table3.setVerticalHeaderLabels(
            ["Voltage", "Current", "AVG Voltage", "Max Cell Voltage", "Min Cell Voltage", "AVG Cell Temp",
             "Max Cell Temp", "Min Cell Temp", "Extra"])
        self.table3.horizontalHeader().setDefaultSectionSize(226)
        self.table3.verticalHeader().setDefaultSectionSize(44)

        self.table4 = QTableWidget(self)
        self.table4.setGeometry(10, 20, 281, 191)
        self.table4.setColumnCount(1)
        self.table4.setRowCount(4)
        self.table4.setHorizontalHeaderLabels(["TABLE 4"])
        self.table4.setVerticalHeaderLabels(["Distance 1", "Distance 2", "Pressure 1", "Pressure 2"])
        self.table4.horizontalHeader().setDefaultSectionSize(202)
        self.table4.verticalHeader().setDefaultSectionSize(41)

        self.table5 = QTableWidget(self)
        self.table5.setGeometry(10, 220, 281, 191)
        self.table5.setColumnCount(1)
        self.table5.setRowCount(4)
        self.table5.setHorizontalHeaderLabels(["TABLE 5"])
        self.table5.setVerticalHeaderLabels(["Status", "Voltage", "Current", "Temperature"])  # Add vertical labels
        self.table5.horizontalHeader().setDefaultSectionSize(198)
        self.table5.verticalHeader().setDefaultSectionSize(36)

        self.lcd1 = QLCDNumber(self)
        self.lcd1.setGeometry(950, 290, 191, 61)

        self.lcd2 = QLCDNumber(self)
        self.lcd2.setGeometry(950, 360, 191, 61)

        self.lcd3 = QLCDNumber(self)
        self.lcd3.setGeometry(950, 430, 191, 61)

        self.Label1 = QLabel(self)
        self.Label1.setGeometry(1150, 300, 71, 51)
        self.Label1.setText('SPEED')

        self.Label2 = QLabel(self)
        self.Label2.setGeometry(1150, 360, 161, 51)
        self.Label2.setText('ACCELERATION')

        self.Label3 = QLabel(self)
        self.Label3.setGeometry(1150, 430, 111, 51)
        self.Label3.setText('DISTANCE')

        self.button1 = QPushButton(self)
        self.button1.setGeometry(950, 580, 181, 81)
        self.button1.clicked.connect(self.button1_clicked)
        self.button1.setText('START')
        self.button1.setStyleSheet("\n"
                                   "QPushButton {\n"
                                   "    background-color: #03C04A; /* Set the background color to red */\n"
                                   "    color: #FFFFFF; /* Set the text color to white */\n"
                                   "    font-size: 16px; /* Set the font size to 16 pixels */\n"
                                   "    border-radius: 8px; /* Set the border radius to 5 pixels */\n"
                                   "    padding: 10px; /* Set the padding around the button */\n"
                                   "}")

        self.button2 = QPushButton(self)
        self.button2.setGeometry(950, 670, 181, 81)
        self.button2.clicked.connect(self.button2_clicked)
        self.button2.setText('BRAKE E')
        self.button2.setStyleSheet("\n"
                                   "QPushButton {\n"
                                   "    background-color: #E6CC00; /* Set the background color to red */\n"
                                   "    color: #FFFFFF; /* Set the text color to white */\n"
                                   "    font-size: 16px; /* Set the font size to 16 pixels */\n"
                                   "    border-radius: 8px; /* Set the border radius to 5 pixels */\n"
                                   "    padding: 10px; /* Set the padding around the button */\n"
                                   "}")

        self.button3 = QPushButton(self)
        self.button3.setGeometry(1140, 670, 181, 81)
        self.button3.clicked.connect(self.button3_clicked)
        self.button3.setText('BRAKE D')
        self.button3.setStyleSheet("\n"
                                   "QPushButton {\n"
                                   "    background-color: #E47200; /* Set the background color to red */\n"
                                   "    color: #FFFFFF; /* Set the text color to white */\n"
                                   "    font-size: 16px; /* Set the font size to 16 pixels */\n"
                                   "    border-radius: 8px; /* Set the border radius to 5 pixels */\n"
                                   "    padding: 10px; /* Set the padding around the button */\n"
                                   "}")

        self.button4 = QPushButton(self)
        self.button4.setGeometry(950, 760, 181, 81)
        self.button4.clicked.connect(self.button4_clicked)
        self.button4.setText('LIM ON')
        self.button4.setStyleSheet("\n"
                                   "QPushButton {\n"
                                   "    background-color: #E6CC00; /* Set the background color to red */\n"
                                   "    color: #FFFFFF; /* Set the text color to white */\n"
                                   "    font-size: 16px; /* Set the font size to 16 pixels */\n"
                                   "    border-radius: 8px; /* Set the border radius to 5 pixels */\n"
                                   "    padding: 10px; /* Set the padding around the button */\n"
                                   "}")

        self.button5 = QPushButton(self)
        self.button5.setGeometry(1140, 760, 181, 81)
        self.button5.clicked.connect(self.button5_clicked)
        self.button5.setText('LIM OFF')
        self.button5.setStyleSheet("\n"
                                   "QPushButton {\n"
                                   "    background-color: #E47200; /* Set the background color to red */\n"
                                   "    color: #FFFFFF; /* Set the text color to white */\n"
                                   "    font-size: 16px; /* Set the font size to 16 pixels */\n"
                                   "    border-radius: 8px; /* Set the border radius to 5 pixels */\n"
                                   "    padding: 10px; /* Set the padding around the button */\n"
                                   "}")

        self.button6 = QPushButton(self)
        self.button6.setGeometry(1140, 580, 181, 81)
        self.button6.clicked.connect(self.button6_clicked)
        self.button6.setText('STOP')
        self.button6.setStyleSheet("\n"
                                   "QPushButton {\n"
                                   "    background-color: #FF0000; /* Set the background color to red */\n"
                                   "    color: #FFFFFF; /* Set the text color to white */\n"
                                   "    font-size: 16px; /* Set the font size to 16 pixels */\n"
                                   "    border-radius: 8px; /* Set the border radius to 5 pixels */\n"
                                   "    padding: 10px; /* Set the padding around the button */\n"
                                   "}")

        self.spin1 = QComboBox(self)
        self.spin1.setGeometry(950, 500, 181, 61)
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
        self.spin2.setGeometry(1140, 500, 181, 61)
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

        self.graph_widget = GraphWidget(self)
        self.graph_widget.setGeometry(300, 20, 641, 391)


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
                elif i < 31:
                    self.table4.setItem(i - 27, 0, item)
                elif i < 35:
                    self.table5.setItem(i - 29, 0, item)

                if len(values) >= 37:
                    self.lcd1.display(int(values[37]))
                if len(values) >= 38:
                    self.lcd2.display(int(values[38]))
                if len(values) >= 39:
                    self.lcd3.display(int(values[39]))

                if len(values) >= 40:
                    line = int(values[40])
                    x_data.append(line)  # Append x-axis data

                if len(values) >= 41:
                    line = int(values[41])
                    y_data.append(line)  # Append y-axis data

                    self.graph_widget.update_graph(x_data, y_data)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    timer = QTimer()
    timer.timeout.connect
    timer.start(200)
    timer.timeout.connect(lambda: send_array(data1))
    window.show()
    sys.exit(app.exec_())
