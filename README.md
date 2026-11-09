# Visualizador de árbol binario de búsqueda

Aplicación educativa hecha en Python y Tkinter. La ventana muestra el árbol de forma gráfica y permite insertar, buscar y eliminar números, animar recorridos y consultar propiedades del árbol.

## Abrir la aplicación

Se necesita Python 3.9 o posterior con Tkinter instalado. Para iniciar la ventana, abre `interfaz_tkinter.py` en IDLE o en tu editor de Python y usa **Run / Ejecutar**. La aplicación no contiene un menú ni una versión de terminal; el editor puede mostrar su propia consola de ejecución.

## Cómo funciona

Cada objeto `Nodo` guarda un número y referencias a sus hijos izquierdo y derecho. La clase `Arbol` conserva la raíz y realiza las operaciones:

- **Insertar:** compara el número con cada nodo; los menores avanzan a la izquierda y los mayores a la derecha. No acepta duplicados.
- **Buscar:** sigue esas mismas comparaciones hasta encontrar el número o llegar a una rama vacía.
- **Eliminar:** contempla nodos sin hijos, con un hijo o con dos hijos. En el último caso usa el sucesor inorden para conservar el orden del árbol.
- **Recorrer:** inorden, preorden y postorden se implementan recursivamente. El recorrido por niveles usa una cola.
- **Consultar:** calcula altura en niveles, cantidad de nodos y hojas, mínimo y máximo.

La interfaz representa cada objeto `Nodo` como un círculo en un `Canvas`. Los enlaces muestran las relaciones entre padres e hijos; durante una animación se resalta cada nodo visitado. También permite cargar un ejemplo, crear un árbol aleatorio y guardar o abrir árboles en formato JSON.

La altura se cuenta en niveles: un árbol vacío tiene altura 0 y uno con solo la raíz tiene altura 1.

## Por qué el código está separado

La lógica del árbol y la ventana están en archivos distintos. `Arbol` y `Nodo` se ocupan de los datos y operaciones; Tkinter se encarga de los botones, el dibujo y la animación. Así se puede explicar cada clase con claridad y cambiar la presentación sin reescribir las operaciones del árbol.


