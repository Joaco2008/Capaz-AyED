import os
import modulos.buscar_secuencial as buscar
import modulos.ordenamiento as ordenar
#def para cargar funciones 
def cargar_fun(obra,hora_inicio,hora_fin,fecha,id_sala,precio):
    arch = open("data/funciones.csv","r+")
    registro = arch.readlines()
    ultimo_registro = registro[-1].split(";")
    id = str(int(ultimo_registro[0]) + 1)
    registro_resultante = ";".join([id,obra,hora_inicio,hora_fin,fecha,id_sala,precio,"Programado\n"])
    arch.writelines(registro_resultante)
    arch.close()
    os.mkdir(f"funcion {id}")
    ruta_fun = open(f"funcion {id}/ubicaciones.csv","w")
    plantilla = open("data/plantilla.csv","r")
    registros_plantilla = plantilla.readline()
    while registros_plantilla != "":
        ruta_fun.write(registros_plantilla)
        registros_plantilla = plantilla.readline()
    plantilla.close()
    ruta_fun.close()

#def para consultar funciones
def consultar_funciones():
    #abrimos el archivo de funciones y leemos todas las lineas
    try:
        with open("data/funciones.csv","r") as arch:
            lineas = arch.readlines()
            
            #si el archivo esta vacio mostramos un texto
            if len(lineas) == 0:
                print("No hay funciones disponibles")
                return
            #si no, recorremos el archivo
            for linea in lineas:
                #separamos los datos de cada funcion
                datos = linea.strip().split(";")
                #verificamos que la funcion tenga todos los datos necesarios.
                if len(datos) < 8:
                    print(linea.strip())
                else:
                    #mostramos los datos de cada funcion
                    print(f"ID: {datos[0]} | Obra: {datos[1]} | Hora de inicio: {datos[2]} | Hora de fin: {datos[3]} | Fecha: {datos[4]} | ID sala: {datos[5]} | Precio: {datos[6]} | Estado: {datos[7]}")
    except FileNotFoundError:
        print("El archivo de funciones no existe. Por favor, cree una función primero.")       
def menu_funciones():
    print("Hola, bienvenido a la gestion de funciones ")
    print("Seleccione que desea hacer: \n 1- Consultar funciones\n 2- Agregar funciones\n 3- Buscar\n 4- Ordenar funciones\n  0 - Volver al menu principal")
    eleccion = int(input())
    #ciclo de eleccion de opciones
    while eleccion != 0:
        #consultamos que requiere hacer el usuario y llamamos a la funcion correspondiente
        if eleccion == 0: #si el usuario desea salir del menu de funciones, se sale del ciclo y vuelve al menu principal
            break
        elif eleccion == 1: #si el usuario desea consultar las funciones, le mostramos un listado de las funciones disponibles
            print("Listado de funciones: ")
            consultar_funciones()
            
            
        elif eleccion == 2:
            print("Agregar funcion: ")
            print("Ingrese los datos de la funcion: ")
            nombre = input("Ingrese el nombre de la obra: ")
            fecha = input("Ingrese la fecha de la funcion (dd/mm/aaaa): ")
            hora_inicio = input("Ingrese la hora de inicio de la funcion (hh:mm): ")
            hora_fin = input("Ingrese la hora de fin de la funcion (hh:mm): ")
            id_sala = input("Ingrese el ID de la sala: ")
            precio = input("Ingrese el precio de la entrada: ")
            cargar_fun(nombre,hora_inicio,hora_fin,fecha,id_sala,precio)
            print("Funcion agregada correctamente")
            
            
        elif eleccion == 3:
            print("Seleccione: \n 1- Buscar por ID\n 2- Buscar por nombre de obra")
            eleccion2 = int(input())
            if eleccion2 == 1:
                id_buscar = input("Ingrese el ID de la funcion: ")
                #llamamos a la funcion de busqueda secuencial
                resultado = buscar.busqueda_por_id(id_buscar,"data/funciones.csv")
                #corroboramos la existencia del ID y mostramos los datos de la funcion si es que existe.
                if resultado != "No existe este dato":
                    print(f"ID: {resultado[0]} | Obra: {resultado[1]} | Hora de inicio: {resultado[2]} | Hora de fin: {resultado[3]} | Fecha: {resultado[4]} | ID sala: {resultado[5]} | Precio: {resultado[6]} | Estado: {resultado[7]}")
                else:
                    print("No existe ninguna funcion con ese ID")
            elif eleccion2 == 2:
                #llamamos a la funcion de busqueda por nombre de obra
                nombre_buscar = input("Ingrese el nombre o parte del nombre de la obra: ")
                resultados = buscar.busqueda_por_nombre(nombre_buscar, "data/funciones.csv")
            
                if len(resultados) > 0:
                    print(f"\nSe encontraron {len(resultados)} función(es) que coinciden con '{nombre_buscar}':")
                    for f in resultados:
                        print(f"ID: {f[0]:<4} | Obra: {f[1]:<20} | Horario: {f[2]} - {f[3]} | Fecha: {f[4]} | Sala: {f[5]} | Precio: ${f[6]} | Estado: {f[7].strip()}")
            else:
                print(f"\nNo se encontraron funciones que contengan '{nombre_buscar}'.")
                
        elif eleccion == 4:
            print("Seleccione: \n 1- Ordenar por ID\n 2- Ordenar por nombre de obra")
            eleccion3 = int(input())
            if eleccion3 == 1:
                #llamamos a la funcion de ordenamiento por ID
                ordenar.ordenar_funciones_por_id()
            elif eleccion3 == 2:
                #llamamos a la funcion de ordenamiento por nombre de obra 
                ordenar.ordenar_funciones_por_nombre()
        eleccion = int(input("Seleccione que desea hacer: \n 1- Consultar funciones\n 2- Agregar funciones\n 3- Buscar\n 4- Ordenar funciones\n  0 - Volver al menu principal"))
