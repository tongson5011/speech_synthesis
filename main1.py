from PySide6.QtWidgets import QMainWindow, QWidget, QDockWidget, QApplication, QTextEdit, QScrollBar, QFileSystemModel, QMenu, QLineEdit, QDialog, QDialogButtonBox
from PySide6.QtCore import Qt, QSize, QThreadPool, QDir,QObject, Signal, QRunnable, Slot, QFileSystemWatcher,QModelIndex,QRect, QThread, QMetaObject, QGenericReturnArgument
from PySide6.QtGui import QCursor, QStandardItemModel, QStandardItem, QAction, QMouseEvent
# 
from ui.input_ui import Ui_Input_form
from ui.output_ui import Ui_Output_form
from ui.log_form_ui import Ui_Log_form
## img 
from ui.img_ui import Ui_Img_form
from ui.img_options_ui import Ui_Img_Dialog
##
from ui.audio_ui import Ui_Audio_form
from ui.audio_img_ui import Ui_Audi_img_Form

# 
import sys
import traceback
import os
import re
import logging
#
from gcp_speech_synthesis import *

# 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')


# path
PATH = os.path.dirname(os.path.abspath(__file__))
inputFolders = os.path.join(PATH, 'inputFolders')
outputAudio = os.path.join(PATH,'outputAudio')
imgFoders = os.path.join(PATH, 'imgFolders')
audioFolders = os.path.join(PATH, 'audioFolders')
os.makedirs(inputFolders, exist_ok=True)
os.makedirs(outputAudio, exist_ok=True)
os.makedirs(imgFoders, exist_ok=True)
os.makedirs(audioFolders, exist_ok=True)



# short files in folder
def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

# threadpool
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

# threadpool
class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done
    def close(self):
        sys.exit()

# create custom signal
class MyObject(QObject):
    # Define the custom signal
    status = Signal(str)
    progress = Signal(int)
# create UI
# img option dialog

class Img_Options(QDialog,Ui_Img_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

##
class Audio_Img_Ui(QMainWindow):
    def __init__(self):
        super().__init__()
         # set line center
        self.edit_line = QWidget()
        self.edit_line.setObjectName('edit_line')
        self.edit_line.setFixedWidth(1)
        self.setCentralWidget(self.edit_line)
        # create dock
        self.dock_audio = QDockWidget("Audio", self)
        self.dock_img = QDockWidget("IMG", self)
        # add dock
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_img)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_audio)
        
        self.imgUi = ImgUi()
        self.audioUi = AudioUi()
        self.dock_img.setWidget(self.imgUi)
        self.dock_audio.setWidget(self.audioUi)
        
        

## audio form
class AudioUi(QWidget, Ui_Audio_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.populate()
    def populate(self):
        path = audioFolders
        # setup fileSystemModel
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath(path)
        self.audio_list.setModel(self.fileSystemModel)
        self.audio_list.setRootIndex(self.fileSystemModel.index(path))
        self.audio_list.setSortingEnabled(True)
        # setup watch 
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(path)
        # 
        # hidden tab
        self.audio_list.hideColumn(1)
        self.audio_list.hideColumn(2)
        self.audio_list.hideColumn(3)
        # 
        self.audio_list.doubleClicked.connect(self.handle_double_clicked)
        
        # Connect the customContextMenuRequested signal of the QTreeView to a slot
        self.audio_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.audio_list.customContextMenuRequested.connect(self.show_context_menu)

        # action
        self.browers.clicked.connect(lambda: os.startfile(path))
        self.fileSystemModel.directoryLoaded.connect(lambda: self.audio_count.setText(str(len(os.listdir(path)))))
        self.watcher.directoryChanged.connect(lambda: self.audio_count.setText(str(len(os.listdir(path)))))
    
    def handle_double_clicked(self, index):
        # Get the file path from the index
        file_path = self.fileSystemModel.filePath(index)
        os.startfile(file_path)
        
    def show_context_menu(self, pos):
        # Get the index under the cursor position
        index = self.audio_list.indexAt(pos)
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
        while rename_file in os.listdir(audioFolders):
            rename_file = f'New Document({count}).txt'
            count +=1
        new_document = os.path.join(audioFolders, rename_file)
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
        self.audio_list.setIndexWidget(index, line_edit)

    def handle_rename(self,index, new_name):
        dir_path = self.fileSystemModel.filePath(index.parent())
        if new_name in os.listdir(dir_path):
            self.audio_list.setIndexWidget(index, None)
            return False
        old_name = self.fileSystemModel.fileName(index)
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)


## img ui
class ImgUi(QWidget, Ui_Img_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.populate()
    def populate(self):
        path = imgFoders
        # setup fileSystemModel
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath(path)
        self.img_list.setModel(self.fileSystemModel)
        self.img_list.setRootIndex(self.fileSystemModel.index(path))
        self.img_list.setSortingEnabled(True)
        # setup watch 
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(path)
        # 
        # hidden tab
        self.img_list.hideColumn(1)
        self.img_list.hideColumn(2)
        self.img_list.hideColumn(3)
        # 
        self.img_list.doubleClicked.connect(self.handle_double_clicked)
        
        # Connect the customContextMenuRequested signal of the QTreeView to a slot
        self.img_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.img_list.customContextMenuRequested.connect(self.show_context_menu)

        # action
        self.browers.clicked.connect(lambda: os.startfile(path))
        self.fileSystemModel.directoryLoaded.connect(lambda: self.output_count.setText(str(len(os.listdir(path)))))
        self.watcher.directoryChanged.connect(lambda: self.output_count.setText(str(len(os.listdir(path)))))
    
    def handle_double_clicked(self, index):
        # Get the file path from the index
        file_path = self.fileSystemModel.filePath(index)
        os.startfile(file_path)
        
    def show_context_menu(self, pos):
        # Get the index under the cursor position
        index = self.img_list.indexAt(pos)
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
        while rename_file in os.listdir(imgFoders):
            rename_file = f'New Document({count}).txt'
            count +=1
        new_document = os.path.join(imgFoders, rename_file)
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
        self.img_list.setIndexWidget(index, line_edit)

    def handle_rename(self,index, new_name):
        dir_path = self.fileSystemModel.filePath(index.parent())
        if new_name in os.listdir(dir_path):
            self.img_list.setIndexWidget(index, None)
            return False
        old_name = self.fileSystemModel.fileName(index)
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)


##log form 
class LogFormUi(QWidget, Ui_Log_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
        self.watcher.directoryChanged.connect(lambda: self.input_count.setText(str(len(os.listdir(inputFolders)))))
    
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

# main ui
class Main_Ui(QMainWindow):
    app_windows = []
    def __init__(self):
        super(Main_Ui, self).__init__()
        # global config
        Main_Ui.app_windows.append(self)
        self.threadpool = QThreadPool()
        self._thread = QThread()
        self.mySignal =MyObject()
        # add UI
        ## img options
        self.img_option = Img_Options()
        self.img_option.setWindowFlags(self.img_option.windowFlags() | Qt.WindowStaysOnTopHint)
        ## add log
        self.log_form = LogFormUi()
        ## add Input UI
        self.inputUi = InputUi()
        ## add Output UI
        self.outputUi = OutputUi()
        ## add audio img UI
        self.audio_img_ui = Audio_Img_Ui()
        # 
        self.resize(QSize(1000,600))
        # create dock widget
        self.dock_input = QDockWidget("Input", self)
        self.dock_output = QDockWidget("Output", self)
        self.dock_audio = QDockWidget("Audio and IMG", self)
        self.dock_combine = QDockWidget("Combine", self)
        
        # set line center
        self.edit_line = QWidget()
        self.edit_line.setObjectName('edit_line')
        self.edit_line.setFixedWidth(1)
        ##########################
        # self.edit_line.setStyleSheet('background-color: #000;')
        self.setCentralWidget(self.edit_line)
        # add dock widget
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_input)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_output)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_audio)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_combine)
        
        self.resizeDocks([self.dock_input, self.dock_output, self.dock_audio, self.dock_combine], [300, 300, 800, 800], Qt.Horizontal)
        self.resizeDocks([ self.dock_audio,self.dock_combine], [400, 400], Qt.Vertical)
        # add widget
        self.handle_add_widget()
        # add Ui
        # main handle
        self.outputUi.output_run.clicked.connect(self.thread_TextToSpeech)
        self.mySignal.status.connect(lambda message: self.log_form.log_list.addItem(message))
        self.mySignal.progress.connect(lambda progress: self.log_form.log_process.setValue(progress))
        # 
        self.audio_img_ui.imgUi.img_btn_options.clicked.connect(self.handleShowImgOptions)
    # handle show img option
    def handleShowImgOptions(self):
        self.img_option.show()
        # 
        img_title_width = self.img_option.img_title_width.text()
        img_title_height = self.img_option.img_title_height.text()
        img_title_fontSize = self.img_option.img_title_fontSize.text()
        img_title_fontFamily = self.img_option.img_title_fontFamily.text()
        img_title_fontColor = self.img_option.img_title_fontColor.text()
        # 
        img_chap_width = self.img_option.img_chap_width.text()
        img_chap_height = self.img_option.img_chap_height.text()
        img_chap_fontSize = self.img_option.img_chap_fontSize.text()
        img_chap_fontFamily = self.img_option.img_chap_fontFamily.text()
        img_chap_fontColor = self.img_option.img_chap_fontColor.text()
        
        img_options = {img_title_width,img_title_height,img_title_fontSize,img_title_fontFamily, img_title_fontColor}
        
        
        
    # add widget to main app 
    def handle_add_widget(self):
        # add text edit to dock widget
        self.dock_input.setWidget(self.inputUi)
        self.dock_output.setWidget(self.outputUi)
        self.dock_combine.setWidget(self.log_form)
        titleWidget = QWidget(self)
        self.dock_audio.setTitleBarWidget(titleWidget)
        self.dock_audio.setWidget(self.audio_img_ui)
        
    def thread_TextToSpeech(self):
        worker = Worker(self.action_TextToSpeech)
        self.threadpool.start(worker)
        
    # handle text to speech 
    def action_TextToSpeech(self):
        self._threadpool = QThreadPool()
        # self._threadpool.setMaxThreadCount(3)
        url = 'url=https://us-central1-texttospeech.googleapis.com/v1beta1/text:synthesize&token=03AFcWeA4GyqF5e3yLHwsMyN4yCmm9WLtKTBMx8RmSLwzzv6OxkHLAus9la3HgRTkkpJkZc_GymUhlqGTkWUHjpdQhQSANRm8nNNH5nJcl-5JpXmqzmdzIA3GCxKBD-emEW_88a1p3N0x39fxYO-tBfkaFCeTyzrvTT-HwpyZNELkZCwPYRGZtmqv_WsBxXtZgvxgi-W4paeCuv-incka_ULApYdp55FUsZQ9J-q3vM2kwslSCs2S11Ip8UEtec89A4gMrFHEbkPBqW74Y1QYttQnptWuTipWdnUW6sPwBgrjAuvnkbH9w3EEM5LJZw1ePDlfHUQr0juGVmrOOSeA9hsqIHFx8uBEXHrLCEIVw1FSzw0hYr8rbwWC5Up0eaRmN_N6kIrkeccYMJ4PBqq8kPZVCBxM6F3QLRamwTp_9TjICoCHwfZXC3HGZEi1R8A_VdxxJkRqjKf_HOhZnYgK__BcvaWe48pqpXNJA5Y6ym-56q3Fkkm9rn_8tQCF3WRucY8k4armQ3s6BF46TpcpG1qsZ-F8QoF5kUzA3YzWTz1oPApNI_Mv_oXVly16quvKW8159gDD8kXNagIlwihwWgy6XEx_ruySKdQ'
        for chapter_name in os.listdir(inputFolders):
            chapter_path = os.path.join(inputFolders, chapter_name)
            with open(chapter_path, 'r', encoding='utf-8') as f:
                chapter_data = f.read()
                worker = Worker(self.handle_TextToSpeech,*[url,chapter_name, chapter_data])
                self._threadpool.start(worker)
    ## text to speech
    def handle_TextToSpeech(self, url = '', chapter_name='', chapter_data='', is_title= False, ):
        if len(os.listdir(inputFolders)) == 0:
            logging.error('Input Folder is emtry')
            return False
        base_logo = 'bạn đang nghe truyện audio trên kênh s truyện 2 4 7. nếu thấy hay đừng quên bấm like và sub cribe kênh nhé'
        # 
        base_url = f'https://cxl-services.appspot.com/proxy?{url}' if not url.startswith(
        'https://cxl-services.appspot.com/proxy?') else url
        # 
        audio_data = []
        # 
        if is_title:
            chapter_title = ' '.join(chapter_name.split('.')[0:-1]) if len(chapter_name.split('.')) > 1 else chapter_name.split('.')[-1]
            chapter_contents = formatText(f'''{chapter_title}. {chapter_data}. {base_logo}''')
        chapter_contents = formatText(f'''{chapter_data}. {base_logo}''')
        # split chapter contents to list with 3000 word
        chapter_lists = textwrap.wrap(chapter_contents, width=3000)
        logging.info(f'Request data from {chapter_name} to server....')
        self.mySignal.status.emit(f'Request data from {chapter_name} to server....')
        for current_count, current_chapter_content in enumerate(chapter_lists):
            current_count +=1
            self.mySignal.progress.emit(int(current_count*100/len(chapter_lists)))
            payload_data = format_payload(text=current_chapter_content)
            request_data = gcp_request(base_url, payload_data)
            if not request_data:
                logging.warning(f'First. false to request {chapter_name} text to server. Split payload and try again...')
                self.mySignal.status.emit(f'First. false to request {chapter_name} text to server. Split payload and try again...')
                new_data_list = textwrap.wrap(current_chapter_content, width=500)
                for new_count, new_chapter_data in enumerate(new_data_list):
                    new_payload_data = format_payload(text=new_chapter_data)
                    request_data = gcp_request(base_url, new_payload_data)
                    if not request_data:
                        logging.error(f'Second. false to request {chapter_name} text to server. Please check error code')
                        self.mySignal.status.emit(f'Second. false to request {chapter_name} text to server. Please check error code')
                        return False
                    else:
                        audio_data.append(request_data)
            else:
                audio_data.append(request_data)
        if audio_data:
            audio_name = ' '.join(chapter_name.split('.')[0:-1]) + '.wav' if len(chapter_name.split('.')) > 1 else chapter_name.split('.')[-1] + '.wav'
            audio_path = os.path.join(outputAudio, audio_name)
            result = combine_audio(audio_name = audio_name, audio_path= audio_path, audio_data=audio_data)
            if result:
                self.mySignal.status.emit(f"Success save audio {audio_name}")
            else:
                self.mySignal.status.emit(f"Failed save audio {audio_name}")
                return False
    
    # close event
    def closeEvent(self, event):
        # Remove this window from the list of windows
        Main_Ui.app_windows.remove(self)
        event.accept()
        self.threadpool.clear()


if __name__ == '__main__':
    app = QApplication([])
    window = Main_Ui()
    window.show()
    app.exec()
