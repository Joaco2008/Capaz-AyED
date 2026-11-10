def busqueda_binaria_recursiva(registros, id_buscado, bajo, alto):

    if bajo > alto:
        return "No existe este dato"
    
    medio = (bajo + alto) // 2
    
    if int(registros[medio][0]) == id_buscado:
        return registros[medio].split(";")
    elif int(registros[medio][0]) > id_buscado:
        return busqueda_binaria_recursiva(registros, id_buscado, bajo, medio - 1)
    else:
        return busqueda_binaria_recursiva(registros, id_buscado, medio + 1, alto)