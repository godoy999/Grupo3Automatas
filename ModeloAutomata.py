from SpamAutomata import SpamAutomata

def ModeloAutomata():
    """
    Función de demostración para la Segunda Entrega.
    Muestra la funcionalidad mínima viable del autómata.
    """
    print("=" * 70)
    print("AUTÓMATA DETECTOR DE SPAM - DEMOSTRACIÓN")
    print("=" * 70)
    print()
    
    # 1. Crear el autómata
    detector = SpamAutomata()
    
    # 2. Cargar diccionario de palabras sospechosas
    palabras_sospechosas = [
        'gratis', 'premio', 'ganador', 'urgente', 'oferta',
        'dinero', 'efectivo', 'credito', 'prestamo',
        'click', 'descarga', 'enlace',
        'viagra', 'casino', 'loteria',
        'limitado', 'expire', 'ahora', 'rapido',
        'promocion', 'descuento', 'garantizado'
    ]
    
    detector.cargar_diccionario(palabras_sospechosas)
    print(f" Diccionario cargado: {detector.obtener_tamaño_diccionario()} palabras")
    print(f"  Palabras: {', '.join(sorted(list(detector.palabras_sospechosas)[:10]))}...")
    print()
    
    # 3. Casos de prueba
    textos_prueba = [
        # Caso 1: Texto normal sin spam
        "Hola, te envío el informe que solicitaste ayer.",
        
        # Caso 2: Spam obvio
        "¡FELICIDADES! Eres el GANADOR de un PREMIO increíble. Click AHORA para reclamar tu DINERO.",
        
        # Caso 3: Spam con variaciones de caracteres
        "Ofert@ GR@TIS por tiempo limit@do. ¡D3scarga ahora!",
        
        # Caso 4: Palabras parciales
        "Superoferta y ultrarapido envío gratis garantizado.",
        
        # Caso 5: Múltiples detecciones
        "Casino online gratis. Loteria urgente. Premio efectivo garantizado."
    ]
    
    # 4. Ejecutar pruebas
    for numero, texto in enumerate(textos_prueba, 1):
        print(f"{'─' * 70}")
        print(f"PRUEBA {numero}:")
        print(f"Texto: \"{texto}\"")
        print()
        
        # Analizar el texto
        analisis = detector.analizar_texto(texto)
        
        # Mostrar resultados
        print(f"  RESULTADOS:")
        print(f"   • Longitud del texto: {analisis['longitud_texto']} caracteres")
        print(f"   • Palabras spam detectadas: {analisis['total_detecciones']}")
        print(f"   • Palabras únicas encontradas: {analisis['palabras_unicas_encontradas']}")
        print(f"   • Puntuación de spam: {analisis['puntuacion_spam']}")
        
        if analisis['frecuencia_palabras']:
            print(f"\n     Frecuencia de palabras:")
            for palabra, cantidad in sorted(analisis['frecuencia_palabras'].items(), 
                                          key=lambda x: x[1], reverse=True):
                print(f"      - '{palabra}': {cantidad} vez/veces")
        
        if analisis['detalle_detecciones']:
            print(f"\n    Detecciones en posiciones:")
            for palabra, posicion in analisis['detalle_detecciones'][:5]:  # Mostrar máximo 5
                print(f"      - '{palabra}' en posición {posicion}")
        
        print()
    
    print("=" * 70)
    print(" DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)

# Ejecutar demostración
if __name__ == "__main__":
    ModeloAutomata()