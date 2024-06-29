from PyQt5 import QtCore, QtGui, QtWidgets
from InterfacesPyQt5.interfaz import *
from InterfacesPyQt5.diedro import *
from InterfacesPyQt5.flecha import *
from InterfacesPyQt5.m_curvas import *
from InterfacesPyQt5.ubic_output import *



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    # Configuración de la interfaz de ubicación del output
    ubic_output = QtWidgets.QMainWindow()
    ui_ubic_output = Ui_ubic_output()
    
    # Configuración de la interfaz de curvas múltiples
    m_curvas = QtWidgets.QMainWindow()
    ui_curvas = Ui_m_curvas()
    
    # Configuración de la interfaz de flecha
    flecha_ui = QtWidgets.QMainWindow()
    ui_flecha = Ui_flecha_ui()
    
    # Configuración de la interfaz de diedro
    diedro_ui = QtWidgets.QMainWindow()
    ui_diedro = Ui_diedro_ui()
    
    # Configuración de la interfaz principal
    MainWindow = QtWidgets.QMainWindow()
    ui_main = Ui_MainWindow()

    # Inicializar todas las interfaces y sus relaciones
    ui_main.setupUi(MainWindow, [diedro_ui, flecha_ui, m_curvas, ubic_output])
    ui_diedro.setupUi(diedro_ui, [MainWindow, flecha_ui, m_curvas, ubic_output], ui_main)
    ui_flecha.setupUi(flecha_ui, [MainWindow, diedro_ui, m_curvas, ubic_output], ui_main) #como si hay flecha hay m_curvas entonces solo puede avanzar a m_curvas viniendo de flecha
    ui_curvas.setupUi(m_curvas,[MainWindow, diedro_ui, flecha_ui, ubic_output], ui_main)
    ui_ubic_output.setupUi(ubic_output, [MainWindow, diedro_ui, flecha_ui, m_curvas], ui_main, ui_diedro, ui_flecha, ui_curvas)

    MainWindow.show()
    sys.exit(app.exec_())
