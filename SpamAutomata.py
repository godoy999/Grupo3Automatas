class TrieNode:
   def __init__(self):
        # Diccionario de transiciones: {caracter: TrieNode}
        self.hijos = {}
        
        # True si este nodo marca el fin de una palabra sospechosa (estado de aceptación)
        self.es_fin_de_palabra = False
        
        # Almacena la palabra completa si es un estado final
        self.palabra = None
        
   def __repr__(self):
        return f"TrieNode(es_fin={self.es_fin_de_palabra}, palabra={self.palabra})"


class SpamAutomata:
    """
    Autómata Finito implementado con Trie para detectar palabras sospechosas.
    Detecta palabras spam y sus variaciones en textos.
    """
    
    # Mapeo de caracteres equivalentes para detectar variaciones (ej: gr@tis, v1agra)
    EQUIVALENCIAS_CARACTERES = {
        '@': 'a',
        '4': 'a',
        '3': 'e',
        '1': 'i',
        '!': 'i',
        '0': 'o',
        '$': 's',
        '5': 's',
        '7': 't',
        '+': 't'
    }
    
    def __init__(self):
        """
        Inicializa el autómata con un nodo raíz (estado inicial q0).
        """
        self.raiz = TrieNode()  # Estado inicial (q0)
        self.palabras_sospechosas = set()  # Conjunto de palabras en el diccionario
        
    def _normalizar_caracter(self, caracter):
        """
        Normaliza un carácter: convierte a minúsculas y maneja equivalencias.
        """
        caracter = caracter.lower()
        # Si el carácter tiene equivalencia (ej: @ -> a), lo reemplaza
        return self.EQUIVALENCIAS_CARACTERES.get(caracter, caracter)
    
    def insertar_palabra(self, palabra):
        """
        Inserta una palabra sospechosa en el Trie.
        Equivalente a definir las transiciones del autómata para reconocer esta palabra.
        """
        if not palabra:
            return
            
        palabra = palabra.lower().strip()
        self.palabras_sospechosas.add(palabra)
        
        nodo_actual = self.raiz
        
        # Recorrer cada carácter y crear transiciones
        for caracter in palabra:
            caracter_normalizado = self._normalizar_caracter(caracter)
            
            # Si no existe transición para este carácter, crear nuevo nodo (nuevo estado)
            if caracter_normalizado not in nodo_actual.hijos:
                nodo_actual.hijos[caracter_normalizado] = TrieNode()
            
            # Avanzar al siguiente estado
            nodo_actual = nodo_actual.hijos[caracter_normalizado]
        
        # Marcar el último nodo como estado de aceptación
        nodo_actual.es_fin_de_palabra = True
        nodo_actual.palabra = palabra
    
    def cargar_diccionario(self, lista_palabras):
        
        #Carga múltiples palabras al diccionario del autómata.
        for palabra in lista_palabras:
            self.insertar_palabra(palabra)
    
    def _buscar_desde_posicion(self, texto, posicion_inicio):
        """
        Busca palabras sospechosas comenzando desde una posición específica.
        Detecta palabras parciales dentro de otras palabras.
        """
        nodo_actual = self.raiz
        coincidencia_mas_larga = None
        longitud_coincidencia = 0
        
        # Recorrer el texto desde la posición inicial
        for i in range(posicion_inicio, len(texto)):
            caracter = self._normalizar_caracter(texto[i])
            
            # Si no hay transición para este carácter, terminar búsqueda
            if caracter not in nodo_actual.hijos:
                break
            
            # Avanzar al siguiente estado
            nodo_actual = nodo_actual.hijos[caracter]
            
            # Si llegamos a un estado de aceptación, registrar la palabra
            if nodo_actual.es_fin_de_palabra:
                coincidencia_mas_larga = nodo_actual.palabra
                longitud_coincidencia = i - posicion_inicio + 1
        
        return coincidencia_mas_larga, longitud_coincidencia
    
    def detectar(self, texto):
        """
        Detecta todas las ocurrencias de palabras sospechosas en el texto.
                - 'detecciones': lista de tuplas (palabra, posición)
                - 'cantidad': número total de palabras detectadas
                - 'palabras_unicas': conjunto de palabras únicas encontradas
                - 'puntuacion': puntuación (cada palabra suma 1 punto)
        """
        if not texto:
            return {
                'detecciones': [],
                'cantidad': 0,
                'palabras_unicas': set(),
                'puntuacion': 0
            }
        
        # Normalizar texto a minúsculas
        texto_normalizado = texto.lower()
        
        detecciones = []  # Lista de (palabra, posición)
        palabras_unicas = set()  # Palabras únicas encontradas
        
        # Recorrer cada posición del texto
        i = 0
        while i < len(texto_normalizado):
            # Buscar palabra sospechosa desde esta posición
            palabra_encontrada, longitud = self._buscar_desde_posicion(texto_normalizado, i)
            
            if palabra_encontrada:
                detecciones.append((palabra_encontrada, i))
                palabras_unicas.add(palabra_encontrada)
                i += longitud  # Saltar la palabra encontrada
            else:
                i += 1  # Avanzar un carácter
        
        return {
            'detecciones': detecciones,
            'cantidad': len(detecciones),
            'palabras_unicas': palabras_unicas,
            'puntuacion': len(detecciones)  # Puntuación: 1 punto por cada detección
        }
    
    def analizar_texto(self, texto):
        #Analiza el texto y devuelve un informe detallado.
        resultados = self.detectar(texto)
        
        # Crear resumen de frecuencia de palabras
        frecuencia_palabras = {}
        for palabra, _ in resultados['detecciones']:
            frecuencia_palabras[palabra] = frecuencia_palabras.get(palabra, 0) + 1
        
        return {
            'longitud_texto': len(texto),
            'total_detecciones': resultados['cantidad'],
            'palabras_unicas_encontradas': len(resultados['palabras_unicas']),
            'puntuacion_spam': resultados['puntuacion'],
            'frecuencia_palabras': frecuencia_palabras,
            'detalle_detecciones': resultados['detecciones']
        }
    
    def obtener_tamaño_diccionario(self):
        return len(self.palabras_sospechosas) #Retorna el número de palabras en el diccionario.