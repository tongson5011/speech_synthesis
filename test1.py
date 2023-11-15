
from qframelesswindow import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys, os
from ui.main_ui import Ui_MainWindow
from ui.input_ui import Ui_Input_form

# path
PATH = os.path.dirname(os.path.abspath(__file__))
inputFolders = os.path.join(PATH, 'inputFolders')
outputAudio = os.path.join(PATH,'outputAudio')
os.makedirs(inputFolders, exist_ok=True)
os.makedirs(outputAudio, exist_ok=True)

# create UI
## input UI
class InputUi(QWidget, Ui_Input_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath(inputFolders)
        self.input_list.setModel(self.fileSystemModel)
        self.input_list.setRootIndex(self.fileSystemModel.index(inputFolders))
        # 
        self.input_list.hideColumn(1)
        self.input_list.hideColumn(2)
        self.input_list.hideColumn(3)
        # 
        self.input_list.doubleClicked.connect(self.handle_double_clicked)
        
        # Connect the customContextMenuRequested signal of the QTreeView to a slot
        self.input_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.input_list.customContextMenuRequested.connect(self.show_context_menu)
        
    def handle_double_clicked(self, index):
        # Get the file path from the index
        file_path = self.fileSystemModel.filePath(index)
        os.startfile(file_path)
        
    def show_context_menu(self, pos):
        # Get the index under the cursor position
        index = self.input_list.indexAt(pos)
        
        # If the index is valid, show a context menu
        if index.isValid():
            menu = QMenu()
            # Add a rename action to the context menu
            rename_action = QAction("Rename", self)
            rename_action.triggered.connect(lambda: self.rename_item(index))
            menu.addAction(rename_action)
            
            # Show the context menu at the cursor position
            cursor = QCursor()
            menu.exec(cursor.pos())
    def rename_item(self, index):
        line_edit = QLineEdit()
        line_edit.setText(self.fileSystemModel.fileName(index))
        line_edit.selectAll()
        line_edit.returnPressed.connect(lambda: self.handle_rename(index, line_edit.text()))
        self.input_list.setIndexWidget(index, line_edit)
        # self.input_list.setIndexWidget(index, None)
    def handle_rename(self,index, new_name):
        
        dir_path = self.fileSystemModel.filePath(index.parent())
        if new_name in os.listdir(dir_path):
            return False
        old_name = self.fileSystemModel.fileName(index)
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)
        # self.fileSystemModel.setData(index, new_path)
        self.input_list.setIndexWidget(index, None)

class DocWidget(QMainWindow):
    def __init__(self):
        super(DocWidget, self).__init__()
        # self.resize(QSize(300,400))
        self.dock_input = QDockWidget("Input", self)
        
        # set line center
        self.edit_line = QWidget()
        self.edit_line.setObjectName('edit_line')
        self.edit_line.setFixedWidth(1)
        self.setCentralWidget(self.edit_line)
        
        
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_input)
        
        self.input_ui = InputUi()
        self.dock_input.setWidget(self.input_ui)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.input_layout.addWidget(DocWidget())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
