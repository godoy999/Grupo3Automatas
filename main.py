from SpamAutomata import SpamAutomata
from BayesianClassifier import BayesianClassifier


def ModeloAutomata():
    """
    Sistema Integrado de Detección de Spam
    Combina Autómata (Trie) + Clasificador Bayesiano Mejorado
    
    Demuestra:
    - Detección de palabras sospechosas con Trie (Autómata)
    - Clasificación probabilística con Naive Bayes
    - Análisis combinado para decisión final
    """
    print("=" * 80)
    print(" SISTEMA INTEGRADO: AUTÓMATA + CLASIFICADOR BAYESIANO")
    print("=" * 80)
    print()
    
    # ========== FASE 1: CONFIGURACIÓN DEL AUTÓMATA ==========
    print("  FASE 1: CONFIGURACIÓN DEL AUTÓMATA (Trie)")
    print("-" * 80)
    
    # 1. Crear el autómata
    detector = SpamAutomata()
    
    # 2. Cargar diccionario de palabras sospechosas
    palabras_sospechosas = [
        'gratis', 'premio', 'ganador', 'urgente', 'oferta',
        'dinero', 'efectivo', 'credito', 'prestamo',
        'click', 'descarga', 'enlace',
        'viagra', 'casino', 'loteria',
        'limitado', 'expire', 'ahora', 'rapido',
        'promocion', 'descuento', 'garantizado',
        'gana', 'millonario', 'sorteo', 'reclama'
    ]
    
    detector.cargar_diccionario(palabras_sospechosas)
    print(f"✓ Diccionario cargado: {detector.obtener_tamaño_diccionario()} palabras")
    print(f"  Palabras: {', '.join(sorted(list(detector.palabras_sospechosas)[:10]))}...")
    print()
    
    # ========== FASE 2: ENTRENAMIENTO DEL CLASIFICADOR BAYESIANO ==========
    print(" FASE 2: ENTRENAMIENTO DEL CLASIFICADOR BAYESIANO")
    print("-" * 80)
    
    # Crear clasificador bayesiano
    bayes = BayesianClassifier(alpha=1.0)
    
    # Dataset de entrenamiento ampliado (40 ejemplos)
    dataset = [
        # SPAM (20 ejemplos)
        ("Gana dinero rápido con esta oferta increíble", "spam"),
        ("Haz click para reclamar tu premio ahora", "spam"),
        ("URGENTE ganaste loteria millonaria", "spam"),
        ("Descarga gratis software premium", "spam"),
        ("Casino online bonos garantizados", "spam"),
        ("Crédito express sin papeles click aquí", "spam"),
        ("Oferta exclusiva descuento 90 por ciento", "spam"),
        ("Premio garantizado reclama ahora mismo", "spam"),
        ("Préstamo rápido aprobado garantizado", "spam"),
        ("Gana efectivo sin esfuerzo click", "spam"),
        ("Promoción limitada solo hoy descuento", "spam"),
        ("Sorteo ganador reclamar premio gratis", "spam"),
        ("Viagra barata compra online ahora", "spam"),
        ("Dinero fácil trabajo desde casa", "spam"),
        ("Ganaste premio sorteo urgente reclama", "spam"),
        ("Oferta única tiempo limitado click", "spam"),
        ("Descarga app ganar dinero rápido", "spam"),
        ("Casino gratis juega gana ahora", "spam"),
        ("Crédito urgente sin intereses click", "spam"),
        ("Premio millonario ganaste sorteo urgente", "spam"),
        
        # HAM (20 ejemplos)
        ("Nos vemos mañana para la reunión", "ham"),
        ("El informe del proyecto está adjunto", "ham"),
        ("Hola María cómo estás espero bien", "ham"),
        ("La junta es a las tres de la tarde", "ham"),
        ("Adjunto encuentras el documento solicitado", "ham"),
        ("Feliz cumpleaños que la pases genial", "ham"),
        ("Quedamos para tomar café el viernes", "ham"),
        ("El reporte mensual ya está terminado", "ham"),
        ("Gracias por tu ayuda con la presentación", "ham"),
        ("Recuerda traer los documentos para mañana", "ham"),
        ("Confirmado nos vemos en la oficina", "ham"),
        ("Buen día equipo revisemos la agenda", "ham"),
        ("Por favor revisa el correo anterior", "ham"),
        ("La clase de matemáticas es el lunes", "ham"),
        ("Muchas gracias por tu tiempo dedicación", "ham"),
        ("El proyecto avanza según lo planeado", "ham"),
        ("Envío información adicional para revisión", "ham"),
        ("Coordinemos horarios para la semana", "ham"),
        ("Todo está listo para la presentación", "ham"),
        ("Saludos cordiales espero tu respuesta", "ham"),
    ]
    
    # Entrenar el modelo
    bayes.entrenar(dataset)
    
    print(f"✓ Clasificador entrenado exitosamente")
    print(f"  - Total ejemplos: {len(dataset)}")
    print(f"  - SPAM: {sum(1 for _, c in dataset if c=='spam')} ejemplos")
    print(f"  - HAM: {sum(1 for _, c in dataset if c=='ham')} ejemplos")
    print(f"  - Vocabulario aprendido: {len(bayes.vocabulario)} palabras únicas")
    print()
    
    # Mostrar palabras más discriminativas
    print("🔍 Palabras más discriminativas por clase:")
    print()
    palabras_info = bayes.obtener_palabras_mas_informativas(top_n=8)
    
    for clase, palabras in palabras_info.items():
        print(f"   Top palabras de {clase.upper()}:")
        for i, (palabra, score) in enumerate(palabras, 1):
            print(f"     {i}. '{palabra}' (score: {score:+.3f})")
        print()
    
    # ========== FASE 3: PRUEBAS DE DETECCIÓN ==========
    print("=" * 80)
    print(" FASE 3: PRUEBAS DE DETECCIÓN INTEGRADA")
    print("=" * 80)
    print()
    
    # Casos de prueba
    textos_prueba = [
        # Caso 1: Texto normal sin spam
        "Hola, te envío el informe que solicitaste ayer.",
        
        # Caso 2: Spam obvio
        "¡FELICIDADES! Eres el GANADOR de un PREMIO increíble. Click AHORA para reclamar tu DINERO.",
        
        # Caso 3: Spam con variaciones de caracteres
        "Ofert@ GR@TIS por tiempo limit@do. ¡D3scarga ahora!",
        
        # Caso 4: Mensaje legítimo
        "La reunión de mañana es a las 10 en la sala principal.",
        
        # Caso 5: Palabras parciales
        "Superoferta y ultrarapido envío gratis garantizado.",
        
        # Caso 6: Múltiples detecciones
        "Casino online gratis. Loteria urgente. Premio efectivo garantizado.",
        
        # Caso 7: Mensaje normal de trabajo
        "Por favor confirma tu asistencia al evento del viernes.",
        
        # Caso 8: Spam agresivo
        "URGENTE: Ganaste sorteo millonario click aquí premio garantizado ahora.",
        
        # Caso 9: Mensaje casual
        "El proyecto está avanzando bien, te mantendré informado.",
        
        # Caso 10: Spam financiero
        "Crédito express sin papeles préstamo rápido dinero urgente click."
    ]
    
    resultados = []
    
    # ========== EJECUTAR PRUEBAS ==========
    for numero, texto in enumerate(textos_prueba, 1):
        print(f"{'═' * 80}")
        print(f" PRUEBA #{numero}")
        print(f"{'═' * 80}")
        print(f"Texto: \"{texto}\"")
        print()
        
        # ========== ANÁLISIS CON AUTÓMATA (TRIE) ==========
        analisis_trie = detector.analizar_texto(texto)
        
        print(f" RESULTADOS AUTÓMATA (Trie):")
        print(f"   • Longitud del texto: {analisis_trie['longitud_texto']} caracteres")
        print(f"   • Palabras spam detectadas: {analisis_trie['total_detecciones']}")
        print(f"   • Palabras únicas encontradas: {analisis_trie['palabras_unicas_encontradas']}")
        print(f"   • Puntuación de spam: {analisis_trie['puntuacion_spam']}")
        
        # Mostrar frecuencia de palabras detectadas
        if analisis_trie['frecuencia_palabras']:
            print(f"   • Palabras detectadas:")
            for palabra, cantidad in sorted(analisis_trie['frecuencia_palabras'].items(), 
                                          key=lambda x: x[1], reverse=True)[:5]:
                print(f"      - '{palabra}': {cantidad} vez/veces")
        
        # Mostrar algunas posiciones de detección
        if analisis_trie['detalle_detecciones']:
            print(f"   • Posiciones (primeras 3):")
            for palabra, posicion in analisis_trie['detalle_detecciones'][:3]:
                print(f"      - '{palabra}' en posición {posicion}")
        
        # ========== ANÁLISIS CON BAYESIANO ==========
        clasificacion_bayes, probabilidades = bayes.clasificar_con_probabilidades(texto)
        
        print(f"\n RESULTADOS CLASIFICADOR BAYESIANO:")
        print(f"   • Clasificación: {clasificacion_bayes.upper()}")
        print(f"   • Confianza por clase:")
        
        for clase, prob in sorted(probabilidades.items(), key=lambda x: x[1], reverse=True):
            barra = "█" * int(prob * 25)
            print(f"      {clase:6s}: {prob:6.2%} {barra}")
        
        # ========== DECISIÓN FINAL INTEGRADA ==========
        print(f"\n DECISIÓN FINAL INTEGRADA:")
        
        confianza_spam = probabilidades.get('spam', 0)
        palabras_detectadas = analisis_trie['palabras_unicas_encontradas']
        
        # Lógica de decisión combinada
        if confianza_spam > 0.70 and palabras_detectadas >= 2:
            decision = " SPAM - Alta confianza"
            explicacion = "Ambos sistemas coinciden: alta probabilidad bayesiana + palabras sospechosas detectadas"
        elif confianza_spam > 0.70:
            decision = " SPAM - Confianza media"
            explicacion = "Clasificador bayesiano indica spam con alta confianza"
        elif palabras_detectadas >= 3:
            decision = "  SPAM - Confianza media"
            explicacion = "Múltiples palabras sospechosas detectadas por el autómata"
        elif confianza_spam > 0.50 or palabras_detectadas >= 1:
            decision = "SOSPECHOSO - Requiere revisión"
            explicacion = "Indicadores débiles de spam detectados"
        else:
            decision = " HAM - Mensaje legítimo"
            explicacion = "No se detectaron indicadores significativos de spam"
        
        print(f"   {decision}")
        print(f"   Razón: {explicacion}")
        
        # Guardar resultados para el resumen
        resultados.append({
            'texto': texto[:50] + "..." if len(texto) > 50 else texto,
            'decision': decision,
            'bayes_spam_prob': confianza_spam,
            'trie_palabras': palabras_detectadas
        })
        
        print()
    
    # ========== RESUMEN FINAL ==========
    print("=" * 80)
    print(" RESUMEN FINAL DEL ANÁLISIS")
    print("=" * 80)
    print()
    
    # Contar por categoría
    spam_alta = sum(1 for r in resultados if "Alta confianza" in r['decision'])
    spam_media = sum(1 for r in resultados if "Confianza media" in r['decision'])
    sospechoso = sum(1 for r in resultados if "SOSPECHOSO" in r['decision'])
    ham = sum(1 for r in resultados if "HAM" in r['decision'])
    
    print(f" Distribución de clasificaciones:")
    print(f"    SPAM Alta confianza:  {spam_alta:2d} mensajes")
    print(f"     SPAM Media confianza: {spam_media:2d} mensajes")
    print(f"    SOSPECHOSOS:           {sospechoso:2d} mensajes")
    print(f"    HAM (Legítimos):       {ham:2d} mensajes")
    print(f"   {'─' * 40}")
    print(f"    TOTAL:                 {len(resultados):2d} mensajes")
    print()
    
    # Estadísticas adicionales
    confianzas_spam = [r['bayes_spam_prob'] for r in resultados if 'SPAM' in r['decision']]
    if confianzas_spam:
        print(f" Estadísticas del Clasificador Bayesiano:")
        print(f"   • Confianza promedio en SPAM: {sum(confianzas_spam)/len(confianzas_spam):.2%}")
        print(f"   • Confianza máxima: {max(confianzas_spam):.2%}")
        print(f"   • Confianza mínima: {min(confianzas_spam):.2%}")
        print()
    
    palabras_detectadas = [r['trie_palabras'] for r in resultados]
    print(f" Estadísticas del Autómata (Trie):")
    print(f"   • Promedio palabras sospechosas: {sum(palabras_detectadas)/len(palabras_detectadas):.1f}")
    print(f"   • Máximo detectado: {max(palabras_detectadas)} palabras")
    print(f"   • Mensajes sin palabras sospechosas: {sum(1 for p in palabras_detectadas if p == 0)}")
    print()
    
    # Tabla resumen
    print(" TABLA RESUMEN:")
    print("-" * 80)
    print(f"{'#':^3} | {'Texto':^50} | {'Decisión':^25}")
    print("-" * 80)
    for i, r in enumerate(resultados, 1):
        texto_corto = r['texto'][:47] + "..." if len(r['texto']) > 50 else r['texto']
        decision_corta = r['decision'].split('-')[0].strip()
        print(f"{i:^3} | {texto_corto:<50} | {decision_corta:<25}")
    print("-" * 80)
    print()
    
    print("=" * 80)
    print(" DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print()
    print(" Nota: Este sistema combina dos enfoques complementarios:")
    print("   - Autómata (Trie): Detección rápida de patrones conocidos")
    print("   - Bayesiano: Análisis probabilístico del contenido completo")
    print()


# Ejecutar demostración
if __name__ == "__main__":
    ModeloAutomata()