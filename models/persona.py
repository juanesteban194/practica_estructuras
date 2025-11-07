from typing import Optional

class Persona:
    
    def __init__(self, id: str, x: int, y: int, defensa_inicial: int = 3) -> None:
        self.id: str = id
        self.x: int = x
        self.y: int = y
        self.infectada: bool = False
        self.defensa: int = defensa_inicial
        self.infectador: Optional['Persona'] = None

    def get_posicion(self) -> tuple[int, int]:
        return (self.x, self.y)

    def set_posicion(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def esta_infectada(self) -> bool:
        return self.infectada

    def infectar(self, infectador: 'Persona') -> None:
        self.infectada = True
        self.defensa = 0
        self.infectador = infectador

    def reducir_defensa(self) -> None:
        if self.defensa > 0:
            self.defensa -= 1

    def aumentar_defensa(self) -> None:
        self.defensa += 1

    def curar(self) -> None:
        self.infectada = False
        self.defensa = 3
        self.infectador = None

    def __repr__(self) -> str:
        estado = "INFECTADA" if self.infectada else "SANA"
        return f"Persona({self.id}, pos=({self.x},{self.y}), def={self.defensa}, {estado})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Persona):
            return False
        return self.id == other.id
    
