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
import plotter

bs=1
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)        

class StateThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(list)
    def __init__(self,cf,plotter_s):
        super(StateThread, self).__init__()
        self.cf=cf
        self.plotter=plotter
        self.lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        self.lg_stab.add_variable('stateEstimate.x', 'float')
        self.lg_stab.add_variable('stateEstimate.y', 'float')
        self.lg_stab.add_variable('stateEstimate.z', 'float')
        self.lg_stab.add_variable('stateEstimate.roll', 'float')
        self.lg_stab.add_variable('stateEstimate.pitch', 'float')
        self.lg_stab.add_variable('stateEstimate.yaw', 'float')
        self.lg_stab.add_variable('radio.isConnected','uint8_t')
        self.is_connected=False
        self.x=0;self.y=0;self.z=0;self.roll=0;self.pitch=0;self.yaw=0

        self.visual=0
     
        self.plotter_s=plotter_s
  

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
            #self.visulize()
            
        except KeyError as e:
            print('Could not start log configuration,''{} not found in TOC'.format(str(e)))

    def _stab_log_data(self, timestamp, data, logconf):
        """Callback from a the log API when data arrives"""
        #print('[%d][%s]: %s' % (timestamp, logconf.name, data))
        self.x=data['stateEstimate.x']
        self.y=data['stateEstimate.y']
        self.z=data['stateEstimate.z']
        self.roll=data['stateEstimate.roll']
        self.pitch=data['stateEstimate.pitch']
        self.yaw=data['stateEstimate.yaw']
        self.is_connected=data['radio.isConnected']
        self.trigger.emit([self.x,self.y,self.z,self.roll,self.pitch,self.yaw,self.is_connected])
        self.plotter_s.set_data(self.x,self.y,self.z,self.roll,self.pitch,self.yaw)
       # print(self.x,self.y,self.z)
      #  print(self.visual)

    def _disconnected(self,link_uri):
        self.is_connected=False
       # self.anim.event_source.stop()
        
        #pyplot.close(self.fig)
        #print(data['stateEstimate.x'],data['stateEstimate.y'],data['stateEstimate.z'])

    
    
   
        #pyplot.show()