# ui/visualizador.py
from __future__ import annotations

# Permite ejecutar este archivo directo: python ui/visualizador.py
if __name__ in {"__main__", "__mp_main__"}:
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import Optional, List
import os
import shutil
import sys

from core.simulador import Simulador
from models.persona import Persona


class Visualizador:
    """
    Visualización en consola de:
      - Matriz con celdas coloreadas (verde: sanas, rojo: infectadas)
      - Árbol de contagio (vía método visualizar del árbol)
      - Tabla de personas (id, posición, defensa, estado)
    Todo con nombres claros y sin dependencias externas.
    """

    def __init__(self, usar_color: bool = True) -> None:
        self.usar_color: bool = usar_color and self._soporta_color()

    # ---------- Público ----------
    def mostrar_matriz(self, sim: Simulador) -> None:
        print("\n--- MATRIZ ---")
        print(self._render_matriz(sim))

    def mostrar_arbol(self, sim: Simulador) -> None:
        print("\n--- ÁRBOL DE CONTAGIO ---")
        print(sim.get_arbol().visualizar())

    def mostrar_tabla_personas(self, sim: Simulador) -> None:
        print("\n--- PERSONAS (vida/estado) ---")
        print(self._render_tabla_personas(sim))

    def mostrar_resumen_ronda(self, sim: Simulador, stats: dict) -> None:
        print(f"Ronda {stats.get('ronda','?')}: "
              f"Sanas={stats.get('sanas','?')}, "
              f"Infectadas={stats.get('infectadas','?')}, "
              f"Profundidad árbol={stats.get('profundidad_arbol','?')}")
        self.mostrar_tabla_personas(sim)

    def limpiar_pantalla(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    # ---------- Render internos ----------
    def _render_matriz(self, sim: Simulador) -> str:
        m = sim.get_matriz()
        n = m.get_tamano()  # asumido por tu Matriz
        ancho = shutil.get_terminal_size((80, 20)).columns

        filas: List[str] = []

        # Encabezado de columnas
        encabezado = "   " + " ".join(f"{i:>3}" for i in range(n))
        filas.append(encabezado)

        for y in range(n):
            celdas: List[str] = []
            for x in range(n):
                personas = m.obtener_personas_en(x, y)  # lista[Persona] (puede estar vacía)
                celdas.append(self._celda_str(personas))
            fila = f"{y:>2} " + " ".join(celdas)
            if len(fila) > ancho:
                fila = fila[:ancho - 3] + "..."
            filas.append(fila)

        filas.append("\nLeyenda: . = vacío | verde=sano | rojo=infectado | [k]=k personas")
        return "\n".join(filas)

    def _render_tabla_personas(self, sim: Simulador) -> str:
        personas = sorted(sim.get_personas(), key=lambda p: p.id)
        if not personas:
            return "(sin personas)"
        filas = [f"{'ID':<5} {'POS':<9} {'DEF':>3}  {'ESTADO'}", "-" * 28]
        for p in personas:
            x, y = p.get_posicion()
            estado = "INFECTADA" if p.esta_infectada() else "SANA"
            filas.append(f"{p.id:<5} ({x:>2},{y:>2})  {p.defensa:>3}  {estado}")
        return "\n".join(filas)

    # ---------- Helpers ----------
    def _celda_str(self, personas: List[Persona]) -> str:
        # vacío
        if not personas:
            return self._gris(" . ")

        # si hay varias, mostramos el conteo
        if len(personas) > 1:
            hay_infectada = any(p.esta_infectada() for p in personas)
            base = f"[{len(personas)}]"
            base = f"{base:>3}"[-3:]  # ancho fijo 3
            return self._rojo(base) if hay_infectada else self._verde(base)

        # solo 1 persona
        p = personas[0]
        etiqueta = f"{p.id:>3}"[-3:]  # usa id en 3 chars
        return self._rojo(etiqueta) if p.esta_infectada() else self._verde(etiqueta)

    # Colores ANSI simples
    def _soporta_color(self) -> bool:
        return sys.stdout.isatty() and os.name != "nt" or "ANSICON" in os.environ

    def _color(self, s: str, code: str) -> str:
        if not self.usar_color:
            return s
        return f"{code}{s}\033[0m"

    def _verde(self, s: str) -> str: return self._color(s, "\033[32m")
    def _rojo(self, s: str) -> str:  return self._color(s, "\033[31m")
    def _gris(self, s: str) -> str:  return self._color(s, "\033[90m")



