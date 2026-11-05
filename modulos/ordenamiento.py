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
lista = [1,123,1241,4512,5125,23523,11111,1,3,6,5,8,6,2]
print(burbuja(lista,False))