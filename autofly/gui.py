# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autofly.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(975, 788)
        self.textEdit_uri = QtWidgets.QTextEdit(Form)
        self.textEdit_uri.setGeometry(QtCore.QRect(60, 20, 281, 31))
        self.textEdit_uri.setObjectName("textEdit_uri")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 30, 80, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 181, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(140, 80, 80, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(240, 80, 80, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(340, 80, 80, 21))
        self.label_5.setObjectName("label_5")
        self.doubleSpinBox_x = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_x.setGeometry(QtCore.QRect(160, 80, 71, 21))
        self.doubleSpinBox_x.setObjectName("doubleSpinBox_x")
        self.doubleSpinBox_y = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_y.setGeometry(QtCore.QRect(260, 80, 71, 21))
        self.doubleSpinBox_y.setObjectName("doubleSpinBox_y")
        self.doubleSpinBox_z = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_z.setGeometry(QtCore.QRect(360, 80, 71, 21))
        self.doubleSpinBox_z.setObjectName("doubleSpinBox_z")
        self.button_send = QtWidgets.QPushButton(Form)
        self.button_send.setGeometry(QtCore.QRect(750, 70, 111, 51))
        self.button_send.setObjectName("button_send")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(440, 80, 80, 21))
        self.label_6.setObjectName("label_6")
        self.doubleSpinBox_yaw = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBox_yaw.setGeometry(QtCore.QRect(490, 80, 71, 21))
        self.doubleSpinBox_yaw.setObjectName("doubleSpinBox_yaw")
        self.button_takeoff = QtWidgets.QPushButton(Form)
        self.button_takeoff.setGeometry(QtCore.QRect(580, 20, 106, 30))
        self.button_takeoff.setObjectName("button_takeoff")
        self.button_land = QtWidgets.QPushButton(Form)
        self.button_land.setGeometry(QtCore.QRect(750, 20, 106, 30))
        self.button_land.setObjectName("button_land")
        self.button_connect = QtWidgets.QPushButton(Form)
        self.button_connect.setGeometry(QtCore.QRect(400, 20, 106, 30))
        self.button_connect.setObjectName("button_connect")
        self.button_visualize = QtWidgets.QPushButton(Form)
        self.button_visualize.setGeometry(QtCore.QRect(750, 180, 111, 41))
        self.button_visualize.setObjectName("button_visualize")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(80, 630, 651, 31))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(20, 140, 261, 21))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(20, 200, 261, 21))
        self.label_9.setObjectName("label_9")
        self.table_points = QtWidgets.QTableView(Form)
        self.table_points.setGeometry(QtCore.QRect(20, 250, 531, 281))
        self.table_points.setObjectName("table_points")
        self.button_add = QtWidgets.QPushButton(Form)
        self.button_add.setGeometry(QtCore.QRect(580, 70, 106, 30))
        self.button_add.setObjectName("button_add")
        self.button_follow = QtWidgets.QPushButton(Form)
        self.button_follow.setGeometry(QtCore.QRect(170, 189, 106, 41))
        self.button_follow.setObjectName("button_follow")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Crazyflie Autofly"))
        self.textEdit_uri.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">radio://0/80/250K</p></body></html>"))
        self.label.setText(_translate("Form", "URI:"))
        self.label_2.setText(_translate("Form", "Send Point:"))
        self.label_3.setText(_translate("Form", "x="))
        self.label_4.setText(_translate("Form", "y="))
        self.label_5.setText(_translate("Form", "z="))
        self.button_send.setText(_translate("Form", "Go"))
        self.label_6.setText(_translate("Form", "yaw="))
        self.button_takeoff.setText(_translate("Form", "Take Off"))
        self.button_land.setText(_translate("Form", "Land"))
        self.button_connect.setText(_translate("Form", "Connect"))
        self.button_visualize.setText(_translate("Form", "Visualize"))
        self.label_7.setText(_translate("Form", "Keyboard control:  up \"w\", down \"s\",   left \"a\", right \"d\", forward \"q\", back \"e\"          "))
        self.label_8.setText(_translate("Form", "Trajectory follow: to do"))
        self.label_9.setText(_translate("Form", "Waypoints follow: "))
        self.button_add.setText(_translate("Form", "Add Point"))
        self.button_follow.setText(_translate("Form", "Follow"))

