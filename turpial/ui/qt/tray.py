# -*- coding: utf-8 -*-

# Qt tray icon for Turpial

from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QCursor
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QSystemTrayIcon

from PyQt4.QtCore import QPoint
from PyQt4.QtCore import pyqtSignal

from turpial import DESC
from turpial.ui.lang import i18n

from libturpial.common import OS_MAC
from libturpial.common.tools import detect_os

class TrayIcon(QSystemTrayIcon):

    settings_clicked = pyqtSignal(QPoint)
    updates_clicked = pyqtSignal()
    messages_clicked = pyqtSignal()
    quit_clicked = pyqtSignal()
    toggled = pyqtSignal()

    def __init__(self, base):
        QSystemTrayIcon.__init__(self)

        self.base = base
        if detect_os() == OS_MAC:
            icon = QIcon(base.get_image_path('turpial-tray-mono-dark.png'))
        else:
            icon = QIcon(base.get_image_path('turpial-tray.png'))
        self.setIcon(icon)
        self.setToolTip(DESC)

        self.activated.connect(self.__activated)
        self.loading()
        self.show()

    def __build_header_menu(self):
        show = QAction(i18n.get('show_hide'), self)
        show.triggered.connect(self.__show_clicked)

        self.menu.addAction(show)
        self.menu.addSeparator()

    def __build_common_menu(self):
        settings = QAction(i18n.get('settings'), self)
        settings.triggered.connect(self.__settings_clicked)
        quit = QAction(i18n.get('quit'), self)
        quit.triggered.connect(self.__quit_clicked)

        self.menu.addAction(settings)
        self.menu.addSeparator()
        self.menu.addAction(quit)

    def __settings_clicked(self):
        self.settings_clicked.emit(QCursor.pos())

    def __updates_clicked(self):
        self.updates_clicked.emit()

    def __messages_clicked(self):
        self.messages_clicked.emit()

    def __quit_clicked(self):
        self.quit_clicked.emit()

    def __show_clicked(self):
        self.toggled.emit()

    def __activated(self, reason):
        if reason == QSystemTrayIcon.Context:
            self.menu.popup(QCursor.pos())

    def empty(self):
        self.menu = QMenu()
        self.__build_common_menu()
        self.setContextMenu(self.menu)

    def loading(self):
        self.menu = QMenu()
        loading = QAction(i18n.get('loading'), self)
        loading.setEnabled(False)
        self.menu.addAction(loading)
        self.setContextMenu(self.menu)

    def normal(self):
        self.menu = QMenu()

        self.__build_header_menu()

        updates = QAction(i18n.get('update_status'), self)
        updates.triggered.connect(self.__updates_clicked)
        messages = QAction(i18n.get('send_direct_message'), self)
        messages.triggered.connect(self.__messages_clicked)
        self.menu.addAction(updates)
        self.menu.addAction(messages)

        self.__build_common_menu()

        self.setContextMenu(self.menu)

    # Change the tray icon image to indicate updates
    def notify(self):
        self.set_from_pixbuf(self.base.load_image('turpial-tray-update.png', True))

    # Clear the tray icon image
    def clear(self):
        self.set_from_pixbuf(self.base.load_image('turpial-tray.png', True))
