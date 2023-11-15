# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audio.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLineEdit,
    QPushButton, QSizePolicy, QToolButton, QVBoxLayout,
    QWidget)

class Ui_Audio_form(object):
    def setupUi(self, Audio_form):
        if not Audio_form.objectName():
            Audio_form.setObjectName(u"Audio_form")
        Audio_form.resize(226, 378)
        Audio_form.setStyleSheet(u"/*\n"
"border-color: rgb(0, 0, 0);\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"*/")
        self.verticalLayout = QVBoxLayout(Audio_form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(Audio_form)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Raised)
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.audio_start = QLineEdit(self.header_frame)
        self.audio_start.setObjectName(u"audio_start")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.audio_start.sizePolicy().hasHeightForWidth())
        self.audio_start.setSizePolicy(sizePolicy)
        self.audio_start.setMaximumSize(QSize(40, 16777215))

        self.header_layout.addWidget(self.audio_start)

        self.audio_count = QLineEdit(self.header_frame)
        self.audio_count.setObjectName(u"audio_count")
        self.audio_count.setMaximumSize(QSize(45, 16777215))

        self.header_layout.addWidget(self.audio_count)

        self.audio_combine = QLineEdit(self.header_frame)
        self.audio_combine.setObjectName(u"audio_combine")
        self.audio_combine.setMaximumSize(QSize(60, 16777215))

        self.header_layout.addWidget(self.audio_combine)

        self.audio_btn_start = QPushButton(self.header_frame)
        self.audio_btn_start.setObjectName(u"audio_btn_start")
        self.audio_btn_start.setMaximumSize(QSize(40, 16777215))

        self.header_layout.addWidget(self.audio_btn_start)

        self.audio_options = QToolButton(self.header_frame)
        self.audio_options.setObjectName(u"audio_options")

        self.header_layout.addWidget(self.audio_options)


        self.verticalLayout.addWidget(self.header_frame)

        self.content_frame = QFrame(Audio_form)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QFrame.Raised)
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setSpacing(0)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.content_frame)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Audio_form)

        QMetaObject.connectSlotsByName(Audio_form)
    # setupUi

    def retranslateUi(self, Audio_form):
        Audio_form.setWindowTitle(QCoreApplication.translate("Audio_form", u"Form", None))
        self.audio_start.setPlaceholderText(QCoreApplication.translate("Audio_form", u"Start", None))
        self.audio_count.setPlaceholderText(QCoreApplication.translate("Audio_form", u"count", None))
        self.audio_combine.setPlaceholderText(QCoreApplication.translate("Audio_form", u"Combine", None))
        self.audio_btn_start.setText(QCoreApplication.translate("Audio_form", u"Start", None))
        self.audio_options.setText(QCoreApplication.translate("Audio_form", u"...", None))
    # retranslateUi

