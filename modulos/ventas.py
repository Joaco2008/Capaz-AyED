from modulos.buscar_secuencial import busqueda_por_id
import modulos.ubicaciones as ubi
import os
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

def calcular_importe(cant_entradas_platea,cant_entradas_palco, precio_base, es_socio):
    """
    RF3 Reglas 5 y 6: Calcular el importe de la operación y aplicar descuento del 30% a socios.
    """
    precio_platea = precio_base * cant_entradas_platea
    precio_palco = precio_base * cant_entradas_palco * 1.3
    subtotal = precio_platea + precio_palco
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
    funcion_encontrada = busqueda_por_id(codigo_funcion, "data/funciones.csv")    
    if funcion_encontrada == "No existe este dato":
        print("No se encontró la función con el código proporcionado.")
        return
    else:
        print("Función encontrada:  ", funcion_encontrada)
        asientos = ubi.mostrarubicaciones(funcion_encontrada)
        if len(asientos[0]) == 0 and len(asientos[1]) == 0:
            print("No se han elegido asientos, se cancela la operacion")
            return
        precio_base = float(funcion_encontrada[-2])
        socio_input = input("¿Es socio? (s/n): ").lower()
        es_socio = socio_input == "s"
        total, descuento = calcular_importe(len(asientos[0]),len(asientos[1]),precio_base,es_socio)
        # Muestra comprobante o ticket de la venta        
        print(f"\n--- TICKET DE VENTA ---")
        print(f"Cod.Funcion: {funcion_encontrada[0]}")
        print(f"Obra: {funcion_encontrada[1]}")
        print(f"Sector: Platea | Entradas: {len(asientos[0])} | Codigo/s: {" ".join(asientos[0])}")
        print(f"Sector: Palcos | Entradas: {len(asientos[1])} | Codigo/s: {" ".join(asientos[1])}")
        print(f"Descuento socio: ${descuento}")
        print(f"TOTAL A PAGAR: ${total}")
        print("-----------------------")
        confirmacion = input("¿Desea confirmar y registrar la venta? (s/n): ")
        
        if confirmacion.lower() == 's':
            actualizar_estado_archivo(codigo_funcion, asientos)
            ubis_platea = ",".join(asientos[0])
            ubis_palco = ",".join(asientos[1])
            # Buscando el ultimo indice de compra - Para autoincrementar
            if os.path.exists(f"funcion {codigo_funcion}/ventas.csv"):
                arch = open(f"funcion {codigo_funcion}/ventas.csv","r+")
                registro = arch.readlines()
                ultimo_registro = registro[-1].split(";")
                id = str(int(ultimo_registro[0]) + 1)
                arch.close()
            else:
                id = 1
            registrar_venta_archivo(id, codigo_funcion,ubis_platea,ubis_palco,len(asientos[0]),len(asientos[1]),descuento,total)
            print("Venta registrada exitosamente.")
        else:
            print("Venta cancelada por el usuario.")
        # else:
        #     print("No se puede realizar la venta, las butacas solicitadas no están disponibles.")

def actualizar_estado_archivo(codigo_funcion, asientos):
    """
    RF3 Regla 7: Actualizar la disponibilidad solamente cuando la venta haya sido validada.
    """
    # Se guarda el archivo en memoria para modificar la línea exacta y reescribirlo
    with open(f"funcion {codigo_funcion}/ubicaciones.csv", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        for i in range(len(lineas)):
            linea = lineas[i].split(";")
            # Verificación de que existen elementos en la lista para evitar IndexError con líneas vacías
            if linea[2] == "platea":    
                butaca = str(linea[1])
                if butaca in asientos[0]:
                    linea[3] = "ocupado\n"
                    lineas[i] = ";".join(linea)
            elif linea[2] == "palco":
                butaca = str(linea[1])
                if butaca in asientos[1]:
                    linea[3] = "ocupado\n"
                    lineas[i] = ";".join(linea)
    with open(f"funcion {codigo_funcion}/ubicaciones.csv", "w", encoding="utf-8") as archivo:
        archivo.writelines(lineas)
def registrar_venta_archivo(numero_venta, codigo_funcion, ubis_platea,ubis_palcos, cant_entradas_platea, cant_entradas_palco, descuento, total):
    """
    RF3 Regla 8: Registrar la operación en un archivo persistente (modo append).
    """
    if os.path.exists(f"funcion {codigo_funcion}/ventas.csv"):
        with open(f"funcion {codigo_funcion}/ventas.csv", "a", encoding="utf-8") as archivo:
            archivo.write(f"{numero_venta};{codigo_funcion};{ubis_platea};{ubis_palcos};{cant_entradas_platea};{cant_entradas_palco};{descuento};{total}\n")
    else:
        with open(f"funcion {codigo_funcion}/ventas.csv", "w", encoding="utf-8") as archivo:
            archivo.write("id_entrada;dato_funcion(nro);dato_ubicacion(nros);cant_entradas_platea;cant_entradas_palco;descuento;total\n")           
            archivo.write(f"{numero_venta};{codigo_funcion};{ubis_platea};{ubis_palcos};{cant_entradas_platea};{cant_entradas_palco};{descuento};{total}\n")        