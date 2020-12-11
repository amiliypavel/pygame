import pygame as pg
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic
import string
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow_design.ui', self)
        self.initUi()
    
    def initUi(self):
        self.btn_login.clicked.connect(self.login)
        self.btn_reg.clicked.connect(self.reg)
    
    def login(self):
        self.log = LogWindow()
        self.log.show()
        self.close()
    
    def reg(self):
        self.reg = RegWindow()
        self.reg.show()
        self.close()


class LogWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('LogWindow_design.ui', self)
        self.initUi()
    
    def initUi(self):
        self.btn_log.clicked.connect(self.log)
        self.btn_back.clicked.connect(self.back)
    
    def log(self):
        name = self.edit_name.text()
        password = self.edit_password.text()
        users = os.listdir('Users')
        if name and set(name) & set(string.ascii_letters):
            self.lbl_name.setStyleSheet('color: black;')
            self.lbl_name.setText('Ваш ник')
        if password and set(password) | set(string.whitespace) != set(string.whitespace):
            self.lbl_password.setStyleSheet('color: black;')
            self.lbl_password.setText('Пароль')
        if not name or not set(name) & set(string.ascii_letters):
            self.lbl_name.setStyleSheet('color: red;')
            self.lbl_name.setText('Ваш ник(обязательное поле!)')
        elif not password or set(password) | set(string.whitespace) == set(string.whitespace):
            self.lbl_password.setStyleSheet('color: red;')
            self.lbl_password.setText('Пароль(обязательное поле!)')
        elif f'{name}~{password}.txt' not in users:
            self.lbl_name.setStyleSheet('color: red;')
            self.lbl_name.setText('Ник или пароль введены неверно!')
        else:
            self.hide()
            pygame()
    
    def back(self):
        self.main = MainWindow()
        self.main.show()
        self.close()


class RegWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('RegWindow_design.ui', self)
        self.initUi()
    
    def initUi(self):
        self.btn_reg.clicked.connect(self.reg)
        self.btn_back.clicked.connect(self.back)
    
    def reg(self):
        global USER_FILE
        
        name = self.edit_name.text()
        password = self.edit_password.text()
        repeat_password = self.repeat_password.text()
        names = [i[:i.find('~')] for i in os.listdir('Users')]
        if name and set(name) & set(string.ascii_letters):
            self.lbl_name.setStyleSheet('color: black;')
            self.lbl_name.setText('Ваш ник')
        if password and set(password) | set(string.whitespace) != set(string.whitespace):
            self.lbl_password.setStyleSheet('color: black;')
            self.lbl_password.setText('Пароль')
        if repeat_password and password == repeat_password:
            self.lbl_rep_password.setStyleSheet('color: black;')
            self.lbl_rep_password.setText('Повторите пароль')
        if not name or not set(name) & set(string.ascii_letters):
            self.lbl_name.setStyleSheet('color: red;')
            self.lbl_name.setText('Ваш ник(обязательное поле!)')
        elif not password or set(password) | set(string.whitespace) == set(string.whitespace):
            self.lbl_password.setStyleSheet('color: red;')
            self.lbl_password.setText('Пароль(обязательное поле!)')
        elif password != repeat_password:
            self.lbl_rep_password.setStyleSheet('color: red;')
            self.lbl_rep_password.setText('Пароли не совпадают!')
        elif name in names:
            self.lbl_name.setStyleSheet('color: red;')
            self.lbl_name.setText('Пользователь с данным ником уже зарегистрирован!')
        else:
            USER_FILE = open(f'Users/{name}~{password}.txt', 'w')
            self.hide()
            pygame()
    
    def back(self):
        self.main = MainWindow()
        self.main.show()
        self.close()


def pygame():
    pg.init()
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    running = True
    map_screen = pg.image.load('map.png')
    map_rect = map_screen.get_rect()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill((0, 0, 0))
        screen.blit(map_screen, map_rect)
        pg.display.flip()
    pg.quit()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec())
