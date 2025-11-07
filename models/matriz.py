from __future__ import annotations
from typing import List, Tuple, Set

from persona import Persona  
       
class Matriz:
    
    def __init__(self, tamano: int) -> None:
        self.tamano: int = tamano
        self.celdas: list[list[list[Persona]]] = []
        
        for fila in range(tamano):
            fila_nueva = []
            for columna in range(tamano):
                fila_nueva.append([])
            self.celdas.append(fila_nueva)

    def esta_dentro_limites(self, x: int, y: int) -> bool:
        dentro_x = (x >= 0 and x < self.tamano)
        dentro_y = (y >= 0 and y < self.tamano)
        
        if dentro_x and dentro_y:
            return True
        else:
            return False

    def ajustar_coordenadas_rebote(self, x: int, y: int) -> tuple[int, int]:
        x_ajustado = x
        y_ajustado = y
        
        if x < 0:
            x_ajustado = 0
        elif x >= self.tamano:
            x_ajustado = self.tamano - 1
        
        if y < 0:
            y_ajustado = 0
        elif y >= self.tamano:
            y_ajustado = self.tamano - 1
        
        return (x_ajustado, y_ajustado)

    def agregar_persona(self, persona: Persona) -> bool:
        x, y = persona.get_posicion()
        
        if not self.esta_dentro_limites(x, y):
            x, y = self.ajustar_coordenadas_rebote(x, y)
            persona.set_posicion(x, y)
        
        self.celdas[x][y].append(persona)
        return True

    def remover_persona(self, persona: Persona) -> bool:
        x, y = persona.get_posicion()
        
        if not self.esta_dentro_limites(x, y):
            return False
        
        celda_actual = self.celdas[x][y]
        persona_encontrada = False
        
        for persona_en_celda in celda_actual:
            if persona_en_celda == persona:
                persona_encontrada = True
                break
        
        if persona_encontrada:
            celda_actual.remove(persona)
            return True
        
        return False

    def mover_persona(self, persona: Persona, nueva_x: int, nueva_y: int) -> bool:
        se_removio = self.remover_persona(persona)
        
        if not se_removio:
            return False
        
        nueva_x, nueva_y = self.ajustar_coordenadas_rebote(nueva_x, nueva_y)
        persona.set_posicion(nueva_x, nueva_y)
        
        return self.agregar_persona(persona)
    
    def mover_diagonal(self, persona: Persona, nueva_x: int, nueva_y: int):

        for x, y in self.get_posicion(persona):
            self.x = x
            self.y = y
            
        for fila in self.celdas:
            for columna in self.celdas[fila]:
                x = columna - 1
                y = fila - 1
                return self.mover_diagonal(persona, nueva_x = x, nueva_y = y )
         

    def obtener_personas_en(self, x: int, y: int) -> list[Persona]:
        if not self.esta_dentro_limites(x, y):
            return []
        
        personas_en_celda = self.celdas[x][y]
        copia_lista = personas_en_celda.copy()
        
        return copia_lista

    def get_todas_personas(self) -> list[Persona]:
        lista_todas = []
        
        for fila in self.celdas:
            for celda in fila:
                for persona in celda:
                    lista_todas.append(persona)
        
        return lista_todas

    def hay_multiple_personas(self, x: int, y: int) -> bool:
        if not self.esta_dentro_limites(x, y):
            return False
        
        cantidad_personas = len(self.celdas[x][y])
        
        if cantidad_personas >= 2:
            return True
        else:
            return False

    def get_celdas_ocupadas(self) -> list[tuple[int, int]]:
        lista_celdas = []
        
        for fila in range(self.tamano):
            for columna in range(self.tamano):
                if len(self.celdas[fila][columna]) > 0:
                    lista_celdas.append((fila, columna))
        
        return lista_celdas

    def get_tamano(self) -> int:
        return self.tamano

    def visualizar(self) -> str:
        texto = "\n"
        
        encabezado = "    "
        for columna in range(self.tamano):
            encabezado = encabezado + f"{columna:2d}  "
        texto = texto + encabezado + "\n"
        
        linea_separacion = "   " + ("─" * (self.tamano * 4)) + "\n"
        texto = texto + linea_separacion
        
        for fila in range(self.tamano):
            linea_fila = f"{fila:2d} │ "
            
            for columna in range(self.tamano):
                personas_celda = self.celdas[fila][columna]
                cantidad_personas = len(personas_celda)
                
                if cantidad_personas == 0:
                    linea_fila = linea_fila + "  "
                elif cantidad_personas == 1:
                    persona = personas_celda[0]
                    id_corto = persona.id[:2]
                    
                    if persona.esta_infectada():
                        linea_fila = linea_fila + f"\033[91m{id_corto}\033[0m"
                    else:
                        linea_fila = linea_fila + f"\033[92m{id_corto}\033[0m"
                else:
                    infectadas = 0
                    for persona in personas_celda:
                        if persona.esta_infectada():
                            infectadas = infectadas + 1
                    
                    if infectadas == cantidad_personas:
                        linea_fila = linea_fila + f"\033[91m{cantidad_personas}I\033[0m"
                    elif infectadas == 0:
                        linea_fila = linea_fila + f"\033[92m{cantidad_personas}S\033[0m"
                    else:
                        linea_fila = linea_fila + f"\033[93m{cantidad_personas}M\033[0m"
                
                linea_fila = linea_fila + " "
            
            linea_fila = linea_fila + "│\n"
            texto = texto + linea_fila
        
        texto = texto + linea_separacion
        texto = texto + "\n🟩 = Sana  🟥 = Infectada  🟨 = Mixta\n"
        
        return texto
