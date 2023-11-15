# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'output.ui'
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
    QPushButton, QSizePolicy, QToolButton, QVBoxLayout,
    QWidget)

class Ui_Output_form(object):
    def setupUi(self, Output_form):
        if not Output_form.objectName():
            Output_form.setObjectName(u"Output_form")
        Output_form.resize(387, 300)
        Output_form.setStyleSheet(u"/*\n"
"border-color: rgb(0, 0, 0);\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"*/")
        self.verticalLayout = QVBoxLayout(Output_form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.heade_frame = QFrame(Output_form)
        self.heade_frame.setObjectName(u"heade_frame")
        self.heade_frame.setFrameShape(QFrame.StyledPanel)
        self.heade_frame.setFrameShadow(QFrame.Raised)
        self.heade_layout = QHBoxLayout(self.heade_frame)
        self.heade_layout.setSpacing(6)
        self.heade_layout.setObjectName(u"heade_layout")
        self.heade_layout.setContentsMargins(0, 0, 0, 0)
        self.output_run_list = QComboBox(self.heade_frame)
        self.output_run_list.addItem("")
        self.output_run_list.addItem("")
        self.output_run_list.setObjectName(u"output_run_list")

        self.heade_layout.addWidget(self.output_run_list)

        self.output_run = QPushButton(self.heade_frame)
        self.output_run.setObjectName(u"output_run")

        self.heade_layout.addWidget(self.output_run)

        self.output_settings = QToolButton(self.heade_frame)
        self.output_settings.setObjectName(u"output_settings")

        self.heade_layout.addWidget(self.output_settings)


        self.verticalLayout.addWidget(self.heade_frame)

        self.content_frame = QFrame(Output_form)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QFrame.Raised)
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setSpacing(0)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.content_frame)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 15)

        self.retranslateUi(Output_form)

        QMetaObject.connectSlotsByName(Output_form)
    # setupUi

    def retranslateUi(self, Output_form):
        Output_form.setWindowTitle(QCoreApplication.translate("Output_form", u"Form", None))
        self.output_run_list.setItemText(0, QCoreApplication.translate("Output_form", u"GCP Text to Speech", None))
        self.output_run_list.setItemText(1, QCoreApplication.translate("Output_form", u"AZ Text to Speech", None))

        self.output_run.setText(QCoreApplication.translate("Output_form", u"Run", None))
        self.output_settings.setText(QCoreApplication.translate("Output_form", u"...", None))
    # retranslateUi

