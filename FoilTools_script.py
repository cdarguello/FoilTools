# Código escrito por Carlos Argüello
# Información de contacto en el README para feedback
# EN: Code written by Carlos Argüello, contact info in README for any feedback

import pandas as pd
import math
import os
import shutil


def aplicarModificaciones(arc_output, eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, i, anguloDiedro, flecha, anguloFlecha, inicio_flecha, cuerda):
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

    # Se calcula el offset automáticamente en caso de que fuera solicitado, respecto al ángulo del diedro y de flecha
    if diedro:
        if eje == 'Z':
            if abs(offsetX) >= abs(inicio_diedro):
                offsetY += abs(offsetX - inicio_diedro) / math.sin(math.pi/2-anguloDiedro) * math.sin(anguloDiedro)
                og = df[df.columns[0]]
                df[df.columns[0]] = df[df.columns[0]] * math.cos(anguloDiedro) - df[df.columns[1]] * math.sin(anguloDiedro)
                df[df.columns[1]] = og * math.sin(anguloDiedro) + df[df.columns[1]] *  math.cos(anguloDiedro)
        elif eje == 'X':
            if abs(offsetZ) >= abs(inicio_diedro):
                offsetY += abs(offsetZ - inicio_diedro) / math.sin(math.pi/2-anguloDiedro) * math.sin(anguloDiedro)       
                og = df[df.columns[1]]
                df[df.columns[1]] = df[df.columns[1]] * math.cos(anguloDiedro) - df[df.columns[2]] * math.sin(anguloDiedro)
                df[df.columns[2]] = og * math.sin(anguloDiedro) + df[df.columns[2]] *  math.cos(anguloDiedro)

    if flecha != 0:
        if eje == 'Z':
            if abs(offsetX) >= abs(inicio_flecha):
                offsetFlecha = (offsetX-inicio_flecha) * math.tan(anguloFlecha)
            else:
                offsetFlecha = 0
        elif eje == 'X':
            if abs(offsetZ) >= abs(inicio_flecha):
                offsetFlecha = (offsetZ-inicio_flecha) * math.tan(anguloFlecha)
            else:
                offsetFlecha = 0
        else:
            offsetFlecha = 0

        if flecha == 1:
            cuerda_flecha = cuerda - (2 * offsetFlecha)
        elif flecha == 2:
            cuerda_flecha = cuerda - (offsetFlecha)
        elif flecha == 3:
            # El offset en este caso no se debe sumar al final
            cuerda_flecha = cuerda - (offsetFlecha)
            offsetFlecha = 0
        else:
            # En el caso de flecha == 4 (cuerda constante) solo es necesario sumar el offset
            cuerda_flecha = cuerda
    else:
        offsetFlecha = 0
        cuerda_flecha = cuerda
    
    # Se modifica la cuerda y se resta el offset de flecha en caso de que fuera necesario
    if eje == 'Z':
        if abs(offsetX) >= abs(inicio_flecha):
            if cuerda_flecha < cuerda:
                df *= cuerda_flecha / cuerda
            df[df.columns[2]] -= offsetFlecha
    elif eje == 'X':
        if abs(offsetZ) >= abs(inicio_flecha):
            if cuerda_flecha < cuerda:
                df *= cuerda_flecha / cuerda
            df[df.columns[0]] -= offsetFlecha

    # Se añade el offset solicitado a cada coordenada
    df[df.columns[0]] += offsetX
    df[df.columns[1]] += offsetY
    df[df.columns[2]] += offsetZ

    # Obtener los path relevantes
    n = len(arc_output) -1
    for c in reversed(arc_output):
        if c == '/':
            break
        n -= 1
    
    if n != -1:
        path = arc_output[:n+1]
        file_name = arc_output[n+1:]
        dir_path = os.path.join(path, "output")
    else:
        file_name = arc_output
        dir_path = "output"

    # Creación en limpio de la carpeta de output
    if i == 0 or i == None:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            os.mkdir(dir_path)
        else:
            os.mkdir(dir_path)
    #Se actualiza el archivo de salida
    if i != None:
        if not isinstance(i, str):
            df.to_csv(dir_path+"/"+file_name[:-4]+"_"+str(i+1)+".txt",index=False, header=False)
        else:
            df.to_csv(dir_path+"/"+file_name[:-4]+"_"+i+".txt",index=False, header=False)
    else:
        df.to_csv(dir_path+"/"+file_name,index=False, header=False)

def main(archivo, arc_output, modo, cuerda, eje, plano, offsetX, offsetY, offsetZ, anguloX, anguloY, anguloZ, diedro, inicio_diedro, anguloDiedro, flecha, inicio_flecha, anguloFlecha, finAla, numCurvas):
    i = 0
    linea_mod = []
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
        aplicarModificaciones(arc_output, eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, None, anguloDiedro, flecha, anguloFlecha, inicio_flecha, cuerda)
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
                aplicarModificaciones(arc_output, eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, i, anguloDiedro, flecha, anguloFlecha, inicio_flecha, cuerda)
            if diedro:
                offsetX = inicio_diedro
                aplicarModificaciones(arc_output, eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, "diedro", anguloDiedro, flecha, anguloFlecha, inicio_flecha, cuerda)
            if flecha != 0:
                offsetX = inicio_flecha
                aplicarModificaciones(arc_output, eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, "flecha", anguloDiedro, flecha, anguloFlecha, inicio_flecha, cuerda)
        else:
            dist = (finAla - offsetZ) / (numCurvas-1)
            offsetZ_inicio = offsetZ
            for i in range(numCurvas):
                if i == numCurvas-1:
                    offsetZ = finAla
                else:
                    offsetZ = offsetZ_inicio + dist*i
                aplicarModificaciones(arc_output, eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, i, anguloDiedro, flecha, anguloFlecha, inicio_flecha, cuerda)
            if diedro:
                offsetZ = inicio_diedro
                aplicarModificaciones(arc_output, eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, "diedro", anguloDiedro, flecha, anguloFlecha, inicio_flecha, cuerda)
            if flecha != 0:
                offsetX = inicio_flecha
                aplicarModificaciones(arc_output, eje, plano, anguloX, anguloY, anguloZ, diedro, inicio_diedro, offsetX, offsetY, offsetZ, "flecha", anguloDiedro, flecha, anguloFlecha, inicio_flecha, cuerda)
    
    #Eliminación del archivo temporal
    try:
        os.remove(arc_output)
    except OSError as error:
        print(error)
        print("No se pudo eliminar el archivo temporal")


if __name__ == '__main__':
    # Inicialización de varibles con valores default
    modo = 0 #Modo 0 es modo simple, y modo 1 es el modo de curvas múltiples
    archivo = "perfil.dat"
    arc_output = "output_perfil.txt"
    cuerda = 250
    eje = 'Z'
    plano = "lateral"
    offsetX = 0
    offsetY = 0
    offsetZ = 0
    anguloX = 0
    anguloY = 0
    anguloZ = 0
    diedro = False
    inicio_diedro = 0
    finAla = 200
    numCurvas = 5
    anguloDiedro = 0
    flecha = 0
    anguloFlecha = 0
    inicio_flecha = 0

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

    diedroinput = input("Requiere calcular la coordenada Y automáticamente con diedro? (Y/n, default: n): ")
    if diedroinput != '':
        if diedroinput == 'Y' or diedroinput == 'y':
            diedro = True
            inicio_diedro_input = input("Coordenada del eje transversal donde inicia diedro (default: 0): ")
            if inicio_diedro_input != '':
                inicio_diedro = float(inicio_diedro_input)
            anguloDiedroinput = input("Ángulo del diedro: ")
            if anguloDiedroinput != '':
                anguloDiedro = math.radians(float(anguloDiedroinput))


    print("Agregue offsets si lo requiere, se usa el sistema coordenado de SolidWorks, ingrese los datos en las unidades del programa. ")
    offsetXinput = input("Offset en eje x: ")
    if offsetXinput != '':
        offsetX = float(offsetXinput)

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
        flechainput = input("Requiere generar un ala en flecha? (Y/n, default: n): ")
        if flechainput == 'Y':
            flechainput = input("Ingrese 1 si quiere ala trapezoidal, 2 borde salida constante, 3 borde entrada constante, 4 cuerda constante: ")
            if flechainput in ['1', '2','3','4']:
                flecha = int(flechainput)
                anguloFlechainput = input("Ingrese el ángulo (°) de la flecha (negativo si flecha invertida): ")
                if anguloFlechainput != '':
                    anguloFlecha = math.radians(float(anguloFlechainput))
                inicio_flecha_input = input("Coordenada del eje transversal donde inicia flecha (default: 0): ")
                if inicio_flecha_input != '':
                    inicio_flecha = float(inicio_flecha_input)
    main(archivo, arc_output, modo, cuerda, eje, plano, offsetX, offsetY, offsetZ, anguloX, anguloY, anguloZ, diedro, inicio_diedro, anguloDiedro, flecha, inicio_flecha, anguloFlecha, finAla, numCurvas)