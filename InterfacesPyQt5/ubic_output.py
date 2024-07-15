# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ubic_output.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import os
import sys
import math


output_path = ""
sys.path.append("..")

class Ui_ubic_output(object):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    def setupUi(self, ubic_output, nextUi, data, ui_diedro, ui_flecha,ui_curvas):
        ubic_output.setObjectName("ubic_output")
        ubic_output.resize(399, 281)
        self.centralwidget = QtWidgets.QWidget(ubic_output)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.b_generar = QtWidgets.QPushButton(self.centralwidget)
        self.b_generar.setGeometry(QtCore.QRect(310, 210, 75, 23))
        self.b_generar.setObjectName("b_generar")
        self.atras = QtWidgets.QPushButton(self.centralwidget)
        self.atras.setGeometry(QtCore.QRect(220, 210, 75, 23))
        self.atras.setObjectName("atras")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(5, 60, 391, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.output_path = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.output_path.setObjectName("output_path")
        self.horizontalLayout.addWidget(self.output_path)
        self.examinar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.examinar.setObjectName("examinar")
        self.horizontalLayout.addWidget(self.examinar)
        ubic_output.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ubic_output)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 399, 22))
        self.menubar.setObjectName("menubar")
        ubic_output.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ubic_output)
        self.statusbar.setObjectName("statusbar")
        ubic_output.setStatusBar(self.statusbar)

        self.retranslateUi(ubic_output)
        QtCore.QMetaObject.connectSlotsByName(ubic_output)

        #Adiciones manuales
        ubic_output.setWindowIcon(QtGui.QIcon('icon.png'))
        self.b_generar.clicked.connect(lambda: self.clicked_siguiente(ubic_output,nextUi, data, ui_diedro, ui_flecha, ui_curvas))
        self.examinar.clicked.connect(self.choose_output_path)
        self.atras.clicked.connect(lambda: self.clicked_atras(ubic_output,nextUi, data))

    # Método llamado cuando se presiona el botón examinar
    def choose_output_path(self):
        global output_path
        output_path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Escoja la carpeta donde se generará la carpeta de salida:', 'F:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        self.output_path.setText(output_path)

    # Método llamado cuando se presiona el botón siguiente
    def clicked_siguiente(self, ubic_output,nextUi, ui_main, ui_diedro, ui_flecha, ui_curvas):
        # Se validan los datos, en caso de que estén bien se abre la siguiente interfaz
        if os.path.exists(self.output_path.text()):
            import FoilTools_script
            # Se cierra la pestaña actual
            ubic_output.close()
            # Se recuperan los inputs obtenidos y se llama al script que genera las curvas
            modo = ui_main.m_curvas.isChecked() #Modo 0 es modo simple, y modo 1 es el modo de curvas múltiples
            archivo = ui_main.path.text()
            arc_output = self.output_path.text() + "/output_perfil.txt"
            cuerda = float(ui_main.cuerda.text())
            eje = ui_main.eje.currentText()
            plano = ui_main.plano.currentText()
            if plano == "Alzado (front)":
                plano = "alzado"
            elif plano == "Planta (top)":
                plano = "planta"
            else:
                plano = "lateral"
            offsetX = float(ui_main.offsetX.text())
            offsetY = float(ui_main.offsetY.text())
            offsetZ = float(ui_main.offsetZ.text())
            anguloX = math.radians(float(ui_main.anguloX.text()))
            anguloY = math.radians(float(ui_main.anguloY.text()))
            anguloZ = math.radians(float(ui_main.anguloZ.text()))
            diedro = ui_main.diedro.isChecked()
            if diedro:
                inicio_diedro = float(ui_diedro.inicio_diedro.text())
                anguloDiedro = math.radians(float(ui_diedro.anguloDiedro.text()))
            else:
                inicio_diedro = 0
                anguloDiedro = 0
            #1 si quiere ala trapezoidal, 2 borde salida constante, 3 borde entrada constante, 4 cuerda constante
            if ui_main.flecha.isChecked():
                anguloFlecha = math.radians(float(ui_flecha.anguloFlecha.text()))
                inicio_flecha = float(ui_flecha.inicio_flecha.text())
                tipoFlecha = ui_flecha.tipo_flecha.currentText()
                if tipoFlecha == "Ala trapezoidal":
                    flecha = 1
                elif tipoFlecha == "Borde salida constante":
                    flecha = 2
                elif tipoFlecha == "Borde entrada constante":
                    flecha = 3
                elif tipoFlecha == "Cuerda constante":
                    flecha = 4
                else:
                    print("Tipo de flecha desconocido")
            else:
                flecha = 0
                anguloFlecha = 0
                inicio_flecha = 0
            if modo:
                finAla = float(ui_curvas.fin_ala.text())
            else:
                finAla = 0
            numCurvas = int(ui_curvas.num_curvas.text())
            FoilTools_script.main(archivo, arc_output, modo, cuerda, eje, plano, offsetX, offsetY, offsetZ, anguloX, anguloY, anguloZ, diedro, inicio_diedro, anguloDiedro, flecha, inicio_flecha, anguloFlecha, finAla, numCurvas)
            # Mostrar mensaje de finalización
            msg = QMessageBox()
            msg.setWindowTitle("Aviso")
            msg.setText("Se generaron el(los) archivo(s) solicitado(s).")
            msg.setIcon(QMessageBox.Information)
            __ = msg.exec_()
            # Volver a la primera interfaz
            nextUi[0].show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("El directorio referenciado no existe")
            msg.setIcon(QMessageBox.Warning)
            __ = msg.exec_()

    # Método llamado cuando se presiona el botón atrás, se cierra la pestaña y se abre la de la interfaz principal
    def clicked_atras(self, ubic_output,nextUi, data):
        ubic_output.close()
        if data.m_curvas.isChecked():
            nextUi[3].show()
        elif data.diedro.isChecked():
            nextUi[1].show()
        else:
            nextUi[0].show()

    def retranslateUi(self, ubic_output):
        _translate = QtCore.QCoreApplication.translate
        ubic_output.setWindowTitle(_translate("ubic_output", "Foil Tools"))
        self.label.setText(_translate("ubic_output", "Ubicación de el(los) archivo(s) de salida"))
        self.b_generar.setText(_translate("ubic_output", "Generar"))
        self.atras.setText(_translate("ubic_output", "Atrás"))
        self.label_2.setText(_translate("ubic_output", "Ubicación:"))
        self.examinar.setText(_translate("ubic_output", "Examinar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ubic_output = QtWidgets.QMainWindow()
    ui = Ui_ubic_output()
    ui.setupUi(ubic_output, None, None, None, None, None)
    ubic_output.show()
    sys.exit(app.exec_())
