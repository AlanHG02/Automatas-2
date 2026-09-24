"""
hardware_catalog.py
---------------------
Catálogo estático de las características físicas del Arduino Uno
(Rev3, ATmega328P). No depende del programa del usuario: es una
referencia fija que el analizador semántico consulta para validar
las declaraciones del usuario contra el hardware real.
"""

from typing import Dict, Optional, Set

BOARD_NAME = "Arduino Uno (Rev3, ATmega328P)"

# ------------------------------------------------------------------
# Pines digitales: 0-13
# ------------------------------------------------------------------
DIGITAL_PIN_MIN = 0
DIGITAL_PIN_MAX = 13

# ------------------------------------------------------------------
# Pines analógicos: A0-A5
# ------------------------------------------------------------------
ANALOG_PINS: Set[str] = {"A0", "A1", "A2", "A3", "A4", "A5"}

# ------------------------------------------------------------------
# Modos de operación permitidos según el tipo de pin.
# (Los pines analógicos del DSL se modelan solo para lectura, como
# analogRead(); si más adelante se agrega analogWrite()/PWM se puede
# ampliar este catálogo sin tocar el analizador semántico.)
# ------------------------------------------------------------------
ALLOWED_MODES: Dict[str, Set[str]] = {
    "digital": {"OUTPUT", "INPUT", "INPUT_PULLUP"},
    "analog": {"INPUT", "INPUT_PULLUP"},
}

# ------------------------------------------------------------------
# Pines reservados por la propia placa: 0 y 1 son el puerto serie
# (UART), usado también para programar el Arduino por USB. No están
# prohibidos, pero declararlos genera una ADVERTENCIA.
# ------------------------------------------------------------------
RESERVED_PINS: Dict[int, str] = {
    0: "RX - usado por el puerto serie (comunicación USB/UART)",
    1: "TX - usado por el puerto serie (comunicación USB/UART)",
}

# ------------------------------------------------------------------
# Límite del firmware: delay() recibe un unsigned long (32 bits) en
# milisegundos.
# ------------------------------------------------------------------
DELAY_MAX_MS = 4294967295


def get_pin_type(pin_ref_text: str) -> Optional[str]:
    """'digital' si el texto son solo dígitos, 'analog' si es A0-A5,
    o None si no tiene una forma reconocible."""
    if pin_ref_text.isdigit():
        return "digital"
    if pin_ref_text in ANALOG_PINS:
        return "analog"
    return None


def is_valid_pin(pin_ref_text: str) -> bool:
    """True si el pin (digital o analógico) existe físicamente en el
    Arduino Uno."""
    tipo = get_pin_type(pin_ref_text)
    if tipo == "digital":
        return DIGITAL_PIN_MIN <= int(pin_ref_text) <= DIGITAL_PIN_MAX
    if tipo == "analog":
        return pin_ref_text in ANALOG_PINS
    return False


def is_valid_digital_pin(number: int) -> bool:
    return DIGITAL_PIN_MIN <= number <= DIGITAL_PIN_MAX


def is_mode_allowed(pin_type: str, mode: str) -> bool:
    """True si 'mode' es un modo de operación válido para ese tipo de
    pin, según el catálogo."""
    return mode in ALLOWED_MODES.get(pin_type, set())


def is_reserved(pin_ref_text: str) -> Optional[str]:
    """Devuelve el motivo por el que un pin está reservado por el
    hardware, o None si es de uso general. Solo aplica a pines
    digitales (0 y 1); los pines analógicos no tienen reserva."""
    if pin_ref_text.isdigit():
        return RESERVED_PINS.get(int(pin_ref_text))
    return None
