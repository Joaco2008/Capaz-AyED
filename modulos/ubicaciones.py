import modulos.buscar_secuencial as b_secuencial
def mostrarubicaciones(nro_funcion):
    datos_funcion = b_secuencial.busqueda_por_id(nro_funcion, "data/funciones.csv")
    if datos_funcion == "No existe este dato":
        return datos_funcion
    # Si la funcion es encontrada
    else:
        estado_funcion = datos_funcion[8]
        print(estado_funcion)
        nro_sala = datos_funcion[5]
        print(nro_sala)
        if estado_funcion.startswith("Programado"):
            datos_sala = b_secuencial.busqueda_por_id(nro_sala,"data/salas.csv")
            if datos_sala == "No existe este dato":
                return "No existe esta sala"
            else:
                f_platea = int(datos_sala[4])
                c_platea = int(datos_sala[5])
                f_palco = int(datos_sala[6])
                c_palco = int(datos_sala[7])
                #proceso de busquedas de butacas
                arch_ubis = open("data/ubicaciones_funcion.csv","r+")
                r_ubis = arch_ubis.readline().split(";")
                lista_plateas = []
                lista_palcos = []
                # Almacenamos los codigos identificadores en 2 listas (plateas y palcos)
                while r_ubis != ['']:
                    if r_ubis[-1].strip("\n") == datos_funcion[0]:
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
                print(len(lista_plateas))
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
                            lista_plateas[cod_ubi-1][1] = "ocupado\n"
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
                            lista_palcos[cod_ubi-1][1] = "ocupado\n"
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
            return"Esta funcion ya ha expirado"
    return f"Platea: {platea_entradas} y Palco: {palco_entradas}"
    