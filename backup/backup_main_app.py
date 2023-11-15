from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# 
from ui.input_ui import Ui_Input_form
from ui.output_ui import Ui_Output_form
#
from global_config import *

class Left_dockWidget(QMainWindow):
    def __init__(self):
        super(Left_dockWidget,self).__init__()
         # set line center
        self.edit_line = QWidget()
        self.edit_line.setFixedWidth(1)
        self.setCentralWidget(self.edit_line)
        
         # create dock widget
        self.dock_input = QDockWidget("Input", self)
        self.dock_output = QDockWidget("Output", self)
        
         # add dock widget
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_input)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_output)
        
                # add UI
        self.input_ui = InputUi()
        self.output_ui = OutputUi()
        # self.input = QListWidget()
        # self.output = QListWidget()
        
        # # add text edit to dock widget
        self.dock_input.setWidget(self.input_ui)
        self.dock_output.setWidget(self.output_ui)
        
        
        
        
class Right_dockWidget(QMainWindow):
    def __init__(self):
        super(Right_dockWidget,self).__init__()
         # set line center
        self.edit_line = QWidget()
        self.edit_line.setFixedWidth(1)
        self.setCentralWidget(self.edit_line)
        
         # create dock widget
        self.dock_img = QDockWidget("IMG", self)
        self.dock_audio = QDockWidget("AUDIO", self)
        self.dock_combine = QDockWidget("COMBINE", self)
        
         # add dock widget
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_img)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_audio)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_combine)
        
        self.img = QListWidget()
        self.audio = QTextEdit()
        self.combine = QTextEdit()
        
        # add text edit to dock widget
        self.dock_img.setWidget(self.img)
        self.dock_audio.setWidget(self.audio)
        self.dock_combine.setWidget(self.combine)
        
        self.resizeDocks([self.dock_img, self.dock_audio,self.dock_combine ], [500, 500, 500], Qt.Vertical)
        
        
class Main_dockWidget(QMainWindow):
    def __init__(self):
        super(Main_dockWidget,self).__init__()
        #  set line center
        self.edit_line = QWidget()
        self.edit_line.setFixedWidth(1)
        self.setCentralWidget(self.edit_line)
        
        self.dock_left = QDockWidget("Left", self)
        self.dock_Right = QDockWidget("Right", self)
        self.dock_left.setTitleBarWidget(QWidget())
        self.dock_Right.setTitleBarWidget(QWidget())

         # add dock widget
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_left)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_Right)
        self.resizeDocks([self.dock_left, self.dock_Right], [400, 700], Qt.Horizontal)
        
## input UI
class InputUi(QWidget, Ui_Input_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.populate()
    
    def populate(self):
        # setup fileSystemModel
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath(inputFolders)
        self.input_list.setModel(self.fileSystemModel)
        self.input_list.setRootIndex(self.fileSystemModel.index(inputFolders))
        self.input_list.setSortingEnabled(True)
        # setup watch 
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(inputFolders)
        # 
        # hidden tab
        self.input_list.hideColumn(1)
        self.input_list.hideColumn(2)
        self.input_list.hideColumn(3)
        # 
        self.input_list.doubleClicked.connect(self.handle_double_clicked)
        
        # Connect the customContextMenuRequested signal of the QTreeView to a slot
        self.input_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.input_list.customContextMenuRequested.connect(self.show_context_menu)

        # action
        self.browers.clicked.connect(lambda: os.startfile(inputFolders))
        self.fileSystemModel.directoryLoaded.connect(lambda: self.input_count.setText(str(len(os.listdir(inputFolders)))))
        self.watcher.directoryChanged.connect(lambda: self.input_count.setText(str(len(os.listdir(inputFolders)))))\
    
    def handle_double_clicked(self, index):
        # Get the file path from the index
        file_path = self.fileSystemModel.filePath(index)
        os.startfile(file_path)
        
    def show_context_menu(self, pos):
        # Get the index under the cursor position
        index = self.input_list.indexAt(pos)
        # If the index is valid, show a context menu
        # 
        if index.isValid():
            menu = QMenu()
            # Add a rename action to the context menu
            rename_action = QAction("Rename", self)
            delete_action = QAction('Delete', self)
            new_action = QAction('New', self)
            
            # 
            menu.addAction(new_action)
            menu.addAction(rename_action)
            menu.addAction(delete_action)
            # 
            new_action.triggered.connect(self.new_item)
            rename_action.triggered.connect(lambda: self.rename_item(index))
            delete_action.triggered.connect(lambda: self.delete_item(index))
            
            # Show the context menu at the cursor position
            cursor = QCursor()
            menu.exec(cursor.pos())
        else:
            menu = QMenu()
            new_action = QAction('New', self)
            # 
            menu.addAction(new_action)
            # 
            new_action.triggered.connect(self.new_item)
            
            # Show the context menu at the cursor position
            cursor = QCursor()
            menu.exec(cursor.pos())
    
    #   
    def new_item(self):
        rename_file = 'New Document.txt'
        count = 1
        while rename_file in os.listdir(inputFolders):
            rename_file = f'New Document({count}).txt'
            count +=1
        new_document = os.path.join(inputFolders, rename_file)
        with open(new_document, 'w', encoding='utf-8') as f:
            pass
    # delete item
    def delete_item(self, index):
        file_path = self.fileSystemModel.filePath(index)
        os.remove(file_path)
        
    # rename item
    def rename_item(self, index):
        print(self.fileSystemModel.fileName(index))
        line_edit = QLineEdit()
        line_edit.setText(self.fileSystemModel.fileName(index))
        line_edit.selectAll()
        line_edit.returnPressed.connect(lambda: self.handle_rename(index, line_edit.text()))
        self.input_list.setIndexWidget(index, line_edit)

    def handle_rename(self,index, new_name):
        dir_path = self.fileSystemModel.filePath(index.parent())
        if new_name in os.listdir(dir_path):
            self.input_list.setIndexWidget(index, None)
            return False
        old_name = self.fileSystemModel.fileName(index)
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)
        # self.fileSystemModel.setData(index, new_path)
        

## input UI
class OutputUi(QWidget, Ui_Output_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.populate()
    def populate(self):
        # setup fileSystemModel
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath(outputAudio)
        self.output_list.setModel(self.fileSystemModel)
        self.output_list.setRootIndex(self.fileSystemModel.index(outputAudio))
        self.output_list.setSortingEnabled(True)
        # setup watch 
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(outputAudio)
        # 
        # hidden tab
        self.output_list.hideColumn(1)
        self.output_list.hideColumn(2)
        self.output_list.hideColumn(3)
        # 
        self.output_list.doubleClicked.connect(self.handle_double_clicked)
        
        # Connect the customContextMenuRequested signal of the QTreeView to a slot
        self.output_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.output_list.customContextMenuRequested.connect(self.show_context_menu)

        # action
        self.browers.clicked.connect(lambda: os.startfile(outputAudio))
        self.fileSystemModel.directoryLoaded.connect(lambda: self.output_count.setText(str(len(os.listdir(inputFolders)))))
        self.watcher.directoryChanged.connect(lambda: self.output_count.setText(str(len(os.listdir(inputFolders)))))
    
    def handle_double_clicked(self, index):
        # Get the file path from the index
        file_path = self.fileSystemModel.filePath(index)
        os.startfile(file_path)
        
    def show_context_menu(self, pos):
        # Get the index under the cursor position
        index = self.output_list.indexAt(pos)
        # If the index is valid, show a context menu
        # 
        # 
        if index.isValid():
            menu = QMenu()
            # Add a rename action to the context menu
            rename_action = QAction("Rename", self)
            delete_action = QAction('Delete', self)
            new_action = QAction('New', self)
            
            # 
            menu.addAction(new_action)
            menu.addAction(rename_action)
            menu.addAction(delete_action)
            # 
            new_action.triggered.connect(self.new_item)
            rename_action.triggered.connect(lambda: self.rename_item(index))
            delete_action.triggered.connect(lambda: self.delete_item(index))
            
            # Show the context menu at the cursor position
            cursor = QCursor()
            menu.exec(cursor.pos())
        else:
            menu = QMenu()
            new_action = QAction('New', self)
            # 
            menu.addAction(new_action)
            # 
            new_action.triggered.connect(self.new_item)
            
            # Show the context menu at the cursor position
            cursor = QCursor()
            menu.exec(cursor.pos())
    #   
    def new_item(self):
        rename_file = 'New Document.txt'
        count = 1
        while rename_file in os.listdir(outputAudio):
            rename_file = f'New Document({count}).txt'
            count +=1
        new_document = os.path.join(outputAudio, rename_file)
        with open(new_document, 'w', encoding='utf-8') as f:
            pass
        
    # delete item
    def delete_item(self, index):
        file_path = self.fileSystemModel.filePath(index)
        os.remove(file_path)
        
    # rename item
    def rename_item(self, index):
        line_edit = QLineEdit()
        line_edit.setText(self.fileSystemModel.fileName(index))
        line_edit.selectAll()
        line_edit.returnPressed.connect(lambda: self.handle_rename(index, line_edit.text()))
        self.output_list.setIndexWidget(index, line_edit)

    def handle_rename(self,index, new_name):
        dir_path = self.fileSystemModel.filePath(index.parent())
        if new_name in os.listdir(dir_path):
            self.output_list.setIndexWidget(index, None)
            return False
        old_name = self.fileSystemModel.fileName(index)
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)
        
        

class Main_ui(QMainWindow):
    def __init__(self):
        super(Main_ui, self).__init__()
        self.threadpool = QThreadPool()
        self.base_layout_config()
        # initial dockWidget
        self.main_dock = Main_dockWidget()
        self.left_dock = Left_dockWidget()
        self.right_dock = Right_dockWidget()
        

        


        
            
        
    # load DockWidget
    def base_layout_config(self):
        # resize app
        self.resize(1000,600)
        # create centraWidget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        # initial dockWidget
        self.main_dock = Main_dockWidget()
        self.left_dock = Left_dockWidget()
        self.right_dock = Right_dockWidget()
        # create main layout
        self.main_layout = QVBoxLayout(self.centralWidget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        # add main dock
        self.main_layout.addWidget(self.main_dock)
        # add left and right dock
        self.main_dock.dock_left.setWidget(self.left_dock)
        self.main_dock.dock_Right.setWidget(self.right_dock)
        
        

if __name__ == '__main__':
    app = QApplication([])
    window = Main_ui()
    window.show()
    app.exec()
