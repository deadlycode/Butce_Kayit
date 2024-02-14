# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gelirListe.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(670, 416)
        Form.setStyleSheet("QPushButton {\n"
"    background-color: #f7f7f7;\n"
"    border: 1px solid #ddd;\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    color: #333;\n"
"    font-family: \"Helvetica Neue\", sans-serif;\n"
"    font-size: 10px;\n"
"    font-weight: 400;\n"
"    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);\n"
"    transition: 0.2s ease-in-out;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #fafafa;\n"
"    border-color: #bbb;\n"
"    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #f5f5f5;\n"
"    border-color: #aaa;\n"
"    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"QLineEdit {\n"
"    background-color: #f7f7f7;\n"
"    border: 1px solid #ddd;\n"
"    border-radius: 4px;\n"
"    padding: 4px;\n"
"    color: #333;\n"
"    font-family: \"Helvetica Neue\", sans-serif;\n"
"    font-size: 11px;\n"
"    font-weight: 400;\n"
"    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);\n"
"    transition: 0.2s ease-in-out;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    background-color: #fafafa;\n"
"    border-color: #bbb;\n"
"    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);\n"
"    font-size: 11px; /* Yazı boyutunu odaklanmış halde de belirleyin */\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"QTableWidget {\n"
"    background-color: #f7f7f7;\n"
"    border: 1px solid #ddd;\n"
"    border-radius: 4px;\n"
"    font-family: \"Helvetica Neue\", sans-serif;\n"
"    font-size: 11px;\n"
"    font-weight: 400;\n"
"    color: #333;\n"
"    gridline-color: #ddd;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 631, 321))
        self.tableWidget.setRowCount(31)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.bitTarih = QtWidgets.QDateEdit(Form)
        self.bitTarih.setGeometry(QtCore.QRect(150, 350, 121, 41))
        self.bitTarih.setDateTime(QtCore.QDateTime(QtCore.QDate(2024, 1, 1), QtCore.QTime(0, 0, 0)))
        self.bitTarih.setMinimumDate(QtCore.QDate(2022, 9, 14))
        self.bitTarih.setCalendarPopup(True)
        self.bitTarih.setDate(QtCore.QDate(2024, 1, 1))
        self.bitTarih.setObjectName("bitTarih")
        self.btnListele = QtWidgets.QPushButton(Form)
        self.btnListele.setGeometry(QtCore.QRect(290, 350, 131, 41))
        self.btnListele.setAutoFillBackground(False)
        self.btnListele.setStyleSheet("color:rgb(0, 170, 0)")
        self.btnListele.setObjectName("btnListele")
        self.basTarih = QtWidgets.QDateEdit(Form)
        self.basTarih.setGeometry(QtCore.QRect(10, 350, 121, 41))
        self.basTarih.setMinimumDate(QtCore.QDate(2022, 9, 14))
        self.basTarih.setCalendarPopup(True)
        self.basTarih.setDate(QtCore.QDate(2024, 1, 1))
        self.basTarih.setObjectName("basTarih")
        self.btnGelirSil = QtWidgets.QPushButton(Form)
        self.btnGelirSil.setGeometry(QtCore.QRect(480, 350, 101, 41))
        self.btnGelirSil.setAutoFillBackground(False)
        self.btnGelirSil.setStyleSheet("color:rgb(212, 12, 12)")
        self.btnGelirSil.setObjectName("btnGelirSil")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Gelir Listesi"))
        self.btnListele.setText(_translate("Form", "GELİRLERİ GETİR"))
        self.btnGelirSil.setText(_translate("Form", "KAYIT SİL"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())