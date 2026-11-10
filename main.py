# Codigo del TPI de la asignatura Algoritmos y Estructuras de datos
# Integrantes: Basso Francesco, Franchetti Benjamin, Gonzalez Gael y Oga Gomez Fernando Joaquin
import modulos.funciones as fun
import modulos.ventas as vts
import modulos.reportes as rep

print("¡¡Bienvenido al Teatro Capaz!!")
print("Porfavor seleccione una de las opciones:")
print("""1 - Gestionar Funciones\n2 - Realizar Venta\n3 - Gestionar Informes\n0 - Salir""")
op = int(input())
while op != 0:
    if op == 1:
        print("Gestionar funciones")
        print(fun.menu_funciones())
    elif op == 2:
        vts.gestionar_venta_entradas()
    elif op == 3:
        rep.menu_reportes()
    else:
        print("Opcion no valida")
    print("Porfavor seleccione una de las opciones:")
    print("""1 - Gestionar Funciones\n2 - Realizar Venta\n3 - Gestionar Informes\n0 - Salir""")
    op = int(input())