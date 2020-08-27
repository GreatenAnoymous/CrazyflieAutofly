import logging
import time
import threading


import numpy as np

import matplotlib


from matplotlib import pyplot
from matplotlib import animation
from mpl_toolkits import mplot3d

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.positioning.motion_commander import MotionCommander

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import gui



from StateThread import *

logging.basicConfig(level=logging.ERROR)

delta=0.05



class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        index=["x","y","z","yaw"]
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return index[section]

            if orientation == QtCore.Qt.Vertical:
                return str(section)





class ExampleApp(QtWidgets.QMainWindow, gui.Ui_Form):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.connected=False
        self.button_takeoff.clicked.connect(self.takeoff) 
        self.button_connect.clicked.connect(self.connect_switch)
        self.button_land.clicked.connect(self.land)
        self.button_send.clicked.connect(self.send_point)
        self.button_add.clicked.connect(self.add_point)
        self.button_follow.clicked.connect(self.follow_point)
        self.cf=Crazyflie()
        self.points=[]
        self.model=QtGui.QStandardItemModel(4,4,self.table_points)
        self.model.setHorizontalHeaderLabels(['x','y','z','yaw'])
      
        self.table_points.setModel(self.model)
        #self.mc=MotionCommander(self.cf)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        print(self.textEdit_uri.toPlainText())  #your uri
        
    def add_point(self):
        x=self.doubleSpinBox_x.value()
        y=self.doubleSpinBox_y.value()
        z=self.doubleSpinBox_z.value()
        yaw=self.doubleSpinBox_yaw.value()
        self.points.append([x,y,z,yaw])
        #rowPosition = self.table_points.rowCount()
        rowPosition = len(self.points)
        self.model=TableModel(self.points)
        #self.model.setHorizontalHeaderLabels(['x','y','z','yaw'])
        self.table_points.setModel(self.model)
        

    # go to the waypoint with velocity=0.1    
    def waypoint_goto(self,point,v=0.1):
        x=self.stateThread.x
        y=self.stateThread.y
        z=self.stateThread.z
        yaw=self.stateThread.yaw
        dist=((x-point[0])**2+(y-point[1])**2+(z-point[2])**2)**0.5
        duration=dist/v
        self.cf.high_level_commander.go_to(point[0],point[1],point[2],point[3],duration)
        time.sleep(duration)

    #follow the waypoints
    def follow_point(self):
        x=self.stateThread.x
        y=self.stateThread.y
        z=self.stateThread.z
        yaw=self.stateThread.yaw
        self.stateThread.trajectory=[]
        for p in self.points:
            self.stateThread.trajectory.append(p)
        for p in self.points:
            self.waypoint_goto(p)
            time.sleep(0.1)


    def connect_switch(self):
        if self.connected==False:
            try:
                self.cf.open_link(self.textEdit_uri.toPlainText())
            except (IndexError,RuntimeError,Exception):
                print("Cannot find a Crazyflie Dongle or the Crazyflie!")
            self.button_connect.setText("Connecting...")
            time.sleep(5)
            self.connected=True
            self.button_connect.setText("Disconnect")
        else:
            self.cf.close_link()
            self.connected=False
            self.button_connect.setText("Connect")

    def activate_high_level_commander(self):
        self.cf.param.set_value('commander.enHighLevel', '1')


    def activate_mellinger_controller(self, use_mellinger):
        controller = 1
        if use_mellinger:
            controller = 2
        self.cf.param.set_value('stabilizer.controller', controller) 

    def reset_estimator(self):
        self.cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        self.cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(0.1)
        
    def takeoff(self):
        print("Take off!")
        self.reset_estimator()
        self.activate_high_level_commander()
        self.stateThread=StateThread(self.cf)
        self.stateThread.start()
        self.cf.high_level_commander.takeoff(.3, 1.0)
        #self.mc.take_off(0.3,0.3)
        time.sleep(3)

    def land(self):
        print("Land!")
        self.cf.high_level_commander.land(0.0, 1.0)
        #self.stateThread.anim.event_source.stop()
       # del self.stateThread.anim
        #pyplot.close('all')
        #pyplot.close(self.stateThread.fig)
        self.stateThread.quit()
        time.sleep(2.0)

    def send_point(self):
        print("Go to the goal point!")
        x=self.doubleSpinBox_x.value()
        y=self.doubleSpinBox_y.value()
        z=self.doubleSpinBox_z.value()
        yaw=self.doubleSpinBox_yaw.value()
        self.cf.high_level_commander.go_to(x,y,z,yaw,1.0)

    

    def keyPressEvent(self, event):
        x=self.stateThread.x
        y=self.stateThread.y
        z=self.stateThread.z
        yaw=self.stateThread.yaw
        if (event.key() == QtCore.Qt.Key_W):
            self.cf.high_level_commander.go_to(x,y,z+delta,yaw,2*delta)
        if (event.key() == QtCore.Qt.Key_S):
            self.cf.high_level_commander.go_to(x,y,z-delta,yaw,2*delta)
        if (event.key() == QtCore.Qt.Key_A):
            self.cf.high_level_commander.go_to(x,y-delta,z,yaw,2*delta)
        if (event.key() == QtCore.Qt.Key_D):
            self.cf.high_level_commander.go_to(x,y+delta,z,yaw,2*delta)
        if (event.key() == QtCore.Qt.Key_Q):
            self.cf.high_level_commander.go_to(x-delta,y,z,yaw,2*delta)
        if (event.key() == QtCore.Qt.Key_E):
            self.cf.high_level_commander.go_to(x+delta,y,z,yaw,2*delta)


def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
    

if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)
    main()