# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'traj_select.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_choose_trajectory(object):
    def setupUi(self, choose_trajectory):
        choose_trajectory.setObjectName("choose_trajectory")
        choose_trajectory.resize(664, 455)
        self.comboBox_traj = QtWidgets.QComboBox(choose_trajectory)
        self.comboBox_traj.setGeometry(QtCore.QRect(230, 20, 221, 31))
        self.comboBox_traj.setObjectName("comboBox_traj")
        self.label = QtWidgets.QLabel(choose_trajectory)
        self.label.setGeometry(QtCore.QRect(30, 30, 191, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(choose_trajectory)
        self.label_2.setGeometry(QtCore.QRect(30, 280, 181, 21))
        self.label_2.setObjectName("label_2")
        self.button_open = QtWidgets.QPushButton(choose_trajectory)
        self.button_open.setGeometry(QtCore.QRect(220, 280, 106, 30))
        self.button_open.setObjectName("button_open")
        self.browser_opened = QtWidgets.QTextBrowser(choose_trajectory)
        self.browser_opened.setGeometry(QtCore.QRect(340, 280, 301, 31))
        self.browser_opened.setObjectName("browser_opened")
        self.rb_pre = QtWidgets.QRadioButton(choose_trajectory)
        self.rb_pre.setGeometry(QtCore.QRect(40, 60, 133, 27))
        self.rb_pre.setObjectName("rb_pre")
        self.rb_file = QtWidgets.QRadioButton(choose_trajectory)
        self.rb_file.setGeometry(QtCore.QRect(40, 310, 133, 27))
        self.rb_file.setObjectName("rb_file")
        self.buttonBox = QtWidgets.QDialogButtonBox(choose_trajectory)
        self.buttonBox.setGeometry(QtCore.QRect(440, 390, 175, 28))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.doubleSpinBox_rc = QtWidgets.QDoubleSpinBox(choose_trajectory)
        self.doubleSpinBox_rc.setGeometry(QtCore.QRect(80, 90, 77, 30))
        self.doubleSpinBox_rc.setObjectName("doubleSpinBox_rc")
        self.label_3 = QtWidgets.QLabel(choose_trajectory)
        self.label_3.setGeometry(QtCore.QRect(40, 90, 80, 31))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(choose_trajectory)
        self.label_5.setGeometry(QtCore.QRect(230, 90, 80, 31))
        self.label_5.setObjectName("label_5")
        self.doubleSpinBox_zc = QtWidgets.QDoubleSpinBox(choose_trajectory)
        self.doubleSpinBox_zc.setGeometry(QtCore.QRect(270, 90, 77, 30))
        self.doubleSpinBox_zc.setObjectName("doubleSpinBox_zc")
        self.label_6 = QtWidgets.QLabel(choose_trajectory)
        self.label_6.setGeometry(QtCore.QRect(440, 90, 80, 31))
        self.label_6.setObjectName("label_6")
        self.doubleSpinBox_vc = QtWidgets.QDoubleSpinBox(choose_trajectory)
        self.doubleSpinBox_vc.setGeometry(QtCore.QRect(480, 90, 77, 30))
        self.doubleSpinBox_vc.setObjectName("doubleSpinBox_vc")

        self.retranslateUi(choose_trajectory)
        QtCore.QMetaObject.connectSlotsByName(choose_trajectory)

    def retranslateUi(self, choose_trajectory):
        _translate = QtCore.QCoreApplication.translate
        choose_trajectory.setWindowTitle(_translate("choose_trajectory", "Choose trajectory"))
        self.label.setText(_translate("choose_trajectory", "Predefined trajectory:"))
        self.label_2.setText(_translate("choose_trajectory", "Trajectory from file:"))
        self.button_open.setText(_translate("choose_trajectory", "Open"))
        self.rb_pre.setText(_translate("choose_trajectory", "Use this"))
        self.rb_file.setText(_translate("choose_trajectory", "Use this"))
        self.label_3.setText(_translate("choose_trajectory", "Rc"))
        self.label_5.setText(_translate("choose_trajectory", "Zc"))
        self.label_6.setText(_translate("choose_trajectory", "Wc"))

