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
from TableModel import *
from trajWin import *



logging.basicConfig(level=logging.ERROR)

delta=0.05



class MainApp(QtWidgets.QMainWindow, gui.Ui_Form):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.connected=False
        self.button_takeoff.clicked.connect(self.takeoff) 
        self.button_connect.clicked.connect(self.connect_switch)
        self.button_land.clicked.connect(self.land)
        self.button_send.clicked.connect(self.send_point)
        self.button_add.clicked.connect(self.add_point)
        self.button_follow.clicked.connect(self.follow_point)
        self.button_traj_select.clicked.connect(self.select_traj)
        self.button_traj_follow.clicked.connect(self.follow_traj)
        self.button_visualize.clicked.connect(self.visualize)
        self.cf=Crazyflie()
        self.points=[]  
        self.model=QtGui.QStandardItemModel(4,4,self.table_points)
        self.model.setHorizontalHeaderLabels(['x','y','z','yaw'])
        self.table_points.setModel(self.model)

        ########if we want to use Motion Commander#############
        ########self.mc=MotionCommander(self.cf)  #############
        #######################################################

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)  #avoid QtThread crashing after closing the windows
        print(self.textEdit_uri.toPlainText())  #your uri

    def visualize(self):
        self.stateThread.visual=1

    def add_point(self):
        x=self.doubleSpinBox_x.value()
        y=self.doubleSpinBox_y.value()
        z=self.doubleSpinBox_z.value()
        yaw=self.doubleSpinBox_yaw.value()
        self.points.append([x,y,z,yaw])
        self.model=TableModel(self.points)
        self.table_points.setModel(self.model)

    #select trajectory to follow

    def select_traj(self):
        self.w=trajWin()
        self.w.show()
    
    def display(self,status):
        slm=QtCore.QStringListModel()
        self.qList=['x: '+str(status[0]),'y: '+str(status[1]),'z: '+str(status[2]),'roll: '+str(status[3]),'pitch: '+str(status[4]),'yaw: '+str(status[5]),'isConnected: '+str(status[6])]
        slm.setStringList(self.qList)
        self.listView.setModel(slm)

    # go to the waypoint with default velocity=0.1    
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

    def follow_traj(self):
        if isinstance(self.w.accept_returned, str):
            if self.w.accept_returned!=' ':
                traj=np.loadtxt(self.w.accept_returned)
                cf2_follow_traj(traj)

        else:
            if len(self.w.accept_returned)!=0:
                rc=self.w.accept_returned[0]
                zc=self.w.accept_returned[1]
                vc=self.w.accept_returned[2]
                self.cf2_circle(rc,zc,vc)


    def cf2_circle(self,rc,zc,vc):
        # Number of setpoints sent per second
        fs = 4
        fsi = 1.0 / fs
        comp = 1.3
        # Compensation for unknown error :-(
        self.cf.high_level_commander.go_to(self.stateThread.x,self.stateThread.y,zc,0,1.0)
        poshold(self.cf, 2, zc)
        for _ in range(2):
        # The time for one revolution
            circle_time = 2*np.pi/vc
            steps = circle_time * fs
            for _ in range(steps):
                self.cf.commander.send_hover_setpoint(2*rc * comp * np.pi / circle_time,0, 360.0 / circle_time, zc)
                time.sleep(fsi)
        poshold(self.cf, 2, zc)

    #follow trajectory x,y,z,yaw
    def cf2_follow_traj(self,data):
        [t0,x0,y0,z0,yaw0]=data[0]
        self.cf.high_level_commander.go_to(x0,y0,z0,yaw0,1.0)
        poshold(self.cf, 2, zc)
        for i in range(1,data.shape[0]):
            p=data[i]
            duration=data[i,0]-data[i-1,0]
            self.cf.commander.send_position_setpoint(self, data[i,1], data[i,2], data[i,3], data[i,4])
            time.sleep(duration)


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
        #self.stateThread.trigger.connect(self.display)
        self.cf.high_level_commander.takeoff(.3, 1.0)
        #self.mc.take_off(0.3,0.3)
        time.sleep(3)

    #land
    def land(self):
        print("Land!")
        self.cf.high_level_commander.land(0.0, 1.0)
        #self.stateThread.anim.event_source.stop()
        #del self.stateThread.anim
        #pyplot.close('all')
        fig = plt.gcf()
        pyplot.close(fig)
        self.stateThread.quit()
        time.sleep(2.0)

    def send_point(self):
        print("Go to the goal point!")
        x=self.doubleSpinBox_x.value()
        y=self.doubleSpinBox_y.value()
        z=self.doubleSpinBox_z.value()
        yaw=self.doubleSpinBox_yaw.value()
        self.cf.high_level_commander.go_to(x,y,z,yaw,1.0)

    
    #use your keyboard to control the uav
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
    form = MainApp()
    form.show()
    app.exec_()
    

if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)
    main()