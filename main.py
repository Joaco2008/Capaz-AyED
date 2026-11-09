# Codigo del TPI de la asignatura Algoritmos y Estructuras de datos
# Integrantes: Basso Francesco, Franchetti Benjamin, Gonzalez Gael y Oga Gomez Fernando Joaquin
import modulos.funciones as fun
import modulos.ubicaciones as ubi
import modulos.ventas as vts
print("¡¡Bienvenido al Teatro Capaz!!")
print("Porfavor seleccione una de las opciones:")
print("""1 - Gestionar Funciones\n2 - Ubicaciones\n3 - Realizar Venta\n4 - Gestionar Informes\n0 - Salir""")
op = int(input())
while op != 0:
    if op == 1:
        print("Gestionar funciones")
        print(fun.menu_funciones())
    elif op == 2:
        print("Ubicaciones")
        id_funcion = input("Ingrese el numero de la funcion: ") 
        print(ubi.mostrarubicaciones(id_funcion))
    elif op == 3:
        vts.gestionar_venta_entradas()
    else:
        print("Opcion no valida")
    print("Porfavor seleccione una de las opciones:")
    print("""1 - Gestionar Funciones\n2 - Ubicaciones\n3 - Realizar Venta\n4 - Gestionar Informes\n0 - Salir""")
    op = int(input())