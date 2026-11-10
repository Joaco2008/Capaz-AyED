import modulos.ubicaciones as ubi
import modulos.busqueda_binaria as binaria
import os

def verificar_estado_socio(dni_ingresado):
    """
    Busca al socio por DNI en el archivo socios.csv y devuelve True si está activo.
    """
    with open("data/socios.csv", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        for i in range(1,len(lineas)):
            datos = lineas[i].strip().split(";")
            if datos[1] == dni_ingresado:
                if datos[2].lower() == "activo":
                    return True
                else:
                    print("El socio adeuda cuotas. No se aplica el descuento del 30%.")
                    return False
        print("El DNI ingresado no está registrado como socio.")
        return False

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
    # Redondea a 2 digitos fraccionarios el precio y descuento final
    return round(total,2), round(descuento,2)
def gestionar_venta_entradas():
    """
    Orquestador principal del proceso de ventas. 
    Delega responsabilidades para mantener la modularización exigida.
    """
    print("--- REGISTRO DE VENTA DE ENTRADAS ---")
    codigo_funcion = input("Ingrese el código de la función para la venta de entradas: ")
        # RF3 Regla 1: Verificar que la función exista (mediante búsqueda manual secuencial)
    archivo = open("data/funciones.csv","r")
    registros = archivo.readlines()
    try:
        funcion_encontrada = binaria.busqueda_binaria_recursiva(registros,int(codigo_funcion),1,len(registros)-1)    
    except ValueError:
        print("Error, Caracteres invalidos para el codigo")
        return False
    if funcion_encontrada == "No existe este dato":
        print("No se encontró la función con el código proporcionado.")
        return
    else:
        print("Función encontrada:  ", funcion_encontrada)
        platea_entradas,enlaces_platea,inicio_platea,palco_entradas,enlaces_palco,inicio_palco = ubi.mostrarubicaciones(funcion_encontrada)
        if len(platea_entradas) == 0 and len(palco_entradas) == 0:
            print("No se han elegido asientos, se cancela la operacion")
            return
        precio_base = float(funcion_encontrada[-2])
        es_socio = False
        socio_input = input("¿El comprador es socio? (s/n): ").lower()
        if socio_input == "s":
            dni_socio = input("Ingrese el DNI del socio: ")
            es_socio = verificar_estado_socio(dni_socio)
        total, descuento = calcular_importe(len(platea_entradas),len(palco_entradas),precio_base,es_socio)
        # Muestra comprobante o ticket de la venta        
        texto_platea = ""
        texto_palco = ""
        for i in range(len(enlaces_platea)):
            if i == 0:
                texto_platea += str(platea_entradas[inicio_platea]) + " "
            else:
                texto_platea += str(platea_entradas[enlaces_platea[i-1]]) + " "
        for i in range(len(enlaces_palco)): 
            if i == 0:
                texto_palco += str(palco_entradas[inicio_palco]) + " "
            else:
                texto_palco += str(palco_entradas[enlaces_palco[i-1]]) + " "
        print(f"\n--- TICKET DE VENTA ---")
        print(f"Cod.Funcion: {funcion_encontrada[0]}")
        print(f"Obra: {funcion_encontrada[1]}")
        print(f"Sector: Platea | Entradas: {len(platea_entradas)} | Codigo/s: {texto_platea} ")
        print(f"Sector: Palcos | Entradas: {len(palco_entradas)} | Codigo/s: {texto_palco}")
        print(f"Descuento socio: ${descuento}")
        print(f"TOTAL A PAGAR: ${total}")
        print("-----------------------")
        confirmacion = input("¿Desea confirmar y registrar la venta? (s/n): ")
        
        if confirmacion.lower() == 's':
            actualizar_estado_archivo(codigo_funcion, platea_entradas,enlaces_platea,inicio_platea,palco_entradas,enlaces_palco,inicio_palco)
            ubis_platea = texto_platea.strip()
            ubis_palco = texto_palco.strip()
            # Buscando el ultimo indice de compra - Para autoincrementar
            if os.path.exists(f"funcion {codigo_funcion}/ventas.csv"):
                arch = open(f"funcion {codigo_funcion}/ventas.csv","r+")
                registro = arch.readlines()
                ultimo_registro = registro[-1].split(";")
                id = str(int(ultimo_registro[0]) + 1)
                arch.close()
            else:
                id = 1
            registrar_venta_archivo(id, codigo_funcion,ubis_platea,ubis_palco,len(platea_entradas),len(palco_entradas),descuento,total)
            print("Venta registrada exitosamente.")
        else:
            print("Venta cancelada por el usuario.")
        # else:
        #     print("No se puede realizar la venta, las butacas solicitadas no están disponibles.")

def actualizar_estado_archivo(codigo_funcion, platea_entradas,enlaces_platea,inicio_platea,palco_entradas,enlaces_palco,inicio_palco):
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
                # Recorre los asientos 
                for e in range(len(enlaces_platea)):
                    if e == 0:
                        if butaca == platea_entradas[inicio_platea]:
                            linea[3] = "ocupado\n"
                            lineas[i] = ";".join(linea)                        
                    else:
                        if butaca == platea_entradas[enlaces_platea[e-1]]:
                            linea[3] = "ocupado\n"
                            lineas[i] = ";".join(linea)
            elif linea[2] == "palco":
                butaca = str(linea[1])
                for e in range(len(enlaces_palco)):
                    if e == 0:
                        if butaca == palco_entradas[inicio_palco]:
                            linea[3] = "ocupado\n"
                            lineas[i] = ";".join(linea)                        
                    else:
                        if butaca == palco_entradas[enlaces_palco[e-1]]:
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
            archivo.write("id_entrada;dato_funcion(nro);plateas_seleccionadas;palcos_seleccionados;cant_entradas_platea;cant_entradas_palco;descuento;total\n")           
            archivo.write(f"{numero_venta};{codigo_funcion};{ubis_platea};{ubis_palcos};{cant_entradas_platea};{cant_entradas_palco};{descuento};{total}\n")        