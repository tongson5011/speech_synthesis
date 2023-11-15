# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'img.ui'
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

class Ui_Img_form(object):
    def setupUi(self, Img_form):
        if not Img_form.objectName():
            Img_form.setObjectName(u"Img_form")
        Img_form.resize(226, 378)
        Img_form.setStyleSheet(u"/*\n"
"border-color: rgb(0, 0, 0);\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"*/")
        self.verticalLayout = QVBoxLayout(Img_form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(Img_form)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Raised)
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.img_start = QLineEdit(self.header_frame)
        self.img_start.setObjectName(u"img_start")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_start.sizePolicy().hasHeightForWidth())
        self.img_start.setSizePolicy(sizePolicy)
        self.img_start.setMaximumSize(QSize(40, 16777215))

        self.header_layout.addWidget(self.img_start)

        self.img_count = QLineEdit(self.header_frame)
        self.img_count.setObjectName(u"img_count")
        self.img_count.setMaximumSize(QSize(45, 16777215))

        self.header_layout.addWidget(self.img_count)

        self.img_combine = QLineEdit(self.header_frame)
        self.img_combine.setObjectName(u"img_combine")
        self.img_combine.setMaximumSize(QSize(60, 16777215))

        self.header_layout.addWidget(self.img_combine)

        self.img_btn_start = QPushButton(self.header_frame)
        self.img_btn_start.setObjectName(u"img_btn_start")
        self.img_btn_start.setMaximumSize(QSize(40, 16777215))

        self.header_layout.addWidget(self.img_btn_start)

        self.img_options = QToolButton(self.header_frame)
        self.img_options.setObjectName(u"img_options")

        self.header_layout.addWidget(self.img_options)


        self.verticalLayout.addWidget(self.header_frame)

        self.content_frame = QFrame(Img_form)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QFrame.Raised)
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setSpacing(0)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.content_frame)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Img_form)

        QMetaObject.connectSlotsByName(Img_form)
    # setupUi

    def retranslateUi(self, Img_form):
        Img_form.setWindowTitle(QCoreApplication.translate("Img_form", u"Form", None))
        self.img_start.setPlaceholderText(QCoreApplication.translate("Img_form", u"Start", None))
        self.img_count.setPlaceholderText(QCoreApplication.translate("Img_form", u"count", None))
        self.img_combine.setPlaceholderText(QCoreApplication.translate("Img_form", u"Combine", None))
        self.img_btn_start.setText(QCoreApplication.translate("Img_form", u"Start", None))
        self.img_options.setText(QCoreApplication.translate("Img_form", u"...", None))
    # retranslateUi

