"""Implementación educativa de un árbol binario de búsqueda (ABB)."""

from collections import deque


class Nodo:
    """Guarda un valor y las referencias a sus hijos izquierdo y derecho."""

    def __init__(self, valor: int):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class Arbol:
    """Árbol binario de búsqueda para valores enteros, sin duplicados."""

    def __init__(self):
        self.raiz = None

    @staticmethod
    def _validar_valor(valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("El árbol solo acepta números enteros.")

    def es_vacio(self) -> bool:
        return self.raiz is None

    def insertar(self, valor: int) -> bool:
        """Inserta un valor. Devuelve False si ya estaba en el árbol."""
        self._validar_valor(valor)
        if self.raiz is None:
            self.raiz = Nodo(valor)
            return True
        return self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual: Nodo, valor: int) -> bool:
        if valor == nodo_actual.valor:
            return False
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(valor)
                return True
            return self._insertar_recursivo(nodo_actual.izquierda, valor)
        if nodo_actual.derecha is None:
            nodo_actual.derecha = Nodo(valor)
            return True
        return self._insertar_recursivo(nodo_actual.derecha, valor)

    def buscar(self, valor: int) -> bool:
        """Indica si el valor está en el árbol."""
        self._validar_valor(valor)
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual: Nodo, valor: int) -> bool:
        if nodo_actual is None:
            return False
        if valor == nodo_actual.valor:
            return True
        if valor < nodo_actual.valor:
            return self._buscar_recursivo(nodo_actual.izquierda, valor)
        return self._buscar_recursivo(nodo_actual.derecha, valor)

    def inorden(self) -> list[int]:
        """Recorre izquierda, raíz y derecha; en un ABB queda ordenado."""
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo_actual: Nodo, resultado: list[int]) -> None:
        if nodo_actual is not None:
            self._inorden_recursivo(nodo_actual.izquierda, resultado)
            resultado.append(nodo_actual.valor)
            self._inorden_recursivo(nodo_actual.derecha, resultado)

    def preorden(self) -> list[int]:
        """Recorre raíz, izquierda y derecha."""
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo_actual: Nodo, resultado: list[int]) -> None:
        if nodo_actual is not None:
            resultado.append(nodo_actual.valor)
            self._preorden_recursivo(nodo_actual.izquierda, resultado)
            self._preorden_recursivo(nodo_actual.derecha, resultado)

    def postorden(self) -> list[int]:
        """Recorre izquierda, derecha y raíz."""
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo_actual: Nodo, resultado: list[int]) -> None:
        if nodo_actual is not None:
            self._postorden_recursivo(nodo_actual.izquierda, resultado)
            self._postorden_recursivo(nodo_actual.derecha, resultado)
            resultado.append(nodo_actual.valor)

    def recorrido_por_niveles(self) -> list[int]:
        """Recorre el árbol por anchura con una cola (BFS)."""
        if self.es_vacio():
            return []
        resultado = []
        cola = deque([self.raiz])
        while cola:
            nodo_actual = cola.popleft()
            resultado.append(nodo_actual.valor)
            if nodo_actual.izquierda is not None:
                cola.append(nodo_actual.izquierda)
            if nodo_actual.derecha is not None:
                cola.append(nodo_actual.derecha)
        return resultado

    def eliminar(self, valor: int) -> bool:
        """Elimina un valor, contemplando cero, uno o dos hijos."""
        self._validar_valor(valor)
        if not self.buscar(valor):
            return False
        self.raiz = self._eliminar_recursivo(self.raiz, valor)
        return True

    def _eliminar_recursivo(self, nodo_actual: Nodo, valor: int):
        if nodo_actual is None:
            return None
        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self._eliminar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self._eliminar_recursivo(nodo_actual.derecha, valor)
        else:
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            if nodo_actual.derecha is None:
                return nodo_actual.izquierda

            # Con dos hijos se usa el menor valor del subárbol derecho:
            # el sucesor inorden conserva el orden del ABB.
            sucesor = self._obtener_nodo_minimo(nodo_actual.derecha)
            nodo_actual.valor = sucesor.valor
            nodo_actual.derecha = self._eliminar_recursivo(
                nodo_actual.derecha, sucesor.valor
            )
        return nodo_actual

    @staticmethod
    def _obtener_nodo_minimo(nodo_actual: Nodo) -> Nodo:
        actual = nodo_actual
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def altura(self) -> int:
        """Devuelve la altura en niveles; un árbol vacío tiene altura cero."""
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo_actual: Nodo) -> int:
        if nodo_actual is None:
            return 0
        izquierda = self._altura_recursiva(nodo_actual.izquierda)
        derecha = self._altura_recursiva(nodo_actual.derecha)
        return 1 + max(izquierda, derecha)

    def contar_nodos(self) -> int:
        return self._contar_nodos_recursivo(self.raiz)

    def _contar_nodos_recursivo(self, nodo_actual: Nodo) -> int:
        if nodo_actual is None:
            return 0
        return (
            1
            + self._contar_nodos_recursivo(nodo_actual.izquierda)
            + self._contar_nodos_recursivo(nodo_actual.derecha)
        )

    def contar_hojas(self) -> int:
        return self._contar_hojas_recursivo(self.raiz)

    def _contar_hojas_recursivo(self, nodo_actual: Nodo) -> int:
        if nodo_actual is None:
            return 0
        if nodo_actual.izquierda is None and nodo_actual.derecha is None:
            return 1
        return (
            self._contar_hojas_recursivo(nodo_actual.izquierda)
            + self._contar_hojas_recursivo(nodo_actual.derecha)
        )

    def obtener_minimo(self):
        """Devuelve el menor valor o None cuando el árbol está vacío."""
        if self.es_vacio():
            return None
        return self._obtener_nodo_minimo(self.raiz).valor

    def obtener_maximo(self):
        """Devuelve el mayor valor o None cuando el árbol está vacío."""
        if self.es_vacio():
            return None
        actual = self.raiz
        while actual.derecha is not None:
            actual = actual.derecha
        return actual.valor

    def limpiar(self) -> None:
        """Vacía el árbol."""
        self.raiz = None

