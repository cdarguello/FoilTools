# Código escrito por Carlos Argüello
# Información de contacto en el README para feedback
# EN: Code written by Carlos Argüello, contact info in README for any feedback

import pandas as pd
import math
import os
import shutil

# Variables globales
arc_output = "D:\Documentos\AeronauTEC\Convertidor perfil XFLR5 a SolidWorks\output_perfil.txt"

def aplicarModificaciones(eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, i, anguloDiedro):
    global arc_output
    columnas = ['x','y','z']
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
    if diedro and i == None:
        if eje == 'Z':
            if abs(offsetX) >= abs(inicio_diedro):
                offsetY = abs(offsetX - inicio_diedro) / math.sin(math.pi/2-anguloZ) * math.sin(anguloZ)
        elif eje == 'X':
            if abs(offsetZ) >= abs(inicio_diedro):
                offsetY = abs(offsetZ - inicio_diedro) / math.sin(math.pi/2-anguloX) * math.sin(anguloX)
    elif diedro and i != None:
        if eje == 'Z':
            if abs(offsetX) >= abs(inicio_diedro):
                offsetY = abs(offsetX - inicio_diedro) / math.sin(math.pi/2-anguloDiedro) * math.sin(anguloDiedro)
                og = df[df.columns[0]]
                df[df.columns[0]] = df[df.columns[0]] * math.cos(anguloDiedro) - df[df.columns[1]] * math.sin(anguloDiedro)
                df[df.columns[1]] = og * math.sin(anguloDiedro) + df[df.columns[1]] *  math.cos(anguloDiedro)
        elif eje == 'X':
            if abs(offsetZ) >= abs(inicio_diedro):
                offsetY = abs(offsetZ - inicio_diedro) / math.sin(math.pi/2-anguloDiedro) * math.sin(anguloDiedro)       
                og = df[df.columns[1]]
                df[df.columns[1]] = df[df.columns[1]] * math.cos(anguloDiedro) - df[df.columns[2]] * math.sin(anguloDiedro)
                df[df.columns[2]] = og * math.sin(anguloDiedro) + df[df.columns[2]] *  math.cos(anguloDiedro)
    # Se añade el offset solicitado a cada coordenada
    df[df.columns[0]] += offsetX
    df[df.columns[1]] += offsetY
    df[df.columns[2]] += offsetZ

    # Obtener los path relevantes
    n = len(arc_output) -1
    for c in reversed(arc_output):
        if c == '\\':
            break
        n -= 1
    path = arc_output[:n+1]
    file_name = arc_output[n+1:]
    dir_path = os.path.join(path, "output")

    # Creación en limpio de la carpeta de output
    if i == 0 or i == None:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            os.mkdir(dir_path)
    #Se actualiza el archivo de salida
    if i != None:
        if not isinstance(i, str):
            df.to_csv(dir_path+"\\"+file_name[:-4]+"_"+str(i+1)+".txt",index=False, header=False)
        else:
            df.to_csv(dir_path+"\\"+file_name[:-4]+"_"+i+".txt",index=False, header=False)
    else:
        df.to_csv(dir_path+"\\"+file_name,index=False, header=False)

def main():
    global arc_output
    # Inicialización de varibles con valores default
    modo = 0 #Modo 0 es modo simple, y modo 1 es el modo de curvas múltiples
    archivo = "D:\Documentos\AeronauTEC\Convertidor perfil XFLR5 a SolidWorks\perfil.dat"
    cuerda = 250
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
    finAla = 200
    numCurvas = 5
    anguloDiedro = 0

    # Se reciben los datos de entrada y son validados
    modoinput = input("Ingrese 1 si quiere usar el modo de curvas múltiples o 0 si quiere el modo simple (default): ")
    if modoinput != '':
        modo = int(modoinput)

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

    if modo == 1:
        finAlainput = input("Coordenada transversal donde termina el ala: ")
        if finAlainput != '':
            finAla = float(finAlainput)
        numCurvasinput = input("Numero de curvas por generar: ")
        if numCurvasinput != '':
            numCurvas = int(numCurvasinput)
        anguloDiedroinput = input("Ángulo del diedro: ")
        if anguloDiedroinput != '':
            anguloDiedro = math.radians(float(anguloDiedroinput))

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
    if modo == 0: #En el modo simple se llama normal a la función
        aplicarModificaciones(eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, None, anguloDiedro)
    else: # En el modo de curvas múltiples se llama iterativamente a la función de modificaciones para crear el número de curvas solicitado
        if eje == 'Z':
            # Se calcula la distancia transversal a la que debe estar cada curva
            dist = (finAla - offsetX) / (numCurvas-1)
            offsetX_inicio = offsetX
            # Se van creando perfiles con un offset transversal cada vez mayor, hasta llegar a un offset igual a donde termina el ala
            for i in range(numCurvas):
                if i == numCurvas-1:
                    offsetX = finAla
                else:
                    offsetX = offsetX_inicio + dist*i
                aplicarModificaciones(eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, i, anguloDiedro)
            if diedro:
                offsetX = inicio_diedro
                aplicarModificaciones(eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, "diedro", anguloDiedro)
        else:
            dist = (finAla - offsetZ) / (numCurvas-1)
            offsetZ_inicio = offsetZ
            for i in range(numCurvas):
                if i == numCurvas-1:
                    offsetZ = finAla
                else:
                    offsetZ = offsetZ_inicio + dist*i
                aplicarModificaciones(eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, i, anguloDiedro)
            if diedro:
                offsetZ = inicio_diedro
                aplicarModificaciones(eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, "diedro", anguloDiedro)
    
    #Eliminación del archivo temporal
    try:
        os.remove(arc_output)
    except OSError as error:
        print(error)
        print("No se pudo eliminar el archivo temporal")

    print("El archivo creado se llama ", arc_output,".")
    input("Presione Enter para terminar el programa")

if __name__ == '__main__':
    main()