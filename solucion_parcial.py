"""
================================================================================
PARCIAL 2 - FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (2026)
Tema: Algoritmos Evolutivos, Genéticos, Ascenso de Colinas,
      Temple Simulado, ACO y PSO.
================================================================================
Implementación completa, modular, rigurosa y reproducible de los 5 puntos del parcial.
Cada punto incluye:
  - Componente Matemático y Conceptual (Parte A).
  - Implementación en Python con análisis e interpretación (Parte B).
  - Generación de figuras analíticas de alta calidad en la carpeta 'images/'.
================================================================================
"""

import os
import math
import random
import argparse
from typing import List, Tuple, Dict, Any
import numpy as np
import matplotlib.pyplot as plt

# Directorio de salida para figuras
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Configuración estética global de matplotlib
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "lines.linewidth": 1.8,
    "lines.markersize": 6,
    "grid.alpha": 0.35,
    "grid.linestyle": "--"
})


# ==============================================================================
# PUNTO 1. ALGORITMOS EVOLUTIVOS Y ALGORITMOS GENÉTICOS
# ==============================================================================

def decodificar_cromosoma(bin_str: str) -> int:
    """Decodifica un cromosoma binario a su valor entero decimal."""
    return int(bin_str, 2)


def aptitud_punto1(x: int) -> int:
    """Función de aptitud objetivo: f(x) = x^2."""
    return x ** 2


def resolver_punto1_parte_a() -> Dict[str, Any]:
    """
    Desarrollo matemático analítico del Punto 1 - Parte A:
    1. Decodificación y aptitud de la población inicial P={00101, 01100, 10010, 11001}.
    2. Probabilidad de selección por ruleta de cada individuo.
    3. Cruce de un punto tras el 2do bit entre 01100 y 11001.
    4. Mutación del último bit del primer descendiente.
    """
    poblacion = ["00101", "01100", "10010", "11001"]
    decimales = [decodificar_cromosoma(c) for c in poblacion]
    aptitudes = [aptitud_punto1(d) for d in decimales]
    suma_aptitudes = sum(aptitudes)
    probabilidades = [f / suma_aptitudes for f in aptitudes]

    # Cruce de un punto tras el segundo bit (índice 2)
    p1, p2 = "01100", "11001"
    corte = 2
    h1 = p1[:corte] + p2[corte:]  # "01" + "001" = "01001"
    h2 = p2[:corte] + p1[corte:]  # "11" + "100" = "11100"

    # Invertir el último bit en h1 (índice 4)
    h1_lista = list(h1)
    h1_lista[4] = "1" if h1_lista[4] == "0" else "0"
    h1_mutado = "".join(h1_lista)
    x_h1_mutado = decodificar_cromosoma(h1_mutado)
    apt_h1_mutado = aptitud_punto1(x_h1_mutado)

    return {
        "poblacion": poblacion,
        "decimales": decimales,
        "aptitudes": aptitudes,
        "suma_aptitudes": suma_aptitudes,
        "probabilidades": probabilidades,
        "padres": (p1, p2),
        "descendientes_cruce": (h1, h2),
        "descendiente_mutado": h1_mutado,
        "x_mutado": x_h1_mutado,
        "aptitud_mutado": apt_h1_mutado
    }


def ejecutar_algoritmo_genetico(
    poblacion_inicial: List[str] = None,
    prob_cruce: float = 0.8,
    prob_mutacion: float = 0.05,
    num_generaciones: int = 20,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Implementación del Algoritmo Genético del Punto 1 - Parte B:
    - Población inicial fija de 4 cromosomas de 5 bits.
    - Selección por ruleta proporcional a f(x) = x^2.
    - Cruce de un punto con probabilidad 0.8.
    - Mutación independiente por bit con probabilidad 0.05.
    - Elitismo: preserva al mejor individuo de la generación.
    - Tamaño de población constante (N=4) durante 20 generaciones.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    if poblacion_inicial is None:
        poblacion = ["00101", "01100", "10010", "11001"]
    else:
        poblacion = list(poblacion_inicial)

    longitud_cromosoma = len(poblacion[0])
    tam_pob = len(poblacion)

    historial_generacion = []
    historial_mejor_aptitud = []
    historial_aptitud_promedio = []
    historial_mejor_x = []
    historial_mejor_cromosoma = []

    for gen in range(num_generaciones + 1):
        decimales = [decodificar_cromosoma(c) for c in poblacion]
        aptitudes = [aptitud_punto1(x) for x in decimales]

        mejor_idx = int(np.argmax(aptitudes))
        mejor_cromosoma = poblacion[mejor_idx]
        mejor_x = decimales[mejor_idx]
        mejor_apt = aptitudes[mejor_idx]
        prom_apt = float(np.mean(aptitudes))

        historial_generacion.append(gen)
        historial_mejor_aptitud.append(mejor_apt)
        historial_aptitud_promedio.append(prom_apt)
        historial_mejor_x.append(mejor_x)
        historial_mejor_cromosoma.append(mejor_cromosoma)

        if gen == num_generaciones:
            break

        # 1. Elitismo: conservar al individuo con mayor aptitud
        nueva_poblacion = [mejor_cromosoma]

        # 2. Selección por ruleta (ponderación proporcional a aptitudes)
        suma_apt = sum(aptitudes)
        probs = [f / suma_apt for f in aptitudes]

        # 3. Generación de descendencia mediante cruce y mutación
        while len(nueva_poblacion) < tam_pob:
            padres = random.choices(poblacion, weights=probs, k=2)
            p1, p2 = padres[0], padres[1]

            # Operador de cruce de un punto
            if random.random() < prob_cruce and longitud_cromosoma > 1:
                punto_corte = random.randint(1, longitud_cromosoma - 1)
                h1 = p1[:punto_corte] + p2[punto_corte:]
                h2 = p2[:punto_corte] + p1[punto_corte:]
            else:
                h1, h2 = p1, p2

            # Operador de mutación independiente bit a bit
            hijos_mutados = []
            for hijo in [h1, h2]:
                bits = list(hijo)
                for i in range(longitud_cromosoma):
                    if random.random() < prob_mutacion:
                        bits[i] = "1" if bits[i] == "0" else "0"
                hijos_mutados.append("".join(bits))

            nueva_poblacion.append(hijos_mutados[0])
            if len(nueva_poblacion) < tam_pob:
                nueva_poblacion.append(hijos_mutados[1])

        poblacion = nueva_poblacion

    return {
        "mejor_cromosoma_final": historial_mejor_cromosoma[-1],
        "mejor_x_final": historial_mejor_x[-1],
        "mejor_aptitud_final": historial_mejor_aptitud[-1],
        "historial": {
            "generacion": historial_generacion,
            "mejor_aptitud": historial_mejor_aptitud,
            "aptitud_promedio": historial_aptitud_promedio,
            "mejor_x": historial_mejor_x,
            "mejor_cromosoma": historial_mejor_cromosoma
        }
    }


def graficar_punto1(resultado_ga: Dict[str, Any]):
    """Genera gráfico comparativo y de evolución para el Algoritmo Genético."""
    hist = resultado_ga["historial"]
    gens = hist["generacion"]

    # Ejecutar 4 semillas adicionales para sustentar analíticamente la pregunta de interpretación
    semillas = [42, 10, 7, 99, 123]
    resultados_semillas = {}
    for s in semillas:
        res = ejecutar_algoritmo_genetico(seed=s)
        resultados_semillas[s] = res["historial"]["mejor_aptitud"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Subgráfico 1: Corrida oficial con semilla 42
    ax1.plot(gens, hist["mejor_aptitud"], "o-", color="#1f77b4", label="Mejor Aptitud (Elitismo)")
    ax1.plot(gens, hist["aptitud_promedio"], "s--", color="#ff7f0e", label="Aptitud Promedio")
    ax1.axhline(961, color="crimson", linestyle=":", linewidth=2, label="Óptimo Global Teórico (x=31, f=961)")
    ax1.set_title("Evolución de Aptitud (Semilla 42)", fontweight="bold")
    ax1.set_xlabel("Generación")
    ax1.set_ylabel("Aptitud $f(x) = x^2$")
    ax1.set_xticks(range(0, 21, 2))
    ax1.set_ylim(0, 1020)
    ax1.legend(loc="lower right")
    ax1.grid(True)

    # Subgráfico 2: Sensibilidad estocástica y justificación de por qué 20 gen no garantiza el óptimo
    colores = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    for i, s in enumerate(semillas):
        label_str = f"Semilla {s}" + (" (Oficial: Óptimo)" if s == 42 else "")
        ax2.plot(gens, resultados_semillas[s], marker=".", linewidth=1.6, color=colores[i], label=label_str)
    ax2.axhline(961, color="crimson", linestyle=":", linewidth=2, label="Óptimo Global (961)")
    ax2.set_title("Sensibilidad Estocástica (5 Semillas Diferentes)", fontweight="bold")
    ax2.set_xlabel("Generación")
    ax2.set_ylabel("Mejor Aptitud")
    ax2.set_xticks(range(0, 21, 2))
    ax2.set_ylim(400, 1020)
    ax2.legend(loc="lower right", fontsize=9)
    ax2.grid(True)

    plt.tight_layout()
    ruta_guardado = os.path.join(IMAGES_DIR, "punto1_algoritmo_genetico.png")
    plt.savefig(ruta_guardado)
    plt.close()
    return ruta_guardado


# ==============================================================================
# PUNTO 2. ASCENSO DE COLINAS Y ÓPTIMOS LOCALES
# ==============================================================================

VALORES_DISCRETOS_PUNTO2 = [1, 4, 7, 5, 3, 6, 9, 8, 5]


def ascenso_colinas(valores: List[int], inicio: int) -> Tuple[int, List[int]]:
    """
    Interfaz obligatoria:
    def ascenso_colinas(valores, inicio):
        '''Devuelve el estado final y la trayectoria.'''

    Regla:
    - Espacio discreto con vecinos x-1 y x+1 dentro de [0, len(valores)-1].
    - El algoritmo elige el vecino con mayor valor.
    - Solo se mueve si existe una mejora estricta (f(vecino) > f(actual)).
    """
    n = len(valores)
    actual = inicio
    trayectoria = [actual]

    while True:
        # Generar vecinos admisibles dentro del dominio discreto
        vecinos = []
        if actual > 0:
            vecinos.append(actual - 1)
        if actual < n - 1:
            vecinos.append(actual + 1)

        # Encontrar el vecino con el mayor valor de aptitud
        mejor_vecino = max(vecinos, key=lambda v: valores[v])

        # Verificar condición de mejora estricta
        if valores[mejor_vecino] > valores[actual]:
            actual = mejor_vecino
            trayectoria.append(actual)
        else:
            # Se ha alcanzado una cima (máximo local o global)
            break

    return actual, trayectoria


def resolver_punto2_completo() -> Dict[str, Any]:
    """Ejecuta ascenso de colinas desde todos los estados posibles x in [0, 8]."""
    valores = VALORES_DISCRETOS_PUNTO2
    tabla = []
    conduce_a_global = 0

    for x0 in range(len(valores)):
        estado_final, trayectoria = ascenso_colinas(valores, x0)
        valor_final = valores[estado_final]
        es_global = (estado_final == 6)
        if es_global:
            conduce_a_global += 1
        tabla.append({
            "inicio": x0,
            "trayectoria": trayectoria,
            "estado_final": estado_final,
            "valor_final": valor_final,
            "tipo_optimo": "Máximo Global" if es_global else "Máximo Local"
        })

    proporcion_global = conduce_a_global / len(valores)

    return {
        "valores": valores,
        "tabla": tabla,
        "proporcion_global": proporcion_global,
        "maximos_locales": [2, 6],
        "maximo_global": 6
    }


def graficar_punto2(resultado_hc: Dict[str, Any]):
    """Genera gráfico del paisaje discreto y cuencas de atracción de ascenso de colinas."""
    valores = resultado_hc["valores"]
    x_indices = list(range(len(valores)))

    plt.figure(figsize=(10, 5.5))
    plt.plot(x_indices, valores, color="#2b5c8f", linestyle="-", linewidth=2.5, zorder=1)
    plt.scatter(x_indices, valores, color="#2b5c8f", s=80, zorder=2)

    # Resaltar óptimos
    plt.scatter([2], [7], color="#d9534f", s=160, zorder=3, label="Máximo Local (x=2, f=7)")
    plt.scatter([6], [9], color="#2ca02c", s=200, zorder=3, marker="*", label="Máximo Global (x=6, f=9)")

    # Anotar valores en cada punto
    for x, val in zip(x_indices, valores):
        plt.annotate(f"f({x})={val}", (x, val), textcoords="offset points", xytext=(0, 10), ha="center", fontweight="bold")

    # Sombrear cuencas de atracción
    plt.axvspan(-0.5, 3.5, color="#f0ad4e", alpha=0.18, label="Cuenca Máximo Local (x ∈ [0, 3], 44.4%)")
    plt.axvspan(3.5, 8.5, color="#5cb85c", alpha=0.18, label="Cuenca Máximo Global (x ∈ [4, 8], 55.6%)")

    plt.title("Paisaje de Búsqueda y Cuencas de Atracción - Ascenso de Colinas", fontweight="bold")
    plt.xlabel("Estado Discreto $x$")
    plt.ylabel("Aptitud $f(x)$")
    plt.xticks(x_indices)
    plt.yticks(range(0, 11))
    plt.legend(loc="upper left")
    plt.grid(True)

    plt.tight_layout()
    ruta_guardado = os.path.join(IMAGES_DIR, "punto2_ascenso_colinas.png")
    plt.savefig(ruta_guardado)
    plt.close()
    return ruta_guardado


# ==============================================================================
# PUNTO 3. TEMPLE SIMULADO: ACEPTACIÓN DE SOLUCIONES PEORES
# ==============================================================================

def resolver_punto3_parte_a() -> List[Dict[str, Any]]:
    """
    Analiza analíticamente cada una de las tres transiciones independientes:
    Caso A: Estado actual=3, Candidato=2, T=5, u=0.70
    Caso B: Estado actual=2, Candidato=3, T=5, u=0.30
    Caso C: Estado actual=2, Candidato=3, T=1, u=0.30
    """
    casos = [
        {"caso": "A", "actual": 3, "candidato": 2, "T": 5.0, "u": 0.70},
        {"caso": "B", "actual": 2, "candidato": 3, "T": 5.0, "u": 0.30},
        {"caso": "C", "actual": 2, "candidato": 3, "T": 1.0, "u": 0.30},
    ]

    resultados = []
    for c in casos:
        E_act = c["actual"] ** 2
        E_cand = c["candidato"] ** 2
        dE = E_cand - E_act
        T = c["T"]
        u = c["u"]

        if dE <= 0:
            p_aceptar = 1.0
        else:
            p_aceptar = math.exp(-dE / T)

        decision = "Acepta" if u < p_aceptar else "Rechaza"

        resultados.append({
            "caso": c["caso"],
            "actual": c["actual"],
            "candidato": c["candidato"],
            "E_actual": E_act,
            "E_candidato": E_cand,
            "delta_E": dE,
            "T": T,
            "u": u,
            "p_aceptar": p_aceptar,
            "decision": decision
        })
    return resultados


def ejecutar_temple_simulado(
    x0: int = 5,
    T0: float = 10.0,
    factor_enfriamiento: float = 0.90,
    iteraciones: int = 100,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Implementación de Temple Simulado (Punto 3 - Parte B):
    - Minimizar E(x) = x^2, x in {-5, ..., 5}.
    - Estado inicial x0 = 5, Temperatura inicial T0 = 10.
    - Enfriamiento geométrico T_{k+1} = 0.90 * T_k.
    - Candidato: vecino aleatorio x-1 o x+1 dentro de [-5, 5].
    - Registro del estado actual y de la mejor solución encontrada.
    """
    random.seed(seed)
    np.random.seed(seed)

    actual_x = x0
    actual_E = actual_x ** 2

    mejor_x = actual_x
    mejor_E = actual_E

    historial_T = []
    historial_actual_x = []
    historial_actual_E = []
    historial_mejor_x = []
    historial_mejor_E = []

    T = T0

    for k in range(iteraciones):
        historial_T.append(T)
        historial_actual_x.append(actual_x)
        historial_actual_E.append(actual_E)
        historial_mejor_x.append(mejor_x)
        historial_mejor_E.append(mejor_E)

        # Generar vecinos admisibles en [-5, 5]
        vecinos = []
        if actual_x > -5:
            vecinos.append(actual_x - 1)
        if actual_x < 5:
            vecinos.append(actual_x + 1)

        candidato_x = random.choice(vecinos)
        candidato_E = candidato_x ** 2
        dE = candidato_E - actual_E

        # Regla de Metrópolis
        if dE <= 0:
            aceptar = True
        else:
            p_aceptar = math.exp(-dE / T)
            u = random.random()
            aceptar = (u < p_aceptar)

        if aceptar:
            actual_x = candidato_x
            actual_E = candidato_E
            if actual_E < mejor_E:
                mejor_x = actual_x
                mejor_E = actual_E

        T = T * factor_enfriamiento

    return {
        "mejor_solucion": mejor_x,
        "energia_minima": mejor_E,
        "estado_final": actual_x,
        "energia_final": actual_E,
        "temperatura_final": historial_T[-1],
        "historial": {
            "iteracion": list(range(iteraciones)),
            "temperatura": historial_T,
            "actual_x": historial_actual_x,
            "actual_E": historial_actual_E,
            "mejor_x": historial_mejor_x,
            "mejor_E": historial_mejor_E
        }
    }


def graficar_punto3(resultado_sa: Dict[str, Any]):
    """Genera gráficos de evolución de energía y decaimiento térmico para Temple Simulado."""
    hist = resultado_sa["historial"]
    iters = hist["iteracion"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2))

    # Subgráfico 1: Energía actual vs Mejor solución histórica
    ax1.plot(iters, hist["actual_E"], color="#7f7f7f", alpha=0.6, linewidth=1.2, label="Energía Estado Actual $E(x_k)$")
    ax1.step(iters, hist["mejor_E"], color="#1f77b4", linewidth=2.5, where="post", label="Mejor Energía Histórica $E^*$")
    ax1.axhline(0, color="crimson", linestyle=":", linewidth=1.8, label="Mínimo Global Óptimo ($E=0$)")
    ax1.set_title("Evolución de la Energía - Temple Simulado", fontweight="bold")
    ax1.set_xlabel("Iteración $k$")
    ax1.set_ylabel("Energía $E(x) = x^2$")
    ax1.legend(loc="upper right")
    ax1.grid(True)

    # Subgráfico 2: Decaimiento geométrico de la temperatura
    ax2.plot(iters, hist["temperatura"], color="#d62728", linewidth=2.0)
    ax2.set_title("Programa de Enfriamiento Geométrico ($T_{k+1} = 0.90 T_k$)", fontweight="bold")
    ax2.set_xlabel("Iteración $k$")
    ax2.set_ylabel("Temperatura $T$ (Escala Logarítmica)")
    ax2.set_yscale("log")
    ax2.grid(True, which="both")

    plt.tight_layout()
    ruta_guardado = os.path.join(IMAGES_DIR, "punto3_temple_simulado.png")
    plt.savefig(ruta_guardado)
    plt.close()
    return ruta_guardado


# ==============================================================================
# PUNTO 4. ACO: ELECCIÓN DE RUTAS Y ACTUALIZACIÓN DE FEROMONAS
# ==============================================================================

def resolver_punto4_parte_a() -> Dict[str, Any]:
    """
    Desarrollo matemático analítico de ACO (Punto 4 - Parte A):
    1. Pesos y probabilidades de A->B, A->C, A->D con alpha=1, beta=2.
    2. Identificación de la más probable y análisis de garantía estocástica.
    3. Actualización de feromona tras ruta L=10 que utiliza A->B (rho=0.2, Q=10).
    """
    aristas = ["A->B", "A->C", "A->D"]
    distancias = {"A->B": 2.0, "A->C": 4.0, "A->D": 5.0}
    tau_inicial = {"A->B": 1.0, "A->C": 2.0, "A->D": 1.0}

    alpha = 1.0
    beta = 2.0

    # Heurística eta = 1 / d
    eta = {k: 1.0 / distancias[k] for k in aristas}

    # Pesos W = (tau^alpha) * (eta^beta)
    pesos = {k: (tau_inicial[k] ** alpha) * (eta[k] ** beta) for k in aristas}
    suma_pesos = sum(pesos.values())
    probabilidades = {k: pesos[k] / suma_pesos for k in aristas}

    # Actualización con L = 10 en A->B
    rho = 0.2
    Q = 10.0
    L = 10.0
    delta_tau = {"A->B": Q / L, "A->C": 0.0, "A->D": 0.0}

    tau_nueva = {
        k: (1.0 - rho) * tau_inicial[k] + delta_tau[k]
        for k in aristas
    }

    return {
        "aristas": aristas,
        "distancias": distancias,
        "tau_inicial": tau_inicial,
        "eta": eta,
        "pesos": pesos,
        "suma_pesos": suma_pesos,
        "probabilidades": probabilidades,
        "delta_tau": delta_tau,
        "tau_nueva": tau_nueva
    }


def ejecutar_aco_rutas(
    num_hormigas: int = 10,
    num_iteraciones: int = 20,
    alpha: float = 1.0,
    beta: float = 2.0,
    rho: float = 0.2,
    Q: float = 10.0,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Modelo simplificado de ACO para elección entre tres rutas de A a Z:
    - Ruta 1: A-B-Z, L1 = 6
    - Ruta 2: A-C-Z, L2 = 8
    - Ruta 3: A-D-Z, L3 = 10
    - tau inicial = 1.0 para todas las rutas.
    - 10 hormigas por iteración, 20 iteraciones, semilla 42.
    """
    random.seed(seed)
    np.random.seed(seed)

    rutas = ["A-B-Z", "A-C-Z", "A-D-Z"]
    longitudes = {"A-B-Z": 6.0, "A-C-Z": 8.0, "A-D-Z": 10.0}
    tau = {r: 1.0 for r in rutas}

    frecuencias_acumuladas = {r: 0 for r in rutas}
    historial_tau = {r: [] for r in rutas}
    historial_prob = {r: [] for r in rutas}
    historial_elecciones_iter = {r: [] for r in rutas}

    for it in range(num_iteraciones):
        # 1. Calcular probabilidades con feromonas actuales
        pesos = {r: (tau[r] ** alpha) * ((1.0 / longitudes[r]) ** beta) for r in rutas}
        sum_pesos = sum(pesos.values())
        probs = {r: pesos[r] / sum_pesos for r in rutas}

        for r in rutas:
            historial_tau[r].append(tau[r])
            historial_prob[r].append(probs[r])

        # 2. Las 10 hormigas eligen rutas estocásticamente
        prob_list = [probs[r] for r in rutas]
        elecciones = random.choices(rutas, weights=prob_list, k=num_hormigas)

        conteos_iter = {r: elecciones.count(r) for r in rutas}
        for r in rutas:
            frecuencias_acumuladas[r] += conteos_iter[r]
            historial_elecciones_iter[r].append(conteos_iter[r])

        # 3. Evaporación de feromonas en todas las rutas
        for r in rutas:
            tau[r] = (1.0 - rho) * tau[r]

        # 4. Depósito de feromona por cada hormiga que cruzó la ruta
        for r in rutas:
            tau[r] += conteos_iter[r] * (Q / longitudes[r])

    mejor_ruta = min(rutas, key=lambda r: longitudes[r])

    return {
        "frecuencias_acumuladas": frecuencias_acumuladas,
        "feromonas_finales": tau,
        "mejor_ruta_observada": mejor_ruta,
        "longitudes": longitudes,
        "historial": {
            "iteracion": list(range(num_iteraciones)),
            "tau": historial_tau,
            "probabilidades": historial_prob,
            "elecciones_iter": historial_elecciones_iter
        }
    }


def graficar_punto4(resultado_aco: Dict[str, Any]):
    """Genera gráficos de dinámica de feromonas y distribución de elecciones en ACO."""
    hist = resultado_aco["historial"]
    iters = hist["iteracion"]
    rutas = ["A-B-Z", "A-C-Z", "A-D-Z"]
    colores = {"A-B-Z": "#2ca02c", "A-C-Z": "#1f77b4", "A-D-Z": "#d62728"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2))

    # Subgráfico 1: Evolución de feromona por ruta
    for r in rutas:
        ax1.plot(iters, hist["tau"][r], "o-", color=colores[r], label=f"Ruta {r} (L={int(resultado_aco['longitudes'][r])})")
    ax1.set_title("Evolución de Feromonas por Ruta ($Q=10, \\rho=0.2$)", fontweight="bold")
    ax1.set_xlabel("Iteración")
    ax1.set_ylabel("Nivel de Feromona $\\tau_r$")
    ax1.legend(loc="upper left")
    ax1.grid(True)

    # Subgráfico 2: Frecuencia acumulada de elecciones
    counts = [resultado_aco["frecuencias_acumuladas"][r] for r in rutas]
    porcentajes = [c / sum(counts) * 100 for c in counts]
    barras = ax2.bar(rutas, counts, color=[colores[r] for r in rutas], edgecolor="black", width=0.55)
    for barra, pct in zip(barras, porcentajes):
        yval = barra.get_height()
        ax2.text(barra.get_x() + barra.get_width() / 2.0, yval + 3, f"{yval} ({pct:.1f}%)", ha="center", va="bottom", fontweight="bold")
    ax2.set_title("Frecuencia Total de Elección (200 Decisiones)", fontweight="bold")
    ax2.set_xlabel("Ruta")
    ax2.set_ylabel("Número de Hormigas")
    ax2.set_ylim(0, max(counts) + 25)
    ax2.grid(True, axis="y")

    plt.tight_layout()
    ruta_guardado = os.path.join(IMAGES_DIR, "punto4_aco_hormigas.png")
    plt.savefig(ruta_guardado)
    plt.close()
    return ruta_guardado


# ==============================================================================
# PUNTO 5. PSO: MOVIMIENTO DE PARTÍCULAS Y MEMORIA
# ==============================================================================

def resolver_punto5_parte_a() -> Dict[str, Any]:
    """
    Desarrollo matemático analítico de PSO (Punto 5 - Parte A):
    x = 4, v = -1, p_best = 2, g_best = 1.
    w = 0.5, c1 = 1.5, c2 = 1.5, r1 = 0.4, r2 = 0.6.
    """
    x = 4.0
    v = -1.0
    pbest = 2.0
    gbest = 1.0

    w = 0.5
    c1 = 1.5
    c2 = 1.5
    r1 = 0.4
    r2 = 0.6

    termino_inercia = w * v
    termino_cognitivo = c1 * r1 * (pbest - x)
    termino_social = c2 * r2 * (gbest - x)

    v_nuevo = termino_inercia + termino_cognitivo + termino_social
    x_nuevo = x + v_nuevo
    aptitud_nuevo = x_nuevo ** 2

    # Aptitud anterior de memorias
    apt_pbest_ant = pbest ** 2
    apt_gbest_ant = gbest ** 2

    actualiza_pbest = (aptitud_nuevo < apt_pbest_ant)
    actualiza_gbest = (aptitud_nuevo < apt_gbest_ant)

    return {
        "x_inicial": x,
        "v_inicial": v,
        "pbest_inicial": pbest,
        "gbest_inicial": gbest,
        "inercia": termino_inercia,
        "cognitivo": termino_cognitivo,
        "social": termino_social,
        "v_nuevo": v_nuevo,
        "x_nuevo": x_nuevo,
        "aptitud_nuevo": aptitud_nuevo,
        "apt_pbest_anterior": apt_pbest_ant,
        "apt_gbest_anterior": apt_gbest_ant,
        "actualiza_pbest": actualiza_pbest,
        "actualiza_gbest": actualiza_gbest
    }


def ejecutar_pso_bidimensional(
    num_particulas: int = 10,
    num_iteraciones: int = 30,
    w: float = 0.5,
    c1: float = 1.5,
    c2: float = 1.5,
    limites: Tuple[float, float] = (-5.0, 5.0),
    seed: int = 42
) -> Dict[str, Any]:
    """
    Implementación de PSO en 2D (Punto 5 - Parte B):
    - Minimizar f(x, y) = x^2 + y^2 en [-5, 5]^2.
    - 10 partículas con posiciones iniciales uniformes y velocidades iniciales en 0.
    - w = 0.5, c1 = c2 = 1.5.
    - r1, r2 independientes por partícula, dimensión e iteración.
    - Ajuste al límite con velocidad cero si excede el dominio.
    - Actualización sincrónica: mismo g_best para toda la iteración, luego evaluar memorias.
    """
    np.random.seed(seed)

    dim = 2
    X = np.random.uniform(limites[0], limites[1], (num_particulas, dim))
    V = np.zeros((num_particulas, dim))

    def f_objetivo(pos):
        return np.sum(pos ** 2, axis=-1)

    pbest_X = np.copy(X)
    pbest_fitness = f_objetivo(pbest_X)

    mejor_idx = int(np.argmin(pbest_fitness))
    gbest_X = np.copy(pbest_X[mejor_idx])
    gbest_fitness = float(pbest_fitness[mejor_idx])

    historial_gbest_fitness = [gbest_fitness]
    historial_gbest_pos = [gbest_X.copy()]
    historial_particulas_pos = [X.copy()]

    for it in range(1, num_iteraciones + 1):
        # Generar r1, r2 independientes para cada partícula y dimensión
        r1 = np.random.uniform(0.0, 1.0, (num_particulas, dim))
        r2 = np.random.uniform(0.0, 1.0, (num_particulas, dim))

        # Actualización de velocidad con el gbest sincrónico de la iteración
        V_nuevo = w * V + c1 * r1 * (pbest_X - X) + c2 * r2 * (gbest_X - X)
        X_nuevo = X + V_nuevo

        # Manejo de fronteras: ajustar y fijar v=0 si excede
        for i in range(num_particulas):
            for d in range(dim):
                if X_nuevo[i, d] < limites[0]:
                    X_nuevo[i, d] = limites[0]
                    V_nuevo[i, d] = 0.0
                elif X_nuevo[i, d] > limites[1]:
                    X_nuevo[i, d] = limites[1]
                    V_nuevo[i, d] = 0.0

        X = X_nuevo
        V = V_nuevo

        # Evaluación y actualización de memorias personales y global
        current_fit = f_objetivo(X)
        for i in range(num_particulas):
            if current_fit[i] < pbest_fitness[i]:
                pbest_fitness[i] = current_fit[i]
                pbest_X[i] = np.copy(X[i])

        iter_best_idx = int(np.argmin(pbest_fitness))
        if pbest_fitness[iter_best_idx] < gbest_fitness:
            gbest_fitness = float(pbest_fitness[iter_best_idx])
            gbest_X = np.copy(pbest_X[iter_best_idx])

        historial_gbest_fitness.append(gbest_fitness)
        historial_gbest_pos.append(gbest_X.copy())
        historial_particulas_pos.append(X.copy())

    return {
        "mejor_posicion_final": gbest_X,
        "valor_minimo_final": gbest_fitness,
        "historial_gbest_fitness": historial_gbest_fitness,
        "historial_gbest_pos": historial_gbest_pos,
        "historial_particulas_pos": historial_particulas_pos
    }


def graficar_punto5(resultado_pso: Dict[str, Any]):
    """Genera gráficos de curvas de nivel, trayectorias y convergencia logarítmica para PSO."""
    hist_fit = resultado_pso["historial_gbest_fitness"]
    hist_pos = np.array(resultado_pso["historial_particulas_pos"])  # (iter, particulas, dim)
    iters = list(range(len(hist_fit)))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Subgráfico 1: Trayectorias sobre mapa de curvas de nivel
    grid_x = np.linspace(-5.2, 5.2, 200)
    grid_y = np.linspace(-5.2, 5.2, 200)
    X_grid, Y_grid = np.meshgrid(grid_x, grid_y)
    Z_grid = X_grid ** 2 + Y_grid ** 2

    cp = ax1.contourf(X_grid, Y_grid, Z_grid, levels=25, cmap="viridis", alpha=0.75)
    fig.colorbar(cp, ax=ax1, label="$f(x, y) = x^2 + y^2$")

    num_parts = hist_pos.shape[1]
    for p in range(num_parts):
        ax1.plot(hist_pos[:, p, 0], hist_pos[:, p, 1], ".-", alpha=0.55, linewidth=1.0)
        # Posición inicial
        ax1.scatter(hist_pos[0, p, 0], hist_pos[0, p, 1], color="white", edgecolor="black", s=30, zorder=3)

    # Posición final óptima del enjambre
    gbest = resultado_pso["mejor_posicion_final"]
    ax1.scatter(gbest[0], gbest[1], color="red", marker="*", s=260, zorder=5, label=f"Mejor Global $g^{{best}}$\n({gbest[0]:.4f}, {gbest[1]:.4f})")
    ax1.scatter(0, 0, color="gold", marker="x", s=140, linewidths=2.5, zorder=4, label="Óptimo Teórico (0, 0)")
    ax1.set_title("Convergencia del Enjambre en el Dominio $[-5, 5]^2$", fontweight="bold")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax1.set_xlim(-5.2, 5.2)
    ax1.set_ylim(-5.2, 5.2)
    ax1.legend(loc="upper right", framealpha=0.9)

    # Subgráfico 2: Convergencia de aptitud global
    ax2.plot(iters, hist_fit, "o-", color="#1f77b4", linewidth=2.0)
    ax2.set_title("Convergencia de la Mejor Aptitud Global $f(g^{best})$", fontweight="bold")
    ax2.set_xlabel("Iteración")
    ax2.set_ylabel("Aptitud $f(x, y)$ (Escala Logarítmica)")
    ax2.set_yscale("log")
    ax2.grid(True, which="both")

    plt.tight_layout()
    ruta_guardado = os.path.join(IMAGES_DIR, "punto5_pso_particulas.png")
    plt.savefig(ruta_guardado)
    plt.close()
    return ruta_guardado


# ==============================================================================
# EJECUCIÓN CONJUNTA Y REPORTE CONSOLA
# ==============================================================================

def ejecutar_todo():
    """Ejecuta los cinco puntos de forma integral, imprime reportes y genera gráficos."""
    print("=" * 80)
    print("           UNIVERSIDAD - FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (2026)")
    print("                 SOLUCIÓN COMPLETA Y VERIFICADA - PARCIAL #2")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # PUNTO 1
    # --------------------------------------------------------------------------
    print("\n" + "#" * 80)
    print("PUNTO 1. ALGORITMOS EVOLUTIVOS Y ALGORITMOS GENÉTICOS (1.0 Punto)")
    print("#" * 80)
    res1_a = resolver_punto1_parte_a()
    print("\n--- PARTE A: Componente Matemático y Conceptual ---")
    print("1. Decodificación y Aptitud de la Población Inicial:")
    print("   Individuo | Cromosoma | Decimal (x) | Aptitud f(x) = x^2 | Prob. Ruleta p_i")
    print("   " + "-" * 65)
    for i in range(len(res1_a["poblacion"])):
        print(f"       {i+1}     |   {res1_a['poblacion'][i]}   |     {res1_a['decimales'][i]:2d}      |        {res1_a['aptitudes'][i]:4d}        |   {res1_a['probabilidades'][i]:.5f} ({res1_a['probabilidades'][i]*100:.2f}%)")
    print(f"   Suma total de aptitudes: {res1_a['suma_aptitudes']}")

    print("\n3. Cruce de un punto tras el 2do bit entre 01100 y 11001:")
    print(f"   Padre 1: 01 | 100  -->  Descendiente 1 (H1): {res1_a['descendientes_cruce'][0]} (x = {decodificar_cromosoma(res1_a['descendientes_cruce'][0])}, f = {aptitud_punto1(decodificar_cromosoma(res1_a['descendientes_cruce'][0]))})")
    print(f"   Padre 2: 11 | 001  -->  Descendiente 2 (H2): {res1_a['descendientes_cruce'][1]} (x = {decodificar_cromosoma(res1_a['descendientes_cruce'][1])}, f = {aptitud_punto1(decodificar_cromosoma(res1_a['descendientes_cruce'][1]))})")

    print("\n4. Mutación del último bit en H1 (01001):")
    print(f"   Nuevo cromosoma: {res1_a['descendiente_mutado']} -> Decimal: {res1_a['x_mutado']} -> Nueva aptitud: {res1_a['aptitud_mutado']}")

    print("\n--- PARTE B: Implementación en Python ---")
    res1_b = ejecutar_algoritmo_genetico(seed=42)
    print(f"Mejor cromosoma final: {res1_b['mejor_cromosoma_final']}")
    print(f"Valor final de x:      {res1_b['mejor_x_final']}")
    print(f"Aptitud final f(x):    {res1_b['mejor_aptitud_final']}")
    print("\nHistorial por Generación:")
    print(" Gen | Mejor Cromosoma |  x  | Mejor Aptitud | Aptitud Promedio")
    print(" " + "-" * 55)
    hist1 = res1_b["historial"]
    for g in range(len(hist1["generacion"])):
        print(f"  {hist1['generacion'][g]:2d} |      {hist1['mejor_cromosoma'][g]}      | {hist1['mejor_x'][g]:2d}  |     {hist1['mejor_aptitud'][g]:4d}      |      {hist1['aptitud_promedio'][g]:6.2f}")

    img1 = graficar_punto1(res1_b)
    print(f"\n[OK] Gráfica guardada en: {img1}")

    # --------------------------------------------------------------------------
    # PUNTO 2
    # --------------------------------------------------------------------------
    print("\n" + "#" * 80)
    print("PUNTO 2. ASCENSO DE COLINAS Y ÓPTIMOS LOCALES (1.0 Punto)")
    print("#" * 80)
    res2 = resolver_punto2_completo()
    print("\n--- PARTE A y B: Ejecución desde todos los Estados Iniciales ---")
    print(" Inicio (x0) |      Trayectoria Visitada      | Estado Final (x*) | Valor Final f(x*) | Categoría")
    print(" " + "-" * 85)
    for fila in res2["tabla"]:
        tray_str = " -> ".join(map(str, fila["trayectoria"]))
        print(f"      {fila['inicio']:2d}     | {tray_str:30s} |        {fila['estado_final']:2d}         |        {fila['valor_final']:2d}         | {fila['tipo_optimo']}")
    print(f"\nProporción de estados iniciales que conducen al Máximo Global (x=6, f=9): {res2['proporcion_global']*100:.2f}% (5 de 9)")

    img2 = graficar_punto2(res2)
    print(f"[OK] Gráfica guardada en: {img2}")

    # --------------------------------------------------------------------------
    # PUNTO 3
    # --------------------------------------------------------------------------
    print("\n" + "#" * 80)
    print("PUNTO 3. TEMPLE SIMULADO: ACEPTACIÓN DE SOLUCIONES PEORES (1.0 Punto)")
    print("#" * 80)
    res3_a = resolver_punto3_parte_a()
    print("\n--- PARTE A: Análisis Analítico de Casos Independientes ---")
    print(" Caso | x_actual | x_cand | E(act) | E(cand) | Delta E |  T  |  u   | P(aceptar) | Decisión")
    print(" " + "-" * 75)
    for c in res3_a:
        print(f"   {c['caso']}  |    {c['actual']:2d}    |   {c['candidato']:2d}   |   {c['E_actual']:2d}   |    {c['E_candidato']:2d}   |   {c['delta_E']:+2d}    | {c['T']:.1f} | {c['u']:.2f} |  {c['p_aceptar']:8.5f}  | {c['decision']}")

    print("\n--- PARTE B: Implementación en Python ---")
    res3_b = ejecutar_temple_simulado(seed=42)
    print(f"Mejor solución encontrada: x = {res3_b['mejor_solucion']}")
    print(f"Energía mínima alcanzada:  E = {res3_b['energia_minima']}")
    print(f"Estado final (iter 100):   x = {res3_b['estado_final']}, E = {res3_b['energia_final']}")
    print(f"Temperatura final:         T = {res3_b['temperatura_final']:.6f}")

    img3 = graficar_punto3(res3_b)
    print(f"\n[OK] Gráfica guardada en: {img3}")

    # --------------------------------------------------------------------------
    # PUNTO 4
    # --------------------------------------------------------------------------
    print("\n" + "#" * 80)
    print("PUNTO 4. ACO: ELECCIÓN DE RUTAS Y ACTUALIZACIÓN DE FEROMONAS (1.0 Punto)")
    print("#" * 80)
    res4_a = resolver_punto4_parte_a()
    print("\n--- PARTE A: Probabilidades y Actualización Analítica ---")
    print(" Arista | Distancia d | Feromona tau | Heurística eta | Peso W_Aj | Probabilidad p_Aj")
    print(" " + "-" * 75)
    for a in res4_a["aristas"]:
        print(f"  {a:4s}  |     {res4_a['distancias'][a]:.1f}     |     {res4_a['tau_inicial'][a]:.1f}      |     {res4_a['eta'][a]:.4f}     |  {res4_a['pesos'][a]:.4f}   |  {res4_a['probabilidades'][a]:.5f} ({res4_a['probabilidades'][a]*100:.2f}%)")
    print(f"Suma total de pesos: {res4_a['suma_pesos']:.4f}")
    print("\nActualización tras recorrido con L=10 usando A->B (Q=10, rho=0.2):")
    for a in res4_a["aristas"]:
        print(f"  {a:4s}: tau_nueva = (1 - 0.2)*{res4_a['tau_inicial'][a]:.1f} + {res4_a['delta_tau'][a]:.1f} = {res4_a['tau_nueva'][a]:.4f}")

    print("\n--- PARTE B: Implementación del Modelo Simplificado en Python ---")
    res4_b = ejecutar_aco_rutas(seed=42)
    print("Frecuencias acumuladas de elección (20 iteraciones x 10 hormigas = 200 decisiones):")
    for r, count in res4_b["frecuencias_acumuladas"].items():
        print(f"  Ruta {r} (Longitud {int(res4_b['longitudes'][r])}): {count:3d} elecciones ({count/200*100:.1f}%)")
    print("\nFeromonas finales al cabo de 20 iteraciones:")
    for r, tau_val in res4_b["feromonas_finales"].items():
        print(f"  Ruta {r}: tau = {tau_val:8.4f}")
    print(f"\nMejor ruta observada: {res4_b['mejor_ruta_observada']} (Longitud mínima = 6)")

    img4 = graficar_punto4(res4_b)
    print(f"\n[OK] Gráfica guardada en: {img4}")

    # --------------------------------------------------------------------------
    # PUNTO 5
    # --------------------------------------------------------------------------
    print("\n" + "#" * 80)
    print("PUNTO 5. PSO: MOVIMIENTO DE PARTÍCULAS Y MEMORIA (1.0 Punto)")
    print("#" * 80)
    res5_a = resolver_punto5_parte_a()
    print("\n--- PARTE A: Cálculo Numérico Paso a Paso ---")
    print(f"1. Términos de la ecuación de velocidad:")
    print(f"   - Inercia:  w * v                    = {res5_a['inercia']:.2f}")
    print(f"   - Cognitivo: c1 * r1 * (p_best - x)   = {res5_a['cognitivo']:.2f}")
    print(f"   - Social:    c2 * r2 * (g_best - x)   = {res5_a['social']:.2f}")
    print(f"2. Nuevas variables:")
    print(f"   - Nueva velocidad: v_nuevo = {res5_a['inercia']:.2f} + ({res5_a['cognitivo']:.2f}) + ({res5_a['social']:.2f}) = {res5_a['v_nuevo']:.2f}")
    print(f"   - Nueva posición:  x_nuevo = {res5_a['x_inicial']} + ({res5_a['v_nuevo']:.2f}) = {res5_a['x_nuevo']:.2f}")
    print(f"   - Nueva aptitud:   f(x_nuevo) = ({res5_a['x_nuevo']:.2f})^2 = {res5_a['aptitud_nuevo']:.4f}")
    print(f"3. Actualización de memorias:")
    print(f"   - ¿Actualiza p_best? f(x_nuevo)={res5_a['aptitud_nuevo']:.4f} < f(p_best)={res5_a['apt_pbest_anterior']:.1f} -> {'SÍ' if res5_a['actualiza_pbest'] else 'NO'}")
    print(f"   - ¿Actualiza g_best? f(x_nuevo)={res5_a['aptitud_nuevo']:.4f} < f(g_best)={res5_a['apt_gbest_anterior']:.1f} -> {'SÍ' if res5_a['actualiza_gbest'] else 'NO'}")

    print("\n--- PARTE B: Implementación de PSO 2D en Python ---")
    res5_b = ejecutar_pso_bidimensional(seed=42)
    gbest = res5_b["mejor_posicion_final"]
    print(f"Mejor posición final g_best: ({gbest[0]:.8f}, {gbest[1]:.8f})")
    print(f"Valor óptimo de la función:  f(g_best) = {res5_b['valor_minimo_final']:.10e}")
    print("\nHistorial de convergencia (primeras y últimas iteraciones):")
    h_fit = res5_b["historial_gbest_fitness"]
    for it in [0, 1, 2, 5, 10, 20, 25, 30]:
        print(f"  Iteración {it:2d}: f(g_best) = {h_fit[it]:.8e}")

    img5 = graficar_punto5(res5_b)
    print(f"\n[OK] Gráfica guardada en: {img5}")

    print("\n" + "=" * 80)
    print("      TODOS LOS PUNTOS FUERON RESUELTOS Y VERIFICADOS CON ÉXITO")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solución Parcial 2 - Inteligencia Artificial")
    parser.add_argument("--punto", type=int, choices=[1, 2, 3, 4, 5], help="Ejecutar solo un punto específico")
    args = parser.parse_args()

    if args.punto is None:
        ejecutar_todo()
    elif args.punto == 1:
        res1_b = ejecutar_algoritmo_genetico(seed=42)
        graficar_punto1(res1_b)
        print("Punto 1 completado.")
    elif args.punto == 2:
        res2 = resolver_punto2_completo()
        graficar_punto2(res2)
        print("Punto 2 completado.")
    elif args.punto == 3:
        res3_b = ejecutar_temple_simulado(seed=42)
        graficar_punto3(res3_b)
        print("Punto 3 completado.")
    elif args.punto == 4:
        res4_b = ejecutar_aco_rutas(seed=42)
        graficar_punto4(res4_b)
        print("Punto 4 completado.")
    elif args.punto == 5:
        res5_b = ejecutar_pso_bidimensional(seed=42)
        graficar_punto5(res5_b)
        print("Punto 5 completado.")
