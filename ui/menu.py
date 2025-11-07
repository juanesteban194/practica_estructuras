# ui/menu.py
from __future__ import annotations

# Permite ejecutar este archivo directo:  python ui/menu.py
if __name__ in {"__main__", "__mp_main__"}:
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import Optional, Any

from core.simulador import Simulador
from ui.visualizador import Visualizador
from models.persona import Persona


class MenuPrincipal:
    """
    Menú de texto simple para manejar la simulación.
    Opciones:
      1) Crear simulador
      2) Inicializar simulación
      3) Ejecutar varias rondas
      4) Curar persona (x, y)
      5) Agregar persona (x, y)
      6) Ver matriz
      7) Ver árbol de contagio
      8) Ver estadísticas
      9) Infectar manualmente por id 
     10) Ver tabla de personas (vida/estado)
      0) Salir\
    """

    def __init__(self) -> None:
        self.simulador: Optional[Simulador] = None
        self.vista: Visualizador = Visualizador()

    # ------------------- BUCLE PRINCIPAL -------------------
    def menu_principal(self) -> None:
        while True:
            self._mostrar_titulo()
            self._mostrar_estado_resumen()

            print("\nOpciones:")
            print(" 1) Crear simulador")
            print(" 2) Inicializar simulación")
            print(" 3) Ejecutar varias rondas (muestra tabla cada ronda)")
            print(" 4) Curar persona (x, y)")
            print(" 5) Agregar persona (x, y)")
            print(" 6) Ver matriz")
            print(" 7) Ver árbol de contagio")
            print(" 8) Ver estadísticas")
            print(" 9) Infectar manualmente por id (además del inicial)")
            print("10) Ver tabla de personas (vida/estado)")
            print(" 0) Salir")

            opcion = input("\nElige una opción: ").strip()

            if opcion == "1":
                self._crear_simulador()
            elif opcion == "2":
                self._inicializar()
            elif opcion == "3":
                self._ejecutar_varias_rondas()
            elif opcion == "4":
                self._curar_persona()
            elif opcion == "5":
                self._agregar_persona()
            elif opcion == "6":
                self._mostrar_matriz()
            elif opcion == "7":
                self._mostrar_arbol()
            elif opcion == "8":
                self._mostrar_estadisticas()
            elif opcion == "9":
                self._infectar_por_id()
            elif opcion == "10":
                self._mostrar_tabla_personas()
            elif opcion == "0":
                print("\nHasta luego 👋")
                return
            else:
                print("Opción inválida.")
            self._esperar_enter()

    # ------------------- ACCIONES -------------------
    def _crear_simulador(self) -> None:
        try:
            tam = int(input("Tamaño de la matriz (N): ").strip())
            n = int(input("Cantidad de personas: ").strip())
        except ValueError:
            print("Debes ingresar números enteros.")
            return

        txt_def = input("Defensa inicial [3]: ").strip()
        txt_seed = input("Semilla (Enter para aleatoria): ").strip()
        txt_multi = input("¿Defensa por múltiples infectados? (s/n) [n]: ").strip().lower()

        defensa_inicial = 3 if txt_def == "" else self._to_int_or(txt_def, 3)
        semilla = None if txt_seed == "" else self._to_int_or(txt_seed, None)
        usar_defensa_multiple = (txt_multi == "s")

        self.simulador = Simulador(
            tamano_matriz=tam,
            cantidad_personas=n,
            defensa_inicial=defensa_inicial,
            semilla_aleatoria=semilla,
            usar_defensa_multiple=usar_defensa_multiple
        )
        print("✅ Simulador creado.")

    def _inicializar(self) -> None:
        if not self._hay_simulador():
            return
        self.simulador.inicializar()  # type: ignore[union-attr]
        print("✅ Simulación inicializada.")
        self._mostrar_matriz()
        self._mostrar_arbol()
        self._mostrar_tabla_personas()

    def _ejecutar_una_ronda(self) -> None:
        if not self._hay_simulador_inicializado():
            return
        stats = self.simulador.ejecutar_ronda()  # type: ignore[union-attr]
        self._mostrar_stats_compactas(stats)
        self._mostrar_tabla_personas()

    def _ejecutar_varias_rondas(self) -> None:
        if not self._hay_simulador_inicializado():
            return
        try:
            k = int(input("¿Cuántas rondas quieres ejecutar?: ").strip())
        except ValueError:
            print("Debes ingresar un entero.")
            return

        k = max(0, k)
        for _ in range(k):
            stats = self.simulador.ejecutar_ronda()  # type: ignore[union-attr]
            print(f"\n>>> Después de la ronda {stats.get('ronda', '?')}:")
            self._mostrar_stats_compactas(stats)
            self._mostrar_tabla_personas()

    def _curar_persona(self) -> None:
        if not self._hay_simulador_inicializado():
            return
        try:
            x = int(input("x: ").strip())
            y = int(input("y: ").strip())
        except ValueError:
            print("Debes ingresar enteros.")
            return
        ok = self.simulador.curar_persona(x, y)  # type: ignore[union-attr]
        print("✅ Persona curada." if ok else "No había persona infectada en esa celda.")

    def _agregar_persona(self) -> None:
        if not self._hay_simulador():
            return
        try:
            x = int(input("x: ").strip())
            y = int(input("y: ").strip())
        except ValueError:
            print("Debes ingresar enteros.")
            return
        ok = self.simulador.agregar_persona(x, y)  # type: ignore[union-attr]
        print("✅ Persona agregada." if ok else "No se pudo agregar la persona.")

    def _infectar_por_id(self) -> None:
        """
        Infecta manualmente a una persona por su id, además del paciente cero.
        Si no hay infectados aún, la persona indicada se convierte en paciente cero.
        """
        if not self._hay_simulador_inicializado():
            return

        pid = input("Id de la persona (ej. p3): ").strip()
        persona = self._buscar_por_id(pid)
        if persona is None:
            print("No existe una persona con ese id.")
            return
        if persona.esta_infectada():
            print("Esa persona ya está infectada.")
            return

        infectados = self.simulador.get_personas_infectadas()  # type: ignore[union-attr]
        if len(infectados) == 0:
            persona.infectar(persona)
            self.simulador.get_arbol().establecer_paciente_cero(persona)  # type: ignore[union-attr]
            print(f"✅ {persona.id} ahora es paciente cero.")
        else:
            infectador = infectados[0]  # simple: el primer infectado (usualmente el paciente cero)
            persona.infectar(infectador)
            self.simulador.get_arbol().agregar_contagio(infectador, persona)  # type: ignore[union-attr]
            print(f"✅ {persona.id} infectada manualmente por {infectador.id}.")

        self._mostrar_tabla_personas()

    def _mostrar_matriz(self) -> None:
        if not self._hay_simulador():
            return
        self.vista.mostrar_matriz(self.simulador)  # type: ignore[arg-type]

    def _mostrar_arbol(self) -> None:
        if not self._hay_simulador():
            return
        self.vista.mostrar_arbol(self.simulador)  # type: ignore[arg-type]

    def _mostrar_estadisticas(self) -> None:
        if not self._hay_simulador():
            return
        stats = self.simulador.get_estadisticas()  # type: ignore[union-attr]
        self._mostrar_stats_detalladas(stats)

    def _mostrar_tabla_personas(self) -> None:
        if not self._hay_simulador():
            return
        self.vista.mostrar_tabla_personas(self.simulador)  # type: ignore[arg-type]

    # ------------------- UTILIDADES -------------------
    def _buscar_por_id(self, pid: str) -> Optional[Persona]:
        if not self._hay_simulador():
            return None
        for p in self.simulador.get_personas():  # type: ignore[union-attr]
            if p.id == pid:
                return p
        return None

    def _mostrar_titulo(self) -> None:
        print("\n" + "=" * 60)
        print(" Resident Evil UDEM - Simulación".center(60))
        print("=" * 60)

    def _mostrar_estado_resumen(self) -> None:
        if self.simulador is None:
            print("Estado: sin simulador creado.")
            return
        ronda = self.simulador.get_ronda_actual()
        tot = len(self.simulador.get_personas())
        print(f"Estado: simulador creado | ronda={ronda} | personas={tot}")

    def _mostrar_stats_compactas(self, stats: dict[str, Any]) -> None:
        print(f"Ronda {stats.get('ronda', '?')}: "
              f"Sanas={stats.get('sanas', '?')}, "
              f"Infectadas={stats.get('infectadas', '?')}, "
              f"Profundidad árbol={stats.get('profundidad_arbol', '?')}")

    def _mostrar_stats_detalladas(self, stats: dict[str, Any]) -> None:
        print("\n--- ESTADÍSTICAS ---")
        for k in ("ronda", "total_personas", "sanas", "infectadas", "profundidad_arbol"):
            print(f"{k}: {stats.get(k)}")

    def _hay_simulador(self) -> bool:
        if self.simulador is None:
            print("Primero crea el simulador (opción 1).")
            return False
        return True

    def _hay_simulador_inicializado(self) -> bool:
        if not self._hay_simulador():
            return False
        if not self.simulador.esta_inicializada:  # type: ignore[union-attr]
            print("Primero inicializa la simulación (opción 2).")
            return False
        return True

    def _to_int_or(self, texto: str, por_defecto: Optional[int]) -> Optional[int]:
        try:
            return int(texto)
        except Exception:
            return por_defecto

    def _esperar_enter(self) -> None:
        input("\nPresiona Enter para continuar...")


# Permite ejecutar:  python -m ui.menu
if __name__ == "__main__":
    MenuPrincipal().menu_principal()
