# graficas.py
# Lee datos/resultados.csv y hace UNA imagen con 4 gráficas (2 x 2):
#   Arriba:  ids aleatorios -> escala normal | escala logarítmica
#   Abajo:   ids ordenados  -> escala normal | escala logarítmica
# Así se puede explicar la diferencia entre la escala normal (las curvas de abajo
# no se ven) y la logarítmica (ya se ven las tres), que fue lo que pidió el profe.
# También guarda datos/tablas.md con las tablas para el informe.
# No mide nada: solo lee el CSV, así que se puede correr las veces que se quiera.
#
# Uso:  python graficas.py

import csv
import os

import matplotlib
matplotlib.use("Agg")                 # guarda la imagen sin abrir ventanas
import matplotlib.pyplot as plt

ARCHIVO = "datos/resultados.csv"
ESTRUCTURAS = ["Lista", "ABB", "B+"]
# Colores, marcadores y estilos de línea propios (distintos a los del compañero).
# Cada estructura con color + marcador + tipo de línea distintos, para que el ABB y el B+
# se distingan aunque en aleatorios den tiempos casi iguales (los dos son O(log N)).
COLOR = {"Lista": "#CC79A7", "ABB": "#E69F00", "B+": "#0072B2"}
MARCA = {"Lista": "o", "ABB": "s", "B+": "^"}
LINEA = {"Lista": "-", "ABB": "-", "B+": "-"}   # todas líneas llenas

if not os.path.exists(ARCHIVO):
    print("Falta", ARCHIVO, "- corre primero: python experimento.py")
    exit()

filas = list(csv.DictReader(open(ARCHIVO, encoding="utf-8")))
datos = {}            # (orden, estructura) -> lista de (N, promedio_us, desviacion_us)
enes = set()
for f in filas:
    datos.setdefault((f["orden"], f["estructura"]), []).append((int(f["N"]), float(f["una_busqueda_us"]), float(f["desv_us"])))
    enes.add(int(f["N"]))
for clave in datos:
    datos[clave].sort()
VALORES_N = sorted(enes)


def formato(x, decimales):
    """Número a la colombiana: 1.234,56"""
    return format(x, ",." + str(decimales) + "f").replace(",", "X").replace(".", ",").replace("X", ".")


def etiqueta(nombre, orden):
    if nombre == "Lista":
        return "Lista  —  O(N)"
    if nombre == "B+":
        return "B+  —  O(log N)"
    return "ABB  —  O(log N)" if orden == "aleatorio" else "ABB  —  O(N) (se degrada)"


def dibujar(eje, orden, titulo, en_log):
    for nombre in ESTRUCTURAS:
        if (orden, nombre) not in datos:
            continue
        puntos = datos[(orden, nombre)]
        x = [p[0] for p in puntos]
        y = [p[1] for p in puntos]
        error = [p[2] for p in puntos]
        # rayitas verticales = la desviación estándar (± 1)
        if en_log:
            # en escala log el extremo de abajo de la rayita no puede ser 0 ni negativo
            abajo = [min(e, v * 0.9) for e, v in zip(error, y)]
            barras = [abajo, error]
        else:
            barras = error
        eje.errorbar(x, y, yerr=barras, color=COLOR[nombre], marker=MARCA[nombre], linestyle=LINEA[nombre],
                     linewidth=2, markersize=8, capsize=4, label=etiqueta(nombre, orden))
    if en_log:
        eje.set_yscale("log")
        eje.set_ylabel("Tiempo de una búsqueda (µs, escala logarítmica)")
    else:
        eje.set_ylim(bottom=0)
        eje.set_ylabel("Tiempo de una búsqueda (µs)")
    eje.set_title(titulo, fontweight="bold")
    eje.set_xlabel("N = número de estudiantes")
    eje.grid(alpha=0.3, which="both")
    eje.legend(loc="upper left")


os.makedirs("figuras", exist_ok=True)
fig, ejes = plt.subplots(2, 2, figsize=(14, 10.5))
dibujar(ejes[0][0], "aleatorio", "Ids aleatorios — escala normal", en_log=False)
dibujar(ejes[0][1], "aleatorio", "Ids aleatorios — escala logarítmica", en_log=True)
dibujar(ejes[1][0], "ordenado", "Ids ordenados — escala normal", en_log=False)
dibujar(ejes[1][1], "ordenado", "Ids ordenados — escala logarítmica", en_log=True)
fig.suptitle("Tiempo de buscar un estudiante según N (las 3 estructuras) — promedio de 10 repeticiones; barras: ± 1 desviación estándar.\n"
             "Arriba: ids aleatorios.  Abajo: ids ordenados.  Izquierda: escala normal (las curvas de abajo no se ven).  "
             "Derecha: escala Y logarítmica (ya se ven las tres).", fontsize=11)
fig.tight_layout()
fig.savefig("figuras/graficas.png", dpi=150)
plt.close(fig)

# --------- tablas para el informe
def buscar_valor(orden, nombre, N):
    for p in datos.get((orden, nombre), []):
        if p[0] == N:
            return p[1], p[2]     # (promedio, desviación)
    return None


def formato_tiempo(x):
    """Redondea según el tamaño: los grandes sin decimales, los chicos con 2."""
    if x >= 100:
        return formato(x, 0)
    if x >= 10:
        return formato(x, 1)
    return formato(x, 2)


def formato_veces(v):
    return (formato(round(v), 0) if v >= 10 else formato(v, 1)) + "×"


def tabla_alineada(encabezados, filas):
    """Tabla markdown con las columnas ALINEADAS (rellena con espacios para que queden parejas)."""
    ancho = []
    for i in range(len(encabezados)):
        w = len(encabezados[i])
        for f in filas:
            w = max(w, len(f[i]))
        ancho.append(w)
    out = ["| " + " | ".join(encabezados[i].rjust(ancho[i]) for i in range(len(encabezados))) + " |"]
    out.append("|" + "|".join("-" * (ancho[i] + 1) + ":" for i in range(len(encabezados))) + "|")
    for f in filas:
        out.append("| " + " | ".join(f[i].rjust(ancho[i]) for i in range(len(encabezados))) + " |")
    return out


# (orden, título, texto de ayuda, estructura lenta para comparar, encabezado, conclusión)
CONFIG = [
    ("aleatorio", "ALEATORIOS",
     "Lista es O(N); el ABB y el B+ son O(log N). La última columna: cuántas veces más lenta es la Lista que el B+.",
     "Lista", "Lista/B+",
     "La Lista se vuelve miles de veces más lenta cuando N crece; los árboles casi no cambian."),
    ("ordenado", "ORDENADOS",
     "Aquí el ABB se degrada a O(N). La última columna: cuántas veces más lento es el ABB que el B+.",
     "ABB", "ABB/B+",
     "Con ids ordenados el ABB se vuelve tan lento como la Lista (o más); solo el B+ se mantiene rápido."),
]
lineas = ["# Tablas de resultados", ""]
for orden, titulo, ayuda, nombre_lento, encabezado_veces, conclusion in CONFIG:
    lineas.append("## Tiempo de una búsqueda con ids " + titulo + " (en µs — menos es más rápido)")
    lineas.append("")
    lineas.append("Promedio ± desviación estándar de 10 repeticiones. " + ayuda)
    lineas.append("")
    encabezados = ["N", "Lista", "ABB", "B+", encabezado_veces]
    filas = []
    for N in sorted({p[0] for nombre in ESTRUCTURAS for p in datos.get((orden, nombre), [])}):
        fila = [formato(N, 0)]
        for nombre in ESTRUCTURAS:
            v = buscar_valor(orden, nombre, N)
            fila.append(formato_tiempo(v[0]) + " ± " + formato_tiempo(v[1]) if v else "—")
        lento = buscar_valor(orden, nombre_lento, N)
        bmas = buscar_valor(orden, "B+", N)
        fila.append(formato_veces(lento[0] / bmas[0]) if (lento and bmas and bmas[0] > 0) else "—")
        filas.append(fila)
    lineas += tabla_alineada(encabezados, filas)
    lineas.append("")
    lineas.append("*" + conclusion + "*")
    lineas.append("")
open("datos/tablas.md", "w", encoding="utf-8").write("\n".join(lineas) + "\n")

print("Listo:")
print("  figuras/graficas.png   (una imagen con las 4 gráficas)")
print("  datos/tablas.md")