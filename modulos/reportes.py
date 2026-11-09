#1-cantidad de entradas vendidas para una funcion#
    #tomar dato de ventas de entradas de una funcion y devolver la cantidad de entradas vendidas para esa funcion#
import os

# 1. Verificar si existe el archivo de ventas de esa función 
def obtener_cantidad_entradas_vendidas(codigo_funcion):
    total_entradas = 0
    suma = 0
    if os.path.exists(f"funcion {codigo_funcion}/ventas.csv"):
        with open(f"funcion {codigo_funcion}/ventas.csv", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            for i in range(1, len(lineas)):
                datos = lineas[i].strip().split(";")
                suma = suma + int(datos[4]) + int(datos[5])
                total_entradas = suma
        # A partir de acá, 'lineas' tiene todas las operaciones de venta de esa función
    else:
    # Si el archivo no existe, significa que todavía no se vendió ninguna entrada
        total_entradas = 0
    return total_entradas


#2-cantidad de ubicaciones disponibles para una funcion#
    #cantidad de ventas - capacidad de sala de una sola funcion, devolver la cantidad de ubicaciones disponibles para esa funcion#
def obtener_ubicaciones_disponibles(codigo_funcion):
    contador_disponibles = 0
    if os.path.exists(f"funcion {codigo_funcion}/ubicaciones.csv"):
            with open(f"funcion {codigo_funcion}/ubicaciones.csv", "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
                for i in range(1, len(lineas)):
                    datos = lineas[i].strip().split(";")
                    if datos[3] == "ocupado":
                        contador_disponibles = contador_disponibles
                    else:
                        contador_disponibles += 1
    else:
            contador_disponibles = 0
    return contador_disponibles



#3-recaudacion total de una funcion#
    #sumar el total de venta de entradas de una solafuncion y devolver la recaudacion total de esa funcion#
def obtener_recaudacion_funcion(codigo_funcion):
    recaudacion_funcion = 0
    if os.path.exists(f"funcion {codigo_funcion}/ventas.csv"):
        with open(f"funcion {codigo_funcion}/ventas.csv", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            for i in range(1, len(lineas)):
                datos = lineas[i].strip().split(";")
                recaudacion_funcion = recaudacion_funcion + int(datos[7]) 
        # A partir de acá, 'lineas' tiene todas las operaciones de venta de esa función
    else:
    # Si el archivo no existe, significa que todavía no se vendió ninguna entrada
        recaudacion_funcion = 0
    return recaudacion_funcion



#4-recaudacion total de todas las funciones#
    #sumar el total de venta de entradas de todas las funciones y devolver la recaudacion total de todas las funciones#
def obtener_recaudacion_total():
    recaudacion_total = 0
    for codigo_funcion in os.listdir("funcion"):
        numero_funcion = codigo_funcion.replace("funcion ", "")
        if os.path.exists(f"funcion {numero_funcion}/ventas.csv"):
            recaudacion_total += obtener_recaudacion_funcion(numero_funcion)
    return recaudacion_total

#5-listado de funciones ordenadosegun un criterio de demanda#
    #ordenar las funciones según la cantidad de entradas vendidas y devolver el listado#
def obtener_funciones_por_demanda():
    lista_demanda = []
    # 1. Recorremos las carpetas y juntamos los datos usando tus funciones anteriores
    for codigo_funcion in os.listdir("funcion"):
        numero_funcion = codigo_funcion.replace("funcion ", "")
        if os.path.exists(f"funcion {numero_funcion}/ubicaciones.csv"): # O el archivo de ventas
            cantidad = obtener_cantidad_entradas_vendidas(numero_funcion)
            lista_demanda.append([numero_funcion, cantidad])     
    # 2. Aplicamos el método de Selección para ordenar de MAYOR a MENOR demanda
    for i in range(len(lista_demanda)):
        mas_grande = lista_demanda[i]
        indice_mas_grande = i
        for e in range(i, len(lista_demanda)):
            # Comparamos la cantidad vendida (que está en la posición 1)
            if mas_grande[1] < lista_demanda[e][1]:
                mas_grande = lista_demanda[e]
                indice_mas_grande = e
        # Intercambio (swap)
        aux = lista_demanda[i]
        lista_demanda[i] = mas_grande
        lista_demanda[indice_mas_grande] = aux
        
    return lista_demanda

            
            
            
#6-identificacion de la funcion con mayor cantidad de entradas vendidas#
    #tomar el listado de funciones y devolver la funcion con mayor cantidad de entradas vendidas#
def funcion_mayor_demanda():
    # Llamamos a la función que ya armamos en el punto 5
    lista_ordenada = obtener_funciones_por_demanda()
    # Verificamos que la lista no esté vacía para que no rompa
    if len(lista_ordenada) > 0:
        # El primero de la lista ordenada de mayor a menor es el campeón
        return lista_ordenada[0]
    else:
        return None

def menu_reportes():
    opcion = ""
    while opcion != "0":
        print("\n=================== MENÚ DE REPORTES - TEATRO ===================")
        print("1. Cantidad de entradas vendidas de una función")
        print("2. Ubicaciones disponibles de una función")
        print("3. Recaudación de una función específica")
        print("4. Recaudación total de todas las funciones")
        print("5. Listado de funciones ordenadas por demanda")
        print("6. Función con mayor demanda")
        print("0. Salir")
        
        opcion = input("Elegí una opción: ")
        
        if opcion == "1":
            codigo = input("Ingresá el código de la función: ")
            cantidad = obtener_cantidad_entradas_vendidas(codigo)
            print(f"-> Entradas vendidas para la función {codigo}: {cantidad}")
            
        elif opcion == "2":
            codigo = input("Ingresá el código de la función: ")
            disponibles = obtener_ubicaciones_disponibles(codigo)
            print(f"-> Butacas libres en la función {codigo}: {disponibles}")
            
        elif opcion == "3":
            codigo = input("Ingresá el código de la función: ")
            recaudacion = obtener_recaudacion_funcion(codigo)
            print(f"-> Recaudación de la función {codigo}: ${recaudacion}")
            
        elif opcion == "4":
            total = obtener_recaudacion_total()
            print(f"-> Recaudación total de todas las funciones: ${total}")
            
        elif opcion == "5":
            print("\nCalculando y ordenando por demanda...")
            ranking = obtener_funciones_por_demanda()
            for func, cant in ranking:
                print(f"Función {func}: {cant} entradas vendidas")
                
        elif opcion == "6":
            campeona = funcion_mayor_demanda()
            if campeona:
                print(f"🏆 La función con mayor demanda es la N° {campeona[0]} con {campeona[1]} entradas vendidas.")
            else:
                print("No hay funciones registradas.")
                
        elif opcion == "0":
            print("Saliendo del módulo de reportes...")
        else:
            print("Opción inválida. Por favor, elegí un número del 0 al 6.")

# Ejecución del menú al correr el script
if __name__ == "__main__":
    menu_reportes()