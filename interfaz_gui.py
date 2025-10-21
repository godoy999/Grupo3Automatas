"""
interfaz_gui.py
Interfaz Gráfica con Tkinter para el Sistema de Detección de Spam
No requiere instalación adicional - usa Tkinter (incluido en Python)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from SpamAutomata import SpamAutomata
from BayesianClassifier import BayesianClassifier
import threading


class SpamDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Sistema de Detección de Spam - Modelo Híbrido")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # Configurar colores
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#667eea',
            'secondary': '#764ba2',
            'spam': '#ff6b6b',
            'ham': '#51cf66',
            'suspicious': '#ffd43b',
            'white': '#ffffff',
            'text_dark': '#333333',
            'text_light': '#666666'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Inicializar sistema
        self.inicializar_sistema()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Variable para controlar pruebas
        self.ejecutando_pruebas = False
        
    def inicializar_sistema(self):
        """Inicializa el autómata y el clasificador bayesiano"""
        # Crear el autómata
        self.detector = SpamAutomata()
        
        # Cargar diccionario de palabras sospechosas
        palabras_sospechosas = [
            'gratis', 'premio', 'ganador', 'urgente', 'oferta',
            'dinero', 'efectivo', 'credito', 'prestamo',
            'click', 'descarga', 'enlace',
            'viagra', 'casino', 'loteria',
            'limitado', 'expire', 'ahora', 'rapido',
            'promocion', 'descuento', 'garantizado',
            'gana', 'millonario', 'sorteo', 'reclama'
        ]
        self.detector.cargar_diccionario(palabras_sospechosas)
        
        # Crear clasificador bayesiano
        self.bayes = BayesianClassifier(alpha=1.0)
        
        # Dataset de entrenamiento
        dataset = [
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
        
        self.bayes.entrenar(dataset)
        
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Header
        self.crear_header()
        
        # Frame principal con scroll
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame de entrada de texto
        self.crear_frame_entrada(main_container)
        
        # Frame de resultados (inicialmente oculto)
        self.frame_resultados = tk.Frame(main_container, bg=self.colors['bg'])
        self.frame_resultados.pack(fill=tk.BOTH, expand=True, pady=10)
        self.crear_frame_resultados()
        
        # Inicialmente ocultar resultados
        self.frame_resultados.pack_forget()
        
    def crear_header(self):
        """Crea el encabezado de la aplicación"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="🛡️ Sistema de Detección de Spam",
            font=("Arial", 24, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header,
            text="Modelo Híbrido: Autómata (Trie) + Clasificador Bayesiano",
            font=("Arial", 12),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        subtitle_label.pack()
        
    def crear_frame_entrada(self, parent):
        """Crea el frame para entrada de texto"""
        frame = tk.LabelFrame(
            parent,
            text="✍️ Ingrese el texto a analizar",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text_dark'],
            padx=15,
            pady=15
        )
        frame.pack(fill=tk.X, pady=5)
        
        # Área de texto con scroll
        self.text_input = scrolledtext.ScrolledText(
            frame,
            height=5,
            font=("Arial", 11),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.text_input.pack(fill=tk.X, pady=5)
        
        # Frame para botones
        button_frame = tk.Frame(frame, bg=self.colors['white'])
        button_frame.pack(fill=tk.X, pady=5)
        
        # Botón Analizar
        self.btn_analizar = tk.Button(
            button_frame,
            text="🔍 Analizar Texto",
            command=self.analizar_texto,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_analizar.pack(side=tk.LEFT, padx=5)
        
        # Botón Limpiar
        btn_limpiar = tk.Button(
            button_frame,
            text="🗑️ Limpiar",
            command=self.limpiar,
            bg=self.colors['text_light'],
            fg=self.colors['white'],
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # Botón Pruebas
        self.btn_pruebas = tk.Button(
            button_frame,
            text="🧪 Ejecutar Pruebas",
            command=self.ejecutar_pruebas,
            bg=self.colors['ham'],
            fg=self.colors['white'],
            font=("Arial", 11, "bold"),
            relief=tk.RAISED,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_pruebas.pack(side=tk.LEFT, padx=5)
        
        # Label de estado
        self.label_estado = tk.Label(
            button_frame,
            text="Sistema listo",
            font=("Arial", 10),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        )
        self.label_estado.pack(side=tk.RIGHT, padx=10)
        
    def crear_frame_resultados(self):
        """Crea el frame para mostrar resultados"""
        # Frame para dos columnas
        columns_frame = tk.Frame(self.frame_resultados, bg=self.colors['bg'])
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda - Autómata
        left_column = tk.Frame(columns_frame, bg=self.colors['bg'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.frame_automata = tk.LabelFrame(
            left_column,
            text="🤖 Análisis del Autómata (Trie)",
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text_dark'],
            padx=15,
            pady=15
        )
        self.frame_automata.pack(fill=tk.BOTH, expand=True)
        
        # Métricas del autómata
        metrics_frame = tk.Frame(self.frame_automata, bg=self.colors['white'])
        metrics_frame.pack(fill=tk.X, pady=5)
        
        self.label_detecciones = self.crear_metrica(metrics_frame, "Palabras Detectadas:", "0")
        self.label_unicas = self.crear_metrica(metrics_frame, "Palabras Únicas:", "0")
        self.label_puntuacion = self.crear_metrica(metrics_frame, "Puntuación Spam:", "0")
        
        # Área para palabras detectadas
        self.text_palabras = scrolledtext.ScrolledText(
            self.frame_automata,
            height=6,
            font=("Arial", 10),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg='#f8f9fa'
        )
        self.text_palabras.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Columna derecha - Bayesiano
        right_column = tk.Frame(columns_frame, bg=self.colors['bg'])
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.frame_bayesiano = tk.LabelFrame(
            right_column,
            text="📊 Clasificador Bayesiano",
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text_dark'],
            padx=15,
            pady=15
        )
        self.frame_bayesiano.pack(fill=tk.BOTH, expand=True)
        
        # Barras de probabilidad
        self.crear_barras_probabilidad()
        
        # Frame de decisión final (abajo, ancho completo)
        self.frame_decision = tk.LabelFrame(
            self.frame_resultados,
            text="🎯 Decisión Final",
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text_dark'],
            padx=15,
            pady=15
        )
        self.frame_decision.pack(fill=tk.X, pady=10)
        
        # Label de decisión
        self.label_decision = tk.Label(
            self.frame_decision,
            text="",
            font=("Arial", 16, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text_dark'],
            pady=10
        )
        self.label_decision.pack()
        
        # Label de explicación
        self.label_explicacion = tk.Label(
            self.frame_decision,
            text="",
            font=("Arial", 11),
            bg=self.colors['white'],
            fg=self.colors['text_light'],
            wraplength=1100,
            justify=tk.LEFT
        )
        self.label_explicacion.pack(pady=5)
        
    def crear_metrica(self, parent, label_text, valor_inicial):
        """Crea un widget de métrica"""
        frame = tk.Frame(parent, bg=self.colors['white'])
        frame.pack(fill=tk.X, pady=3)
        
        label = tk.Label(
            frame,
            text=label_text,
            font=("Arial", 10),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        )
        label.pack(side=tk.LEFT)
        
        value = tk.Label(
            frame,
            text=valor_inicial,
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        value.pack(side=tk.RIGHT)
        
        return value
        
    def crear_barras_probabilidad(self):
        """Crea las barras de probabilidad para cada clase"""
        self.barras_frame = tk.Frame(self.frame_bayesiano, bg=self.colors['white'])
        self.barras_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Canvas para SPAM
        self.crear_barra_clase("SPAM", self.colors['spam'])
        
        # Canvas para HAM
        self.crear_barra_clase("HAM", self.colors['ham'])
        
    def crear_barra_clase(self, clase, color):
        """Crea una barra de probabilidad para una clase"""
        frame = tk.Frame(self.barras_frame, bg=self.colors['white'])
        frame.pack(fill=tk.X, pady=10)
        
        # Label
        label_frame = tk.Frame(frame, bg=self.colors['white'])
        label_frame.pack(fill=tk.X)
        
        tk.Label(
            label_frame,
            text=clase,
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text_dark']
        ).pack(side=tk.LEFT)
        
        value_label = tk.Label(
            label_frame,
            text="0.00%",
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            fg=color
        )
        value_label.pack(side=tk.RIGHT)
        
        # Canvas para la barra
        canvas = tk.Canvas(frame, height=30, bg='#e0e0e0', highlightthickness=0)
        canvas.pack(fill=tk.X, pady=5)
        
        # Guardar referencias
        if clase == "SPAM":
            self.spam_canvas = canvas
            self.spam_value_label = value_label
            self.spam_color = color
        else:
            self.ham_canvas = canvas
            self.ham_value_label = value_label
            self.ham_color = color
            
    def actualizar_barra(self, canvas, value_label, probabilidad, color):
        """Actualiza una barra de probabilidad"""
        canvas.delete("all")
        width = canvas.winfo_width()
        fill_width = int(width * probabilidad)
        
        if fill_width > 0:
            canvas.create_rectangle(0, 0, fill_width, 30, fill=color, outline="")
        
        value_label.config(text=f"{probabilidad * 100:.2f}%")
        
    def analizar_texto(self):
        """Analiza el texto ingresado"""
        texto = self.text_input.get("1.0", tk.END).strip()
        
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un texto para analizar")
            return
        
        self.label_estado.config(text="Analizando...", fg=self.colors['primary'])
        self.btn_analizar.config(state=tk.DISABLED)
        self.root.update()
        
        # Análisis con Autómata
        analisis_trie = self.detector.analizar_texto(texto)
        
        # Análisis con Bayesiano
        clasificacion_bayes, probabilidades = self.bayes.clasificar_con_probabilidades(texto)
        
        # Mostrar resultados
        self.mostrar_resultados(texto, analisis_trie, clasificacion_bayes, probabilidades)
        
        self.label_estado.config(text="Análisis completado", fg=self.colors['ham'])
        self.btn_analizar.config(state=tk.NORMAL)
        
    def mostrar_resultados(self, texto, analisis_trie, clasificacion_bayes, probabilidades):
        """Muestra los resultados del análisis"""
        # Mostrar frame de resultados
        self.frame_resultados.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Actualizar métricas del autómata
        self.label_detecciones.config(text=str(analisis_trie['total_detecciones']))
        self.label_unicas.config(text=str(analisis_trie['palabras_unicas_encontradas']))
        self.label_puntuacion.config(text=str(analisis_trie['puntuacion_spam']))
        
        # Mostrar palabras detectadas
        self.text_palabras.config(state=tk.NORMAL)
        self.text_palabras.delete("1.0", tk.END)
        
        if analisis_trie['frecuencia_palabras']:
            self.text_palabras.insert("1.0", "Palabras detectadas:\n\n")
            for palabra, cantidad in sorted(analisis_trie['frecuencia_palabras'].items(), 
                                          key=lambda x: x[1], reverse=True):
                self.text_palabras.insert(tk.END, f"• '{palabra}': {cantidad} vez/veces\n")
        else:
            self.text_palabras.insert("1.0", "No se detectaron palabras sospechosas")
        
        self.text_palabras.config(state=tk.DISABLED)
        
        # Actualizar barras de probabilidad (esperar a que el canvas esté listo)
        self.root.update()
        spam_prob = probabilidades.get('spam', 0)
        ham_prob = probabilidades.get('ham', 0)
        
        self.actualizar_barra(self.spam_canvas, self.spam_value_label, spam_prob, self.spam_color)
        self.actualizar_barra(self.ham_canvas, self.ham_value_label, ham_prob, self.ham_color)
        
        # Decisión final
        confianza_spam = probabilidades.get('spam', 0)
        palabras_detectadas = analisis_trie['palabras_unicas_encontradas']
        
        if confianza_spam > 0.70 and palabras_detectadas >= 2:
            decision = "🚨 SPAM - Alta confianza"
            explicacion = "Ambos sistemas coinciden: alta probabilidad bayesiana + palabras sospechosas detectadas"
            color = self.colors['spam']
        elif confianza_spam > 0.70:
            decision = "⚠️ SPAM - Confianza media"
            explicacion = "Clasificador bayesiano indica spam con alta confianza"
            color = self.colors['spam']
        elif palabras_detectadas >= 3:
            decision = "⚠️ SPAM - Confianza media"
            explicacion = "Múltiples palabras sospechosas detectadas por el autómata"
            color = self.colors['spam']
        elif confianza_spam > 0.50 or palabras_detectadas >= 1:
            decision = "⚡ SOSPECHOSO - Requiere revisión"
            explicacion = "Indicadores débiles de spam detectados"
            color = self.colors['suspicious']
        else:
            decision = "✅ HAM - Mensaje legítimo"
            explicacion = "No se detectaron indicadores significativos de spam"
            color = self.colors['ham']
        
        self.label_decision.config(text=decision, fg=color)
        self.label_explicacion.config(text=explicacion)
        
    def limpiar(self):
        """Limpia la interfaz"""
        self.text_input.delete("1.0", tk.END)
        self.frame_resultados.pack_forget()
        self.label_estado.config(text="Sistema listo", fg=self.colors['text_light'])
        
    def ejecutar_pruebas(self):
        """Ejecuta las pruebas predefinidas"""
        if self.ejecutando_pruebas:
            return
        
        respuesta = messagebox.askyesno(
            "Ejecutar Pruebas",
            "¿Desea ejecutar las 10 pruebas predefinidas?\nSe ejecutarán automáticamente cada 2 segundos."
        )
        
        if not respuesta:
            return
        
        self.ejecutando_pruebas = True
        self.btn_pruebas.config(state=tk.DISABLED)
        self.btn_analizar.config(state=tk.DISABLED)
        
        # Casos de prueba
        textos_prueba = [
            "Hola, te envío el informe que solicitaste ayer.",
            "¡FELICIDADES! Eres el GANADOR de un PREMIO increíble. Click AHORA para reclamar tu DINERO.",
            "Ofert@ GR@TIS por tiempo limit@do. ¡D3scarga ahora!",
            "La reunión de mañana es a las 10 en la sala principal.",
            "Superoferta y ultrarapido envío gratis garantizado.",
            "Casino online gratis. Loteria urgente. Premio efectivo garantizado.",
            "Por favor confirma tu asistencia al evento del viernes.",
            "URGENTE: Ganaste sorteo millonario click aquí premio garantizado ahora.",
            "El proyecto está avanzando bien, te mantendré informado.",
            "Crédito express sin papeles préstamo rápido dinero urgente click."
        ]
        
        # Ejecutar en thread separado
        def ejecutar():
            for i, texto in enumerate(textos_prueba, 1):
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", texto)
                self.label_estado.config(text=f"Ejecutando prueba {i}/10...")
                self.root.update()
                
                self.analizar_texto()
                self.root.after(2000)  # Esperar 2 segundos
                
            self.ejecutando_pruebas = False
            self.btn_pruebas.config(state=tk.NORMAL)
            self.btn_analizar.config(state=tk.NORMAL)
            self.label_estado.config(text="Pruebas completadas", fg=self.colors['ham'])
            messagebox.showinfo("Completado", "✅ Pruebas completadas exitosamente")
        
        thread = threading.Thread(target=ejecutar)
        thread.daemon = True
        thread.start()


def main():
    """Función principal"""
    root = tk.Tk()
    app = SpamDetectorGUI(root)
    
    # Centrar ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()