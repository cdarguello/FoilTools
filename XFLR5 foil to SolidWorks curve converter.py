# Código escrito por Carlos Argüello
# Información de contacto en el README para feedback
# EN: Code written by Carlos Argüello, contact info in README for any feedback

import pandas as pd
import math

# Inicialización de varibles con valores default
archivo = "D:\Documentos\AeronauTEC\Convertidor perfil XFLR5 a SolidWorks\perfil.dat"
arc_output = "D:\Documentos\AeronauTEC\Convertidor perfil XFLR5 a SolidWorks\output_perfil.txt"
cuerda = 250
columnas = ['x','y','z']
eje = 'Z'
plano = "lateral"
offsetX = 0
offsetY = 0
offsetZ = 0
anguloX = 0
anguloY = 0
anguloZ = 0
i = 0
linea_mod = []
diedro = False
inicio_diedro = 0

def aplicarModificaciones():
    global eje
    global plano
    global anguloX
    global anguloY
    global anguloZ
    global diedro
    global inicio_diedro
    global offsetX
    global offsetY
    global offsetZ
    # Se reordenan las coordenadas tal que la curva aparezca en el plano solicitado
    df = pd.read_csv(arc_output, names=columnas,sep=',')
    if eje == 'Z':
        if plano == "lateral":
            df = df[['z','y','x']]
        elif plano == "planta":
            df = df[['y','z','x']]
    else:
        if plano == "lateral":
            df = df[['z','y','x']]
        elif plano == "planta":
            df = df[['x','z','y']]
    df['x'] = df['x'] *-1 # Inversión requerida porque en XFLR5 el eje X está al revés que en Solid       

    # Se aplica la rotación del perfil
    og = df[df.columns[1]]
    df[df.columns[1]] = df[df.columns[1]] * math.cos(anguloX) - df[df.columns[2]] * math.sin(anguloX)
    df[df.columns[2]] = og * math.sin(anguloX) + df[df.columns[2]] *  math.cos(anguloX)
    og = df[df.columns[2]]
    df[df.columns[2]] = df[df.columns[2]] * math.cos(anguloY) - df[df.columns[0]] * math.sin(anguloY)
    df[df.columns[0]] = og * math.sin(anguloY) + df[df.columns[0]] *  math.cos(anguloY)
    og = df[df.columns[0]]
    df[df.columns[0]] = df[df.columns[0]] * math.cos(anguloZ) - df[df.columns[1]] * math.sin(anguloZ)
    df[df.columns[1]] = og * math.sin(anguloZ) + df[df.columns[1]] *  math.cos(anguloZ)

    # Se calcula el offset automáticamente en caso de que fuera solicitado, respecto al ángulo del diedro
    if diedro:
        if eje == 'Z':
            if abs(offsetX) >= abs(inicio_diedro):
                offsetY = abs(offsetX - inicio_diedro) / math.sin(math.pi/2-anguloZ) * math.sin(anguloZ)
        elif eje == 'X':
            if abs(offsetZ) >= abs(inicio_diedro):
                offsetY = abs(offsetZ - inicio_diedro) / math.sin(math.pi/2-anguloX) * math.sin(anguloX)
            
        
    # Se añade el offset solicitado a cada coordenada
    df[df.columns[0]] += offsetX
    df[df.columns[1]] += offsetY
    df[df.columns[2]] += offsetZ
    #Se actualiza el archivo de salida
    df.to_csv(arc_output,index=False, header=False)

# Se reciben los datos de entrada y son validados
arcinput = input("Nombre del archivo por convertir junto con su extension, debe estar en la misma carpeta que este script (default: perfil.dat): ")
if arcinput != '':
    archivo = arcinput

ejeinput = input("Eje sobre el que está el eje longitudinal del avión ('X', 'Z' [default]): ")
if ejeinput != '':
    if ejeinput in ['X', 'Z']:
        eje = ejeinput
planoinput = input("Plano sobre el que quiere que se imprima el perfil? Ingrese 'alzado' (front),'lateral' (right) o 'planta' (top) (default: lateral): ")
if planoinput != '':
    plano = planoinput

cuerdainput = input("Dimension de la cuerda, use las mismas unidades con las que esta trabajando en SolidWorks (default: 250): ")
if cuerdainput != '':
    cuerda = float(cuerdainput)

anguloXinput = input("Angulo de rotacion respecto a eje x (default: 0°): ")
if anguloXinput != '':
    anguloX = math.radians(float(anguloXinput))

anguloYinput = input("Angulo de rotacion respecto a eje y (default: 0°): ")
if anguloYinput != '':
    anguloY = math.radians(float(anguloYinput))

anguloZinput = input("Angulo de rotacion respecto a eje z (default: 0°): ")
if anguloZinput != '':
    anguloZ = math.radians(float(anguloZinput))

print()
diedroinput = input("Requiere calcular la coordenada Y automáticamente con diedro? (Y/n, default: n): ")
if diedroinput != '':
    if diedroinput == 'Y' or diedroinput == 'y':
        diedro = True
        inicio_diedro_input = input("Coordenada del eje transversal donde inicia diedro (default: 0): ")
        if inicio_diedro_input != '':
            inicio_diedro = float(inicio_diedro_input)


print("Agregue offsets si lo requiere, se usa el sistema coordenado de SolidWorks, ingrese los datos en las unidades del programa. ")
offsetXinput = input("Offset en eje x: ")
if offsetXinput != '':
    offsetX = float(offsetXinput)

if not diedro:
    offsetYinput = input("Offset en eje y: ")
    if offsetYinput != '':
        offsetY = float(offsetYinput)

offsetZinput = input("Offset en eje z: ")
if offsetZinput != '':
    offsetZ = float(offsetZinput)

# Preprocesamiento de los datos (transformación al formato requerido por SolidWorks)    
try:
    with open(archivo, "r+") as arc:
        for linea in arc:
            if i != 0:
                # Se cambian los espacios en blanco por comas, si el número es negativo hay un espacio en blanco de menos
                if linea[14] != '-':
                    linea = linea.replace('     ', ',')
                else:
                    linea = linea.replace('    ', ',')
                # Se elimina el espacio en blanco del inicio de cada línea
                if linea[0] == ' ':
                    linea = linea[1:]
                # Se rellena la coordenada faltante con ceros
                linea = linea[:-1] + ",0\n"
                # Se multiplica cada coordenada por el valor de la cuerda
                dato1Fin = linea.find(",")
                linea = linea.replace(linea[:dato1Fin], str(float(linea[:dato1Fin])*cuerda))
                dato1Fin = linea.find(",")
                dato2Fin = linea[dato1Fin+1:].find(",") + dato1Fin +1
                linea = linea.replace(linea[dato1Fin+1:dato2Fin], str(float(linea[dato1Fin+1:dato2Fin])*cuerda))
                linea_mod.append(linea)
            i +=1
except FileNotFoundError:
    raise FileNotFoundError("No se encontro el archivo " + arcinput + ", asegurese de que el nombre es correcto y esta en la misma carpeta que el script")

# Se escribe el archivo de salida con formato modificado   
with open(arc_output,'w') as mod:
    for linea in linea_mod:
        mod.write(linea)

# Se le aplican a los datos las modificaciones adicionales solicitadas
aplicarModificaciones()

print("El archivo creado se llama 'output_perfil.txt'.")
input("Presione Enter para terminar el programa")
