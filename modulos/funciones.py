import os
import modulos.buscar_secuencial as buscar
import modulos.ordenamiento as ordenar
#def para cargar funciones
dias_meses = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def validar_fecha(dia,mes,ano):
    # Primero controlamos que el dia no se exceda en un instante del rango "Habitual" que deberia estar en los dias
    if dia > 31 or dia < 1:
        return False
    # Segundo controlamo que nose exceda del indice de los meses
    if mes > 12 or mes < 1:
        return False
    # Tercero no controla que los años sean negativos
    if ano < 1:
        return False
    # Por ultimo controlar que no se exceda el dia segun lo que contenga el mes
    if dia > dias_meses[mes - 1]:
        return False
    return True
def cargar_fun(obra,hora_inicio,hora_fin,fecha,id_sala,precio):
    arch = open("data/funciones.csv","r+")
    registro = arch.readlines()
    ultimo_registro = registro[-1].split(";")
    # Si nunca hubieron funciones previamente grabadas
    try:
        id = str(int(ultimo_registro[0]) + 1)
    except ValueError:
        id = "1"
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
            for i in range(1,len(lineas)):
                #separamos los datos de cada funcion
                datos = lineas[i].strip().split(";")
                #verificamos que la funcion tenga todos los datos necesarios.
                if len(datos) < 8:
                    print(lineas[i].strip())
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
            fecha_separada = fecha.split("/")
            # Mientras no sea valida la fecha, va a preguntar
            while not(validar_fecha(int(fecha_separada[0]),int(fecha_separada[1]),int(fecha_separada[2]))):
                print("Fecha invalidad, porfavor ingrese una fecha valida")
                fecha = input("Ingrese la fecha de la funcion (dd/mm/aaaa): ")
                fecha_separada = fecha.split("/")
            hora_inicio = input("Ingrese la hora de inicio de la funcion (hh:mm): ")
            hora_fin = input("Ingrese la hora de fin de la funcion (hh:mm): ")
            # Controla que este en el intervalo de salas que existente en el teatro
            id_sala = input("Ingrese el ID de la sala: ")
            while int(id_sala) > 5 or int(id_sala) < 1:
                print("Error, sala inexistente. Ingrese un id valido de sala")
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
                #llamamos a la funcion de busqueda secuencial
                nombre_buscar = input("Ingrese el nombre o parte del nombre de la obra: ")
                resultados = buscar.buscar_funciones_por_nombre(nombre_buscar)
            
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
