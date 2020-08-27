import logging
import time
import threading


import numpy as np
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


logging.basicConfig(level=logging.ERROR)
bs=1
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


class StateThread(QtCore.QThread):
    def __init__(self,cf):
        super(StateThread, self).__init__()
        self.cf=cf
        self.arm_length=0.1
        self.lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        self.lg_stab.add_variable('stateEstimate.x', 'float')
        self.lg_stab.add_variable('stateEstimate.y', 'float')
        self.lg_stab.add_variable('stateEstimate.z', 'float')
        self.lg_stab.add_variable('stateEstimate.roll', 'float')
        self.lg_stab.add_variable('stateEstimate.pitch', 'float')
        self.lg_stab.add_variable('stateEstimate.yaw', 'float')
        self.is_connected=False
        self.x=0;self.y=0;self.z=0;self.roll=0;self.pitch=0;self.yaw=0
  

    def run(self):
        
        self.is_connected=True
        
        try:
            self.cf.log.add_config(self.lg_stab)
            self.is_connected=True
            #self.cf.disconnected.add_callback(self._disconnected)
            # This callback will receive the data
            self.lg_stab.data_received_cb.add_callback(self._stab_log_data)
            # This callback will be called on errors
            #self._lg_stab.error_cb.add_callback(self._stab_log_error)
            # Start the logging
            self.lg_stab.start()
            self.visulize()
        except KeyError as e:
            print('Could not start log configuration,''{} not found in TOC'.format(str(e)))

    def _stab_log_data(self, timestamp, data, logconf):
        """Callback from a the log API when data arrives"""
        #print('[%d][%s]: %s' % (timestamp, logconf.name, data))
        self.x=data['stateEstimate.x']
        self.y=data['stateEstimate.y']
        self.z=data['stateEstimate.z']
        self.roll=data['stateEstimate.roll']
        self.pitch=data['stateEstimate.y']
        self.yaw=data['stateEstimate.y']
        #print(self.x,self.y,self.z)

    def _disconnected(self,link_uri):
        self.is_connected=False
        
       # self.anim.event_source.stop()
        
        #pyplot.close(self.fig)
        #print(data['stateEstimate.x'],data['stateEstimate.y'],data['stateEstimate.z'])

    def setup_plot(self):
        # setup
        self.fig = pyplot.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        pyplot.axis("equal")
        # plot labels
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        
        # plot limits
        plt_limits = np.array([[-bs, bs],[-bs, bs],[0, bs]])
        self.ax.set_xlim3d(plt_limits[0])
        self.ax.set_ylim3d(plt_limits[1])
        self.ax.set_zlim3d(plt_limits[2])
        flight_path, = self.ax.plot([], [], [], '--')
        colors = ['r', 'g', 'b', 'y']
        arms = [self.ax.plot([], [], [], c=colors[i], marker='^')[0] for i in range(4)]
        self.plot_artists = [flight_path, arms]
    
    def rotate(self, euler_angles, point):
        #phi=euler_angles[0]*np.pi/180.;theta=euler_angles[1];psi=euler_angles[2]
        [phi, theta, psi] = (euler_angles*np.pi/180.).tolist()
        cphi = np.cos(phi)
        sphi = np.sin(phi)
        cthe = np.cos(theta)
        sthe = np.sin(theta)
        cpsi = np.cos(psi)
        spsi = np.sin(psi)
        m = np.array([[cthe * cpsi, sphi * sthe * cpsi - cphi * spsi, cphi * sthe * cpsi + sphi * spsi],
                      [cthe * spsi, sphi * sthe * spsi + cphi * cpsi, cphi * sthe * spsi - sphi * cpsi],
                      [-sthe,       cthe * sphi,                      cthe * cphi]])

        return np.dot(m, point)

    def init_animate(self):
       
        self.plot_artists[0].set_data(0, 0)
        self.plot_artists[0].set_3d_properties(0)
        
        for arm in self.plot_artists[1]:
            arm.set_data([], [])
            arm.set_3d_properties([])

        return [self.plot_artists[0]] + self.plot_artists[1]

    def animate(self, i):
        center_point = np.array([self.x,self.y,self.z])
        euler_angles = np.array([self.roll,self.pitch,self.yaw])
        self.plot_artists[0].set_data(self.x, self.y)
        self.plot_artists[0].set_3d_properties(self.z)
        
        arm_base_pos = [[self.arm_length, 0, 0],
                                 [0, -self.arm_length, 0],
                                 [-self.arm_length, 0, 0],
                                 [0, self.arm_length, 0]]
        #print(euler_angles)
        arm_base_pos = [self.rotate(euler_angles, arm) for arm in arm_base_pos]
        # update the position
        arm_base_pos = [(arm + center_point) for arm in arm_base_pos]
        self.plot_arms(center_point, arm_base_pos)
        return [self.plot_artists[0]] + self.plot_artists[1]

    def plot_arms(self, center, arm_pos):
        arm_lines = self.plot_artists[1]
        for index, arm in enumerate(arm_pos):
            pos = np.column_stack((center, arm))
            arm_lines[index].set_data(pos[:2])
            arm_lines[index].set_3d_properties(pos[-1:])

    def visulize(self):
        self.setup_plot()
        
        self.anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init_animate, interval=20,blit=True)
        
        pyplot.gca().set_aspect("equal", adjustable="box")
       
        pyplot.show()



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
        
    def waypoint_goto(self,point,v=0.1):
        x=self.stateThread.x
        y=self.stateThread.y
        z=self.stateThread.z
        yaw=self.stateThread.yaw
        dist=((x-point[0])**2+(y-point[1])**2+(z-point[2])**2)**0.5
        duration=dist/v
        self.cf.high_level_commander.go_to(point[0],point[1],point[2],point[3],duration)
        time.sleep(duration)




    def follow_point(self):
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
       # pyplot.close(self.stateThread.fig)
        #self.stateThread.anim.event_source.stop()
        #del self.stateThread.anim
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

    def get_state(self):
        if self.connected==True:
            return

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