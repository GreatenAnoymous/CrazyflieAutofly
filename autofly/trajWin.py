from StateThread import *
from TableModel import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import gui2

class trajWin(QtWidgets.QMainWindow, gui2.Ui_choose_trajectory):
    def __init__(self,parent=None):
        super(trajWin, self).__init__(parent)
        self.setupUi(self)
        self.comboBox_initalize()
        self.comboBox_traj.currentIndexChanged.connect(self.selectionchange)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.rb_pre.clicked.connect(self.check)
        self.rb_file.clicked.connect(self.check)
        self.button_open.clicked.connect(self.openfile)
        self.opt=0
        self.accept_returned=[]
        

    def comboBox_initalize(self):
        self.comboBox_traj.addItem('circle')
        self.comboBox_traj.addItem('spiral')

    # to do if I want to add more items
    def selectionchange(self):
        return 0

    def openfile(self):
        self.openfile_name = QtWidgets.QFileDialog.getOpenFileName(self,'Select file')
        
        #print(type(openfile_name))
        
        if self.openfile_name[0]!='':
            self.browser_opened.setText(self.openfile_name[0])
            
        
  
    def check(self):
        if self.rb_pre.isChecked():
            self.opt=0
        else:
            self.opt=1

    def reject(self):
        self.hide()

    def accept(self):
        if opt==0:
            rc=self.doubleSpinBox_rc.value()
            zc=self.doubleSpinBox_zc.value()
            vc=self.doubleSpinBox_vc.value()
            #print([xc,yc,zc,vc])
            self.hide()
            self.accept_returned=[rc,zc,vc]

        else:
            if self.opt==1:
                self.hide()
                self.accept_returned=self.openfile_name[0]
            else: 
                self.accept_returned=[]
        

def gui2_main():
    app = QApplication(sys.argv)
    form = trajWin()
    form.show()
    app.exec_()
    
if __name__ == '__main__':
    gui2_main()