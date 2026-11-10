import os
import modulos.buscar_secuencial as buscar
import modulos.ordenamiento as ordenar
import modulos.validar_funciones as validar

RUTA_FUNCIONES = "data/funciones.csv"
RUTA_PLANTILLA = "data/plantilla.csv"
CABECERA = "id;obra;hora_inicio;hora_fin;fecha;id_sala;precio;asientos_disponibles;estado\n"
# Si data/plantilla.csv tiene una primera fila de titulos, no cuenta como asiento
PLANTILLA_TIENE_CABECERA = True

# Si el archivo de funciones no existe o esta vacio, lo crea con su cabecera
def asegurar_archivo_funciones():
    os.makedirs("data", exist_ok=True)
    vacio = True
    if os.path.exists(RUTA_FUNCIONES):
        arch = open(RUTA_FUNCIONES, "r")
        if arch.readline() != "":
            vacio = False
        arch.close()
    if vacio:
        arch = open(RUTA_FUNCIONES, "w")
        arch.write(CABECERA)
        arch.close()

# Busca el ID mas alto del archivo (saltando la cabecera) y devuelve el siguiente
def calcular_nuevo_id():
    arch = open(RUTA_FUNCIONES, "r")
    arch.readline()  # saltamos la cabecera
    linea = arch.readline()
    mayor = 0
    while linea != "":
        datos = linea.strip().split(";")
        if datos[0].isdecimal() and int(datos[0]) > mayor:
            mayor = int(datos[0])
        linea = arch.readline()
    arch.close()
    return mayor + 1

# Copia la plantilla de ubicaciones a la carpeta de la funcion y devuelve la cantidad de asientos
def crear_ubicaciones(carpeta):
    plantilla = open(RUTA_PLANTILLA, "r")  # si no existe, lanza FileNotFoundError
    os.makedirs(carpeta, exist_ok=True)
    ruta_fun = open(f"{carpeta}/ubicaciones.csv", "w")
    asientos = 0
    linea = plantilla.readline()
    primera = True
    while linea != "":
        ruta_fun.write(linea if linea[len(linea)-1:len(linea)] == "\n" else linea + "\n")
        if linea.strip() != "" and not (primera and PLANTILLA_TIENE_CABECERA):
            asientos += 1
        primera = False
        linea = plantilla.readline()
    plantilla.close()
    ruta_fun.close()
    return asientos

#def para cargar funciones
# Devuelve el ID de la nueva funcion, o None si no se pudo crear
def cargar_fun(obra, hora_inicio, hora_fin, fecha, id_sala, precio):
    asegurar_archivo_funciones()
    id = str(calcular_nuevo_id())
    # primero creamos las ubicaciones: si falla la plantilla, no se guarda la funcion a medias
    try:
        asientos = crear_ubicaciones(f"funcion {id}")
    except FileNotFoundError:
        print("No se encontro data/plantilla.csv. No se pudo crear la funcion.")
        return None
    registro_resultante = ";".join([id, obra, hora_inicio, hora_fin, fecha, id_sala, precio, "Programado\n"])
    arch = open(RUTA_FUNCIONES, "a")
    arch.write(registro_resultante)
    arch.close()
    return id

# Muestra una funcion (vector de 9 columnas) en una linea
def mostrar_funcion(datos):
    print(f"ID: {datos[0]} | Obra: {datos[1]} | Hora de inicio: {datos[2]} | Hora de fin: {datos[3]} | Fecha: {datos[4]} | ID sala: {datos[5]} | Precio: {datos[6]}  | Estado: {datos[7]}")

#def para consultar funciones (solo muestra las "Programado")
def consultar_funciones():
    try:
        arch = open(RUTA_FUNCIONES, "r")
        arch.readline()  # saltamos la cabecera
        linea = arch.readline()
        cantidad = 0
        while linea != "":
            datos = linea.split(";")
            # solo mostramos funciones completas y no expiradas
            if len(datos) >= 8 and datos[7] != "Expirado":
                mostrar_funcion(datos)
                cantidad += 1
            linea = arch.readline()
        arch.close()
        if cantidad == 0:
            print("No hay funciones disponibles")
    except FileNotFoundError:
        print("El archivo de funciones no existe. Por favor, cree una funcion primero.")
        return

# Submenu de busqueda
def buscar_funciones():
    print("Seleccione: \n 1- Buscar por ID\n 2- Buscar por nombre de obra\n 0- Volver")
    eleccion2 = validar.leer_opcion("Opcion: ", 0, 2)
    if eleccion2 == 1:
        id_buscar = input("Ingrese el ID de la funcion: ").strip()
        # llamamos a la funcion de busqueda secuencial
        resultado = buscar.busqueda_por_id(id_buscar, RUTA_FUNCIONES)
        # mostramos la funcion solo si existe, esta completa y no esta expirada
        if resultado != "No existe este dato" and len(resultado) >= 8 and resultado[7] != "Expirado":
            mostrar_funcion(resultado)
        else:
            print("No existe ninguna funcion programada con ese ID")
    elif eleccion2 == 2:
        texto = input("Ingrese el nombre (o parte del nombre) de la obra: ").strip()
        if texto == "":
            print("Debe ingresar un texto para buscar.")
            return
        # llamamos a la funcion de busqueda secuencial por coincidencia parcial
        resultados = buscar.busqueda_por_nombre(texto, RUTA_FUNCIONES)
        cantidad = 0
        i = 0
        while i < len(resultados):
            if len(resultados[i]) >= 8 and resultados[i][7] != "Expirado":
                mostrar_funcion(resultados[i])
                cantidad += 1
            i += 1
        if cantidad == 0:
            print("No se encontraron funciones con ese nombre")

# Submenu de ordenamiento
def ordenar_funciones():
    print("Seleccione: \n 1- Ordenar por ID\n 2- Ordenar por nombre de obra\n 0- Volver")
    eleccion3 = validar.leer_opcion("Opcion: ", 0, 2)
    if eleccion3 == 0:
        return
    print("Elija el orden:\n 1- Ascendente\n 2- Descendente")
    ascendente = validar.leer_opcion("Opcion: ", 1, 2) == 1
    if eleccion3 == 1:
        # llamamos a la funcion de ordenamiento por ID
        ordenadas = ordenar.ordenar_funciones_por_id(ascendente)
    else:
        # llamamos a la funcion de ordenamiento por nombre de obra
        ordenadas = ordenar.ordenar_funciones_por_nombre(ascendente)
    if len(ordenadas) == 0:
        print("No hay funciones registradas para ordenar.")
    else:
        print("\n=================== FUNCIONES ORDENADAS ===================")
        i = 0
        while i < len(ordenadas):
            mostrar_funcion(ordenadas[i])
            i += 1

# Alta de una funcion pidiendo los datos y validandolos
def agregar_funcion():
    print("Agregar funcion: ")
    print("Ingrese los datos de la funcion: ")
    nombre = input("Ingrese el nombre de la obra: ").strip()
    fecha = input("Ingrese la fecha de la funcion (dd/mm/aaaa): ").strip()
    hora_inicio = input("Ingrese la hora de inicio de la funcion (hh:mm): ").strip()
    hora_fin = input("Ingrese la hora de fin de la funcion (hh:mm): ").strip()
    id_sala = input("Ingrese el ID de la sala: ").strip()
    precio = input("Ingrese el precio de la entrada: ").strip().replace(",", ".")
    if validar.validar_nombre(nombre) and validar.validar_precio(precio) and validar.es_funcion_valida(id_sala, fecha, hora_inicio, hora_fin):
        nuevo_id = cargar_fun(nombre, hora_inicio, hora_fin, fecha, id_sala, precio)
        if nuevo_id is not None:
            print(f"Funcion agregada correctamente (ID {nuevo_id})")
    else:
        print("La funcion no fue agregada.")

def menu_funciones():
    print("Hola, bienvenido a la gestion de funciones ")
    eleccion = -1
    #ciclo de eleccion de opciones
    while eleccion != 0:
        # en cada interaccion actualizamos las funciones cuyo horario ya paso
        validar.deshabilitar_funciones_pasadas()
        print("Seleccione que desea hacer: \n 1- Consultar funciones\n 2- Agregar funciones\n 3- Buscar\n 4- Ordenar funciones\n 0 - Volver al menu principal")
        eleccion = validar.leer_opcion("Opcion: ", 0, 4)
        #consultamos que requiere hacer el usuario y llamamos a la funcion correspondiente
        if eleccion == 1:
            print("Listado de funciones: ")
            consultar_funciones()
        elif eleccion == 2:
            agregar_funcion()
        elif eleccion == 3:
            buscar_funciones()
        elif eleccion == 4:
            ordenar_funciones()
