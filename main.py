import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
#

from ui.file_manager_ui import Ui_File_manager_Form
from ui.output_ui import Ui_Output_form
from ui.input_ui import Ui_Input_form
from ui.img_ui import Ui_Img_form
from ui.audio_ui import Ui_Audio_form
# 
from global_config import *
from gcp_speech_synthesis import *
from multiprocessing import Process
import textwrap

### Create UI
# input UI
class Input_Ui(QWidget,Ui_Input_form):
    def __init__(self, path):
        super().__init__()
        self.setupUi(self)
        self.content_layout.addWidget(File_manager(path))

# output UI
class Output_Ui(QWidget,Ui_Output_form):
    def __init__(self, path):
        super().__init__()
        self.setupUi(self)
        self.content_layout.addWidget(File_manager(path))
        
# img UI
class Img_Ui(QWidget,Ui_Img_form):
    def __init__(self, path):
        super().__init__()
        self.setupUi(self)
        self.content_layout.addWidget(File_manager(path))


# img UI
class Audio_Ui(QWidget,Ui_Audio_form):
    def __init__(self, path):
        super().__init__()
        self.setupUi(self)
        self.content_layout.addWidget(File_manager(path))


class File_manager(QWidget, Ui_File_manager_Form):
    def __init__(self, path):
        super(File_manager, self).__init__()
        self.setupUi(self)
        self.path = path
        self.isRename = False
        self.current_list = []
        self.delete_list = []
        self.populate(self.path)
    
    def populate(self, path):
        # add QFileSystemModel
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath(path)
        self.list_item.setModel(self.fileSystemModel)
        self.list_item.setRootIndex(self.fileSystemModel.index(path))
        self.list_item.setSortingEnabled(True)
        self.list_item.sortByColumn(0, Qt.AscendingOrder)
        
        self.list_item.setDragEnabled(True)
        self.list_item.setAcceptDrops(True)
        
        # 
        self.list_item.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        # setup watch 
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(path)
        
        # hidden tab
        self.list_item.hideColumn(1)
        self.list_item.hideColumn(2)
        self.list_item.hideColumn(3)
        # handle double click
        self.list_item.doubleClicked.connect(self.handle_double_clicked)
        self.list_item.pressed.connect(self.handle_currentChange)
        
        
        # Connect the customContextMenuRequested signal of the QTreeView to a slot
        self.list_item.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_item.customContextMenuRequested.connect(self.show_context_menu)

        # action
        self.browser.clicked.connect(lambda: os.startfile(self.path))
        self.fileSystemModel.directoryLoaded.connect(lambda: self.list_item_count.setText(str(len(os.listdir(self.path)))))
        self.watcher.directoryChanged.connect(lambda: self.list_item_count.setText(str(len(os.listdir(self.path)))))
 
    # remove elineEdit when click another item
    def handle_currentChange(self, e):
        self.delete_list = self.list_item.selectedIndexes()
        self.current_list.append(e)
        if len(self.current_list) >=2:
            prev_index = self.current_list.pop(0)
            self.list_item.setIndexWidget(prev_index, None)
            self.isRename = False
         
    # show context menu 
    def show_context_menu(self, pos):
        # Get the index under the cursor position
        index = self.list_item.indexAt(pos)
        self.old_index = 0
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
            delete_action.triggered.connect(self.delete_item)
            
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
            
    # new item
    def new_item(self):
        rename_file = 'New Document.txt'
        count = 1
        while rename_file in os.listdir(self.path):
            rename_file = f'New Document({count}).txt'
            count +=1
        new_document = os.path.join(self.path, rename_file)
        with open(new_document, 'w', encoding='utf-8') as f:
            pass
    # delete item
    def delete_item(self):
        print(self.delete_list)
        if self.delete_list:
            for cur_index in self.delete_list:
                self.fileSystemModel.remove(cur_index)
                self.delete_list = []
        
    # rename item
    def rename_item(self, index):
        self.isRename = True
        line_edit = QLineEdit()
        line_edit.setText(self.fileSystemModel.fileName(index))
        line_edit.selectAll()
        line_edit.returnPressed.connect(lambda: self.handle_rename(index, line_edit.text()))
        self.list_item.setIndexWidget(index, line_edit)

    def handle_rename(self,index, new_name):
        dir_path = self.fileSystemModel.filePath(index.parent())
        if new_name in os.listdir(dir_path):
            self.list_item.setIndexWidget(index, None)
            return False
        old_name = self.fileSystemModel.fileName(index)
        old_path = os.path.join(dir_path, old_name)
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)
        
    def handle_double_clicked(self, index):
        # Get the file path from the index
        file_path = self.fileSystemModel.filePath(index)
        os.startfile(file_path)
    
    
class Main_ui(QMainWindow):
    def __init__(self):
        super().__init__()
        # resize app
        self.resize(1000,600)
        self.threadpool = QThreadPool()
        
        self.load_baseConfig()
        self.setMouseTracking(True)
    # load DockWidget
    def load_baseConfig(self):
    
        # create centraWidget
        self.centralWidget = QWidget(self)
        self.centralWidget.setFixedWidth(1)
        self.setCentralWidget(self.centralWidget)
        
        # create dock
        self.dock_input = QDockWidget("input", self)
        self.dock_output = QDockWidget("output", self)
        self.dock_img = QDockWidget("IMG", self)
        self.dock_audio = QDockWidget("Audio", self)
        self.dock_logging = QDockWidget("Logging", self)
        self.dock_video = QDockWidget('Video', self)
        
        # add dock widget to main app
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_input)
        self.addDockWidget(Qt.RightDockWidgetArea , self.dock_img)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_audio)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_output)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_logging)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_video)
        # split img and audio dock to equally
        self.splitDockWidget(self.dock_img, self.dock_audio, Qt.Horizontal)
        self.splitDockWidget(self.dock_audio, self.dock_video, Qt.Horizontal)
        # 
        self.resizeDocks([self.dock_input, self.dock_img,self.dock_audio,self.dock_output,self.dock_logging,self.dock_video], [400, 400, 400,400,600,400], Qt.Horizontal)
        self.resizeDocks([self.dock_input, self.dock_img,self.dock_audio,self.dock_output,self.dock_logging, self.dock_video], [500, 500, 500,450,450, 400], Qt.Vertical)
        
        # create child widget
        self.input = Input_Ui(inputFolders)
        self.output = Output_Ui(outputAudio)
        self.img = Img_Ui(imgFoders)
        self.audio = Audio_Ui(audioFolders)
        self.video = File_manager(outputMP4)
        self.logging = QTextEdit()
        self.logging.setReadOnly(True)
        self.logging.ensureCursorVisible()
        
        # add widget to dock
        self.dock_input.setWidget(self.input)
        self.dock_output.setWidget(self.output)
        self.dock_img.setWidget(self.img)
        self.dock_audio.setWidget(self.audio)
        self.dock_logging.setWidget(self.logging)
        self.dock_video.setWidget(self.video)
        # 
        # sys.stdout = StdoutRedirector(self.combine)
        # 
        self.output.output_run.clicked.connect(self.thread_text_to_speech)
        

    def thread_text_to_speech(self):
        gcp_synthesis_worker = Worker(lambda: self.gcp_multi_text_to_speech(self.logging))
        self.threadpool.start(gcp_synthesis_worker)
    
    # logging 
    def logging_info(self, message ='', text_edit=''):
        print(f"{datetime.now()} - INFO : {str(message)}")
        QMetaObject.invokeMethod(text_edit, "append", Qt.QueuedConnection, Q_ARG(str, f"{datetime.now()} - INFO : {str(message)}"))
        
    def logging_warning(self, message ='', text_edit=''):
        print(f"{datetime.now()} - WARNING : {str(message)}")
        QMetaObject.invokeMethod(text_edit, "append", Qt.QueuedConnection, Q_ARG(str, f"{datetime.now()} - WARNING : {str(message)}"))
    
    def logging_error(self, message ='', text_edit=''):
        print(f"{datetime.now()} - ERROR : {str(message)}")
        QMetaObject.invokeMethod(text_edit, "append", Qt.QueuedConnection, Q_ARG(str, f"{datetime.now()} - ERROR : {str(message)}"))
        
    
    def gcp_text_to_speech(self, chapter_name='', chapter_data= '', text_edit = ''):
        self.handle_logging = Handle_logging()
        # initial veriable
        url = 'https://cxl-services.appspot.com/proxy?url=https://us-central1-texttospeech.googleapis.com/v1beta1/text:synthesize&token=0'
        base_logo = 'bạn đang nghe truyện audio trên kênh s truyện 2 4 7. nếu thấy hay đừng quên bấm like và sub cribe kênh nhé'
        chapter_data = chapter_data  + base_logo
        # audio
        audio_data = []
        audio_name = chapter_name.removesuffix('.txt') + '.wav'
        audio_path = os.path.join(outputAudio, audio_name)
        # split data
        self.logging_info(f'Split data from {chapter_name}', text_edit)
        list_contents = textwrap.wrap(chapter_data, width=3000)
        # 
        for current_count, current_content in enumerate(list_contents):
            payload_data = format_payload(text=current_content)
            try:
                self.logging_info(f'Request data from {chapter_name} to server....', text_edit)
                request_data = gcp_request(url=url, headers=gcp_headers, payload=payload_data)
                # return error when status code != 200 or != 201
                if request_data['status_code'] == 401:
                    self.logging_error(f'Failed to request server with message: {request_data["message"]}', text_edit)
                    return False
            except Exception as message:
                self.logging_error.error(message, text_edit)
                return False
            else:
                if request_data['status_code'] == 400:
                    self.logging_warning(f'False to request {chapter_name} text to server. Split payload and try again...', text_edit)
                    child_contents = textwrap.wrap(current_content, width=500)
                    for child_count, child_current_content in enumerate(child_contents):
                        child_payload_data = format_payload(text=child_current_content)
                        request_data = gcp_request(url=url, headers=gcp_headers, payload=child_payload_data)
                        if request_data['status'] == False:
                            self.logging_error(f'Second. false to request {chapter_name} text to server. Please check error code', text_edit)
                            return False
                        else:
                            audio_data.append(request_data)
        if not audio_data:
            self.logging_error(f"audio_data from {audio_name} is emtry", text_edit)
            return False
        combine_audio(audio_name=audio_name, audio_path= audio_path, audio_data=audio_data)
        self.logging_info(f"Success save audio {audio_name}", text_edit)
                    
    def gcp_multi_text_to_speech(self, text_edit):
        for chapter_name in os.listdir(inputFolders):
            chapter_path = os.path.join(inputFolders, chapter_name)
            with open(chapter_path, 'r', encoding='utf-8') as f:
                chapter_data = f.read()         
            result = self.gcp_text_to_speech(chapter_name=chapter_name, chapter_data=chapter_data, text_edit = text_edit)
            if not result:
                return
            print('result:', result)
    
    # 
    def closeEvent(self, event: QCloseEvent) -> None:
        # self.process.terminate()
        return super().closeEvent(event)
    
if __name__ == '__main__':
    app = QApplication([])
    window = Main_ui()
    window.show()
    app.exec()
    
