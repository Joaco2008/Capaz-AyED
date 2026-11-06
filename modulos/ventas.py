from buscar_secuencial import busqueda_por_id

def generar_matriz_estado(codigo_funcion, sector):
    """
    Función para generar la matriz de estado de los asientos de una función.
    Requisito obligatorio de la cátedra: Implementar recorrido y consulta sobre matriz.
    """
    archivo_ubicaciones = open("ubicaciones_funcion.csv", "r", encoding="utf-8")
    
    # Dimensiones fijas según reglas de negocio SPN: 350 ubicaciones (platea) y 250 (palco).
    if sector == "platea":
        matriz=[[0]*10 for i in range(35)]
    elif sector == "palco":
        matriz=[[0]*10 for i in range(25)]
        
    archivo_ubicaciones.readline()
    linea = archivo_ubicaciones.readline().split(";")
    
    # Lectura secuencial de archivo para cargar estado actual de la sala
    while linea != [""]:
        if linea[5]== codigo_funcion and linea[3]== sector:
           butaca = int(linea[2])
           estado_butaca = linea[4]
           
           # Conversión matemática de butaca lineal a coordenadas matriciales
           fila = (butaca - 1) // 10
           columna = (butaca - 1) % 10
           matriz[fila][columna] = estado_butaca
           
        linea = archivo_ubicaciones.readline().split(";")
    archivo_ubicaciones.close()
    return matriz

def validar_disponibilidad(matriz_estado, butacas_solicitadas):
    """
    RF3 Regla 3: Comprobar que todas las ubicaciones solicitadas estén disponibles.
    Se consulta directamente la matriz mediante índices.
    """
    indice = 0
    estan_disponibles = True
    
    # Ciclo while con variable bandera para frenar al encontrar un error sin usar 'break'
    while indice < len(butacas_solicitadas) and estan_disponibles:
        butaca = int(butacas_solicitadas[indice])
        fila = (butaca - 1) // 10
        columna = (butaca - 1) % 10
        
        if matriz_estado[fila][columna] == "ocupado":
            estan_disponibles = False
        indice += 1
        
    return estan_disponibles

def calcular_importe(cant_entradas, precio_base, sector, es_socio):
    """
    RF3 Reglas 5 y 6: Calcular el importe de la operación y aplicar descuento del 30% a socios.
    """
    if sector == "platea":
        precio_unitario = precio_base
    elif sector == "palco":
        precio_unitario = precio_base * 1.3
        
    subtotal = cant_entradas * precio_unitario
    
    if es_socio:
        descuento = subtotal * 0.30 
    else:
        descuento = 0
        
    total = subtotal - descuento
    return total, descuento

def gestionar_venta_entradas():
    """
    Orquestador principal del proceso de ventas. 
    Delega responsabilidades para mantener la modularización exigida.
    """
    print("--- REGISTRO DE VENTA DE ENTRADAS ---")
    codigo_funcion = input("Ingrese el código de la función para la venta de entradas: ")
    
    # RF3 Regla 1: Verificar que la función exista (mediante búsqueda manual secuencial)
    funcion_encontrada = busqueda_por_id(codigo_funcion, "funciones.csv")
    
    if funcion_encontrada == "No existe este dato":
        print("No se encontró la función con el código proporcionado.")
        return
    else:
        print("Función encontrada:  ", funcion_encontrada)
        sector = input("ingrese el sector de la función: ")
        cant_entradas = int(input("Ingrese la cantidad de entradas:"))
        butacas_solicitadas = []
        asientos_ingresados = 0
        
        # Carga de datos evitando ciclo for/break
        while asientos_ingresados < cant_entradas:
            asiento = input(f"Ingrese el asiento {asientos_ingresados + 1}: ")
            butacas_solicitadas.append(asiento)
            asientos_ingresados += 1
            
        matriz_sala = generar_matriz_estado(codigo_funcion, sector)
        validacion_ok = validar_disponibilidad(matriz_sala, butacas_solicitadas)
        
        if validacion_ok == True:
            precio_base = float(funcion_encontrada[7])
            socio_input = input("¿Es socio? (s/n): ")
            es_socio = socio_input == "s"
            total, descuento = calcular_importe(cant_entradas, precio_base, sector, es_socio)
            
            print(f"\n--- TICKET DE VENTA ---")
            print(f"Obra: {funcion_encontrada[1]}")
            print(f"Sector: {sector} | Entradas: {cant_entradas}")
            print(f"Descuento socio: ${descuento}")
            print(f"TOTAL A PAGAR: ${total}")
            print("-----------------------")
            confirmacion = input("¿Desea confirmar y registrar la venta? (s/n): ")
            
            if confirmacion.lower() == 's':
                actualizar_estado_archivo(codigo_funcion, sector, butacas_solicitadas)
                registrar_venta_archivo(numero_venta=1, codigo_funcion=codigo_funcion, sector=sector, butacas_solicitadas=butacas_solicitadas, cant_entradas=cant_entradas, descuento=descuento, total=total)
                print("Venta registrada exitosamente.")
            else:
                print("Venta cancelada por el usuario.")
        else:
            print("No se puede realizar la venta, las butacas solicitadas no están disponibles.")

def actualizar_estado_archivo(codigo_funcion, sector, butacas_solicitadas):
    """
    RF3 Regla 7: Actualizar la disponibilidad solamente cuando la venta haya sido validada.
    """
    # Se guarda el archivo en memoria para modificar la línea exacta y reescribirlo
    with open("ubicaciones_funcion.csv", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        for i in range(len(lineas)):
            linea = lineas[i].strip().split(";")
            
            # Verificación de que existen elementos en la lista para evitar IndexError con líneas vacías
            if len(linea) > 5 and codigo_funcion == linea[5] and sector == linea[3]:
                butaca = str(linea[2])
                if butaca in butacas_solicitadas:
                    linea[4] = "ocupado"
                    lineas[i] = ";".join(linea) + "\n"
                    
    with open("ubicaciones_funcion.csv", "w", encoding="utf-8") as archivo:
        archivo.writelines(lineas)

def registrar_venta_archivo(numero_venta, codigo_funcion, sector, butacas_solicitadas, cant_entradas, descuento, total):
    """
    RF3 Regla 8: Registrar la operación en un archivo persistente (modo append).
    """
    with open("ventas.csv", "a", encoding="utf-8") as archivo:
        archivo.write(f"{numero_venta};{codigo_funcion};{sector};{butacas_solicitadas};{cant_entradas};{descuento};{total}\n")