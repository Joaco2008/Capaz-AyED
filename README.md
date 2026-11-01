Trabajo Práctico Integrador: Sistema de Gestión - Teatro CaPaz S.A.

Información del Proyecto
Institución: Universidad Tecnológica Nacional (UTN) - Facultad Regional Villa María
Carrera: Ingeniería en Sistemas de Información
Asignatura: Algoritmos y Estructuras de Datos (AyED) - 2026
Integración: Caso de estudio en articulación con Sistemas y Procesos de Negocio (SPN)

Descripción General
Este proyecto consiste en el desarrollo de una aplicación de consola modularizada en Python que resuelve los requerimientos operativos y de información para la gestión del Teatro CaPaz S.A.
La solución está orientada a la demostración práctica de conceptos clave de la materia Algoritmos y Estructuras de Datos, incluyendo el diseño de algoritmos manuales (búsqueda y ordenamiento), uso de matrices, vectores, estructuras dinámicas lineales implementadas manualmente y recursividad.
Arquitectura del Proyecto
El sistema aplica una separación clara de responsabilidades dividiendo el software en un módulo de entrada principal (main.py), una carpeta de lógica interna (modulos/) y una carpeta de persistencia de datos (data/).

teatro_capaz/
│
├── data/                       # Archivos de persistencia (.csv)
│   ├── funciones.csv           # Registro de funciones en cartelera
│   ├── ventas.csv              # Registro persistente de ventas realizadas (RF3)
│   ├── obras.csv               # Soporte de obras teatrales y espectáculos
│   ├── salas.csv               # Soporte de configuración de salas
│   ├── socios.csv              # Soporte para validación de elegibilidad de descuentos
│   ├── ubicaciones.csv
│   ├── tipo_ubicacion.csv
├── modulos/                    # Lógica interna y algoritmos
│   ├── __init__.py
│   ├── funciones.py            # Registro, consulta y búsqueda de funciones (RF1)
│   ├── ubicaciones.py          # Gestión de matriz de plateas y palcos (RF2)
│   ├── ventas.py               # Registro de transacciones y cálculo de importes (RF3)
│   ├── reportes.py             # Generación de informes y estadísticas (RF4)
│
│
│
├── main.py                     # Menú interactivo de consola y orquestador principal
└── README.md                   # Documentación del proyecto


Mapeo de Requerimientos y Estructuras de Datos (AyED vs. SPN)

A diferencia de la especificación conceptual amplia de Sistemas y Procesos de Negocio (SPN), este prototipo académico enfoca los alcances de soporte esenciales para resolver la lógica algorítmica exigida por AyED:
1. Alcances de Soporte Seleccionados
Obras (obras.csv): Datos requeridos para la consulta por nombre parcial o total.
Salas (salas.csv): Definición de los parámetros de las salas del teatro.
Socios (socios.csv): Validación de elegibilidad para la aplicación del 30% de descuento.
Funciones y Ventas (funciones.csv, ventas.csv): Persistencia de transacciones e historial.
Ubicaciones y TipoUbicacion (ubicaciones.csv, tipo_ubicacion.csv): Listar las ubicaciones y su variacion en el precio

2. Contenidos Algoritmos y Estructuras de Datos Obligatorios
Vectores: Utilizados para la administración en memoria del conjunto de funciones y/o ventas registrando su recorrido explícito.
Matrices: Representación de ubicaciones por función (350 plateas y 250 palcos) para validar estados (disponible / vendida).
Algoritmo de Búsqueda Manual: Implementación propia de búsqueda (secuencial o binaria) para localizar funciones por su código identificador sin hacer uso de métodos integrados nativos de búsqueda.
Algoritmo de Ordenamiento Manual: Implementación propia de un algoritmo de ordenamiento (ej. Burbuja, Selección, Inserción) para clasificar las funciones por demanda o criterio de cartelera sin utilizar sort() o sorted().
Estructura Dinámica Lineal: Implementación manual con nodos de una estructura lineal (Lista Enlazada, Pila o Cola) para una función concreta dentro del sistema.
Recursividad: Función recursiva con caso base y caso recursivo explícito para la resolución de un problema operativo del prototipo.
Manejo de Cadenas de Caracteres: Procesamiento de texto case-insensitive para búsquedas parciales y totales de nombres de obras.

Funcionalidades del Sistema:
RF1. Gestión y Consulta de Funciones
RF2. Representación y Consulta de Ubicaciones
RF3. Registro de Ventas
RF4. Consultas y Reportes

Ejecución del Proyecto
Para ejecutar la aplicación localmente:
Clonar el repositorio:
git clone https://github.com/usuario/Capaz-AyED.git

Ejecutar el archivo principal:
python main.py

Integrantes del Equipo (Grupo N° 10)
Basso, Francesco Atilio
Franchetti, Benjamin Santino
González, Alejo Gael
Oga Gomez, Fernando Joaquin

Quintans Callejas, Lucio Agustín
