# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
import requests
from pagerank2 import searchQuery
import content_based
from content_based import content_rec, df
from collab_filter import collab_filter
import json
import pandas as pd
from ast import literal_eval
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QListWidgetItem, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QImage
import urllib

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QStyledItemDelegate, QWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPen, QPainter


user_favs = []
initial = 1


class CustomItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Call the default paint method first
        super().paint(painter, option, index)

        # Draw a divider after each item
        if index.row() < index.model().rowCount() - 1:
            divider_pen = QPen(Qt.lightGray, 1, Qt.SolidLine)
            painter.setPen(divider_pen)
            painter.drawLine(option.rect.bottomLeft(),
                             option.rect.bottomRight())


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.selected_product = -1
        self.searchText = ''

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 681, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setPlaceholderText("Search Product")
        self.textEdit.textChanged.connect(self.searchTermUpdate)
        self.resultsScollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.resultsScollArea.setGeometry(QtCore.QRect(20, 100, 751, 471))
        self.resultsScollArea.setWidgetResizable(True)
        self.resultsScollArea.setObjectName("resultsScollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 749, 469))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.listWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listWidget.setGeometry(QtCore.QRect(-5, 1, 761, 471))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemDoubleClicked.connect(self.showProduct)

        self.listWidget.setWordWrap(True)
        delegate = CustomItemDelegate()
        self.listWidget.setItemDelegate(delegate)
        self.listWidget.setIconSize(QSize(100, 100))

        self.resultsScollArea.setWidget(self.scrollAreaWidgetContents)
        global initial
        global user_favs
        

        self.sortButton = QtWidgets.QPushButton(self.centralwidget)
        self.sortButton.setObjectName("sortButton")
        self.sortButton.setGeometry(QtCore.QRect(650, 60, 141, 31))
        self.sortButton.clicked.connect(self.sortPopularity)

        self.sortButtonLH = QtWidgets.QPushButton(self.centralwidget)
        self.sortButtonLH.setObjectName("sortButtonLH")
        self.sortButtonLH.clicked.connect(self.sortLH)
        
        self.sortButtonLH.setGeometry(QtCore.QRect(330, 60, 151, 31))
        self.sortButtonHL = QtWidgets.QPushButton(self.centralwidget)
        self.sortButtonHL.setObjectName("sortButtonHL")
        self.sortButtonHL.setGeometry(QtCore.QRect(490, 60, 151, 31))
        self.sortButtonHL.clicked.connect(self.sortHL)

        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(710, 20, 81, 31))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.submitSearch)

        
        if initial == 1 or len(user_favs) < 1:
            self.submitSearch()
        else:
            self.fetchCollab()
        initial = 0

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Product Recommender"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.sortButton.setText(_translate("MainWindow", "Sort by Popularity"))
        self.sortButtonLH.setText(_translate("MainWindow", "Sort by Price: Low to High"))
        self.sortButtonHL.setText(_translate("MainWindow", "Sort by Price: High to Low"))

    def fetchCollab(self):
        self.search_index_map = {}
        self.search_list=[]
        collab_results = collab_filter(user_favs)
        self.listWidget.clear()
        i = 0

        for column in collab_results.columns:
            if i > 50:
                break
            if column == 'productId':
                continue
            ind = int(column)
            self.search_list.append(ind)
            name = df['product_name'][ind] + '\n\n' + df['discounted_price'][ind] + '\n\n' + 'Average Rating : ' + str(df['rating'][ind])
            name = name.replace('\u20b9', 'Rs. ')
            
            icon = QIcon('placeholder.png')
            listWidgetItem = QListWidgetItem(icon, name)

            self.listWidget.addItem(listWidgetItem)
            
            self.search_index_map[i] = id
            i += 1
    def clearAllButton(self):
        self.sortButtonHL.setStyleSheet("")
        self.sortButtonLH.setStyleSheet("")
        self.sortButton.setStyleSheet("")
    def sortHL(self):
        self.clearAllButton()
        self.sortButtonHL.setStyleSheet("background-color: green;")
        self.listWidget.clear()
        
        rating_ind=[]

        for i in range(len(self.search_list)):
            ind = self.search_list[i]
           
            rating_ind.append((float(df['discounted_price'][ind].replace(',','').replace('\u20b9','')), ind))

        sorted_rating_ind = sorted(rating_ind, key=lambda x: x[0],reverse=True)

        self.search_index_map = {}
        self.search_list=[]
        i=0
        for ps, ind in sorted_rating_ind:
            self.search_list.append(ind)
            name = df['product_name'][ind] + '\n\n' + df['discounted_price'][ind] + '\n\n' + 'Average Rating : ' + str(df['rating'][ind])
            name = name.replace('\u20b9', 'Rs. ')
            
            icon = QIcon('placeholder.png')
            listWidgetItem = QListWidgetItem(icon, name)

            self.listWidget.addItem(listWidgetItem)
            self.search_index_map[i] = ind
            i += 1

    def sortLH(self):
        self.clearAllButton()
        self.sortButtonLH.setStyleSheet("background-color: green;")
        self.listWidget.clear()
        
        rating_ind=[]

        for i in range(len(self.search_list)):
            ind = self.search_list[i]
           
            rating_ind.append((float(df['discounted_price'][ind].replace(',','').replace('\u20b9','')), ind))

        sorted_rating_ind = sorted(rating_ind, key=lambda x: x[0])

        self.search_index_map = {}
        self.search_list=[]
        i=0
        for ps, ind in sorted_rating_ind:
            self.search_list.append(ind)
            name = df['product_name'][ind] + '\n\n' + df['discounted_price'][ind] + '\n\n' + 'Average Rating : ' + str(df['rating'][ind])
            name = name.replace('\u20b9', 'Rs. ')
            
            icon = QIcon('placeholder.png')
            listWidgetItem = QListWidgetItem(icon, name)

            self.listWidget.addItem(listWidgetItem)
            self.search_index_map[i] = ind
            i += 1


    def sortPopularity(self):
        self.clearAllButton()
        self.sortButton.setStyleSheet("background-color: green;")
        self.listWidget.clear()
        
        rating_ind=[]
        w_avg = 0.6
        w_cnt = 0.4
        list_ps = []
        for ind in self.search_list:
            rating = float(df['rating'][ind])
            rating_count = float(df['rating_count'][ind].replace(',',''))
            ps = w_avg*rating + w_cnt*rating_count
            list_ps.append(ps)
        print('lol')
        print(len(list_ps))
        print(list_ps)
        max_ps = max(list_ps)
        for i in range(len(list_ps)):
            ind = self.search_list[i]
            ps = list_ps[i]/max_ps
            rating_ind.append((ps, ind))

        sorted_rating_ind = sorted(rating_ind, key=lambda x: x[0], reverse=True)

        self.search_index_map = {}
        self.search_list=[]
        i=0
        for ps, ind in sorted_rating_ind:
            self.search_list.append(ind)
            name = df['product_name'][ind] + '\n\n' + df['discounted_price'][ind] + '\n\n' + 'Average Rating : ' + str(df['rating'][ind])
            name = name.replace('\u20b9', 'Rs. ')
            
            icon = QIcon('placeholder.png')
            listWidgetItem = QListWidgetItem(icon, name)

            self.listWidget.addItem(listWidgetItem)
            self.search_index_map[i] = ind
            i += 1

        



    def searchTermUpdate(self):
        self.searchText = self.textEdit.toPlainText()
        print(self.searchText)

    def submitSearch(self):
        self.clearAllButton()   
        self.search_index_map = {}
        self.search_list=[]
        self.listWidget.clear()
        self.searchResults = searchQuery(self.searchText) #rank, index
        print(self.searchResults)
        i = 0
        for id in self.searchResults:
            if i > 50:
                break
            id = int(id)
            ind=int(id)
            self.search_list.append(ind)
            #id = self.searchResults['index'][ind]
            name = df['product_name'][ind] + '\n\n' + df['discounted_price'][ind] + '\n\n' + 'Average Rating : ' + str(df['rating'][ind])
            name = name.replace('\u20b9', 'Rs. ')
            
            icon = QIcon('placeholder.png')

            listWidgetItem = QListWidgetItem(icon, name)

            self.listWidget.addItem(listWidgetItem)
            self.search_index_map[i] = id
            i += 1

    def showProduct(self):
        if self.listWidget.currentRow() >= 0:

            id = self.search_index_map[self.listWidget.currentRow()]

            self.selected_product = id
            content_results = content_rec(df['product_name'][id])
            collab_results = collab_filter([(df['product_name'][id], id, 5)])
            global user_favs
            #name, id, rating
            
            if (df['product_name'][id], id, 3) not in user_favs:
                user_favs.append((df['product_name'][id], id, 3))

            self.p_window = ProductWindow()
            self.p_window.setupUi(
                MainWindow, id, content_results, collab_results)

            print('lol')


class ProductWindow(QWidget):
    # def __init__(self, id):
    #     super().__init__()
    #     layout = QVBoxLayout()
    #     print(id)
    #     # layout.addWidget(self.label)
    #     self.setLayout(layout)

    def setupUi(self, MainWindow, id, content_results, collab_results):
        self.content_results = content_results
        self.collab_results = collab_results
        self.id = id
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(20, 20, 91, 31))
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(self.go_back)
        self.productImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.productImageLabel.setGeometry(QtCore.QRect(40, 70, 321, 211))
        self.productImageLabel.setText("")
        self.productImageLabel.setObjectName("productImageLabel")
        
        pixmap = QPixmap('placeholder.png')
        pixmap.scaled(64, 64)
        self.productImageLabel.setPixmap(pixmap)

        print('lol')
        print(df['product_name'][id])
        self.productLabel = QtWidgets.QTextBrowser(self.centralwidget)
        self.productLabel.setObjectName(u"productLabel")
        self.productLabel.setGeometry(QtCore.QRect(400, 70, 371, 210))
        self.productLabel.setMinimumSize(371, 210)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.productLabel.setFont(font)
        self.productLabel.setText(df['discounted_price'][id]+'\n\n'+'Average Rating : '+df['rating'][id]+'\n\n'+df['about_product'][id])


        self.productTitle = QtWidgets.QLabel(self.centralwidget)
        self.productTitle.setGeometry(QtCore.QRect(120, 20, 651, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.productTitle.setFont(font)
        self.productTitle.setObjectName("productTitle")
        self.productTitle.setText(df['product_name'][id])

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 370, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 370, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setObjectName("label_2")
        self.label_2.setText('Customers who bought this also bought')
        self.label_2.setFont(font)

        self.contentBasedList = QtWidgets.QListWidget(self.centralwidget)
        self.contentBasedList.setGeometry(QtCore.QRect(40, 400, 321, 171))
        # self.contentBasedList.setFlow(QtWidgets.QListView.TopToBottom)
        self.contentBasedList.setObjectName("contentBasedList")
        self.contentBasedList.setWordWrap(True)
        delegate = CustomItemDelegate()
        self.contentBasedList.setItemDelegate(delegate)
        self.contentBasedList.setIconSize(QSize(100, 100))
        self.contentBasedList.itemDoubleClicked.connect(self.showProductContent)

        self.collabBasedList = QtWidgets.QListWidget(self.centralwidget)
        self.collabBasedList.setGeometry(QtCore.QRect(430, 400, 321, 171))
        self.collabBasedList.itemDoubleClicked.connect(self.showProductCollab)

        # self.collabBasedList.setFlow(QtWidgets.QListView.TopToBottom)
        self.collabBasedList.setObjectName("collabBasedList")
        self.collabBasedList.setWordWrap(True)
        delegate = CustomItemDelegate()
        self.collabBasedList.setItemDelegate(delegate)
        self.collabBasedList.setIconSize(QSize(100, 100))
        self.populateContent(id)
        self.populateCollab(id)
        self.buyButton = QtWidgets  .QPushButton(self.centralwidget)
        self.buyButton.setObjectName(u"buyButton")
        self.buyButton.setGeometry(QtCore.QRect(510, 320, 141, 24))
        self.buyButton.clicked.connect(self.addToFav)
        self.buyButton.setText('Buy')
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.backButton.setText(_translate("MainWindow", "Go back"))
        #self.productLabel.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "Similiar Products"))
        self.label_2.setText(_translate(
            "MainWindow", "Users who bought this also bought"))

    def go_back(self):

        ui.setupUi(MainWindow)

    def addToFav(self):
        global user_favs
        id = self.id
        rating = 4
        name = df['product_name'][id]
        tupel = (name, id, rating)
        if tupel not in user_favs and (df['product_name'][id], id, 3) not in user_favs:
            user_favs.append(tupel)
        elif (df['product_name'][id], id, 3) in user_favs:
            loc = user_favs.index((df['product_name'][id], id, 3))
            user_favs[loc]=(df['product_name'][id], id, 4)
            
    def showProductContent(self):
        if self.contentBasedList.currentRow() >= 0:

            id = self.content_index_map[self.contentBasedList.currentRow()]

            self.selected_product = id
            content_results = content_rec(df['product_name'][id])
            collab_results = collab_filter([(df['product_name'][id], id, 5)])
            global user_favs
            #name, id, rating
            
            if (df['product_name'][id], id, 3) not in user_favs:
                user_favs.append((df['product_name'][id], id, 3))

            self.p_window = ProductWindow()
            self.p_window.setupUi(
                MainWindow, id, content_results, collab_results)

            print('lol')
    def showProductCollab(self):
        if self.collabBasedList.currentRow() >= 0:

            id = self.collab_index_map[self.collabBasedList.currentRow()]

            self.selected_product = id
            content_results = content_rec(df['product_name'][id])
            collab_results = collab_filter([(df['product_name'][id], id, 5)])
            global user_favs
            #name, id, rating
            
            if (df['product_name'][id], id, 3) not in user_favs:
                user_favs.append((df['product_name'][id], id, 3))

            self.p_window = ProductWindow()
            self.p_window.setupUi(
                MainWindow, id, content_results, collab_results)

            print('lol')
    def populateContent(self, id):
        # (name, index)
        self.content_index_map={}
        i=0
        for name, ind in self.content_results:
            if ind == id:
                continue
            icon = QIcon('placeholder.png')

            listWidgetItem = QListWidgetItem(icon, name)
            self.contentBasedList.addItem(listWidgetItem)
            self.content_index_map[i]=ind
            i+=1

    def populateCollab(self, id):
        self.collab_index_map={}
        i=0
        for column in self.collab_results.columns:
            if column == 'productId':
                continue
            ind = int(column)
            if ind == id:
                continue
            icon = QIcon('placeholder.png')
            name = df['product_name'][ind]
            listWidgetItem = QListWidgetItem(icon, name)
            self.collab_index_map[i]=ind
            self.collabBasedList.addItem(listWidgetItem)
            i+=1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
