# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diedro.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import os
from InterfacesPyQt5.interfaz import isNumerical


class Ui_diedro_ui(object):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    def setupUi(self, diedro_ui, nextUi, data):
        diedro_ui.setObjectName("diedro_ui")
        diedro_ui.resize(399, 281)
        self.centralwidget = QtWidgets.QWidget(diedro_ui)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 30, 381, 71))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_15 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.inicio_diedro = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.inicio_diedro.setText("")
        self.inicio_diedro.setObjectName("inicio_diedro")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inicio_diedro)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.anguloDiedro = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.anguloDiedro.setObjectName("anguloDiedro")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.anguloDiedro)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.siguiente = QtWidgets.QPushButton(self.centralwidget)
        self.siguiente.setGeometry(QtCore.QRect(310, 210, 75, 23))
        self.siguiente.setObjectName("siguiente")
        self.atras = QtWidgets.QPushButton(self.centralwidget)
        self.atras.setGeometry(QtCore.QRect(220, 210, 75, 23))
        self.atras.setObjectName("atras")
        diedro_ui.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(diedro_ui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 399, 22))
        self.menubar.setObjectName("menubar")
        diedro_ui.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(diedro_ui)
        self.statusbar.setObjectName("statusbar")
        diedro_ui.setStatusBar(self.statusbar)

        self.retranslateUi(diedro_ui)
        QtCore.QMetaObject.connectSlotsByName(diedro_ui)

        #Adiciones manuales
        diedro_ui.setWindowIcon(QtGui.QIcon('icon.png'))
        self.siguiente.clicked.connect(lambda: self.clicked_siguiente(diedro_ui,nextUi, data))
        self.atras.clicked.connect(lambda: self.clicked_atras(diedro_ui,nextUi))

    # Método llamado cuando se presiona el botón siguiente
    def clicked_siguiente(self, diedro_ui,nextUi, data):
        # Se validan los datos, en caso de que estén bien se abre la siguiente interfaz
        if isNumerical(self.inicio_diedro.text()) and isNumerical(self.anguloDiedro.text()):
            diedro_ui.close()
            if data.flecha.isChecked() and data.m_curvas.isChecked():
                nextUi[1].show()
            elif data.m_curvas.isChecked():
                nextUi[2].show()
            else:
                nextUi[3].show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Rellene todos los campos solicitados con valores numéricos")
            msg.setIcon(QMessageBox.Warning)
            __ = msg.exec_()
    
    # Método llamado cuando se presiona el botón atrás, se cierra la pestaña y se abre la de la interfaz principal
    def clicked_atras(self, diedro_ui,nextUi):
        diedro_ui.close()
        nextUi[0].show()

    def retranslateUi(self, diedro_ui):
        _translate = QtCore.QCoreApplication.translate
        diedro_ui.setWindowTitle(_translate("diedro_ui", "Foil Tools"))
        self.label_15.setText(_translate("diedro_ui", "Coordenada del eje transversal donde inicia diedro: "))
        self.label_2.setText(_translate("diedro_ui", "Ángulo del diedro (°):"))
        self.label.setText(_translate("diedro_ui", "Opciones del diedro"))
        self.siguiente.setText(_translate("diedro_ui", "Siguiente"))
        self.atras.setText(_translate("diedro_ui", "Atrás"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    diedro_ui = QtWidgets.QMainWindow()
    ui = Ui_diedro_ui()
    ui.setupUi(diedro_ui)
    diedro_ui.show()
    sys.exit(app.exec_())
