"""
symbol_table.py
----------------
Tabla de símbolos del DSL de Arduino.

En esta versión los pines se declaran con un identificador propio
(`pin led = 13 as OUTPUT;`), igual que las variables (`var espera =
500;`). Por eso ambos comparten un único espacio de nombres: un mismo
nombre no puede usarse dos veces, sin importar si la primera vez fue
para un pin y la segunda para una variable (o viceversa).

Cada símbolo guarda:
    - Identificador   (name)
    - Tipo de pin      (pin_type: 'digital' | 'analog', solo pines)
    - Modo de operación (mode: OUTPUT/INPUT/INPUT_PULLUP, solo pines)
    - Pin físico        (physical_pin: '13', 'A0', ..., solo pines)
    - Línea de declaración (line)
    - (para variables) valor inicial (value)
"""

from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class Symbol:
    name: str
    kind: str                      # 'pin' o 'var'
    line: int
    pin_type: Optional[str] = None      # 'digital' | 'analog' (solo pines)
    mode: Optional[str] = None          # OUTPUT/INPUT/INPUT_PULLUP (solo pines)
    physical_pin: Optional[str] = None  # '13', 'A0', ... (solo pines)
    value: Optional[int] = None         # valor inicial (solo variables)


class SymbolTable:
    """Espacio de nombres único (sin ámbitos anidados: en el DSL los
    pines y variables son, en la práctica, globales)."""

    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}

    # ---------------- Declaración ----------------
    def declare_pin(self, name: str, physical_pin: str, pin_type: str,
                     mode: str, line: int) -> Optional[str]:
        """Declara un pin con nombre. Devuelve un mensaje de error si
        el identificador ya existía, o None si fue exitosa."""
        if name in self.symbols:
            prev = self.symbols[name]
            return (f"Línea {line}: el identificador '{name}' ya fue "
                    f"declarado en la línea {prev.line} "
                    f"(como {prev.kind}).")
        self.symbols[name] = Symbol(
            name=name, kind='pin', line=line, pin_type=pin_type,
            mode=mode, physical_pin=physical_pin,
        )
        return None

    def declare_var(self, name: str, value: int, line: int) -> Optional[str]:
        if name in self.symbols:
            prev = self.symbols[name]
            return (f"Línea {line}: el identificador '{name}' ya fue "
                    f"declarado en la línea {prev.line} "
                    f"(como {prev.kind}).")
        self.symbols[name] = Symbol(name=name, kind='var', line=line, value=value)
        return None

    # ---------------- Consulta ----------------
    def is_declared(self, name: str) -> bool:
        return name in self.symbols

    def get(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    # ---------------- Utilidades ----------------
    def as_rows(self):
        """Filas (tuplas) listas para imprimir en el reporte:
        (identificador, tipo, modo, pin_físico, valor, línea)."""
        rows = []
        for sym in self.symbols.values():
            if sym.kind == 'pin':
                rows.append((sym.name, sym.pin_type, sym.mode,
                              sym.physical_pin, "-", sym.line))
            else:
                rows.append((sym.name, "var", "-", "-", sym.value, sym.line))
        rows.sort(key=lambda r: r[5])
        return rows
