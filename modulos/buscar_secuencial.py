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