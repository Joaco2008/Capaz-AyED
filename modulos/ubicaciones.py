import modulos.buscar_secuencial as b_secuencial
def mostrarubicaciones(datos_funcion):
    registros_plateas = b_secuencial.busqueda_por_grupo_vectores("platea",f"funcion {datos_funcion[0]}/ubicaciones.csv",2)
    registros_palcos = b_secuencial.busqueda_por_grupo_vectores("palco",f"funcion {datos_funcion[0]}/ubicaciones.csv",2)
    plateas_disponibles = 0
    palcos_disponibles = 0
    platea = [[""]*25 for _ in range(14)]
    palco = [[""]*25 for _ in range(10)]
    print("Ubicaciones Platea")
    contador_ubicaciones = 0
    # Le asignamos segun el estado de la ubicacion, un valor al elemento de la matriz (Nro = Disponible, 3X = Ocupado)
    for f in range(14):
        for c in range(25):
            if registros_plateas[contador_ubicaciones][3] == "ocupado\n":
                platea[f][c] = "XXX"
            else:
                if len(registros_plateas[contador_ubicaciones][1]) == 1:
                    platea[f][c] = f"00{registros_plateas[contador_ubicaciones][1]}"
                elif len(registros_plateas[contador_ubicaciones][1]) == 2:
                    platea[f][c] = f"0{registros_plateas[contador_ubicaciones][1]}"
                else:
                    platea[f][c] = registros_plateas[contador_ubicaciones][0]
                plateas_disponibles += 1
            contador_ubicaciones += 1
            print(platea[f][c],end=" ")
        print("")
    contador_ubicaciones = 0
    print("Ubicaciones Palcos")
    for f in range(10):
        for c in range(25):
            if registros_palcos[contador_ubicaciones][3] == "ocupado\n":
                palco[f][c] = "XXX"
            else:
                if len(registros_palcos[contador_ubicaciones][1]) == 1:
                    palco[f][c] = f"00{registros_palcos[contador_ubicaciones][1]}"
                elif len(registros_palcos[contador_ubicaciones][1]) == 2:
                    palco[f][c] = f"0{registros_palcos[contador_ubicaciones][1]}"
                else:
                    palco[f][c] = registros_palcos[contador_ubicaciones][1]
                palcos_disponibles += 1
            contador_ubicaciones += 1
            print(palco[f][c],end=" ")
        print("")
    print(f"PLATEAS DISPONIBLES = {plateas_disponibles}")
    print(f"PALCOS DISPONIBLES = {palcos_disponibles}")
    print(f"TOTAL DISPONIBLES = {plateas_disponibles + palcos_disponibles}")    
    # Seleccionamos las ubicaciones que queremos ocupar en la funcion (no se pueden seleccionar ocupadas)
    cant_platea = int(input("Ingrese la cantidad de entradas para platea: "))
    while cant_platea > plateas_disponibles or cant_platea < 0:
        print("Error, Ingrese una cantidad mayor o igual 0 y menor a las ubicaciones disponibles")
        cant_platea = int(input("Ingrese la cantidad de entradas para platea: "))
    cont_cant_platea = 0
    # Creamos las listas para almacenar nuestras entradas
    platea_entradas = []
    palco_entradas = []
    posicion_lista_entradas = 0
    while cont_cant_platea < cant_platea:
        cod_ubi = int(input(f"Ingrese el codigo de la ubicacion nro {cont_cant_platea+1}:"))
        if cod_ubi > 0 and cod_ubi <= 350:
            if registros_plateas[cod_ubi-1][3] == "ocupado\n":
                print("Ubicacion ocupada, porfavor seleccione otro")
            else:
                print(f"Ubicacion {registros_plateas[cod_ubi-1][0]} seleccionada")                            
                registros_plateas[cod_ubi-1][3] = "ocupado\n"
                for i in range(len(platea_entradas)):
                    if int(platea_entradas[i]) > cod_ubi:
                        posicion_lista_entradas = i
                        break
                else:
                    # Si es mayor que todos, va al final
                    posicion_lista_entradas = len(platea_entradas)
                cont_cant_platea += 1
                codigo_en_caracter = str(cod_ubi)
                platea_entradas.insert(posicion_lista_entradas, codigo_en_caracter)
        else:
            print("Ubicacion Inexistente, porfavor seleccione una ubicacion valida")
    cant_palco = int(input("Ingrese la cantidad de entradas para palco: "))
    while cant_palco > palcos_disponibles or cant_palco < 0:
        print("Error, Ingrese una cantidad mayor o igual 0 y menor a las ubicaciones disponibles")
        cant_palco = int(input("Ingrese la cantidad de entradas para palco: "))
    cont_cant_palco = 0
    posicion_lista_entradas = 0
    while cont_cant_palco < cant_palco:
        cod_ubi = int(input(f"Ingrese el codigo de la ubicacion nro {cont_cant_palco+1}:"))
        if cod_ubi > 0 and cod_ubi <= 250:
            if registros_palcos[cod_ubi-1][3] == "ocupado\n":
                print("Ubicacion ocupada, porfavor seleccione otro")
            else:
                print(f"Ubicacion {registros_palcos[cod_ubi-1][1]} seleccionada")
                registros_palcos[cod_ubi-1][3] = "ocupado\n"
                for i in range(len(palco_entradas)):
                    if int(palco_entradas[i]) > cod_ubi:
                        posicion_lista_entradas = i
                        break
                else:
                    # Si es mayor que todos, va al final
                    posicion_lista_entradas = len(palco_entradas)
                codigo_en_caracter = str(cod_ubi)
                palco_entradas.insert(posicion_lista_entradas, codigo_en_caracter)
                cont_cant_palco += 1
        else:
            print("Ubicacion Inexistente, porfavor seleccione una ubicacion valida")
    asientos = [platea_entradas,palco_entradas]
    return asientos