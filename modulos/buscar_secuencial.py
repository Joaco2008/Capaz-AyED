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
# Compara subcadenas caracter por caracter (sin distinguir mayusculas/minusculas)
# Devuelve True si "buscado" aparece dentro de "texto_completo"
def contiene_texto(texto_completo, buscado):
    texto = texto_completo.lower()
    buscado = buscado.lower()
    if len(buscado) > len(texto):
        return False
    i = 0
    while i <= len(texto) - len(buscado):
        j = 0
        # avanzamos mientras los caracteres coincidan
        while j < len(buscado) and texto[i + j] == buscado[j]:
            j += 1
        # si coincidieron todos los caracteres de lo buscado, lo encontramos
        if j == len(buscado):
            return True
        i += 1
    return False

# Busca por coincidencia parcial en el nombre de la obra (columna 1)
# Retorna una lista con todos los registros (vectores) que coinciden
def busqueda_por_nombre(texto_buscado, ruta):
    v_registros = []
    try:
        arch = open(ruta, "r")
    except FileNotFoundError:
        return v_registros
    arch.readline()  # saltamos la cabecera
    linea = arch.readline()
    while linea != "":
        registro = linea.strip().split(";")
        if len(registro) > 1 and contiene_texto(registro[1], texto_buscado):
            v_registros.append(registro)
        linea = arch.readline()
    arch.close()
    return v_registros
