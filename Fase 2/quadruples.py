
from dataclasses import dataclass
from typing import List, Optional

from ArduinoDSLParser import ArduinoDSLParser
from ArduinoDSLVisitor import ArduinoDSLVisitor
from symbol_table import SymbolTable
import hardware_catalog as hw


# ======================================================================
# Operandos y cuádruplos
# ======================================================================
@dataclass(frozen=True)
class Operand:
    """Argumento o resultado de un cuádruplo.

    kind: 'const' | 'var' | 'temp' | 'label' | 'func'
    name: texto con el que se imprime (p. ej. '500', 'HIGH', 'espera', 't3')
    value: valor entero (solo para 'const')
    """
    kind: str
    name: str
    value: Optional[int] = None

    def __str__(self) -> str:
        return self.name

    @property
    def is_hidden_var(self) -> bool:
        """Variable generada por el compilador (contador de `repeat`).
        Su nombre empieza con '$', carácter que un ID del DSL no admite,
        por lo que nunca choca con una variable del usuario."""
        return self.kind == "var" and self.name.startswith("$")


def const(value: int, text: Optional[str] = None) -> Operand:
    return Operand("const", text if text is not None else str(value), value)


def var(name: str) -> Operand:
    return Operand("var", name)


def temp(n: int) -> Operand:
    return Operand("temp", f"t{n}")


def label(name: str) -> Operand:
    return Operand("label", name)


def func(name: str) -> Operand:
    return Operand("func", name)


# Operadores
ADD, SUB, MUL, DIV, MOD = "+", "-", "*", "/", "%"
LT, LE, GT, GE, EQ, NE = "<", "<=", ">", ">=", "==", "!="
UMINUS, ASSIGN = "UMINUS", "="
PARAM, CALL = "PARAM", "CALL"
LABEL, GOTO, IF_FALSE = "LABEL", "GOTO", "IF_FALSE"
FUNC_BEGIN, FUNC_END, RETURN = "FUNC_BEGIN", "FUNC_END", "RETURN"

ARITHMETIC_OPS = {ADD, SUB, MUL, DIV, MOD}
RELATIONAL_OPS = {LT, LE, GT, GE, EQ, NE}


@dataclass
class Quad:
    op: str
    arg1: Optional[Operand] = None
    arg2: Optional[Operand] = None
    result: Optional[Operand] = None
    line: int = 0          # línea del programa DSL de donde proviene

    def as_tuple(self):
        """Tupla de textos (op, arg1, arg2, resultado); '_' = vacío."""
        f = lambda o: "_" if o is None else str(o)
        return (self.op, f(self.arg1), f(self.arg2), f(self.result))

    def __str__(self) -> str:
        return "(" + ", ".join(self.as_tuple()) + ")"


# ======================================================================
# Generador
# ======================================================================
class QuadrupleGenerator(ArduinoDSLVisitor):
    """Visitor sobre el AST validado que produce `self.quads`."""

    MAIN = "main"

    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table       # tabla de la Fase 1 (reutilizada)
        self.quads: List[Quad] = []
        self._temp_count = 0
        self._label_counts = {}
        self._hidden_count = 0
        self._line = 0

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def generate(self, tree) -> List[Quad]:
        self.visit(tree)
        return self.quads

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def _emit(self, op, arg1=None, arg2=None, result=None) -> Quad:
        q = Quad(op, arg1, arg2, result, self._line)
        self.quads.append(q)
        return q

    def _new_temp(self) -> Operand:
        self._temp_count += 1
        return temp(self._temp_count)

    def _label_set(self, construct: str, *parts: str):
        """Crea las etiquetas de una construcción con el mismo sufijo
        numérico: _label_set('if', 'then', 'else', 'end')."""
        n = self._label_counts.get(construct, 0) + 1
        self._label_counts[construct] = n
        return [label(f"{construct}_{p}_{n}") for p in parts]

    def _call(self, name: str, args: List[Operand]) -> Optional[Operand]:
        """Emite PARAM* + CALL para una función externa de Arduino."""
        api = hw.ARDUINO_API[name]
        assert len(args) == api.n_params, f"aridad incorrecta en {name}"
        for a in args:
            self._emit(PARAM, a)
        result = self._new_temp() if api.returns_value else None
        self._emit(CALL, func(name), const(len(args)), result)
        return result

    def _track(self, ctx):
        """Registra la línea DSL de la sentencia que se está traduciendo."""
        self._line = ctx.start.line

    # ------------------------------------------------------------------
    # Programa y bloques
    # ------------------------------------------------------------------
    def visitProgram(self, ctx: ArduinoDSLParser.ProgramContext):
        self._line = 0
        self._emit(FUNC_BEGIN, func(self.MAIN))
        for st in ctx.statement():
            self.visit(st)
        self._line = 0
        self._emit(RETURN, const(0))
        self._emit(FUNC_END, func(self.MAIN))

    def visitBlock(self, ctx: ArduinoDSLParser.BlockContext):
        for st in ctx.statement():
            self.visit(st)

    def visitStatement(self, ctx: ArduinoDSLParser.StatementContext):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------
    # Declaraciones
    # ------------------------------------------------------------------
    # pin 13 as OUTPUT;   ->   PARAM 13 / PARAM OUTPUT / CALL pinMode, 2
    def visitPinDeclaration(self, ctx: ArduinoDSLParser.PinDeclarationContext):
        self._track(ctx)
        number = ctx.INT().getText()
        mode = self.symbol_table.get_pin(number).mode      # tabla de símbolos
        self._call("pinMode", [const(int(number)),
                               const(hw.PIN_MODE_CODES[mode], mode)])

    # var x = expr;   ->   cálculo de expr y  (=, e, _, x)
    def visitVarDeclaration(self, ctx: ArduinoDSLParser.VarDeclarationContext):
        self._track(ctx)
        value = self.visit(ctx.expr())
        self._emit(ASSIGN, value, None, var(ctx.ID().getText()))

    # x = expr;
    def visitAssignStatement(self, ctx: ArduinoDSLParser.AssignStatementContext):
        self._track(ctx)
        value = self.visit(ctx.expr())
        self._emit(ASSIGN, value, None, var(ctx.ID().getText()))

    # ------------------------------------------------------------------
    # Entrada / salida y retardos
    # ------------------------------------------------------------------
    # set 13 = expr;   ->   digitalWrite(13, expr)
    def visitSetStatement(self, ctx: ArduinoDSLParser.SetStatementContext):
        self._track(ctx)
        value = self.visit(ctx.expr())      # primero se evalúa, luego PARAM/CALL
        self._call("digitalWrite", [const(int(ctx.INT().getText())), value])

    # read 7 [into s];   ->   t = digitalRead(7) [; s = t]
    def visitReadStatement(self, ctx: ArduinoDSLParser.ReadStatementContext):
        self._track(ctx)
        t = self._call("digitalRead", [const(int(ctx.INT().getText()))])
        if ctx.ID() is not None:
            self._emit(ASSIGN, t, None, var(ctx.ID().getText()))

    # delay expr;   ->   delay(expr)
    def visitDelayStatement(self, ctx: ArduinoDSLParser.DelayStatementContext):
        self._track(ctx)
        self._call("delay", [self.visit(ctx.expr())])

    # ------------------------------------------------------------------
    # Estructuras de control
    # ------------------------------------------------------------------
    # if cond { A } [else { B }]
    #
    #         <cálculo de cond>
    #         IF_FALSE cond, if_else_N      (o if_end_N si no hay else)
    #   if_then_N:   A
    #         GOTO if_end_N                 (solo si hay else)
    #   if_else_N:   B                      (solo si hay else)
    #   if_end_N:
    def visitIfStatement(self, ctx: ArduinoDSLParser.IfStatementContext):
        self._track(ctx)
        then_blk = ctx.block(0)
        else_blk = ctx.block(1) if len(ctx.block()) > 1 else None
        l_then, l_else, l_end = self._label_set("if", "then", "else", "end")

        cond = self.visit(ctx.expr())
        self._emit(IF_FALSE, cond, None, l_else if else_blk else l_end)
        self._emit(LABEL, None, None, l_then)
        self.visit(then_blk)
        if else_blk is not None:
            self._emit(GOTO, None, None, l_end)
            self._emit(LABEL, None, None, l_else)
            self.visit(else_blk)
        self._emit(LABEL, None, None, l_end)

    # while cond { A }
    #
    #   while_cond_N:  <cálculo de cond>
    #         IF_FALSE cond, while_end_N
    #   while_body_N:  A
    #         GOTO while_cond_N
    #   while_end_N:
    def visitWhileStatement(self, ctx: ArduinoDSLParser.WhileStatementContext):
        self._track(ctx)
        l_cond, l_body, l_end = self._label_set("while", "cond", "body", "end")

        self._emit(LABEL, None, None, l_cond)
        cond = self.visit(ctx.expr())
        self._emit(IF_FALSE, cond, None, l_end)
        self._emit(LABEL, None, None, l_body)
        self.visit(ctx.block())
        self._line = ctx.start.line
        self._emit(GOTO, None, None, l_cond)
        self._emit(LABEL, None, None, l_end)

    # repeat n times { A }
    #
    # El conteo se evalúa UNA sola vez y se copia a un contador oculto
    # ($repN) que baja hasta 0; así, modificar la variable `n` dentro del
    # cuerpo no cambia el número de repeticiones, y n <= 0 no ejecuta nada.
    #
    #         $repN = n
    #   repeat_cond_N:  t = $repN > 0 ; IF_FALSE t, repeat_end_N
    #   repeat_body_N:  A
    #         $repN = $repN - 1 ; GOTO repeat_cond_N
    #   repeat_end_N:
    def visitRepeatStatement(self, ctx: ArduinoDSLParser.RepeatStatementContext):
        self._track(ctx)
        l_cond, l_body, l_end = self._label_set("repeat", "cond", "body", "end")
        self._hidden_count += 1
        counter = var(f"$rep{self._hidden_count}")

        count = self.visit(ctx.expr())
        self._emit(ASSIGN, count, None, counter)
        self._emit(LABEL, None, None, l_cond)
        t = self._new_temp()
        self._emit(GT, counter, const(0), t)
        self._emit(IF_FALSE, t, None, l_end)
        self._emit(LABEL, None, None, l_body)
        self.visit(ctx.block())
        self._line = ctx.start.line
        t2 = self._new_temp()
        self._emit(SUB, counter, const(1), t2)
        self._emit(ASSIGN, t2, None, counter)
        self._emit(GOTO, None, None, l_cond)
        self._emit(LABEL, None, None, l_end)

    # ------------------------------------------------------------------
    # Expresiones: cada visita devuelve el Operand que contiene el valor
    # ------------------------------------------------------------------
    def visitParenExpr(self, ctx: ArduinoDSLParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitIntExpr(self, ctx: ArduinoDSLParser.IntExprContext):
        return const(int(ctx.INT().getText()))

    def visitLevelExpr(self, ctx: ArduinoDSLParser.LevelExprContext):
        text = ctx.LEVEL().getText()
        return const(hw.LEVEL_CODES[text], text)

    def visitIdExpr(self, ctx: ArduinoDSLParser.IdExprContext):
        return var(ctx.ID().getText())

    def visitNegExpr(self, ctx: ArduinoDSLParser.NegExprContext):
        a = self.visit(ctx.expr())
        t = self._new_temp()
        self._emit(UMINUS, a, None, t)
        return t

    def _binary(self, ctx):
        a = self.visit(ctx.expr(0))
        b = self.visit(ctx.expr(1))
        t = self._new_temp()
        self._emit(ctx.op.text, a, b, t)
        return t

    visitMulExpr = _binary
    visitAddExpr = _binary
    visitRelExpr = _binary


# ======================================================================
# Presentación
# ======================================================================
def format_quadruples(quads: List[Quad]) -> str:
    """Tabla de texto con los cuádruplos numerados."""
    header = ("#", "OP", "ARG1", "ARG2", "RESULT", "LÍNEA")
    rows = [(str(i), *q.as_tuple(), str(q.line) if q.line else "-")
            for i, q in enumerate(quads)]
    widths = [max(len(r[c]) for r in [header] + rows) for c in range(len(header))]

    def fmt(r):
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(r)).rstrip()

    lines = [fmt(header), "  ".join("-" * w for w in widths)]
    lines += [fmt(r) for r in rows]
    return "\n".join(lines)
