from buscar_secuencial import busqueda_por_id
def generar_matriz_estado(codigo_funcion, sector):
    """
    Función para generar la matriz de estado de los asientos de una función.
    """
    
    archivo_ubicaciones = open("ubicaciones_funcion.csv", "r", encoding="utf-8")
    if sector == "platea":
        matriz=[[0]*10 for i in range(35)]
        #dimensiones de la matriz para platea: 35 filas y 10 columnas porque son 350 butacas
    elif sector == "palco":
        matriz=[[0]*10 for i in range(25)]
        #dimensiones de la matriz para palco: 25 filas y 10 columnas porque son 250 butacas
    encabezado = archivo_ubicaciones.readline()
    linea = archivo_ubicaciones.readline().split(";")
    # Usamos while controlado por contador para pedir butacas y evitar el uso de 'break'
    while linea != [""]:
        if linea[5]== codigo_funcion and linea[3]== sector:
           butaca = int(linea[2])
           estado_butaca = linea[4]
           fila = (butaca - 1) // 10
           #Calcula la fila correspondiente a la butaca en la matriz. Se resta 1 a la butaca para que el índice comience desde 0 y se divide por 10 para obtener la fila.
           columna = (butaca - 1) % 10
           #Calcula la columna correspondiente a la butaca en la matriz. Se resta 1 a la butaca para que el índice comience desde 0 y se obtiene el residuo de la división por 10 para obtener la columna.
           matriz[fila][columna] = estado_butaca
        linea = archivo_ubicaciones.readline().split(";")
    archivo_ubicaciones.close()
    return matriz
        

def gestionar_venta_entradas():
    """
    Función para gestionar la venta de entradas.
    """
    print("--- REGISTRO DE VENTA DE ENTRADAS ---")
    codigo_funcion = input("Ingrese el código de la función para la venta de entradas: ")
    funcion_encontrada = busqueda_por_id(codigo_funcion, "funciones.csv")
    """Condicional para verificar si la función fue encontrada o no. Si no se encuentra, se muestra un mensaje de error y se termina la función. Si se encuentra, se solicita al usuario que ingrese el sector y la cantidad de entradas a vender."""
    if funcion_encontrada == "No existe este dato":
        print("No se encontró la función con el código proporcionado.")
        return
    else:
        print("Función encontrada:  ", funcion_encontrada)
        sector = input("ingrese el sector de la función: ")
        cant_entradas = int(input("Ingrese la cantidad de entradas:"))
        butacas_solicitadas = []
        asientos_ingresados = 0
        while asientos_ingresados < cant_entradas:
            asiento = input(f"Ingrese el asiento {asientos_ingresados + 1}: ")
            butacas_solicitadas.append(asiento)
            asientos_ingresados += 1
        