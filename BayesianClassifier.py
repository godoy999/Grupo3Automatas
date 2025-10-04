"""
BayesianClassifier.py
Clasificador Bayesiano Ingenuo Mejorado para Detección de Spam
"""

import math
import re
from collections import defaultdict


class BayesianClassifier:
    """
    Clasificador Bayesiano Ingenuo (Naive Bayes) Mejorado
    """

    def __init__(self, alpha=1.0):
        """
        Inicializa el clasificador.
        
        Args:
            alpha (float): Parámetro de suavizado de Laplace
        """
        self.clases = set()
        self.frecuencias = defaultdict(lambda: defaultdict(int))
        self.total_palabras = defaultdict(int)
        self.documentos = defaultdict(int)
        self.vocabulario = set()
        self.alpha = alpha
        self.entrenado = False

    def _preprocesar_texto(self, texto):
        """
        Preprocesa el texto para normalizar y limpiar.
        
        Returns:
            list: Lista de palabras limpias
        """
        texto = texto.lower()
        texto = re.sub(r'[^a-záéíóúñü\s]', ' ', texto)
        palabras = [palabra for palabra in texto.split() if len(palabra) >= 2]
        return palabras

    def entrenar(self, ejemplos):
        """
        Entrena el clasificador con ejemplos etiquetados.
        
        Args:
            ejemplos (list): Lista de tuplas (texto, clase)
        """
        if not ejemplos:
            raise ValueError("La lista de ejemplos no puede estar vacía")
        
        for texto, clase in ejemplos:
            self.clases.add(clase)
            self.documentos[clase] += 1
            palabras = self._preprocesar_texto(texto)
            
            for palabra in palabras:
                self.frecuencias[clase][palabra] += 1
                self.total_palabras[clase] += 1
                self.vocabulario.add(palabra)
        
        self.entrenado = True

    def clasificar(self, texto):
        """
        Clasifica un texto usando Naive Bayes.
        
        Args:
            texto (str): Texto a clasificar
            
        Returns:
            str: Clase predicha ('spam' o 'ham')
        """
        if not self.entrenado:
            return "sin_entrenar"
        
        if not self.clases:
            return "sin_entrenar"
        
        palabras = self._preprocesar_texto(texto)
        
        if not palabras:
            return max(self.documentos, key=self.documentos.get)
        
        puntajes = {}
        total_docs = sum(self.documentos.values())
        vocab_size = len(self.vocabulario)

        for clase in self.clases:
            log_prob_clase = math.log(self.documentos[clase] / total_docs)
            log_prob_total = log_prob_clase

            for palabra in palabras:
                freq = self.frecuencias[clase][palabra] + self.alpha
                total = self.total_palabras[clase] + (self.alpha * vocab_size)
                log_prob_palabra = math.log(freq / total)
                log_prob_total += log_prob_palabra

            puntajes[clase] = log_prob_total

        return max(puntajes, key=puntajes.get)

    def clasificar_con_probabilidades(self, texto):
        """
        Clasifica un texto y retorna las probabilidades de cada clase.
        
        Args:
            texto (str): Texto a clasificar
            
        Returns:
            tuple: (clase_predicha, dict_probabilidades)
        """
        if not self.entrenado:
            return "sin_entrenar", {}
        
        palabras = self._preprocesar_texto(texto)
        
        if not palabras:
            clase_mas_frecuente = max(self.documentos, key=self.documentos.get)
            return clase_mas_frecuente, {clase: 0.0 for clase in self.clases}
        
        log_puntajes = {}
        total_docs = sum(self.documentos.values())
        vocab_size = len(self.vocabulario)

        for clase in self.clases:
            log_prob_clase = math.log(self.documentos[clase] / total_docs)
            log_prob_total = log_prob_clase

            for palabra in palabras:
                freq = self.frecuencias[clase][palabra] + self.alpha
                total = self.total_palabras[clase] + (self.alpha * vocab_size)
                log_prob_palabra = math.log(freq / total)
                log_prob_total += log_prob_palabra

            log_puntajes[clase] = log_prob_total

        max_log = max(log_puntajes.values())
        exp_puntajes = {clase: math.exp(log_val - max_log) 
                        for clase, log_val in log_puntajes.items()}
        
        suma_exp = sum(exp_puntajes.values())
        probabilidades = {clase: exp_val / suma_exp 
                         for clase, exp_val in exp_puntajes.items()}
        
        clase_predicha = max(probabilidades, key=probabilidades.get)
        
        return clase_predicha, probabilidades

    def obtener_palabras_mas_informativas(self, top_n=10):
        """
        Identifica las palabras más discriminativas para cada clase.
        
        Args:
            top_n (int): Número de palabras a retornar por clase
            
        Returns:
            dict: {clase: [(palabra, score), ...]}
        """
        if not self.entrenado:
            return {}
        
        palabras_informativas = {}
        
        for clase in self.clases:
            ratios = {}
            
            for palabra in self.vocabulario:
                prob_en_clase = (self.frecuencias[clase][palabra] + self.alpha) / \
                               (self.total_palabras[clase] + self.alpha * len(self.vocabulario))
                
                otras_clases = [c for c in self.clases if c != clase]
                prob_en_otras = sum(
                    (self.frecuencias[c][palabra] + self.alpha) / \
                    (self.total_palabras[c] + self.alpha * len(self.vocabulario))
                    for c in otras_clases
                ) / len(otras_clases) if otras_clases else 1e-10
                
                ratio = math.log(prob_en_clase / prob_en_otras) if prob_en_otras > 0 else 0
                ratios[palabra] = ratio
            
            top_palabras = sorted(ratios.items(), key=lambda x: x[1], reverse=True)[:top_n]
            palabras_informativas[clase] = top_palabras
        
        return palabras_informativas

    def obtener_estadisticas(self):
        """
        Retorna estadísticas del modelo entrenado.
        
        Returns:
            dict: Diccionario con estadísticas del modelo
        """
        if not self.entrenado:
            return {"error": "Modelo no entrenado"}
        
        return {
            "entrenado": self.entrenado,
            "clases": list(self.clases),
            "num_clases": len(self.clases),
            "vocabulario_size": len(self.vocabulario),
            "total_documentos": sum(self.documentos.values()),
            "docs_por_clase": dict(self.documentos),
            "palabras_por_clase": dict(self.total_palabras),
            "alpha": self.alpha
        }

    def __repr__(self):
        """Representación en string del clasificador"""
        if not self.entrenado:
            return "BayesianClassifier(sin entrenar)"
        
        return f"BayesianClassifier(clases={list(self.clases)}, vocab_size={len(self.vocabulario)}, alpha={self.alpha})"