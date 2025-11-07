from __future__ import annotations
from typing import Optional, List

from .persona import Persona          


class NodoArbol:
    
    def __init__(self, persona: Persona) -> None:
        self.persona: Persona = persona
        self.padre: Optional['NodoArbol'] = None
        self.hijos: list['NodoArbol'] = []

    def agregar_hijo(self, nodo_hijo: 'NodoArbol') -> None:
        ya_existe = False
        
        for hijo_actual in self.hijos:
            if hijo_actual.persona == nodo_hijo.persona:
                ya_existe = True
                break
        if not ya_existe:
            # Setea el padre del nuevo hijo como este nodo.
            nodo_hijo.padre = self
            self.hijos.append(nodo_hijo)

    def eliminar_hijo(self, nodo_hijo: 'NodoArbol') -> bool:
        hijo_encontrado = False
        
        for hijo_actual in self.hijos:
            if hijo_actual == nodo_hijo:
                hijo_encontrado = True
                break
        
        if hijo_encontrado:
            self.hijos.remove(nodo_hijo)
            nodo_hijo.padre = None
            return True
        
        return False

    def get_hijos(self) -> list['NodoArbol']:
        return self.hijos

    def get_padre(self) -> Optional['NodoArbol']:
        return self.padre

    def set_padre(self, nodo_padre: Optional['NodoArbol']) -> None:
        self.padre = nodo_padre

    def es_raiz(self) -> bool:
        if self.padre is None:
            return True
        else:
            return False

    def get_nivel(self) -> int:
        nivel = 0
        nodo_actual = self
        
        while nodo_actual.padre is not None:
            nivel = nivel + 1
            nodo_actual = nodo_actual.padre
        
        return nivel

    def get_persona(self) -> Persona:
        return self.persona

    def __repr__(self) -> str:
        id_persona = self.persona.id
        texto = f"NodoArbol({id_persona})"
        return texto


