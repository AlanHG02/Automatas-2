"""
symbol_table.py
----------------
Estructura de datos de la tabla de símbolos para el DSL de Arduino.

Se manejan dos espacios de nombres, ya que en el DSL los pines se
identifican por número (INT) y las variables por nombre (ID):

    - pines:     clave = número de pin (str), valor = Symbol(kind='pin')
    - variables: clave = nombre de la variable (str), valor = Symbol(kind='var')
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class Symbol:
    name: str            # nombre o número de pin, como texto
    kind: str             # 'pin' o 'var'
    line: int             # línea donde fue declarado
    mode: Optional[str] = None   # OUTPUT / INPUT / INPUT_PULLUP (solo pines)
    value: Optional[int] = None  # valor entero inicial (solo variables)


class SymbolTable:
    """Tabla de símbolos plana (el DSL no tiene ámbitos anidados: los
    pines y variables de Arduino son, en la práctica, globales)."""

    def __init__(self):
        self.pins: Dict[str, Symbol] = {}
        self.vars: Dict[str, Symbol] = {}

    # ---------------- Pines ----------------
    def declare_pin(self, number: str, mode: str, line: int) -> Optional[str]:
        """Declara un pin. Devuelve un mensaje de error (str) si ya
        existía, o None si la declaración fue exitosa."""
        if number in self.pins:
            prev = self.pins[number]
            return (f"Línea {line}: el pin {number} ya fue declarado "
                    f"en la línea {prev.line} (modo {prev.mode}).")
        self.pins[number] = Symbol(name=number, kind='pin', line=line, mode=mode)
        return None

    def is_pin_declared(self, number: str) -> bool:
        return number in self.pins

    def get_pin(self, number: str) -> Optional[Symbol]:
        return self.pins.get(number)

    # ---------------- Variables ----------------
    def declare_var(self, name: str, value: int, line: int) -> Optional[str]:
        if name in self.vars:
            prev = self.vars[name]
            return (f"Línea {line}: la variable '{name}' ya fue declarada "
                    f"en la línea {prev.line}.")
        self.vars[name] = Symbol(name=name, kind='var', line=line, value=value)
        return None

    def is_var_declared(self, name: str) -> bool:
        return name in self.vars

    def get_var(self, name: str) -> Optional[Symbol]:
        return self.vars.get(name)

    # ---------------- Utilidades ----------------
    def all_symbols(self) -> List[Symbol]:
        return list(self.pins.values()) + list(self.vars.values())

    def as_rows(self):
        """Devuelve filas (tuplas) listas para imprimir en una tabla."""
        rows = []
        for sym in self.pins.values():
            rows.append((sym.name, "pin", sym.mode, "-", sym.line))
        for sym in self.vars.values():
            rows.append((sym.name, "var", "-", sym.value, sym.line))
        # Orden estable por línea de declaración
        rows.sort(key=lambda r: r[4])
        return rows
