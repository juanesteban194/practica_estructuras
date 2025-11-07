from __future__ import annotations
from typing import Optional, List

from .nodo_arbol import NodoArbol     
from .persona import Persona          


class ArbolContagio:
    
    def __init__(self) -> None:
        self.raiz: Optional[NodoArbol] = None
        self.nodos: dict[str, NodoArbol] = {}

    def establecer_paciente_cero(self, persona: Persona) -> None:
        nodo_nuevo = NodoArbol(persona)
        self.raiz = nodo_nuevo
        
        id_persona = persona.id
        self.nodos[id_persona] = nodo_nuevo

    def agregar_contagio(self, infectador: Persona, infectado: Persona) -> bool:
        id_infectador = infectador.id
        
        if id_infectador not in self.nodos:
            return False
        
        nodo_infectador = self.nodos[id_infectador]
        nodo_infectado = NodoArbol(infectado)
        
        nodo_infectador.agregar_hijo(nodo_infectado)
        
        id_infectado = infectado.id
        self.nodos[id_infectado] = nodo_infectado
        
        return True

    def curar_persona(self, persona: Persona) -> bool:
        id_persona = persona.id
        
        if id_persona not in self.nodos:
            return False
        
        nodo_a_curar = self.nodos[id_persona]
        nodo_padre = nodo_a_curar.get_padre()
        lista_hijos = nodo_a_curar.get_hijos()
        
        if nodo_padre is not None:
            for hijo in lista_hijos:
                nodo_padre.agregar_hijo(hijo)
            
            nodo_padre.eliminar_hijo(nodo_a_curar)
        else:
            if len(lista_hijos) > 0:
                nueva_raiz = lista_hijos[0]
                nueva_raiz.set_padre(None)
                self.raiz = nueva_raiz
                
                for i in range(1, len(lista_hijos)):
                    hijo = lista_hijos[i]
                    nueva_raiz.agregar_hijo(hijo)
            else:
                self.raiz = None
        
        del self.nodos[id_persona]
        persona.curar()
        
        return True

    def obtener_nodo(self, id_persona: str) -> Optional[NodoArbol]:
        if id_persona in self.nodos:
            return self.nodos[id_persona]
        else:
            return None

    def existe_persona(self, id_persona: str) -> bool:
        return (id_persona in self.nodos)

    def get_infectados(self) -> list[Persona]:
        lista_personas = []
        
        for id_persona in self.nodos:
            nodo = self.nodos[id_persona]
            persona = nodo.get_persona()
            lista_personas.append(persona)
        
        return lista_personas

    def contar_nodos(self) -> int:
        cantidad = len(self.nodos)
        return cantidad

    def get_profundidad(self) -> int:
        if len(self.nodos) == 0:
            return 0
        
        profundidad_maxima = 0
        
        for id_persona in self.nodos:
            nodo = self.nodos[id_persona]
            nivel_nodo = nodo.get_nivel()
            
            if nivel_nodo > profundidad_maxima:
                profundidad_maxima = nivel_nodo
        
        return profundidad_maxima
    
    def cuarar_k_rama(self, k:int):

        persona = persona.id
        if k == self.get_profundidad:
            self.nodos[persona] = self.persona.curar()          

    def visualizar(self) -> str:
        if self.raiz is None:
            return "Árbol vacío (sin infectados)"
        
        texto = "\n╔═══════════════════════════════════════╗\n"
        texto = texto + "║     ÁRBOL DE PROPAGACIÓN              ║\n"
        texto = texto + "╚═══════════════════════════════════════╝\n\n"
        
        id_raiz = self.raiz.get_persona().id
        texto = texto + f"{id_raiz} (Paciente Cero)\n"
        
        hijos_raiz = self.raiz.get_hijos()
        cantidad_hijos = len(hijos_raiz)
        
        for i in range(cantidad_hijos):
            hijo = hijos_raiz[i]
            es_ultimo = (i == cantidad_hijos - 1)
            texto = texto + self._construir_string_recursivo(hijo, "", es_ultimo)
        
        return texto

    def _construir_string_recursivo(self, nodo: NodoArbol, prefijo: str, es_ultimo: bool) -> str:
        if es_ultimo:
            marcador = "└── "
            prefijo_hijos = prefijo + "    "
        else:
            marcador = "├── "
            prefijo_hijos = prefijo + "│   "
        
        id_persona = nodo.get_persona().id
        texto = prefijo + marcador + id_persona + "\n"
        
        hijos = nodo.get_hijos()
        cantidad_hijos = len(hijos)
        
        for i in range(cantidad_hijos):
            hijo = hijos[i]
            es_ultimo_hijo = (i == cantidad_hijos - 1)
            texto = texto + self._construir_string_recursivo(hijo, prefijo_hijos, es_ultimo_hijo)
        
        return texto

