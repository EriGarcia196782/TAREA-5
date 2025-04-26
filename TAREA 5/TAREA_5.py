
import csv
from graphviz import Digraph

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t 
        self.leaf = leaf
        self.keys = []
        self.children = []

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys.pop(-1))

    def traverse(self):
        for i in range(len(self.keys)):
            if not self.leaf:
                self.children[i].traverse()
            print(self.keys[i], end=' ')
        if not self.leaf:
            self.children[len(self.keys)].traverse()

    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        if i < len(self.keys) and self.keys[i] == key:
            return self
        if self.leaf:
            return None
        return self.children[i].search(key)


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, key):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, False)
            s.children.insert(0, r)
            s.split_child(0)
            i = 0
            if key > s.keys[0]:
                i += 1
            s.children[i].insert_non_full(key)
            self.root = s
        else:
            r.insert_non_full(key)

    def search(self, key):
        return self.root.search(key)

    def traverse(self):
        self.root.traverse()
        print()

    def load_from_csv(self, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for value in row:
                    try:
                        self.insert(int(value.strip()))
                    except ValueError:
                        continue

    def generate_graphviz(self, filename='btree'):
        dot = Digraph()
        self._generate_graphviz(self.root, dot)
        dot.render(filename, view=True, format='png')

    def _generate_graphviz(self, node, dot, parent_id=None):
        node_id = str(id(node))
        label = '|'.join(str(k) for k in node.keys)
        dot.node(node_id, label, shape='record')

        if parent_id:
            dot.edge(parent_id, node_id)

        for child in node.children:
            self._generate_graphviz(child, dot, node_id)


# Ejemplo de uso interactivo
def main():
    grado = int(input("Ingrese el grado del arbol B"))
    arbol = BTree(grado)

    while True:
        print("1. Insertar clave")
        print("2. Buscar clave")
        print("3. Mostrar arbol")
        print("4. Cargar desde CSV")
        print("5. Generar grafico")
        print("6. Salir")
        opcion = input("Seleccione una opcion")

        if opcion == '1':
            clave = int(input("Ingrese la clave a insertar:"))
            arbol.insert(clave)
        elif opcion == '2':
            clave = int(input("Ingrese la clave a buscar:"))
            resultado = arbol.search(clave)
            if resultado:
                print("Se ha encontrado la clave")
            else:
                print("No se ha encontrando en clave")
        elif opcion == '3':
            arbol.traverse()
        elif opcion == '4':
            ruta = input("Ingrese la ruta del archivo CSV:")
            arbol.load_from_csv(ruta)
        elif opcion == '5':
            arbol.generate_graphviz()
        elif opcion == '6':
            break
        else:
            print("La opcion ingresada es invalida")

if __name__ == '__main__':
    main()
