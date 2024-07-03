import heapq  # Biblioteca para manejar la cola de prioridad

# Definir los costos de los diferentes tipos de terreno
COSTOS = {
    "camino": 1,  # Camino normal con costo bajo
    "agua": 10,  # Agua con costo alto
    "edificio": float('inf'),  # Edificio, intransitable
}

# Función para generar un mapa de tamaño n x n con caminos
def generar_mapa(tamaño):
    # Crear una matriz de tamaño n x n llena de caminos
    return [[COSTOS["camino"] for _ in range(tamaño)] for _ in range(tamaño)]

# Función para obtener coordenadas del usuario y ajustarlas a índices basados en 0
def obtener_coordenadas(mensaje, tamaño):
    while True:  # Repetir hasta que se ingresen coordenadas válidas
        try:
            y, x = map(int, input(mensaje).split())  # Leer y dividir la entrada en y e x
            x -= 1  # Ajustar x para índice basado en 0
            y -= 1  # Ajustar y para índice basado en 0
            if 0 <= x < tamaño and 0 <= y < tamaño:  # Verificar si las coordenadas están dentro del mapa
                return (y, x)  # Devolver las coordenadas ajustadas
            else:
                print(f"Por favor, introduce coordenadas válidas entre 1 y {tamaño}.")
        except ValueError:  # Manejar errores de formato
            print("Entrada inválida. Por favor, introduce dos números separados por un espacio.")

# Función para añadir obstáculos al mapa
def añadir_obstaculos(mapa, tipo_obstaculo, cantidad):
    for _ in range(cantidad):  # Repetir para la cantidad de obstáculos
        y, x = obtener_coordenadas(f"Introduce las coordenadas del obstáculo {tipo_obstaculo} (formato: y x): ", len(mapa))
        mapa[y][x] = COSTOS[tipo_obstaculo]  # Asignar el costo del obstáculo a la celda correspondiente

# Clase Nodo para representar cada punto en el mapa
class Nodo:
    def __init__(self, posicion, g, h):
        self.posicion = posicion  # Posición del nodo en el mapa
        self.g = g  # Costo desde el inicio hasta el nodo
        self.h = h  # Costo heurístico hasta la meta
        self.f = g + h  # Costo total

    def __lt__(self, otro):
        return self.f < otro.f  # Comparar nodos por su costo total

# Función heurística que usa la distancia de Manhattan
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Calcular la distancia de Manhattan

# Implementación del algoritmo A*
def a_estrella(mapa, inicio, meta):
    lista_abierta = []  # Lista de nodos por explorar
    heapq.heappush(lista_abierta, Nodo(inicio, 0, heuristica(inicio, meta)))  # Añadir el nodo inicial
    de_donde_viene = {}  # Diccionario para rastrear de dónde viene cada nodo
    costo_hasta_ahora = {inicio: 0}  # Diccionario para almacenar el costo hasta cada nodo

    while lista_abierta:  # Mientras haya nodos por explorar
        actual = heapq.heappop(lista_abierta).posicion  # Obtener el nodo con el menor costo total

        if actual == meta:  # Si se llegó a la meta
            return reconstruir_camino(de_donde_viene, inicio, meta)  # Reconstruir el camino

        for vecino in obtener_vecinos(mapa, actual):  # Obtener los vecinos del nodo actual
            nuevo_costo = costo_hasta_ahora[actual] + mapa[vecino[0]][vecino[1]]  # Calcular el nuevo costo
            if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:  # Si el nuevo costo es menor
                costo_hasta_ahora[vecino] = nuevo_costo  # Actualizar el costo
                heapq.heappush(lista_abierta, Nodo(vecino, nuevo_costo, heuristica(vecino, meta)))  # Añadir el vecino a la lista abierta
                de_donde_viene[vecino] = actual  # Registrar de dónde viene el vecino

    return None  # Si no se encuentra camino

# Función para obtener vecinos válidos de un nodo
def obtener_vecinos(mapa, posicion):
    vecinos = []
    direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Posibles direcciones de movimiento (derecha, abajo, izquierda, arriba)
    for direccion in direcciones:
        vecino = (posicion[0] + direccion[0], posicion[1] + direccion[1])  # Calcular la posición del vecino
        if 0 <= vecino[0] < len(mapa) and 0 <= vecino[1] < len(mapa[0]) and mapa[vecino[0]][vecino[1]] != float('inf'):
            vecinos.append(vecino)  # Añadir vecino si está dentro del mapa y no es intransitable
    return vecinos

# Función para reconstruir el camino desde la meta hasta el inicio
def reconstruir_camino(de_donde_viene, inicio, meta):
    actual = meta
    camino = []
    while actual != inicio:  # Mientras no se llegue al inicio
        camino.append(actual)  # Añadir el nodo actual al camino
        if actual not in de_donde_viene:  # Si no hay registro de de dónde viene el nodo
            return None  # No se puede reconstruir el camino
        actual = de_donde_viene[actual]  # Moverse al nodo anterior
    camino.append(inicio)  # Añadir el nodo inicial
    camino.reverse()  # Invertir el camino para que vaya del inicio a la meta
    return camino

# Función para imprimir el mapa inicial vacío
def imprimir_mapa(mapa):
    for fila in mapa:
        print(" ".join(["." for _ in fila]))  # Imprimir cada celda como un punto

# Función para imprimir el mapa con obstáculos
def imprimir_mapa_con_obstaculos(mapa):
    for fila in mapa:
        print(" ".join(["E" if celda == float('inf') else "A" if celda == 10 else "." for celda in fila]))  # Imprimir "E" para edificios, "A" para agua, "." para caminos

# Función para imprimir el mapa con el camino encontrado
def imprimir_mapa_con_camino(mapa, camino, inicio, meta):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if (i, j) == inicio:
                print("I", end=" ")  # Imprimir "I" para el punto de inicio
            elif (i, j) == meta:
                print("D", end=" ")  # Imprimir "D" para el punto de destino
            elif (i, j) in camino:
                print("C", end=" ")  # Imprimir "C" para el camino
            elif mapa[i][j] == float('inf'):
                print("E", end=" ")  # Imprimir "E" para edificios
            elif mapa[i][j] == 10:
                print("A", end=" ")  # Imprimir "A" para agua
            else:
                print(".", end=" ")  # Imprimir "." para caminos
        print()

# Generar el mapa
tamaño = int(input("Introduce el tamaño del mapa: "))  # Pedir el tamaño del mapa al usuario
mapa = generar_mapa(tamaño)  # Crear el mapa

# Imprimir el mapa vacío
print("Mapa vacío:")
imprimir_mapa(mapa)

# Añadir obstáculos
cantidad_edificios = int(input("Introduce la cantidad de edificios: "))  # Pedir la cantidad de edificios
añadir_obstaculos(mapa, "edificio", cantidad_edificios)  # Añadir edificios al mapa

cantidad_agua = int(input("Introduce la cantidad de áreas de agua: "))  # Pedir la cantidad de áreas de agua
añadir_obstaculos(mapa, "agua", cantidad_agua)  # Añadir áreas de agua al mapa

# Imprimir el mapa con obstáculos
print("Mapa con obstáculos:")
imprimir_mapa_con_obstaculos(mapa)

# Obtener las coordenadas de inicio y meta
inicio = obtener_coordenadas("Introduce las coordenadas de inicio (formato: y x): ", tamaño)
meta = obtener_coordenadas("Introduce las coordenadas de meta (formato: y x): ", tamaño)

# Ejecutar el algoritmo A*
camino = a_estrella(mapa, inicio, meta)  # Buscar el camino

# Imprimir el resultado
if camino is None:
    print("No se encontró ningún camino.")
else:
    print("Mapa con el camino encontrado:")
    imprimir_mapa_con_camino(mapa, camino, inicio, meta)
