# FoilTools
 Esta aplicación convierte un perfil exportado de XFLR5 a un archivo legible por SolidWorks, además de incluir funciones adicionales para facilitar la creación de cuerpos alares. Entre estas funciones se encuentran:
 1. Modo simple:
    - Adaptar perfil exportado de XFLR5 a un archivo estilo .csv con formato más adecuado (legible por SolidWorks)
    - Impresión del perfil en cualquiera de los 3 planos.
    - Rotación del perfil respecto a cualquier eje.
    - Cálculo automático de coordenada Y para diedros, calculado con el ángulo de rotación respectivo dado anteriormente y con cierto valor de coordenada en la que inicia el       diedro.
    - Suma de traslaciones en cualquiera de los 3 ejes.
    - Interfaz gráfica de usuario.
    - Instalador para Windows.

 2. Modo de curvas múltiples:
    - Todo lo anterior para definir una curva base.
    - Recibir un intervalo de coordenadas y crear dado número de curvas intermedias según las especificaciones (tomando en cuenta diedro y flecha).
    - Generación automática de alas en flecha del estilo: trapezoidales o elípticas, flechas normales e invertidas con coordenada de borde de salida/ataque (respectivamente)         fija (cuerda va disminuyendo), y alas en flecha normal e invertida con cuerda constante.
   
  Este programa fue hecho por Carlos Argüello, colíder del área de CAD del galardonado equipo de SAE Aerodesign "AeronauTEC", basado en el Instituto Tecnológico de Costa Rica (ITCR, Cartago, Costa Rica). 

  ENGLISH

  This program converts a foil exported from XFLR5 to a text file legible by SolidWorks, as well as including several additional functions for the creation of wings. Some of these functions are:
  1. Simple mode:
     - Adapt the format exported from XFLR5 to a .csv style file with a more adequate format.
     - Rotation of the foil with respect to any axis.
     - Automatic calculation of the Y coordinate for dihedral/anhedral wings, using the angle of rotation given and a given coordinate where the dihedral starts.
     - Adding an offset to any of the 3 axes.
     - Graphical User Interface.
     - Windows Installer.

  2. Multiple Curves mode:
     - Uses all of the previous functions to define a base curve.
     - Asks for a coordinate interval and a number of intermediate curves according to specifications (taking into account dihedral and swept-wings).
     - Automatic generation of swept-wing foils of the following types: trapezoidal or elliptical, [inverse] swept-wings with a certain fixed leading/trailing edge (chord 
       gets smaller), and [inverse] swept-wings with a fixed chord.
       
  This project was made by Carlos Argüello, co-leader of the CAD department of the award-winning SAE Aerodesign team "AeronauTEC", based in Costa Rican Institute of Technology (ITCR, Cartago, Costa Rica).
  **IMPORTANT NOTE: this project currently has no plans to have a full English translation, the user-guide and the GUI is completely in Spanish due to me not seeing the necessity in it; but if enough people reach out to me by preferably writing a comment on the repo or at cdavid.030715@gmail.com I will consider adding full English support.

  ## Guía de Instalación

  Existen dos posibilidades:
  1. Usando Python: se requiere tener instalado Python 3.X y Git, luego se debe clonar este repositorio y ejecutar en una consola en la carpeta principal donde se clonó el repositorio lo siguiente:

```
pip install -r requirements.txt
```

   Una vez hecho esto debería ser posible ejecutar el script con interfaz o sin interfaz para utilizar la aplicación.
   
  2. Instalador de Windows: si su sistema operativo es Windows puede descargar y seguir los pasos del archivo llamado "FoilTools-installer" y luego utilizar un acceso directo o el .exe para usar la aplicación con interfaz gráfica.

 ## Guía de Uso
### Obtención del perfil de XFLR5
 Al ejecutar la aplicación aparece una ventana con diferentes campos para datos, en el primer espacio se debe escoger cuál es el archivo de perfil de ala terminado en .dat generado por XFLR5 con el que se desea trabajar, este puede ser generado abriendo el proyecto de interés en XFLR5, yendo a Plane>>Current Plane>>Edit wing/elevator/fin para comprobar el nombre del perfil utilizado en cierta sección del avión, y luego en Module>>Direct Foil Design seleccionar el perfil de interés y darle click derecho y export, en la aplicación FoilTools se escoge luego la ubicación de este archivo generado.
### Opciones de la aplicación 
 En la misma pestaña se seleccionan ciertos datos o modificaciones que se le quieran hacer al perfil, además, si se selecciona la opción de Diedro se puede aplicar un ángulo de diedro a partir de cierta distancia del inicio del ala (si se está usando el modo de múltiples curvas) o sino será aplicado el ángulo tomando como referencia el offset en el eje respectivo que haya sido dado. La opción de Flecha solo funciona junto con la de múltiples curvas y permite dar al ala generada un ángulo de flecha de 4 tipos distintos: flecha trapezoidal, flecha con borde de entrada constante, flecha con borde de salida constante o flecha con cuerda constante. El modo de múltiples curvas genera de una sola vez varios perfiles que en conjunto formarían un ala.
 ### Ubicación de el(los) archivo(s) de salida
 Al final es solicitada una ubicación donde se generarán los archivos o archivo de salida, ahí se selecciona el lugar donde quiere que se genere la carpeta de output, es decir, si escoge el Escritorio como ubicación entonces aparecerá en el escritorio una carpeta llamada output donde están los archivos generados por la aplicación.
 CUIDADO: si vuelve a utilizar la aplicación y especifica la misma ubicación de salida entonces se borrarán los archivos generados anteriormente por la aplicación, si quiere mantenerlos hágales una copia previamente.
