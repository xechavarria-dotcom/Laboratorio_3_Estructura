# pruebas.py
# Revisa que las tres estructuras hagan lo que pide el laboratorio, ANTES de medir:
#   1) buscar encuentra a cada estudiante (y devuelve justo ese estudiante)
#   2) buscar un id que no existe devuelve None
#   3) listar_en_orden devuelve los ids 1, 2, 3, ..., N
#   4) se puede insertar un estudiante nuevo después y encontrarlo
#   5) la altura del ABB es correcta, y el B+ cumple sus reglas
# Se prueba con ids aleatorios, ordenados (1, 2, 3...) y descendentes (N, ..., 2, 1).
# Si algo falla, "assert" detiene el programa y muestra la línea del error.
#
# Uso:  python pruebas.py      (tarda unos segundos)

import random

from lista import Lista
from abb import ArbolBinario
from bmas import ArbolBMas, MAX_CLAVES


def crear_estudiantes(ids):
    estudiantes = []
    for i in ids:
        estudiantes.append({"id": i, "nombre": "Prueba", "edad": 20, "promedio": 4.0})
    return estudiantes


def altura_real_abb(arbol):
    # Cuenta los niveles del ABB recorriéndolo nivel por nivel
    if arbol.raiz is None:
        return 0
    niveles = 0
    nivel_actual = [arbol.raiz]
    while len(nivel_actual) > 0:
        niveles = niveles + 1
        siguiente_nivel = []
        for nodo in nivel_actual:
            if nodo.izquierdo is not None:
                siguiente_nivel.append(nodo.izquierdo)
            if nodo.derecho is not None:
                siguiente_nivel.append(nodo.derecho)
        nivel_actual = siguiente_nivel
    return niveles


def revisar_reglas_bmas(arbol):
    # Ningún nodo pasa de MAX_CLAVES, los internos tienen un hijo más que claves,
    # y todas las hojas están en el mismo nivel, que es arbol.niveles
    pendientes = [[arbol.raiz, 1]]
    while len(pendientes) > 0:
        nodo, nivel = pendientes.pop()
        assert len(nodo.claves) <= MAX_CLAVES
        if nodo.es_hoja:
            assert nivel == arbol.niveles
        else:
            assert len(nodo.hijos) == len(nodo.claves) + 1
            for hijo in nodo.hijos:
                pendientes.append([hijo, nivel + 1])


random.seed(2026)
for N in [0, 1, 2, 3, 10, 100, 1000, 5000]:
    for orden in ["aleatorio", "ordenado", "descendente"]:
        ids = list(range(1, N + 1))
        if orden == "aleatorio":
            random.shuffle(ids)
        if orden == "descendente":
            ids.reverse()
        estudiantes = crear_estudiantes(ids)

        for nombre in ["Lista", "ABB", "B+"]:
            if nombre == "Lista":
                estructura = Lista()
            elif nombre == "ABB":
                estructura = ArbolBinario()
            else:
                estructura = ArbolBMas()
            for estudiante in estudiantes:
                estructura.insertar(estudiante)

            # 1) encuentra a cada estudiante, y es justo ese estudiante
            for estudiante in estudiantes:
                assert estructura.buscar(estudiante["id"]) is estudiante
            # 2) un id que no existe devuelve None
            assert estructura.buscar(0) is None
            assert estructura.buscar(N + 1) is None
            # 3) listar en orden da 1, 2, 3, ..., N
            listado = estructura.listar_en_orden()
            assert len(listado) == N
            for posicion in range(N):
                assert listado[posicion]["id"] == posicion + 1
            # 5) altura del ABB y reglas del B+
            if nombre == "ABB":
                assert estructura.altura() == altura_real_abb(estructura)
                if orden != "aleatorio":
                    assert estructura.altura() == N     # una sola rama de N niveles
            if nombre == "B+":
                revisar_reglas_bmas(estructura)
            altura = "" if nombre == "Lista" else estructura.altura()
            # 4) insertar uno nuevo después y encontrarlo
            nuevo = {"id": N + 1, "nombre": "Nuevo", "edad": 18, "promedio": 3.5}
            estructura.insertar(nuevo)
            assert estructura.buscar(N + 1) is nuevo
            assert estructura.listar_en_orden()[-1] is nuevo

            print(f"OK  {nombre:5}  N = {N:4}  {orden:11}  altura = {altura}")

print("\nTodas las pruebas pasaron.")
