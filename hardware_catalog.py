"""
hardware_catalog.py
---------------------
Catálogo estático de las características físicas del Arduino Uno
(Rev3, ATmega328P).

A diferencia de la tabla de símbolos (que registra lo que el programa
del usuario declaró), este módulo NO depende del programa analizado:
es una referencia fija de lo que la placa permite. El analizador
semántico lo consulta para validar las declaraciones del usuario
contra el hardware real.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Set

BOARD_NAME = "Arduino Uno (Rev3, ATmega328P)"

# ------------------------------------------------------------------
# Pines digitales
# ------------------------------------------------------------------
DIGITAL_PIN_MIN = 0
DIGITAL_PIN_MAX = 13

# Pines digitales que además soportan PWM (analogWrite), marcados
# con '~' en la placa física.
PWM_PINS: Set[int] = {3, 5, 6, 9, 10, 11}

# Pines con un uso especial reservado por el propio hardware/placa.
# No están prohibidos por el DSL, pero usarlos para propósito general
# puede traer problemas (por eso el analizador los reporta como
# advertencia y no como error).
RESERVED_PINS: Dict[int, str] = {
    0: "RX - usado por el puerto serie (comunicación USB/UART)",
    1: "TX - usado por el puerto serie (comunicación USB/UART)",
    13: "conectado al LED integrado (L) de la placa",
}

# ------------------------------------------------------------------
# Pines analógicos (no usados todavía por el DSL; se incluyen para
# facilitar una futura extensión con analogRead()/analogWrite()).
# ------------------------------------------------------------------
ANALOG_PINS: Dict[str, int] = {
    "A0": 14, "A1": 15, "A2": 16, "A3": 17, "A4": 18, "A5": 19,
}

# ------------------------------------------------------------------
# Límites propios del firmware de Arduino
# ------------------------------------------------------------------
# delay() recibe un unsigned long (32 bits) en milisegundos.
DELAY_MAX_MS = 4294967295


@dataclass
class PinInfo:
    number: int
    is_digital: bool = True
    supports_pwm: bool = False
    reserved_reason: Optional[str] = None


def get_pin_info(number: int) -> Optional[PinInfo]:
    """Ficha de hardware de un pin digital, o None si el número no
    corresponde a ningún pin físico del Arduino Uno."""
    if not is_valid_digital_pin(number):
        return None
    return PinInfo(
        number=number,
        is_digital=True,
        supports_pwm=number in PWM_PINS,
        reserved_reason=RESERVED_PINS.get(number),
    )


def is_valid_digital_pin(number: int) -> bool:
    """True si el número está dentro del rango físico de pines
    digitales del Arduino Uno (0-13)."""
    return DIGITAL_PIN_MIN <= number <= DIGITAL_PIN_MAX


def is_reserved(number: int) -> Optional[str]:
    """Devuelve el motivo por el que un pin está reservado, o None si
    el pin es de uso general."""
    return RESERVED_PINS.get(number)


def supports_pwm(number: int) -> bool:
    return number in PWM_PINS
