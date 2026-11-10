# Modulo de validaciones del sistema de funciones del Teatro Capaz.
# Regla de la catedra: los archivos CSV se leen con while + readline() y se saltea la cabecera.
from datetime import datetime

RUTA_FUNCIONES = "data/funciones.csv"
RUTA_SALAS = "data/salas.csv"

# ---------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------
# Lee un menu numerico y no deja avanzar hasta que el usuario ingrese un numero valido
def leer_opcion(mensaje, minimo, maximo):
    valida = False
    while not valida:
        texto = input(mensaje).strip()
        if texto.isdecimal() and minimo <= int(texto) <= maximo:
            valida = True
        else:
            print(f"Opcion invalida. Ingrese un numero entre {minimo} y {maximo}.")
    return int(texto)

# Verifica que el formato sea exactamente HH:MM y que sea una hora real (00:00 a 23:59)
def formato_hora_valido(hora):
    if len(hora) != 5 or hora[2] != ":":
        return False
    if not (hora[0:2].isdecimal() and hora[3:5].isdecimal()):
        return False
    return int(hora[0:2]) < 24 and int(hora[3:5]) < 60

# Convierte "HH:MM" a minutos desde las 00:00 (sirve para comparar horarios con numeros)
def hora_a_minutos(hora):
    return int(hora[0:2]) * 60 + int(hora[3:5])

# Verifica que la fecha tenga formato DD/MM/AAAA y que sea una fecha real (ej: rechaza 31/02/2026)
def validar_fecha(fecha):
    if len(fecha) != 10:
        print("La fecha debe tener el formato DD/MM/AAAA.")
        return False
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        print("La fecha ingresada no es valida (formato DD/MM/AAAA).")
        return False
    return True

# Arma un objeto datetime a partir de fecha y hora del CSV. Si los datos estan mal devuelve None
def armar_fecha_hora(fecha, hora):
    try:
        return datetime.strptime(fecha + " " + hora, "%d/%m/%Y %H:%M")
    except ValueError:
        return None

# El nombre de la obra no puede estar vacio ni contener ";" (romperia el CSV)
def validar_nombre(nombre):
    if nombre == "":
        print("El nombre de la obra no puede estar vacio.")
        return False
    if ";" in nombre:
        print("El nombre no puede contener el caracter ';'.")
        return False
    return True

# El precio debe ser un numero mayor a 0
def validar_precio(precio):
    try:
        valor = float(precio)
    except ValueError:
        print("El precio debe ser un numero.")
        return False
    if valor > 0 and valor < 1000000000:
        return True
    print("El precio debe ser mayor a 0.")
    return False

# ---------------------------------------------------------------
# Validaciones pedidas por la catedra
# ---------------------------------------------------------------
# Verifica que la sala exista en data/salas.csv (el ID esta en la columna 0)
def validar_sala_existente(id_sala):
    try:
        arch = open(RUTA_SALAS, "r")
    except FileNotFoundError:
        print("No se encontro el archivo de salas.")
        return False
    arch.readline()  # saltamos la cabecera
    linea = arch.readline()
    encontrada = False
    while linea != "" and not encontrada:
        datos = linea.strip().split(";")
        if datos[0] == id_sala:
            encontrada = True
        linea = arch.readline()
    arch.close()
    if not encontrada:
        print("La sala ingresada no existe.")
        return False
    return True

# Verifica formato HH:MM y que la hora de inicio sea menor a la de fin
def validar_horarios(hora_inicio, hora_fin):
    if not formato_hora_valido(hora_inicio) or not formato_hora_valido(hora_fin):
        print("Las horas deben tener el formato HH:MM (ej: 20:30).")
        return False
    if hora_a_minutos(hora_inicio) >= hora_a_minutos(hora_fin):
        print("La hora de inicio debe ser menor a la hora de fin.")
        return False
    return True

# Devuelve True si NO hay conflicto (la funcion se puede cargar) y False si se superpone.
# Solo se comparan funciones de la misma sala, misma fecha y que no esten "Expirado".
# Dos funciones que se tocan en el borde (una termina 20:00 y otra empieza 20:00) NO se superponen.
def validar_superposicion_horario(id_sala, fecha, hora_inicio, hora_fin):
    try:
        arch = open(RUTA_FUNCIONES, "r")
    except FileNotFoundError:
        return True  # sin archivo no hay funciones con las que chocar
    nuevo_inicio = hora_a_minutos(hora_inicio)
    nuevo_fin = hora_a_minutos(hora_fin)
    arch.readline()  # saltamos la cabecera
    linea = arch.readline()
    hay_conflicto = False
    while linea != "" and not hay_conflicto:
        datos = linea.strip().split(";")
        if len(datos) >= 9 and datos[8] != "Expirado":
            if datos[5] == id_sala and datos[4] == fecha:
                if formato_hora_valido(datos[2]) and formato_hora_valido(datos[3]):
                    ini = hora_a_minutos(datos[2])
                    fin = hora_a_minutos(datos[3])
                    if nuevo_inicio < fin and nuevo_fin > ini:
                        hay_conflicto = True
        linea = arch.readline()
    arch.close()
    if hay_conflicto:
        print("Ya existe una funcion en esa sala, fecha y horario.")
        return False
    return True

# Funcion integradora: ejecuta todas las validaciones antes de guardar
def es_funcion_valida(id_sala, fecha, hora_inicio, hora_fin):
    if not validar_sala_existente(id_sala):
        return False
    if not validar_horarios(hora_inicio, hora_fin):
        return False
    if not validar_fecha(fecha):
        return False
    # no tiene sentido cargar una funcion que ya termino
    fin = armar_fecha_hora(fecha, hora_fin)
    if fin is None or fin < datetime.now():
        print("No se puede cargar una funcion que ya finalizo.")
        return False
    if not validar_superposicion_horario(id_sala, fecha, hora_inicio, hora_fin):
        return False
    return True

# Pasa a "Expirado" las funciones "Programado" cuya fecha y hora de fin ya pasaron.
# Lee el archivo completo con while, modifica en memoria y reescribe solo si hubo cambios.
# Devuelve la cantidad de funciones que expiraron.
def deshabilitar_funciones_pasadas():
    try:
        arch = open(RUTA_FUNCIONES, "r")
    except FileNotFoundError:
        return 0
    lineas = []
    linea = arch.readline()
    while linea != "":
        lineas.append(linea)
        linea = arch.readline()
    arch.close()

    ahora = datetime.now()
    cambios = 0
    i = 1  # empezamos en 1 para no tocar la cabecera
    while i < len(lineas):
        datos = lineas[i].strip().split(";")
        if len(datos) >= 9 and datos[8] == "Programado":
            fin = armar_fecha_hora(datos[4], datos[3])
            if fin is not None and fin < ahora:
                datos[8] = "Expirado"
                lineas[i] = ";".join(datos) + "\n"
                cambios += 1
        i += 1

    if cambios > 0:
        arch = open(RUTA_FUNCIONES, "w")
        j = 0
        while j < len(lineas):
            arch.write(lineas[j])
            j += 1
        arch.close()
    return cambios
