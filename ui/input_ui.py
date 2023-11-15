# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLineEdit, QPushButton, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Input_form(object):
    def setupUi(self, Input_form):
        if not Input_form.objectName():
            Input_form.setObjectName(u"Input_form")
        Input_form.resize(245, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Input_form.sizePolicy().hasHeightForWidth())
        Input_form.setSizePolicy(sizePolicy)
        Input_form.setStyleSheet(u"/*\n"
"border-color: rgb(0, 0, 0);\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"*/")
        self.verticalLayout = QVBoxLayout(Input_form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.heade_frame = QFrame(Input_form)
        self.heade_frame.setObjectName(u"heade_frame")
        self.heade_frame.setFrameShape(QFrame.StyledPanel)
        self.heade_frame.setFrameShadow(QFrame.Raised)
        self.heade_layout = QHBoxLayout(self.heade_frame)
        self.heade_layout.setSpacing(6)
        self.heade_layout.setObjectName(u"heade_layout")
        self.heade_layout.setContentsMargins(0, 0, 0, 0)
        self.input_form = QLineEdit(self.heade_frame)
        self.input_form.setObjectName(u"input_form")
        self.input_form.setMaximumSize(QSize(100, 16777215))

        self.heade_layout.addWidget(self.input_form)

        self.input_search = QPushButton(self.heade_frame)
        self.input_search.setObjectName(u"input_search")
        self.input_search.setMaximumSize(QSize(44, 16777215))

        self.heade_layout.addWidget(self.input_search)

        self.input_search_list = QComboBox(self.heade_frame)
        self.input_search_list.addItem("")
        self.input_search_list.addItem("")
        self.input_search_list.addItem("")
        self.input_search_list.setObjectName(u"input_search_list")
        self.input_search_list.setMaximumSize(QSize(60, 16777215))

        self.heade_layout.addWidget(self.input_search_list)

        self.input_settings = QToolButton(self.heade_frame)
        self.input_settings.setObjectName(u"input_settings")

        self.heade_layout.addWidget(self.input_settings)


        self.verticalLayout.addWidget(self.heade_frame, 0, Qt.AlignTop)

        self.content_frame = QFrame(Input_form)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QFrame.Raised)
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setSpacing(0)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.content_frame)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Input_form)

        QMetaObject.connectSlotsByName(Input_form)
    # setupUi

    def retranslateUi(self, Input_form):
        Input_form.setWindowTitle(QCoreApplication.translate("Input_form", u"Form", None))
        self.input_form.setPlaceholderText(QCoreApplication.translate("Input_form", u"Enter URL", None))
        self.input_search.setText(QCoreApplication.translate("Input_form", u"Search", None))
        self.input_search_list.setItemText(0, QCoreApplication.translate("Input_form", u"BNS", None))
        self.input_search_list.setItemText(1, QCoreApplication.translate("Input_form", u"STRUYEN", None))
        self.input_search_list.setItemText(2, QCoreApplication.translate("Input_form", u"TRUYEN YY", None))

        self.input_settings.setText(QCoreApplication.translate("Input_form", u"...", None))
    # retranslateUi

