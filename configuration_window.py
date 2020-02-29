from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QFrame
import sys
from configparser import ConfigParser

class MyWindow1(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow1, self).__init__() #dziedziczenie konstruktora z klasy rodzica
        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle("Configure")
        self.initUI()

    def initUI(self):
        config = ConfigParser()
        config.read('config.ini')
        grid = QGridLayout()
        self.setLayout(grid)

        label1 = QtWidgets.QLabel(self)
        label1.setText('Optical Sensor Pin')
        grid.addWidget(label1, 0, 0)

        text1 = QtWidgets.QLineEdit(self)
        optical_pin_read = str(config.get('pins', 'opt_sensor'))
        text1.setText(optical_pin_read)
        grid.addWidget(text1,0 ,1)

        label2 = QtWidgets.QLabel(self)
        label2.setText('Reed 1 Pin')
        grid.addWidget(label2,1,0)

        text2 = QtWidgets.QLineEdit(self)
        reed1_pin_read = str(config.get('pins', 'reed1'))
        text2.setText(reed1_pin_read)
        grid.addWidget(text2,1, 1)

        label3 = QtWidgets.QLabel(self)
        label3.setText('Reed 2 Pin')
        grid.addWidget(label3,2,0)

        text3 = QtWidgets.QLineEdit(self)
        reed2_pin_read = str(config.get('pins', 'reed2'))
        text3.setText(reed2_pin_read)
        grid.addWidget(text3,2, 1)

        label4 = QtWidgets.QLabel(self)
        label4.setText('Reed 3 Pin')
        grid.addWidget(label4,3,0)

        text4 = QtWidgets.QLineEdit(self)
        reed3_pin_read = str(config.get('pins', 'reed3'))
        text4.setText(reed3_pin_read)
        grid.addWidget(text4,3, 1)

        line1 = QtWidgets.QFrame(self)
        line1.setFrameShape(QFrame.HLine)
        grid.addWidget(line1,4,0)
        line2 = QtWidgets.QFrame(self)
        line2.setFrameShape(QFrame.HLine)
        grid.addWidget(line2,4,1)

        label5 = QtWidgets.QLabel(self)
        label5.setText('Acceptable Delay Time')
        grid.addWidget(label5,5,0)

        text5 = QtWidgets.QLineEdit(self)
        accepted_delay_time = str(config.get('delay', 'accepted_low_time'))
        text5.setText(accepted_delay_time)
        grid.addWidget(text5,5, 1)

        #files

        label6 = QtWidgets.QLabel(self)
        label6.setText('Optical Sensor Output File')
        grid.addWidget(label6,6,0)

        text6 = QtWidgets.QLineEdit(self)
        optical_file = str(config.get('files', 'optical_file'))
        text6.setText(optical_file)
        grid.addWidget(text6,6, 1)

        #file2
        label7 = QtWidgets.QLabel(self)
        label7.setText('Reed1 Sensor Output File')
        grid.addWidget(label7,7,0)

        text7 = QtWidgets.QLineEdit(self)
        reed1_file = str(config.get('files', 'reed1_file'))
        text7.setText(reed1_file)
        grid.addWidget(text7,7, 1)

        #file3
        label8 = QtWidgets.QLabel(self)
        label8.setText('Reed2 Sensor Output File')
        grid.addWidget(label8,8,0)

        text8 = QtWidgets.QLineEdit(self)
        reed2_file = str(config.get('files', 'reed2_file'))
        text8.setText(reed2_file)
        grid.addWidget(text8,8, 1)

        #file4
        label9 = QtWidgets.QLabel(self)
        label9.setText('Reed3 Sensor Output File')
        grid.addWidget(label9,9,0)

        text9 = QtWidgets.QLineEdit(self)
        reed3_file = str(config.get('files', 'reed3_file'))
        text9.setText(reed3_file)
        grid.addWidget(text9,9, 1)

        btn1 = QtWidgets.QPushButton(self)
        btn1.setText("Save & Reboot")
        grid.addWidget(btn1, 10, 0)

        btn2 = QtWidgets.QPushButton(self)
        btn2.setText("Cancel")
        grid.addWidget(btn2, 10, 1)