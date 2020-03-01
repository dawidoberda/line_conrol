from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QFrame
import sys
from configparser import ConfigParser
import os

class MyWindow1(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow1, self).__init__() #dziedziczenie konstruktora z klasy rodzica
        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle("Configure")
        self.initUI()

    def cancel_clicked(self):
        self.close()

    def save_clicked(self):
        optical_pin_write = self.text1.text()
        print('Optical pin set to : {}'.format(optical_pin_write))

        reed1_pin_write = self.text2.text()
        print('Reed 1 pin set to : {}'.format(reed1_pin_write))

        reed2_pin_write = self.text3.text()
        print('Reed 2 pin set to : {}'.format(reed2_pin_write))

        reed3_pin_write = self.text4.text()
        print('Reed 3 pin set to : {}'.format(reed3_pin_write))

        delay_time_write = self.text5.text()
        print('delay time write set to : {}'.format(delay_time_write))

        optical_file_write = self.text6.text()
        print('optical file set to {}'.format(optical_file_write))

        reed1_file_write = self.text7.text()
        print('reed 1 file set to {}'.format(reed1_file_write))

        reed2_file_write = self.text8.text()
        print('reed 2 file set to {}'.format(reed2_file_write))

        reed3_file_write = self.text9.text()
        print('reed3 file set to : {}'.format(reed3_file_write))

        delay_file_write = self.text10.text()
        print('delay file set to : {}'.format(delay_file_write))

        self.close()

        config = ConfigParser()

        config.add_section('pins')
        config.set('pins', 'opt_sensor', optical_pin_write)
        config.set('pins', 'reed1', reed1_pin_write)
        config.set('pins', 'reed2', reed2_pin_write)
        config.set('pins', 'reed3', reed3_pin_write)

        config.add_section('delay')
        config.set('delay', 'accepted_low_time', delay_time_write)

        config.add_section('files')
        config.set('files', 'optical_file', optical_file_write)
        config.set('files', 'reed1_file', reed1_file_write)
        config.set('files', 'reed2_file', reed2_file_write)
        config.set('files', 'reed3_file', reed3_file_write)
        config.set('files', 'delay_file', delay_file_write)

        #TODO: dokonczyc zapis do ini

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        python = sys.executable
        os.execl(python, python, * sys.argv)


    def initUI(self):
        config = ConfigParser()
        config.read('config.ini')
        grid = QGridLayout()
        self.setLayout(grid)

        label1 = QtWidgets.QLabel(self)
        label1.setText('Optical Sensor Pin')
        grid.addWidget(label1, 0, 0)

        self.text1 = QtWidgets.QLineEdit(self)
        optical_pin_read = str(config.get('pins', 'opt_sensor'))
        self.text1.setText(optical_pin_read)
        grid.addWidget(self.text1,0 ,1)

        label2 = QtWidgets.QLabel(self)
        label2.setText('Reed 1 Pin')
        grid.addWidget(label2,1,0)

        self.text2 = QtWidgets.QLineEdit(self)
        reed1_pin_read = str(config.get('pins', 'reed1'))
        self.text2.setText(reed1_pin_read)
        grid.addWidget(self.text2,1, 1)

        label3 = QtWidgets.QLabel(self)
        label3.setText('Reed 2 Pin')
        grid.addWidget(label3,2,0)

        self.text3 = QtWidgets.QLineEdit(self)
        reed2_pin_read = str(config.get('pins', 'reed2'))
        self.text3.setText(reed2_pin_read)
        grid.addWidget(self.text3,2, 1)

        label4 = QtWidgets.QLabel(self)
        label4.setText('Reed 3 Pin')
        grid.addWidget(label4,3,0)

        self.text4 = QtWidgets.QLineEdit(self)
        reed3_pin_read = str(config.get('pins', 'reed3'))
        self.text4.setText(reed3_pin_read)
        grid.addWidget(self.text4,3, 1)

        line1 = QtWidgets.QFrame(self)
        line1.setFrameShape(QFrame.HLine)
        grid.addWidget(line1,4,0)
        line2 = QtWidgets.QFrame(self)
        line2.setFrameShape(QFrame.HLine)
        grid.addWidget(line2,4,1)

        label5 = QtWidgets.QLabel(self)
        label5.setText('Acceptable Delay Time')
        grid.addWidget(label5,5,0)

        self.text5 = QtWidgets.QLineEdit(self)
        accepted_delay_time = str(config.get('delay', 'accepted_low_time'))
        self.text5.setText(accepted_delay_time)
        grid.addWidget(self.text5,5, 1)

        #files

        label6 = QtWidgets.QLabel(self)
        label6.setText('Optical Sensor Output File')
        grid.addWidget(label6,6,0)

        self.text6 = QtWidgets.QLineEdit(self)
        optical_file = str(config.get('files', 'optical_file'))
        self.text6.setText(optical_file)
        grid.addWidget(self.text6,6, 1)

        #file2
        label7 = QtWidgets.QLabel(self)
        label7.setText('Reed1 Sensor Output File')
        grid.addWidget(label7,7,0)

        self.text7 = QtWidgets.QLineEdit(self)
        reed1_file = str(config.get('files', 'reed1_file'))
        self.text7.setText(reed1_file)
        grid.addWidget(self.text7,7, 1)

        #file3
        label8 = QtWidgets.QLabel(self)
        label8.setText('Reed2 Sensor Output File')
        grid.addWidget(label8,8,0)

        self.text8 = QtWidgets.QLineEdit(self)
        reed2_file = str(config.get('files', 'reed2_file'))
        self.text8.setText(reed2_file)
        grid.addWidget(self.text8,8, 1)

        #file4
        label9 = QtWidgets.QLabel(self)
        label9.setText('Reed3 Sensor Output File')
        grid.addWidget(label9,9,0)

        self.text9 = QtWidgets.QLineEdit(self)
        reed3_file = str(config.get('files', 'reed3_file'))
        self.text9.setText(reed3_file)
        grid.addWidget(self.text9,9, 1)

        #file5
        label10 = QtWidgets.QLabel(self)
        label10.setText('delay Output File')
        grid.addWidget(label10,10,0)

        self.text10 = QtWidgets.QLineEdit(self)
        delay_file = str(config.get('files', 'delay_file'))
        self.text10.setText(delay_file)
        grid.addWidget(self.text10, 10,1)

        btn1 = QtWidgets.QPushButton(self)
        btn1.setText("Save and Reboot")
        btn1.clicked.connect(self.save_clicked)
        grid.addWidget(btn1, 11, 0)

        btn2 = QtWidgets.QPushButton(self)
        btn2.setText("Cancel")
        btn2.clicked.connect(self.cancel_clicked)
        grid.addWidget(btn2, 11, 1)