# experimento.py
# Mide cuánto tarda BUSCAR un estudiante en la Lista, el ABB y el B+, según cuántos
# estudiantes hay (N), con ids aleatorios y con ids ordenados. Repite 10 veces y
# guarda SOLO EL RESUMEN (promedio ± desviación de cada caso) en datos/resultados.csv.
# Son 30 filas, una por caso. Después, graficas.py hace las dos gráficas con ese archivo.
#
# Uso:  python experimento.py           corrida completa (unos 25-30 minutos)
#       python experimento.py rapido    una sola repetición de prueba (unos 3 minutos)

import csv
import gc
import os
import random
import statistics
import sys
import time

from lista import Lista
from abb import ArbolBinario
from bmas import ArbolBMas

REPETICIONES = 10          # el laboratorio pide al menos 10
FACTOR = 1                 # si la prueba rápida lo pide, ponlo en 2 (duplica las búsquedas)

# Con ids ALEATORIOS la búsqueda es rápida, así que se puede llegar más lejos (más valores de N).
# Con ids ORDENADOS se usan pocos, porque construir el ABB ordenado crece como N² y es lentísimo.
VALORES_N_ALEATORIO = [1000, 5000, 10000, 20000, 35000, 50000, 75000, 100000]
VALORES_N_ORDENADO = [1000, 5000, 10000, 20000]
ORDENES = ["aleatorio", "ordenado"]
ESTRUCTURAS = ["Lista", "ABB", "B+"]

# Cuántas BÚSQUEDAS hace cada medición, para que dure más de 1 segundo (lo pide el profe).
# Buscar en la Lista (y en el ABB con ids ordenados) es LENTO -> pocas búsquedas (depende de N).
# Buscar en el ABB/B+ con ids aleatorios (y el B+ ordenado) es RÁPIDO -> muchas búsquedas.
BUSQUEDAS_LENTO = {1000: 200000, 5000: 40000, 10000: 20000, 20000: 10000,
                   35000: 4000, 50000: 2500, 75000: 1500, 100000: 1200}
BUSQUEDAS_RAPIDO = 2000000

NOMBRES = ["Laura", "Andrés", "Camila", "Julián", "Valeria", "Felipe", "Natalia", "Sebastián"]


def crear_estudiantes(N, orden):
    """N estudiantes con ids 1..N. 'aleatorio' los mezcla; 'ordenado' los deja 1, 2, 3..."""
    ids = list(range(1, N + 1))
    if orden == "aleatorio":
        random.shuffle(ids)
    estudiantes = []
    for i in ids:
        estudiantes.append({"id": i, "nombre": random.choice(NOMBRES),
                            "edad": random.randint(17, 35), "promedio": round(random.uniform(0, 5), 1)})
    return estudiantes


def crear_estructura(nombre):
    if nombre == "Lista":
        return Lista()
    if nombre == "ABB":
        return ArbolBinario()
    return ArbolBMas()


def cuantas_busquedas(orden, nombre, N):
    lento = (nombre == "Lista") or (nombre == "ABB" and orden == "ordenado")
    return (BUSQUEDAS_LENTO[N] if lento else BUSQUEDAS_RAPIDO) * FACTOR


def medir_construccion(estructura, estudiantes):
    gc.collect()
    gc.disable()                      # se apaga el recolector de basura mientras se mide
    inicio = time.perf_counter()
    for e in estudiantes:
        estructura.insertar(e)
    segundos = time.perf_counter() - inicio
    gc.enable()
    return segundos


def medir_busquedas(estructura, ids_a_buscar):
    gc.collect()
    gc.disable()
    inicio = time.perf_counter()
    for b in ids_a_buscar:
        estructura.buscar(b)
    segundos = time.perf_counter() - inicio
    gc.enable()
    return segundos


rapido = len(sys.argv) > 1 and sys.argv[1].startswith("rapid")
if rapido:
    REPETICIONES = 1
    RUTA = "datos/prueba_rapida.csv"
else:
    RUTA = "datos/resultados.csv"

busqueda = {}        # (orden, estructura, N) -> microsegundos de una búsqueda, en cada repetición
construir = {}       # (orden, estructura, N) -> segundos de construcción, en cada repetición
altura_de = {}       # (orden, estructura, N) -> altura del árbol
mas_corta = 1000000.0
inicio_total = time.perf_counter()

for rep in range(1, REPETICIONES + 1):
    random.seed(rep)                  # semilla = número de repetición: los datos se repiten igualitos
    for orden in ORDENES:
        valores_n = VALORES_N_ALEATORIO if orden == "aleatorio" else VALORES_N_ORDENADO
        for N in valores_n:
            # Los ids a buscar se escogen una vez por cada caso: las 3 estructuras buscan los mismos.
            ids_a_buscar = random.choices(range(1, N + 1), k=BUSQUEDAS_RAPIDO * FACTOR)
            estudiantes = crear_estudiantes(N, orden)
            for nombre in ESTRUCTURAS:
                M = cuantas_busquedas(orden, nombre, N)
                estructura = crear_estructura(nombre)
                t_construir = medir_construccion(estructura, estudiantes)
                t_buscar = medir_busquedas(estructura, ids_a_buscar[:M])
                una_us = t_buscar / M * 1000000
                clave = (orden, nombre, N)
                busqueda.setdefault(clave, []).append(una_us)
                construir.setdefault(clave, []).append(t_construir)
                if nombre != "Lista":
                    altura_de[clave] = estructura.altura()
                mas_corta = min(mas_corta, t_buscar)
                print(f"rep {rep:2} | {orden:9} | N = {N:6} | {nombre:5} | M = {M:8} | "
                      f"buscar: {t_buscar:5.2f} s | una búsqueda: {una_us:9.2f} µs")
                if t_buscar < 1:
                    print("      ¡Ojo! esta medición duró menos de 1 segundo (pon FACTOR = 2)")
    print(f"--- Repetición {rep} de {REPETICIONES} lista ({(time.perf_counter() - inicio_total) / 60:.1f} min) ---\n")

# Se guarda el RESUMEN: una fila por caso, con el promedio y la desviación de las repeticiones.
os.makedirs("datos", exist_ok=True)
archivo = open(RUTA, "w", newline="", encoding="utf-8")
escritor = csv.writer(archivo)
escritor.writerow(["orden", "N", "estructura", "M", "una_busqueda_us", "desv_us", "construir_s", "altura"])
for orden in ORDENES:
    valores_n = VALORES_N_ALEATORIO if orden == "aleatorio" else VALORES_N_ORDENADO
    for N in valores_n:
        for nombre in ESTRUCTURAS:
            clave = (orden, nombre, N)
            if clave not in busqueda:
                continue
            valores = busqueda[clave]
            media = statistics.mean(valores)
            desviacion = statistics.stdev(valores) if len(valores) > 1 else 0
            media_construir = statistics.mean(construir[clave])
            escritor.writerow([orden, N, nombre, cuantas_busquedas(orden, nombre, N),
                               round(media, 4), round(desviacion, 4), round(media_construir, 6),
                               altura_de.get(clave, "")])
archivo.close()

print("Datos guardados en", RUTA, "(una fila por caso)")
print(f"\nLa medición más corta duró {mas_corta:.2f} s.")
if mas_corta < 1:
    print("¡Ojo! Hubo mediciones de menos de 1 segundo: pon FACTOR = 2 y vuelve a correr.")
elif rapido and mas_corta < 1.2:
    print("Pasa de 1 segundo por poco: mejor pon FACTOR = 2 antes de la corrida completa.")
else:
    print("Bien: todas las mediciones pasaron de 1 segundo.")
