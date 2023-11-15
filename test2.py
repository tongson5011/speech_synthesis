import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QMenu, QAction, QLineEdit, QFileSystemModel
from PyQt5.QtCore import QDir, Qt,QEvent, QObject, pyqtSignal


class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)

        self.tree_view = QTreeView(self)
        self.tree_view.setGeometry(10, 10, 780, 580)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.tree_view.setModel(self.file_model)

        self.tree_view.setRootIndex(self.file_model.index('/inputFolders'))

        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

        self.rename_edit = QLineEdit(self.tree_view)
        self.rename_edit.hide()
        self.rename_edit.returnPressed.connect(self.rename_item)

        self.event_filter = EventFilter(self.rename_edit, self.tree_view.viewport())
        self.event_filter.mouse_clicked.connect(self.hide_rename_edit)

    def show_context_menu(self, position):
        index = self.tree_view.indexAt(position)
        if index.isValid():
            menu = QMenu(self)

            rename_action = QAction("Rename", self)
            rename_action.triggered.connect(lambda: self.start_rename(index))
            menu.addAction(rename_action)

            remove_action = QAction("Remove", self)
            remove_action.triggered.connect(lambda: self.remove_item(index))
            menu.addAction(remove_action)

            menu.exec_(self.tree_view.viewport().mapToGlobal(position))

    def start_rename(self, index):
        rect = self.tree_view.visualRect(index)
        self.rename_edit.setFixedSize(rect.width(), rect.height())
        self.rename_edit.move(rect.topLeft())
        self.rename_edit.setText(self.file_model.fileName(index))
        self.rename_edit.show()
        self.rename_edit.setFocus()

    def rename_item(self):
        index = self.tree_view.currentIndex()
        new_name = self.rename_edit.text()
        if not new_name:
            return
        self.file_model.setData(index, new_name)
        self.rename_edit.hide()

    def remove_item(self, index):
        file_info = self.file_model.fileInfo(index)
        if file_info.isDir():
            self.file_model.rmdir(index)
        else:
            self.file_model.remove(index)

    def hide_rename_edit(self):
        self.rename_edit.hide()

class EventFilter(QObject):
    mouse_clicked = pyqtSignal()

    def __init__(self, widget, parent):
        super().__init__(parent)
        self.widget = widget

    def eventFilter(self, obj, event):
        print(event)
        if obj == self.widget and event.type() == QEvent.MouseButtonPress:
            if not self.widget.rect().contains(event.pos()):
                self.mouse_clicked.emit()
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec_())