import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import listele
# from butce_gui import *
from listele import liste_tablosu
from anamenu import *
from listele import *
from anasayfa import anamenu_ui



app=QApplication([])
pencere=liste_tablosu()


anamenu=anamenu_ui()

anamenu.show()
app.exec_()



















# uygulama = QApplication(sys.argv)
# pencere = QMainWindow()
#
# ui = Ui_Form()
# ui.setupUi(pencere)
#
#
# uygulama2=QApplication(sys.argv)
# pencere2=QMainWindow()
#
# ui2=Ui_MainWindow()
# ui2.setupUi(pencere2)
#
#
# def listeler():
#     pencere2.show()
#
#
#
# ui.btnListele.clicked.connect(listeler)
#
#
#
# # Kodunun devamı buraya gelecek
#
# pencere.show()
# sys.exit(uygulama.exec_())

