from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

#
from global_config import *

class Main_ui(QMainWindow):
    def __init__(self):
        super(Main_ui, self).__init__()
        self.threadpool = QThreadPool()
        self.base_layout_config()
    # load DockWidget
    def base_layout_config(self):
        # resize app
        self.resize(1000,600)
        # create centraWidget
        self.centralWidget = QWidget(self)
        self.centralWidget.setFixedWidth(1)
        self.setCentralWidget(self.centralWidget)
        
        # create dock
        self.dock_input = QDockWidget("input", self)
        self.dock_output = QDockWidget("output", self)
        self.dock_img = QDockWidget("IMG", self)
        self.dock_audio = QDockWidget("Audio", self)
        self.dock_combine = QDockWidget("Combine", self)
        # add dock widget to main app
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_input)
        self.addDockWidget(Qt.RightDockWidgetArea , self.dock_img)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_audio)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_output)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_combine)
        # split img and audio dock to equally
        self.splitDockWidget(self.dock_img, self.dock_audio, Qt.Horizontal)
        self.resizeDocks([self.dock_input, self.dock_img,self.dock_audio,self.dock_output,self.dock_combine], [400, 400, 400,400,600], Qt.Horizontal)
        self.resizeDocks([self.dock_input, self.dock_img,self.dock_audio,self.dock_output,self.dock_combine], [500, 500, 500,400,400], Qt.Vertical)
        
        # create child widget
        input = QTextEdit()
        output = QTextEdit()
        img = QTextEdit()
        audio = QTextEdit()
        combine = QTextEdit()
        
        
        # add widget to dock
        self.dock_input.setWidget(input)
        self.dock_output.setWidget(output)
        self.dock_img.setWidget(img)
        self.dock_audio.setWidget(audio)
        self.dock_combine.setWidget(combine)

        

if __name__ == '__main__':
    app = QApplication([])
    window = Main_ui()
    window.show()
    app.exec()
