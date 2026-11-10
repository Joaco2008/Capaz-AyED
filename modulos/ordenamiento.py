# Metodo de ordenamiento por seleccion, True = Ordenar ascendentemente, False = Ordenar Desendentemente
def seleccion(vector, forma):
    copia_vector = vector.copy()
    if forma:
        for i in range(len(copia_vector)):
            mas_chico = copia_vector[i]
            indice_mas_chico = i
            for e in range(i, len(copia_vector)):
                if mas_chico > copia_vector[e]:
                    mas_chico = copia_vector[e]
                    indice_mas_chico = e
            aux = copia_vector[i]
            copia_vector[i] = mas_chico
            copia_vector[indice_mas_chico] = aux
    else:
        for i in range(len(vector)):
            mas_grande = vector[i]
            indice_mas_grande = i
            for e in range(i, len(vector)):
                if mas_grande < vector[e]:
                    mas_grande = vector[e]
                    indice_mas_grande = e
            aux = vector[i]
            vector[i] = mas_grande
            vector[indice_mas_grande] = aux
    return copia_vector

# Metodo de ordenamiento por seleccion, True = Ordenar ascendentemente, False = Ordenar Desendentemente
def obtener_enlaces(vector):
    if len(vector) == 0:
        return [], 0
    vector_original = vector.copy()
    vector_ordenado = seleccion(vector,True)
    enlace = [int()]*len(vector)
    indice_enlace = 0
    inicio = 0
    for i in range(len(vector)):
        for e in range(len(vector)):
            if vector_ordenado[i] == vector_original[e]:
                if i == 0:
                    inicio = e
                else:
                    enlace[indice_enlace] = e
                    indice_enlace += 1
    enlace[-1] = -1 
    return enlace,inicio

# Metodo de ordenamiento Burbuja (no recomendable para medianas o grandes volumnes de datos), True = ASC y False = DESC
def burbuja(vector, forma):
    if forma:
        for i in range(len(vector)):
            for e in range(len(vector) - 1):
                if vector[e] > vector[e + 1]:
                    aux = vector[e]
                    vector[e] = vector[e + 1]
                    vector[e + 1] = aux
    else:
        for i in range(len(vector)):
            for e in range(len(vector) - 1):
                if vector[e] < vector[e + 1]:
                    aux = vector[e]
                    vector[e] = vector[e + 1]
                    vector[e + 1] = aux
    return vector

# Carga en memoria solo las funciones "Programado" (omite cabecera, expiradas y registros incompletos)
def cargar_funciones_programadas(ruta):
    funciones = []
    try:
        arch = open(ruta, "r")
    except FileNotFoundError:
        return funciones
    arch.readline()  # saltamos la cabecera
    linea = arch.readline()
    while linea != "":
        datos = linea.strip().split(";")
        # len >= 9 (estructura completa), ID numerico y estado Programado
        if len(datos) >= 8 and datos[0].isdecimal() and datos[7] == "Programado":
            funciones.append(datos)
        linea = arch.readline()
    arch.close()
    return funciones

# Clave de comparacion: numero entero para el ID, texto en minusculas para el nombre
def obtener_clave(registro, columna, es_numerica):
    if es_numerica:
        return int(registro[columna])
    return registro[columna].lower()

# Ordenamiento por SELECCION sobre una lista de registros, usando la columna indicada.
# ascendente=True -> menor a mayor / A-Z ; ascendente=False -> mayor a menor / Z-A
def seleccion_registros(registros, columna, es_numerica, ascendente):
    for i in range(len(registros)):
        elegido = i  # posicion del menor (o mayor) encontrado hasta ahora
        for e in range(i + 1, len(registros)):
            clave_e = obtener_clave(registros[e], columna, es_numerica)
            clave_elegido = obtener_clave(registros[elegido], columna, es_numerica)
            if ascendente and clave_e < clave_elegido:
                elegido = e
            elif not ascendente and clave_e > clave_elegido:
                elegido = e
        # intercambiamos el elegido con la posicion i
        aux = registros[i]
        registros[i] = registros[elegido]
        registros[elegido] = aux
    return registros

# Devuelve las funciones "Programado" ordenadas por ID numerico (lista vacia si no hay ninguna)
def ordenar_funciones_por_id(ascendente=True):
    funciones = cargar_funciones_programadas("data/funciones.csv")
    return seleccion_registros(funciones, 0, True, ascendente)

# Devuelve las funciones "Programado" ordenadas alfabeticamente por nombre de obra
def ordenar_funciones_por_nombre(ascendente=True):
    funciones = cargar_funciones_programadas("data/funciones.csv")
    return seleccion_registros(funciones, 1, False, ascendente)
