import os
# import logging
import sys
import traceback
import re
from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThread, QCoreApplication, QMetaObject, Qt, Q_ARG
from PySide6.QtWidgets import QTextEdit, QApplication
from datetime import datetime
import time
import signal

# config loggin
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')
app = QApplication([])

class Handle_logging():
    def __init__(self):
        self.widget = QTextEdit()
    def info(self, text):
        QMetaObject.invokeMethod(self.widget, "append", Qt.QueuedConnection, Q_ARG(str, f'{datetime.now()} - INFO: {text}'))
    
    def warning(self, text):
        QMetaObject.invokeMethod(self.widget, "append", Qt.QueuedConnection, Q_ARG(str, f'{datetime.now()} - WARNING: {text}'))

    def error(self, text):
        QMetaObject.invokeMethod(self.widget, "append", Qt.QueuedConnection, Q_ARG(str, f'{datetime.now()} - ERROR: {text}'))
        
logging = Handle_logging()    

# short files in folder
def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

# path
PATH = os.path.dirname(os.path.abspath(__file__))
inputFolders = os.path.join(PATH, 'inputFolders')
outputAudio = os.path.join(PATH,'outputAudio')
imgFoders = os.path.join(PATH, 'imgFolders')
audioFolders = os.path.join(PATH, 'audioFolders')
outputMP4 = os.path.join(PATH, 'outputMP4')

os.makedirs(inputFolders, exist_ok=True)
os.makedirs(outputAudio, exist_ok=True)
os.makedirs(imgFoders, exist_ok=True)
os.makedirs(audioFolders, exist_ok=True)
os.makedirs(outputMP4, exist_ok=True)


# threadpool
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
#

# threadpool
class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.cancelled = False
        

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        if not self.cancelled:
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
    def cancel(self):
        self.cancelled = True

