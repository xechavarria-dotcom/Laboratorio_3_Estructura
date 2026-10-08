# bmas.py
# Árbol B+:
#   - Cada nodo guarda varias claves (ids) ordenadas: máximo MAX_CLAVES.
#   - Los estudiantes solo están en las HOJAS. Los nodos de arriba (internos)
#     guardan "claves guía" que dicen por cuál hijo bajar.
#   - Las hojas están enlazadas: cada una apunta a la hoja de su derecha.
#   - Cuando un nodo se pasa de MAX_CLAVES, se parte en dos y le pasa una clave
#     a su padre. Si se parte la raíz, se crea una raíz nueva encima: el árbol
#     crece hacia arriba y todas las hojas quedan siempre al mismo nivel.
#     Por eso nunca se desbalancea, sin importar el orden de los ids: buscar es O(log N).
#   insertar          -> baja hasta la hoja guardando el camino, y parte los nodos llenos.
#   buscar            -> baja por las claves guía hasta la hoja y busca ahí.
#   listar_en_orden   -> recorre las hojas de izquierda a derecha.
#   altura            -> número de niveles; sube en 1 cada vez que se parte la raíz.

MAX_CLAVES = 4        # un nodo puede tener hasta 4 claves; cuando llega a 5 se parte


class NodoBMas:
    def __init__(self, es_hoja):
        self.es_hoja = es_hoja
        self.claves = []              # ids, ordenados de menor a mayor
        self.estudiantes = []         # solo en hojas: estudiantes[i] tiene el id claves[i]
        self.hijos = []               # solo en nodos internos: siempre hay len(claves) + 1
        self.siguiente = None         # solo en hojas: la hoja de la derecha


class ArbolBMas:
    def __init__(self):
        self.raiz = NodoBMas(True)    # al principio el árbol es una sola hoja vacía
        self.niveles = 1

    def buscar(self, id_buscado):
        nodo = self.raiz
        while not nodo.es_hoja:
            # Se baja por el hijo i: el primero cuya clave guía es mayor que el id
            i = 0
            while i < len(nodo.claves) and id_buscado >= nodo.claves[i]:
                i = i + 1
            nodo = nodo.hijos[i]
        for i in range(len(nodo.claves)):
            if nodo.claves[i] == id_buscado:
                return nodo.estudiantes[i]
        return None

    def insertar(self, estudiante):
        id_nuevo = estudiante["id"]

        # 1) Bajar hasta la hoja, anotando en "camino" los nodos internos por los que se pasa
        camino = []
        nodo = self.raiz
        while not nodo.es_hoja:
            camino.append(nodo)
            i = 0
            while i < len(nodo.claves) and id_nuevo >= nodo.claves[i]:
                i = i + 1
            nodo = nodo.hijos[i]

        # 2) Meter el id y el estudiante en la hoja, en su lugar ordenado
        i = 0
        while i < len(nodo.claves) and nodo.claves[i] < id_nuevo:
            i = i + 1
        nodo.claves.insert(i, id_nuevo)
        nodo.estudiantes.insert(i, estudiante)

        # 3) Mientras el nodo tenga más de MAX_CLAVES, se parte y se sube al padre
        while len(nodo.claves) > MAX_CLAVES:
            clave_que_sube, nodo_derecho = self.partir(nodo)
            if len(camino) == 0:
                # Se partió la raíz: se crea una raíz nueva encima de las dos mitades
                nueva_raiz = NodoBMas(False)
                nueva_raiz.claves = [clave_que_sube]
                nueva_raiz.hijos = [nodo, nodo_derecho]
                self.raiz = nueva_raiz
                self.niveles = self.niveles + 1
                return
            padre = camino.pop()              # el último nodo del camino es el padre
            posicion = padre.hijos.index(nodo)
            padre.claves.insert(posicion, clave_que_sube)
            padre.hijos.insert(posicion + 1, nodo_derecho)
            nodo = padre                      # ahora se revisa si el padre se llenó

    def partir(self, nodo):
        # Parte un nodo en dos. La mitad izquierda se queda en "nodo" y la derecha
        # va a un nodo nuevo. Devuelve la clave que sube al padre y el nodo nuevo.
        mitad = len(nodo.claves) // 2
        derecho = NodoBMas(nodo.es_hoja)
        if nodo.es_hoja:
            derecho.claves = nodo.claves[mitad:]
            derecho.estudiantes = nodo.estudiantes[mitad:]
            nodo.claves = nodo.claves[:mitad]
            nodo.estudiantes = nodo.estudiantes[:mitad]
            derecho.siguiente = nodo.siguiente    # las hojas siguen enlazadas
            nodo.siguiente = derecho
            return derecho.claves[0], derecho     # en una hoja, la clave guía es una COPIA
        clave_que_sube = nodo.claves[mitad]       # en un nodo interno, la del medio SUBE
        derecho.claves = nodo.claves[mitad + 1:]
        derecho.hijos = nodo.hijos[mitad + 1:]
        nodo.claves = nodo.claves[:mitad]
        nodo.hijos = nodo.hijos[:mitad + 1]
        return clave_que_sube, derecho

    def listar_en_orden(self):
        # Bajar a la hoja de más a la izquierda y seguir el enlace a la siguiente
        nodo = self.raiz
        while not nodo.es_hoja:
            nodo = nodo.hijos[0]
        resultado = []
        while nodo is not None:
            for estudiante in nodo.estudiantes:
                resultado.append(estudiante)
            nodo = nodo.siguiente
        return resultado

    def altura(self):
        return self.niveles
