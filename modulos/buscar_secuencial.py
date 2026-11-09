# Esta funcion simplemente le cargas la id del determinando registro y la ruta del archivo
# Retorna un vector con los datos
def busqueda_por_id(id, ruta):
    encontrado = False
    arch = open(ruta, "r")
    registro = arch.readline().split(";")
    # Recorre todos los registros mientras no haya llegado al fin o no haya sido encontrado el registro
    while registro != [''] and not(encontrado):
        # Si es encontrado el registro
        if registro[0] == id:
            encontrado = True
            arch.close()
            return registro
        # Sino es encontrado, busca otro registro
        registro = arch.readline().split(";")
    # Si recorrio todo el archivo y no lo encontro
    if not(encontrado):
        arch.close()
        return "No existe este dato"
    
# Buscar por un grupo de vectores
def busqueda_por_grupo_vectores(parametro, ruta,indice_registro):
    arch = open(ruta, "r")
    registro = arch.readline().split(";")
    v_registros = []
    # Recorre todos los registros mientras no haya llegado al fin o no haya sido encontrado el registro
    while registro != ['']:
        # Si es encontrado el registro
        if registro[indice_registro] == parametro:
            v_registros.append(registro)
        # Busca mas registros
        registro = arch.readline().split(";")
    # Si recorrio todo el archivo y no lo encontro
    arch.close()
    return v_registros
#funcion que verifica si un texto contiene otro texto, sin importar mayusculas o minusculas
def contiene_texto(texto_completo, buscado):
    texto = texto_completo.lower()
    sub = buscado.lower()
    
    len_texto = len(texto)
    len_sub = len(sub)
    
    # Si lo que buscamos es más largo que el texto original, no puede estar contenido
    if len_sub > len_texto or len_sub == 0:
        return False

    # Recorremos el texto principal posición por posición
    for i in range(len_texto - len_sub + 1):
        coincide = True
        # Comparamos letra por letra con la subcadena buscada
        for j in range(len_sub):
            if texto[i + j] != sub[j]:
                coincide = False
                break
        
        # Si coincidieron todas las letras consecutivas, la encontramos
        if coincide:
            return True
            
    return False
#funcion para buscar por nombre de obra
def buscar_funciones_por_nombre(texto_buscado):
    coincidencias = []
    #leemos el archivo de funciones y buscamos las coincidencias
    try:
        with open("data/funciones.csv", "r") as arch:
            for linea in arch:
                registro = linea.strip().split(";")
                if len(registro) >= 8:
                    nombre_obra = registro[1]
                    
                    # Llamamos a la función contiene_texto para verificar si el nombre de la obra contiene el texto buscado
                    if contiene_texto(nombre_obra, texto_buscado):
                        coincidencias.append(registro)
    except FileNotFoundError:
        print("El archivo 'data/funciones.csv' no existe.")
        return []