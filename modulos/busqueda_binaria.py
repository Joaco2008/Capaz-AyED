def busqueda_binaria_recursiva(registros, id_buscado, bajo, alto):
    if bajo > alto:
        return None
    
    medio = (bajo + alto) // 2
    
    if registros[medio].id == id_buscado:
        return registros[medio]
    elif registros[medio].id > id_buscado:
        return busqueda_binaria_recursiva(registros, id_buscado, bajo, medio - 1)
    else:
        return busqueda_binaria_recursiva(registros, id_buscado, medio + 1, alto)