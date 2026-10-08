# abb.py
# Árbol binario de búsqueda (ABB): en cada nodo, los ids menores van a la
# izquierda y los mayores a la derecha.
#   insertar          -> baja comparando hasta un espacio vacío.
#   buscar            -> baja comparando: un paso por cada nivel que recorre.
#                        Con ids en orden aleatorio, en promedio es O(log N).
#                        Con ids ya ordenados el árbol queda como una sola rama
#                        de N niveles y buscar es O(N).
#   listar_en_orden   -> recorrido inorden (izquierda, nodo, derecha).
#   altura            -> número de niveles; se va calculando al insertar.
# Todo se hace con ciclos while y no con recursión: con ids ordenados el árbol
# tiene miles de niveles y la recursión pasaría el límite de Python.


class NodoABB:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izquierdo = None         # ids menores
        self.derecho = None           # ids mayores


class ArbolBinario:
    def __init__(self):
        self.raiz = None
        self.niveles = 0

    def insertar(self, estudiante):
        nuevo = NodoABB(estudiante)
        if self.raiz is None:
            self.raiz = nuevo
            self.niveles = 1
            return
        actual = self.raiz
        nivel = 1                     # nivel del nodo actual (la raíz está en el nivel 1)
        while True:
            nivel = nivel + 1         # el hijo de "actual" queda un nivel más abajo
            if estudiante["id"] < actual.estudiante["id"]:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    break
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    break
                actual = actual.derecho
        if nivel > self.niveles:      # el nuevo quedó más abajo que todos: la altura crece
            self.niveles = nivel

    def buscar(self, id_buscado):
        actual = self.raiz
        while actual is not None:
            if id_buscado == actual.estudiante["id"]:
                return actual.estudiante
            if id_buscado < actual.estudiante["id"]:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None

    def listar_en_orden(self):
        # Inorden con una pila: se baja todo a la izquierda guardando los nodos;
        # luego se saca uno, se anota y se sigue por su derecha.
        resultado = []
        pila = []
        actual = self.raiz
        while actual is not None or len(pila) > 0:
            while actual is not None:
                pila.append(actual)
                actual = actual.izquierdo
            actual = pila.pop()
            resultado.append(actual.estudiante)
            actual = actual.derecho
        return resultado

    def altura(self):
        return self.niveles
