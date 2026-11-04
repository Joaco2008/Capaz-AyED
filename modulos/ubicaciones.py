def mostrarubicaciones(nro_funcion):
    arch_fun = open("data/funciones.csv", "r")
    r_fun = arch_fun.readline().split(";")
    encontrado_fun = False
    nro_sala = 0
    estado = ""
    # Buscar la funcion
    while r_fun != [''] and not(encontrado_fun):
        if r_fun[0] == nro_funcion:
            print(f"Funcion encontrada, obra: {r_fun[1]}")
            encontrado_fun = True
            nro_sala = r_fun[5]
            estado = r_fun[8]
        r_fun = arch_fun.readline().split(";")
    if not(encontrado_fun):
        print("No existe esta funcion")
    # Si la funcion es encontrada
    else:
        if estado == "Programado" or estado == "Reprogramado":
            arch_salas = open("data/salas.csv","r")
            r_salas = arch_salas.readline()
            encontrado_sala = False
            c_platea = 0
            f_platea = 0
            c_palco = 0
            f_palco = 0
            # Buscamos Sala
            while r_salas != [''] and not(encontrado_sala):
                if r_salas[2] == nro_sala:
                    print(f"Sala encontrada, capacidad: {r_salas[1]}")
                    encontrado_sala = True
                    f_platea = int(r_salas[4])
                    c_platea = int(r_salas[5])
                    f_palco = int(r_salas[6])
                    c_palco = int(r_salas[7])
                r_salas = arch_salas.readline().split(";")
            if not(encontrado_sala):
                print("No existe esta sala")
            else:
                #proceso de busquedas de butacas
                arch_ubis = open("data/ubicaciones.csv","r+")
                r_ubis = arch_ubis.readline().split(";")
                lista_plateas = []
                lista_palcos = []
                # Almacenamos los codigos identificadores en 2 listas (plateas y palcos)
                while r_ubis != ['']:
                    if r_ubis[1] == nro_sala:
                        if r_ubis[3] == "platea":
                            if len(r_ubis[2]) == 1: 
                                lista_plateas.append(["00"+r_ubis[2],r_ubis[4]])
                            elif len(r_ubis[2]) == 2: 
                                lista_plateas.append(["0"+r_ubis[2],r_ubis[4]])
                            else: 
                                lista_plateas.append([r_ubis[2],r_ubis[4]])
                        elif r_ubis[3] == "palco":
                            if len(r_ubis[2]) == 1: 
                                lista_palcos.append(["00"+r_ubis[2],r_ubis[4]])
                            elif len(r_ubis[2]) == 2: 
                                lista_palcos.append(["0"+r_ubis[2],r_ubis[4]])
                            else: 
                                lista_palcos.append([r_ubis[2],r_ubis[4]])
                    r_ubis = arch_ubis.readline().split(";")
                # Generamos las matrices
                platea = [[""]*c_platea for _ in range(f_platea)]
                palco = [[""]*c_palco for _ in range(f_palco)]
                print("Ubicaciones Platea")
                contador_ubicaciones = 0
                # Le asignamos segun el estado de la ubicacion, un valor al elemento de la matriz (Nro = Disponible, 3X = Ocupado)
                for f in range(f_platea):
                    for c in range(c_platea):
                        if lista_plateas[contador_ubicaciones][1] == "ocupado\n":
                            platea[f][c] = "XXX"
                        else:
                            platea[f][c] = lista_plateas[contador_ubicaciones][0]
                        contador_ubicaciones += 1
                        print(platea[f][c],end=" ")
                    print("")
                contador_ubicaciones = 0
                print("Ubicaciones Palcos")
                for f in range(f_palco):
                    for c in range(c_palco):
                        if lista_palcos[contador_ubicaciones][1] == "ocupado\n":
                            palco[f][c] = "XXX"
                        else:
                            palco[f][c] = lista_palcos[contador_ubicaciones][0]
                        contador_ubicaciones += 1
                        print(palco[f][c],end=" ")
                    print("")
                # Seleccionamos las ubicaciones que queremos ocupar en la funcion (no se pueden seleccionar ocupadas)
                cant_platea = int(input("Ingrese la cantidad de entradas para platea: "))
                cont_cant_platea = 0
                # Creamos las listas para almacenar nuestras entradas
                platea_entradas = []
                palco_entradas = []
                posicion_lista_entradas = 0
                while cont_cant_platea < cant_platea:
                    cod_ubi = int(input(f"Ingrese el codigo de la ubicacion nro {cont_cant_platea+1}:"))
                    if cod_ubi > 0 and cod_ubi <= 350:
                        if lista_plateas[cod_ubi-1][1] == "ocupado\n":
                            print("Ubicacion ocupada, porfavor seleccione otro")
                        else:
                            print(f"Ubicacion {lista_plateas[cod_ubi-1][0]} seleccionada")                            
                            for i in range(len(platea_entradas)):
                                if platea_entradas[i] > cod_ubi:
                                    posicion_lista_entradas = i
                                    break
                            else:
                                # Si es mayor que todos, va al final
                                posicion_lista_entradas = len(platea_entradas)
                            cont_cant_platea += 1
                            platea_entradas.insert(posicion_lista_entradas, cod_ubi)
                    else:
                        print("Ubicacion Inexistente, porfavor seleccione una ubicacion valida")
                cant_palco = int(input("Ingrese la cantidad de entradas para palco: "))
                cont_cant_palco = 0
                posicion_lista_entradas = 0
                while cont_cant_palco < cant_palco:
                    cod_ubi = int(input(f"Ingrese el codigo de la ubicacion nro {cont_cant_palco+1}:"))
                    if cod_ubi > 0 and cod_ubi <= 250:
                        if lista_palcos[cod_ubi-1][1] == "ocupado\n":
                            print("Ubicacion ocupada, porfavor seleccione otro")
                        else:
                            print(f"Ubicacion {lista_palcos[cod_ubi-1][0]} seleccionada")
                            for i in range(len(palco_entradas)):
                                if palco_entradas[i] > cod_ubi:
                                    posicion_lista_entradas = i
                                    break
                            else:
                                # Si es mayor que todos, va al final
                                posicion_lista_entradas = len(palco_entradas)
                            palco_entradas.insert(posicion_lista_entradas, cod_ubi)
                            cont_cant_palco += 1
                    else:
                        print("Ubicacion Inexistente, porfavor seleccione una ubicacion valida")
                # Queriendo implementar una funcion para registrar la ocupacion de una ubicacion en el archivo
                # arch_ubis.seek(0)
                # r_ubis = arch_ubis.readline().split(";")
                # total_entradas = cant_palco + cant_platea
                # cont_cant_platea = 0
                # i = 0
                # while r_ubis != [''] and i < total_entradas:
                #     if r_ubis[1] == nro_sala and r_ubis[3] == "Platea" and r_ubis[2] == platea_entradas[cont_cant_platea][0]:
                        
                #     r_ubis = arch_ubis.readline().split(";")
                    
        else:
            print("Esta funcion ya ha expirado")
    return f"Platea: {len(platea_entradas)} y Palco: {len(palco_entradas)}"
    