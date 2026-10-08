# lista.py
# Lista: guarda los estudiantes en una lista normal de Python (un arreglo).
#   insertar          -> agrega al final de la lista. Es rápido: O(1).
#   buscar            -> recorre la lista de uno en uno desde el principio. Es O(N).
#   listar_en_orden   -> hace una copia ordenada por id.
# Cada estudiante es un diccionario: {"id", "nombre", "edad", "promedio"}.
#
# El profe dijo que la Lista se puede hacer con la lista de Python, así que
# no se usa una lista enlazada con nodos: se usa directamente list.append().


class Lista:
    def __init__(self):
        self.datos = []                   # aquí se van guardando los estudiantes

    def insertar(self, estudiante):
        self.datos.append(estudiante)     # lo pone al final: O(1)

    def buscar(self, id_buscado):
        # Recorre de uno en uno. Si el estudiante está de último, da N pasos: O(N).
        for estudiante in self.datos:
            if estudiante["id"] == id_buscado:
                return estudiante
        return None                       # recorrió toda la lista y no lo encontró

    def listar_en_orden(self):
        # 1) Se arman parejas [id, estudiante].
        # 2) sort() las ordena por su primer valor, que es el id.
        parejas = []
        for estudiante in self.datos:
            parejas.append([estudiante["id"], estudiante])
        parejas.sort()
        ordenados = []
        for pareja in parejas:
            ordenados.append(pareja[1])
        return ordenados
