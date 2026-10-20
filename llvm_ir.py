"""
llvm_ir.py
-----------
FASE 2 - Generador de código intermedio (parte 2): cuádruplos -> LLVM IR.

Toma la lista de cuádruplos producida por `quadruples.QuadrupleGenerator`
y la tabla de símbolos de la Fase 1 y emite un módulo LLVM IR en formato
de texto (.ll). Tampoco repite el análisis semántico.

Correspondencia de conceptos
----------------------------
  Variable del DSL (var x)     alloca i32 en el bloque `entry`  (%x.addr),
                               lectura con `load`, escritura con `store`.
                               Se inicializan a 0 en `entry`, de modo que
                               ninguna lectura es de memoria sin definir.
  Contador de `repeat`         igual que una variable, con nombre `$repN`.
  Temporal tN                  valor SSA (%tN): se define una sola vez.
  Operadores + - * / %         add / sub / mul / sdiv / srem  (i32 con signo)
  Operadores relacionales      icmp slt|sle|sgt|sge|eq|ne  (resultado i1)
                               y, si el valor se usa como número, `zext`
                               a i32 (como en C: verdadero = 1).
  LABEL / GOTO / IF_FALSE      bloques básicos / `br label` / `br i1`
  PARAM + CALL                 `call` a funciones externas declaradas con
                               `declare` (pinMode, digitalWrite, ...)
  Programa                     `define i32 @main()`

Notas de portabilidad
---------------------
* Usa punteros opacos (`ptr`): requiere LLVM 15 o superior (se probó con
  LLVM 18). No se fija `target triple` para poder ejecutarlo en el equipo
  anfitrión con `lli`; para una placa real se compilaría con
  `llc -mtriple=avr` y se enlazaría con el núcleo de Arduino.
* Los enteros son de 32 bits con signo. Un literal mayor que 2^31-1
  (aceptado por la Fase 1 por compatibilidad con el `unsigned long` de
  delay) se escribe en complemento a dos.
"""

from typing import Dict, List, Optional, Set

from quadruples import (
    Quad, Operand,
    ADD, SUB, MUL, DIV, MOD, LT, LE, GT, GE, EQ, NE,
    UMINUS, ASSIGN, PARAM, CALL, LABEL, GOTO, IF_FALSE,
    FUNC_BEGIN, FUNC_END, RETURN,
)
from symbol_table import SymbolTable
import hardware_catalog as hw

_BINARY_INSTR = {ADD: "add", SUB: "sub", MUL: "mul", DIV: "sdiv", MOD: "srem"}
_ICMP_PRED = {LT: "slt", LE: "sle", GT: "sgt", GE: "sge", EQ: "eq", NE: "ne"}


class LLVMGenerator:

    def __init__(self, quads: List[Quad], symbol_table: SymbolTable,
                 module_name: str = "arduino_dsl"):
        self.quads = quads
        self.symbol_table = symbol_table
        self.module_name = module_name

        self._out: List[str] = []
        self._terminated = False        # ¿el bloque actual ya tiene terminador?
        self._params: List[Operand] = []
        self._load_n = 0                # contador para nombrar los `load`
        self._cond_n = 0                # ... los `icmp ne` de condiciones
        self._extra_blocks = 0          # ... bloques auxiliares
        self._line = None               # última línea DSL anotada
        # temporal -> nombre del valor i1 (solo para resultados relacionales)
        self._i1: Dict[str, str] = {}
        # temporales relacionales que se usan como número (necesitan zext)
        self._numeric_temps: Set[str] = self._find_numeric_relational_temps()

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def generate(self) -> str:
        self._out = [
            f"; ModuleID = '{self.module_name}'",
            f'source_filename = "{self.module_name}"',
            "; Generado por el compilador del DSL de Arduino (Fase 2).",
            "; Requiere LLVM >= 15 (punteros opacos `ptr`).",
            "",
            "; --- Funciones externas del núcleo de Arduino ---",
        ]
        for fn in hw.ARDUINO_API.values():
            ret = "i32" if fn.returns_value else "void"
            params = ", ".join(["i32"] * fn.n_params)
            self._out.append(f"declare {ret} @{fn.name}({params})")
        self._out.append("")

        for i, q in enumerate(self.quads):
            self._translate(i, q)
        return "\n".join(self._out) + "\n"

    # ------------------------------------------------------------------
    # Análisis previo
    # ------------------------------------------------------------------
    def _find_numeric_relational_temps(self) -> Set[str]:
        """Temporales producidos por una comparación y consumidos en algo
        distinto de IF_FALSE. Esos necesitan además una versión i32."""
        rel = {q.result.name for q in self.quads
               if q.op in _ICMP_PRED and q.result is not None}
        numeric = set()
        for q in self.quads:
            if q.op == IF_FALSE:
                continue
            for o in (q.arg1, q.arg2):
                if o is not None and o.kind == "temp" and o.name in rel:
                    numeric.add(o.name)
        return numeric

    def _all_variables(self) -> List[str]:
        """Variables que necesitan memoria: las de la tabla de símbolos
        (Fase 1) más los contadores ocultos que creó el generador."""
        names = list(self.symbol_table.vars.keys())
        for q in self.quads:
            for o in (q.arg1, q.arg2, q.result):
                if o is not None and o.is_hidden_var and o.name not in names:
                    names.append(o.name)
        return names

    # ------------------------------------------------------------------
    # Emisión de texto
    # ------------------------------------------------------------------
    def _inst(self, text: str):
        """Emite una instrucción; si el bloque actual ya terminó (código
        inalcanzable), abre antes un bloque nuevo para seguir siendo IR
        válido."""
        if self._terminated:
            self._extra_blocks += 1
            self._begin_block(f"unreachable.{self._extra_blocks}")
        self._out.append(f"  {text}")

    def _terminator(self, text: str):
        self._inst(text)
        self._terminated = True

    def _begin_block(self, name: str):
        self._out.append("")
        self._out.append(f"{name}:")
        self._terminated = False

    def _annotate(self, q: Quad):
        if q.line and q.line != self._line:
            self._out.append(f"  ; --- línea {q.line} del programa DSL ---")
            self._line = q.line

    # ------------------------------------------------------------------
    # Valores
    # ------------------------------------------------------------------
    @staticmethod
    def _addr(var_name: str) -> str:
        return f"%{var_name}.addr"

    def _value(self, o: Operand) -> str:
        """Devuelve el valor i32 de un operando, emitiendo un `load` si es
        una variable."""
        if o.kind == "const":
            v = o.value
            return str(v - (1 << 32) if v >= (1 << 31) else v)
        if o.kind == "temp":
            return f"%{o.name}"
        if o.kind == "var":
            self._load_n += 1
            reg = f"%{o.name}.val{self._load_n}"
            self._inst(f"{reg} = load i32, ptr {self._addr(o.name)}, align 4")
            return reg
        raise ValueError(f"operando no evaluable: {o}")

    def _as_i1(self, o: Operand) -> str:
        """Valor i1 de una condición (para `br i1`)."""
        if o.kind == "temp" and o.name in self._i1:
            return self._i1[o.name]          # ya es resultado de un icmp
        v = self._value(o)
        self._cond_n += 1
        reg = f"%cond{self._cond_n}"
        self._inst(f"{reg} = icmp ne i32 {v}, 0")
        return reg

    # ------------------------------------------------------------------
    # Traducción cuádruplo por cuádruplo
    # ------------------------------------------------------------------
    def _translate(self, i: int, q: Quad):
        op = q.op

        if op == FUNC_BEGIN:
            self._out.append(f"define i32 @{q.arg1.name}() {{")
            self._out.append("entry:")
            self._terminated = False
            self._line = None
            self._out.append("  ; variables: memoria en la pila, inicializadas a 0")
            for name in self._all_variables():
                self._out.append(f"  {self._addr(name)} = alloca i32, align 4")
            for name in self._all_variables():
                self._out.append(f"  store i32 0, ptr {self._addr(name)}, align 4")
            return

        if op == FUNC_END:
            if not self._terminated:
                self._terminator("ret i32 0")
            self._out.append("}")
            return

        self._annotate(q)

        if op == ASSIGN:
            value = self._value(q.arg1)
            self._inst(f"store i32 {value}, ptr {self._addr(q.result.name)}, align 4")

        elif op in _BINARY_INSTR:
            a, b = self._value(q.arg1), self._value(q.arg2)
            self._inst(f"%{q.result.name} = {_BINARY_INSTR[op]} i32 {a}, {b}")

        elif op == UMINUS:
            a = self._value(q.arg1)
            self._inst(f"%{q.result.name} = sub i32 0, {a}")

        elif op in _ICMP_PRED:
            a, b = self._value(q.arg1), self._value(q.arg2)
            t = q.result.name
            if t in self._numeric_temps:
                # se usa como número: icmp (i1) + zext a i32
                self._i1[t] = f"%{t}.i1"
                self._inst(f"%{t}.i1 = icmp {_ICMP_PRED[op]} i32 {a}, {b}")
                self._inst(f"%{t} = zext i1 %{t}.i1 to i32")
            else:
                # solo alimenta saltos: basta el i1
                self._i1[t] = f"%{t}"
                self._inst(f"%{t} = icmp {_ICMP_PRED[op]} i32 {a}, {b}")

        elif op == PARAM:
            self._params.append(q.arg1)

        elif op == CALL:
            n = q.arg2.value
            args, self._params = self._params[-n:], self._params[:-n]
            rendered = ", ".join(f"i32 {self._value(a)}" for a in args)
            fname = q.arg1.name
            if q.result is not None:
                self._inst(f"%{q.result.name} = call i32 @{fname}({rendered})")
            else:
                self._inst(f"call void @{fname}({rendered})")

        elif op == LABEL:
            name = q.result.name
            if not self._terminated:
                self._out.append(f"  br label %{name}")     # caída natural
            self._begin_block(name)

        elif op == GOTO:
            self._terminator(f"br label %{q.result.name}")

        elif op == IF_FALSE:
            cond = self._as_i1(q.arg1)
            # Si el siguiente cuádruplo es una etiqueta, ese es el destino
            # de "condición verdadera"; si no, se crea un bloque auxiliar.
            nxt = self.quads[i + 1] if i + 1 < len(self.quads) else None
            if nxt is not None and nxt.op == LABEL:
                self._terminator(
                    f"br i1 {cond}, label %{nxt.result.name}, label %{q.result.name}")
            else:
                self._extra_blocks += 1
                cont = f"cont.{self._extra_blocks}"
                self._terminator(
                    f"br i1 {cond}, label %{cont}, label %{q.result.name}")
                self._begin_block(cont)

        elif op == RETURN:
            self._terminator(f"ret i32 {self._value(q.arg1)}")

        else:
            raise ValueError(f"cuádruplo no soportado: {q}")


def generate_llvm_ir(quads: List[Quad], symbol_table: SymbolTable,
                     module_name: str = "arduino_dsl") -> str:
    return LLVMGenerator(quads, symbol_table, module_name).generate()
