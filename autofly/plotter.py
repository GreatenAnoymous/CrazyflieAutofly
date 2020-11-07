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

class Plotter:
    def __init__(self,cf,canvas,fig):
        self.cf=cf
        self.canvas=canvas
        self.fig=fig
        
        self.x=0;self.y=0;self.z=0;self.roll=0;self.pitch=0;self.yaw=0
        self.arm_length=0.1
        self.trajectory=[]

    def set_data(self,x,y,z,roll,pitch,yaw):
        self.x=x
        self.y=y
        self.z=z
        self.roll=roll
        self.pitch=pitch
        self.yaw=yaw

    def setup_plot(self):
        # setup
        #self.fig = pyplot.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.axis("equal")
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

    def animate(self):
     
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
        self.canvas.draw()
        return [self.plot_artists[0]] + self.plot_artists[1]

    def plot_arms(self, center, arm_pos):
        arm_lines = self.plot_artists[1]
        for index, arm in enumerate(arm_pos):
            pos = np.column_stack((center, arm))
            arm_lines[index].set_data(pos[:2])
            arm_lines[index].set_3d_properties(pos[-1:])

    def visulize(self):
        self.setup_plot()
        self._timer = self.canvas.new_timer(100, [(self.animate, (), {})])
        self._timer.start()
        #self.anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init_animate, interval=20,blit=True)
     
        self.ax.set_aspect("equal",adjustable="box")
        #pyplot.gca().set_aspect("equal", adjustable="box")
       # self.fig.canvas.draw()
  
