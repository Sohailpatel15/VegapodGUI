import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLCDNumber, QLabel, QPushButton, \
    QComboBox, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import pyqtgraph as pg
import time

device = XBeeDevice("COM7", 115200)  # Replace 'COM6' with the appropriate port name
device.open()

baud_rate = 115200

data1 = [0, 0, 0, 0]

x_data = []
y_data = []

x2_data = []
y2_data = []


class XBeeThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.xbee = None

    # Inside the XBeeThread class
    def run(self):
        self.xbee = device
        try:
            while True:
                start_time = time.time()
                xbee_data = None
                while xbee_data is None:
                    xbee_data = self.xbee.read_data_block(1000)  # Read a block of data as bytes
                    if xbee_data is not None:
                        break
                    if time.time() - start_time > 10:
                        break
                if xbee_data is not None:
                    data = xbee_data.data
                    self.data_received.emit(data.decode('utf-8').strip())  # Decode the data as UTF-8
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
        self.plot_widget.setTitle("")
        self.plot_widget.setLabel("left", "Value")
        self.plot_widget.setLabel("bottom", "Time")
        self.plot_widget.setBackground('w')

        # Create a layout and add the plot widget to it
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def update_graph(self, x_data, y_data):
        # Clear the previous plot
        self.plot_widget.clear()

        # Plot the new data
        self.plot_widget.plot(x_data, y_data)

    def update_graph2(self, x2_data, y2_data):
        # Clear the previous plot
        self.plot_widget.clear()

        # Plot the new data
        self.plot_widget.plot(x2_data, y2_data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VEGAPOD Hyperloop")
        self.setGeometry(0, 0, 1333, 888)

        self.setStyleSheet("""
                    QMainWindow {
                        background-color: #00001A;
                    }

                    QTableWidget {
                        background-color: #013A63;
                        border: 1px solid #013A63;
                    }

                    QLCDNumber {
                        background-color: #013A63;
                        color: white;
                        border: 1px solid #CCCCCC;
                    }

                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: white;
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
                        color: #29C5F6;
                        font-size: 16px;
                        border: 1px solid #CCCCCC;
                        padding: 5px;
            }
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

        self.Label = QLabel(self)
        self.Label.setGeometry(960, 30, 171, 51)
        self.Label.setText('ERROR DISPLAY!')

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
        self.graph_widget.setGeometry(300, 20, 321, 391)
        self.counter = 0

        self.graph_widget2 = GraphWidget(self)
        self.graph_widget2.setGeometry(620, 20, 321, 391)
        self.counter2 = 0

        self.countdown_timer = QTimer()
        self.countdown_value = 5
        self.button1.clicked.connect(self.start_countdown)

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
        data1[1] = self.selected_item1
        data1[2] = self.selected_item2
        data1[3] = 0
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
        data1[2] = 0
        data1[3] = 0

    send_array(data1)

    def start_countdown(self):
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)  # Update the countdown every 1 second

    def update_countdown(self):
        self.countdown_value -= 1
        if self.countdown_value > 0:
            # Update the button text with the current countdown value
            self.button1.setText(str(self.countdown_value))
        else:
            # Countdown finished, stop the timer and perform any desired actions
            self.countdown_timer.stop()
            self.button1.setText("START")  # Reset the button text
            # Add any additional actions to perform after the countdown here

    def update_table_rows(self, data):
        chunks = data.split(",")
        if chunks[0] == "start" and chunks[-1] == "stop":
            values = chunks[1:-1]
            for i in range(min(len(values), 35)):
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

            if len(values) >= 36:
                self.lcd1.display(int(values[36]))
            if len(values) >= 37:
                self.lcd2.display(int(values[37]))
            if len(values) >= 38:
                self.lcd3.display(int(values[38]))

            if len(values) >= 42:
                self.counter += 1

                x = float(self.counter)
                x_data.append(x)

                line = float(values[42])
                y_data.append(line)  # Append y-axis data

                self.graph_widget.update_graph(x_data, y_data)

            if len(values) >= 43:
                self.counter2 += 1

                x2 = float(self.counter2)
                x2_data.append(x2)

                line2 = float(values[43])
                y2_data.append(line2)  # Append y-axis data

                self.graph_widget2.update_graph2(x2_data, y2_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    timer = QTimer()
    timer.timeout.connect
    timer.start(200)
    timer.timeout.connect(lambda: send_array(data1))
    window.show()
    sys.exit(app.exec_())
