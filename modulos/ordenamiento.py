# Metodo de ordenamiento por seleccion, True = Ordenar ascendentemente, False = Ordenar Desendentemente
def seleccion(vector, forma):
    if forma:
        for i in range(len(vector)):
            mas_chico = vector[i]
            indice_mas_chico = i
            for e in range(i,len(vector)):
                if mas_chico > vector[e]:
                    mas_chico = vector[e]
                    indice_mas_chico = e
            aux = vector[i]
            vector[i] = mas_chico
            vector[indice_mas_chico] = aux
    else:
        for i in range(len(vector)):
            mas_grande = vector[i]
            indice_mas_grande = i
            for e in range(i,len(vector)):
                if mas_grande < vector[e]:
                    mas_grande = vector[e]
                    indice_mas_grande = e
            aux = vector[i]
            vector[i] = mas_grande
            vector[indice_mas_grande] = aux
    return vector

# Metodo de ordenamiento Burbuja (no recomendable para medianas o grandes volumnes de datos), True = ASC y False = DESC
def burbuja(vector, forma):
    if forma:
        for i in range(len(vector)):
            for e in range(len(vector)-1):
                if vector[e] > vector[e+1]:
                    aux = vector[e]
                    vector[e] = vector[e+1]
                    vector[e+1] = aux
    else:
        for i in range(len(vector)):
            for e in range(len(vector)-1):
                if vector[e] < vector[e+1]:
                    aux = vector[e]
                    vector[e] = vector[e+1]
                    vector[e+1] = aux
    return vector

def ordenar_funciones_por_id():
    # 1. Preguntamos al usuario el sentido de ordenamiento
    opcion = int(input("Elegí el orden:\n 1. Menor a mayor (Ascendente)\n 2. Mayor a menor (Descendente)\nOpción: "))

    # 2. Leemos las funciones desde el CSV
    funciones = []
    try:
        with open("data/funciones.csv", "r") as arch:
            for linea in arch:
                datos = linea.strip().split(";")
                if len(datos) >= 8:
                    funciones.append(datos)
    except FileNotFoundError:
        print("El archivo 'data/funciones.csv' no existe.")
        return

    if len(funciones) == 0:
        print("No hay funciones registradas para ordenar.")
        return

    # 3. Lógica de SELECCIÓN idéntica a ordenamiento.py
    if opcion == 1:
        # Ordenamiento Ascendente (Menor a Mayor por ID)
        for i in range(len(funciones)):
            mas_chico = funciones[i]
            indice_mas_chico = i
            for e in range(i, len(funciones)):
                if int(mas_chico[0]) > int(funciones[e][0]):
                    mas_chico = funciones[e]
                    indice_mas_chico = e
            aux = funciones[i]
            funciones[i] = mas_chico
            funciones[indice_mas_chico] = aux

    elif opcion == 2:
        # Ordenamiento Descendente (Mayor a Menor por ID)
        for i in range(len(funciones)):
            mas_grande = funciones[i]
            indice_mas_grande = i
            for e in range(i, len(funciones)):
                if int(mas_grande[0]) < int(funciones[e][0]):
                    mas_grande = funciones[e]
                    indice_mas_grande = e
            aux = funciones[i]
            funciones[i] = mas_grande
            funciones[indice_mas_grande] = aux

    # 4. Mostramos las funciones ordenadas en pantalla
    print("\n=================== FUNCIONES ORDENADAS POR ID ===================")
    for f in funciones:
        print(f"ID: {f[0]:<4} | Obra: {f[1]:<20} | Horario: {f[2]} - {f[3]} | Fecha: {f[4]} | Sala: {f[5]} | Precio: ${f[6]} | Estado: {f[7].strip()}")

#funcion para ordenar las funciones por nombre de obra
def ordenar_funciones_por_nombre():
    # 1. Preguntamos al usuario el sentido de ordenamiento
    opcion = input("Elegí el orden:\n 1. De A a Z (Ascendente)\n 2. De Z a A (Descendente)\nOpción: ")

    # 2. Leemos las funciones desde el CSV
    funciones = []
    try:
        with open("data/funciones.csv", "r") as arch:
            for linea in arch:
                datos = linea.strip().split(";")
                if len(datos) >= 8:
                    funciones.append(datos)
    except FileNotFoundError:
        print("El archivo 'data/funciones.csv' no existe.")
        return

    if len(funciones) == 0:
        print("No hay funciones registradas para ordenar.")
        return

    # 3. Lógica de SELECCIÓN por Nombre de Obra (posición 1)
    if opcion == "1":
        # Ordenamiento de A a Z
        for i in range(len(funciones)):
            mas_chico = funciones[i]
            indice_mas_chico = i
            for e in range(i, len(funciones)):
                # Comparamos alfabéticamente en minúsculas en la posición 1
                if mas_chico[1].lower() > funciones[e][1].lower():
                    mas_chico = funciones[e]
                    indice_mas_chico = e
            aux = funciones[i]
            funciones[i] = mas_chico
            funciones[indice_mas_chico] = aux

    elif opcion == "2":
        # Ordenamiento de Z a A
        for i in range(len(funciones)):
            mas_grande = funciones[i]
            indice_mas_grande = i
            for e in range(i, len(funciones)):
                # Comparamos alfabéticamente en minúsculas en la posición 1
                if mas_grande[1].lower() < funciones[e][1].lower():
                    mas_grande = funciones[e]
                    indice_mas_grande = e
            aux = funciones[i]
            funciones[i] = mas_grande
            funciones[indice_mas_grande] = aux

    # 4. Mostramos las funciones ordenadas en pantalla
    print("\n=================== FUNCIONES ORDENADAS POR NOMBRE ===================")
    for f in funciones:
        print(f"ID: {f[0]:<4} | Obra: {f[1]:<20} | Horario: {f[2]} - {f[3]} | Fecha: {f[4]} | Sala: {f[5]} | Precio: ${f[6]} | Estado: {f[7].strip()}")
