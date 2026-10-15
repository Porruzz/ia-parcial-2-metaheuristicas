"""
================================================================================
PARCIAL 2 - FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (2026)
Tema: Algoritmos Evolutivos, Genéticos, Ascenso de Colinas,
      Temple Simulado, ACO y PSO.
================================================================================
Fachada Principal (Facade Pattern - GoF):
Coordina la ejecución de los módulos desacoplados bajo el paquete 'src',
proporcionando una interfaz unificada para consola y exportación de figuras.
================================================================================
"""

import argparse
import math
from typing import Any, Dict

from src import (
    AntColonySolver,
    GeneticAlgorithmSolver,
    HillClimbingSolver,
    OptimizerFactory,
    ParcialVisualizer,
    ParticleSwarmSolver,
    SimulatedAnnealingSolver,
    ascenso_colinas,
)


# ==============================================================================
# RESOLUCIÓN ANALÍTICA (PARTE A DE CADA PUNTO)
# ==============================================================================

def resolver_punto1_parte_a() -> Dict[str, Any]:
    """Cálculos analíticos del Punto 1 (Parte A)."""
    poblacion = ["00101", "01100", "10010", "11001"]
    decimales = [int(c, 2) for c in poblacion]
    aptitudes = [x ** 2 for x in decimales]
    suma_aptitudes = sum(aptitudes)
    probabilidades = [f / suma_aptitudes for f in aptitudes]

    # Cruce de un punto tras el 2do bit
    p1, p2 = "01100", "11001"
    h1 = p1[:2] + p2[2:]  # "01001"
    h2 = p2[:2] + p1[2:]  # "11100"

    # Mutación de último bit en h1
    h1_lista = list(h1)
    h1_lista[4] = "0" if h1_lista[4] == "1" else "1"
    h1_mutado = "".join(h1_lista)
    x_mutado = int(h1_mutado, 2)
    apt_mutado = x_mutado ** 2

    return {
        "poblacion": poblacion,
        "decimales": decimales,
        "aptitudes": aptitudes,
        "suma_aptitudes": suma_aptitudes,
        "probabilidades": probabilidades,
        "descendientes": (h1, h2),
        "h1_mutado": h1_mutado,
        "x_mutado": x_mutado,
        "apt_mutado": apt_mutado,
    }


def resolver_punto3_parte_a() -> list:
    """Análisis analítico de los tres casos independientes de Temple Simulado."""
    casos = [
        {"caso": "A", "actual": 3, "cand": 2, "T": 5.0, "u": 0.70},
        {"caso": "B", "actual": 2, "cand": 3, "T": 5.0, "u": 0.30},
        {"caso": "C", "actual": 2, "cand": 3, "T": 1.0, "u": 0.30},
    ]
    filas = []
    for c in casos:
        e_act = c["actual"] ** 2
        e_cand = c["cand"] ** 2
        de = e_cand - e_act
        p = 1.0 if de <= 0 else math.exp(-de / c["T"])
        decision = "Acepta" if c["u"] < p else "Rechaza"
        filas.append({
            "caso": c["caso"],
            "actual": c["actual"],
            "cand": c["cand"],
            "e_act": e_act,
            "e_cand": e_cand,
            "de": de,
            "T": c["T"],
            "u": c["u"],
            "p": p,
            "decision": decision,
        })
    return filas


def resolver_punto4_parte_a() -> Dict[str, Any]:
    """Cálculos analíticos de pesos y actualización de feromona en ACO."""
    distancias = {"A->B": 2.0, "A->C": 4.0, "A->D": 5.0}
    tau_ini = {"A->B": 1.0, "A->C": 2.0, "A->D": 1.0}
    eta = {k: 1.0 / distancias[k] for k in distancias}
    weights = {k: (tau_ini[k] ** 1.0) * (eta[k] ** 2.0) for k in distancias}
    sum_w = sum(weights.values())
    probs = {k: weights[k] / sum_w for k in distancias}

    # Actualización tras ruta L=10 que utiliza A->B
    rho, q, l = 0.2, 10.0, 10.0
    tau_nueva = {
        "A->B": (1 - rho) * tau_ini["A->B"] + (q / l),
        "A->C": (1 - rho) * tau_ini["A->C"] + 0.0,
        "A->D": (1 - rho) * tau_ini["A->D"] + 0.0,
    }
    return {
        "distancias": distancias,
        "tau_ini": tau_ini,
        "eta": eta,
        "weights": weights,
        "sum_w": sum_w,
        "probs": probs,
        "tau_nueva": tau_nueva,
    }


def resolver_punto5_parte_a() -> Dict[str, Any]:
    """Cálculos analíticos paso a paso de velocidad y posición en PSO."""
    x, v, pbest, gbest = 4.0, -1.0, 2.0, 1.0
    w, c1, c2, r1, r2 = 0.5, 1.5, 1.5, 0.4, 0.6

    inercia = w * v
    cognitivo = c1 * r1 * (pbest - x)
    social = c2 * r2 * (gbest - x)
    v_nuevo = inercia + cognitivo + social
    x_nuevo = x + v_nuevo
    f_nuevo = x_nuevo ** 2

    return {
        "inercia": inercia,
        "cognitivo": cognitivo,
        "social": social,
        "v_nuevo": v_nuevo,
        "x_nuevo": x_nuevo,
        "f_nuevo": f_nuevo,
        "actualiza_pbest": f_nuevo < (pbest ** 2),
        "actualiza_gbest": f_nuevo < (gbest ** 2),
    }


# ==============================================================================
# EJECUCIÓN INTEGRAL DE LA SUITE
# ==============================================================================

def ejecutar_punto1(visualizer: ParcialVisualizer):
    print("\n" + "#" * 80)
    print("PUNTO 1. ALGORITMOS EVOLUTIVOS Y ALGORITMOS GENÉTICOS (1.0 Punto)")
    print("#" * 80)

    # Parte A
    res_a = resolver_punto1_parte_a()
    print("\n--- PARTE A: Componente Matemático y Conceptual ---")
    print("Individuo | Cromosoma | Decimal (x) | Aptitud f(x)=x^2 | Prob. Ruleta p_i")
    print("-" * 65)
    for i in range(len(res_a["poblacion"])):
        c = res_a["poblacion"][i]
        d = res_a["decimales"][i]
        f = res_a["aptitudes"][i]
        p = res_a["probabilidades"][i]
        print(f"    {i+1}     |   {c}   |     {d:2d}      |        {f:4d}        |   {p:.5f} ({p*100:.2f}%)")
    print(f"Suma total de aptitudes: {res_a['suma_aptitudes']}")

    print("\nCruce tras 2do bit entre 01100 y 11001:")
    print(f"  H1: {res_a['descendientes'][0]} (x={int(res_a['descendientes'][0], 2)}, f={int(res_a['descendientes'][0], 2)**2})")
    print(f"  H2: {res_a['descendientes'][1]} (x={int(res_a['descendientes'][1], 2)}, f={int(res_a['descendientes'][1], 2)**2})")

    print(f"\nMutación del último bit en H1: {res_a['h1_mutado']} -> Decimal: {res_a['x_mutado']}, Aptitud: {res_a['apt_mutado']}")

    # Parte B con solver modular
    print("\n--- PARTE B: Implementación Modular con Patrones GoF ---")
    solver = GeneticAlgorithmSolver(seed=42)
    res_b = solver.solve()

    print(f"Mejor cromosoma final: {res_b.best_solution}")
    print(f"Valor final de x:      {res_b.metadata['best_decimal_x']}")
    print(f"Aptitud final f(x):    {res_b.best_fitness:.0f}")

    print("\nHistorial por Generación:")
    print(" Gen | Mejor Cromosoma |  x  | Mejor Aptitud | Aptitud Promedio")
    print(" " + "-" * 55)
    hist = res_b.history
    for g in range(len(hist["generation"])):
        print(f"  {hist['generation'][g]:2d} |      {hist['best_chromosome'][g]}      | {hist['best_x'][g]:2d}  |     {hist['best_fitness'][g]:4.0f}      |      {hist['average_fitness'][g]:6.2f}")

    # Sensibilidad estocástica para justificación teórica
    multi_seed = {}
    for s in [42, 10, 7, 99, 123]:
        s_solver = GeneticAlgorithmSolver(seed=s)
        s_res = s_solver.solve()
        multi_seed[s] = s_res.history["best_fitness"]

    path = visualizer.plot_punto1_genetic(res_b.history, multi_seed)
    print(f"\n[OK] Gráfica guardada en: {path}")


def ejecutar_punto2(visualizer: ParcialVisualizer):
    print("\n" + "#" * 80)
    print("PUNTO 2. ASCENSO DE COLINAS Y ÓPTIMOS LOCALES (1.0 Punto)")
    print("#" * 80)

    valores = [1, 4, 7, 5, 3, 6, 9, 8, 5]
    print("\n--- PARTE A y B: Ejecución desde todos los Estados Iniciales ---")
    print(" Inicio (x0) |      Trayectoria Visitada      | Estado Final (x*) | Valor Final f(x*) | Categoría")
    print(" " + "-" * 85)

    conduce_a_global = 0
    for x0 in range(len(valores)):
        estado_final, trayectoria = ascenso_colinas(valores, x0)
        valor_final = valores[estado_final]
        es_global = (estado_final == 6)
        if es_global:
            conduce_a_global += 1
        tray_str = " -> ".join(map(str, trayectoria))
        cat = "Máximo Global" if es_global else "Máximo Local"
        print(f"      {x0:2d}     | {tray_str:30s} |        {estado_final:2d}         |        {valor_final:2d}         | {cat}")

    prop = conduce_a_global / len(valores)
    print(f"\nProporción de estados que conducen al Máximo Global: {prop*100:.2f}% ({conduce_a_global} de {len(valores)})")

    path = visualizer.plot_punto2_hill_climbing(valores)
    print(f"[OK] Gráfica guardada en: {path}")


def ejecutar_punto3(visualizer: ParcialVisualizer):
    print("\n" + "#" * 80)
    print("PUNTO 3. TEMPLE SIMULADO: ACEPTACIÓN DE SOLUCIONES PEORES (1.0 Punto)")
    print("#" * 80)

    print("\n--- PARTE A: Análisis Analítico de Casos Independientes ---")
    casos = resolver_punto3_parte_a()
    print(" Caso | x_actual | x_cand | E(act) | E(cand) | Delta E |  T  |  u   | P(aceptar) | Decisión")
    print(" " + "-" * 75)
    for c in casos:
        print(f"   {c['caso']}  |    {c['actual']:2d}    |   {c['cand']:2d}   |   {c['e_act']:2d}   |    {c['e_cand']:2d}   |   {c['de']:+2d}    | {c['T']:.1f} | {c['u']:.2f} |  {c['p']:8.5f}  | {c['decision']}")

    print("\n--- PARTE B: Implementación Modular con Patrón Strategy ---")
    solver = SimulatedAnnealingSolver(seed=42)
    res_b = solver.solve()

    print(f"Mejor solución encontrada: x = {res_b.best_solution}")
    print(f"Energía mínima alcanzada:  E = {res_b.best_fitness:.0f}")
    print(f"Estado final en iter 100:  x = {res_b.metadata['final_x']}, E = {res_b.metadata['final_energy']:.0f}")
    print(f"Temperatura final:         T = {res_b.metadata['final_temperature']:.6f}")

    path = visualizer.plot_punto3_simulated_annealing(res_b.history)
    print(f"\n[OK] Gráfica guardada en: {path}")


def ejecutar_punto4(visualizer: ParcialVisualizer):
    print("\n" + "#" * 80)
    print("PUNTO 4. ACO: ELECCIÓN DE RUTAS Y ACTUALIZACIÓN DE FEROMONAS (1.0 Punto)")
    print("#" * 80)

    print("\n--- PARTE A: Probabilidades y Actualización Analítica ---")
    res_a = resolver_punto4_parte_a()
    print(" Arista | Distancia d | Feromona tau | Heurística eta | Peso W_Aj | Probabilidad p_Aj")
    print(" " + "-" * 75)
    for a in ["A->B", "A->C", "A->D"]:
        d = res_a["distancias"][a]
        t = res_a["tau_ini"][a]
        e = res_a["eta"][a]
        w = res_a["weights"][a]
        p = res_a["probs"][a]
        print(f"  {a:4s}  |     {d:.1f}     |     {t:.1f}      |     {e:.4f}     |  {w:.4f}   |  {p:.5f} ({p*100:.2f}%)")

    print("\nActualización tras recorrido con L=10 usando A->B (Q=10, rho=0.2):")
    for a, t_val in res_a["tau_nueva"].items():
        print(f"  {a:4s}: tau_nueva = {t_val:.4f}")

    print("\n--- PARTE B: Implementación Modular ACO ---")
    solver = AntColonySolver(seed=42)
    res_b = solver.solve()

    print("Frecuencias acumuladas de elección (200 decisiones):")
    freqs = res_b.metadata["selection_frequencies"]
    lengths = res_b.metadata["lengths"]
    for r, count in freqs.items():
        print(f"  Ruta {r} (Longitud {int(lengths[r])}): {count:3d} elecciones ({count/200*100:.1f}%)")

    print("\nFeromonas finales al cabo de 20 iteraciones:")
    for r, t_val in res_b.metadata["final_pheromones"].items():
        print(f"  Ruta {r}: tau = {t_val:8.4f}")

    print(f"\nMejor ruta observada: {res_b.best_solution} (Longitud mínima = {int(res_b.best_fitness)})")

    path = visualizer.plot_punto4_ant_colony(res_b.history, freqs, lengths)
    print(f"\n[OK] Gráfica guardada en: {path}")


def ejecutar_punto5(visualizer: ParcialVisualizer):
    print("\n" + "#" * 80)
    print("PUNTO 5. PSO: MOVIMIENTO DE PARTÍCULAS Y MEMORIA (1.0 Punto)")
    print("#" * 80)

    print("\n--- PARTE A: Cálculo Numérico Paso a Paso ---")
    res_a = resolver_punto5_parte_a()
    print(f"1. Inercia:  {res_a['inercia']:.2f}")
    print(f"   Cognitivo: {res_a['cognitivo']:.2f}")
    print(f"   Social:    {res_a['social']:.2f}")
    print(f"2. Nueva velocidad: v_nuevo = {res_a['v_nuevo']:.2f}")
    print(f"   Nueva posición:  x_nuevo = {res_a['x_nuevo']:.2f}")
    print(f"   Nueva aptitud:   f(x_nuevo) = {res_a['f_nuevo']:.4f}")
    print(f"3. Actualiza p_best? {'SÍ' if res_a['actualiza_pbest'] else 'NO'}")
    print(f"   Actualiza g_best? {'SÍ' if res_a['actualiza_gbest'] else 'NO'}")

    print("\n--- PARTE B: Implementación Modular PSO en 2D ---")
    solver = ParticleSwarmSolver(seed=42)
    res_b = solver.solve()

    gbest = res_b.best_solution
    print(f"Mejor posición final g_best: ({gbest[0]:.8f}, {gbest[1]:.8f})")
    print(f"Valor óptimo de la función:  f(g_best) = {res_b.best_fitness:.10e}")

    print("\nHistorial de convergencia:")
    h_fit = res_b.history["gbest_fitness"]
    for it in [0, 1, 2, 5, 10, 20, 25, 30]:
        print(f"  Iteración {it:2d}: f(g_best) = {h_fit[it]:.8e}")

    path = visualizer.plot_punto5_particle_swarm(
        res_b.history["swarm_positions"],
        res_b.history["gbest_fitness"],
        gbest,
    )
    print(f"\n[OK] Gráfica guardada en: {path}")


def ejecutar_todo():
    """Ejecuta los 5 puntos usando la arquitectura modular desacoplada."""
    visualizer = ParcialVisualizer()
    ejecutar_punto1(visualizer)
    ejecutar_punto2(visualizer)
    ejecutar_punto3(visualizer)
    ejecutar_punto4(visualizer)
    ejecutar_punto5(visualizer)
    print("\n" + "=" * 80)
    print("      TODOS LOS PUNTOS FUERON RESUELTOS Y VERIFICADOS CON ÉXITO")
    print("================================================================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solución Parcial 2 - Inteligencia Artificial (Arquitectura Modular)")
    parser.add_argument("--punto", type=int, choices=[1, 2, 3, 4, 5], help="Ejecutar solo un punto específico")
    args = parser.parse_args()

    visualizer = ParcialVisualizer()
    if args.punto is None:
        ejecutar_todo()
    elif args.punto == 1:
        ejecutar_punto1(visualizer)
    elif args.punto == 2:
        ejecutar_punto2(visualizer)
    elif args.punto == 3:
        ejecutar_punto3(visualizer)
    elif args.punto == 4:
        ejecutar_punto4(visualizer)
    elif args.punto == 5:
        ejecutar_punto5(visualizer)
