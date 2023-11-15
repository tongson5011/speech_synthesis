# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_manager.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTreeView, QVBoxLayout, QWidget)

class Ui_File_manager_Form(object):
    def setupUi(self, File_manager_Form):
        if not File_manager_Form.objectName():
            File_manager_Form.setObjectName(u"File_manager_Form")
        File_manager_Form.resize(305, 300)
        self.verticalLayout = QVBoxLayout(File_manager_Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.list_item = QTreeView(File_manager_Form)
        self.list_item.setObjectName(u"list_item")
        self.list_item.setDragEnabled(True)
        self.list_item.setDragDropOverwriteMode(True)
        self.list_item.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_item.setDefaultDropAction(Qt.CopyAction)
        self.list_item.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.list_item)

        self.frame = QFrame(File_manager_Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 0, 8, 0)
        self.del_all = QPushButton(self.frame)
        self.del_all.setObjectName(u"del_all")
        self.del_all.setMaximumSize(QSize(45, 16777215))

        self.horizontalLayout.addWidget(self.del_all)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.browser = QPushButton(self.frame)
        self.browser.setObjectName(u"browser")

        self.horizontalLayout.addWidget(self.browser)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.list_item_count = QLabel(self.frame)
        self.list_item_count.setObjectName(u"list_item_count")
        self.list_item_count.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.list_item_count, 0, Qt.AlignLeft)


        self.verticalLayout.addWidget(self.frame, 0, Qt.AlignVCenter)


        self.retranslateUi(File_manager_Form)

        QMetaObject.connectSlotsByName(File_manager_Form)
    # setupUi

    def retranslateUi(self, File_manager_Form):
        File_manager_Form.setWindowTitle(QCoreApplication.translate("File_manager_Form", u"Form", None))
        self.del_all.setText(QCoreApplication.translate("File_manager_Form", u"Del All", None))
        self.browser.setText(QCoreApplication.translate("File_manager_Form", u"Browser", None))
        self.label.setText(QCoreApplication.translate("File_manager_Form", u"Count", None))
        self.list_item_count.setText(QCoreApplication.translate("File_manager_Form", u"0", None))
    # retranslateUi

