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

bs=1
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)        

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
        self.trajectory=[]
  

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
        plt_limits = [[-bs, bs],[-bs, bs],[0, bs]]
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
        self.plot_artists[0].set_data([p[0] for p in self.trajectory],[p[1] for p in self.trajectory])
        self.plot_artists[0].set_3d_properties([p[2] for p in self.trajectory])
        
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