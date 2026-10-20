"""
semantic_analyzer.py
---------------------
Analizador semántico del DSL de control de Arduino Uno.

Recorre el árbol sintáctico generado por ANTLR4 (usando el patrón
Visitor) y verifica:

  1. Declaraciones de pines válidas y sin duplicados.
  2. Que el número de pin esté dentro del rango físico del Arduino
     Uno, según el catálogo de hardware (pines digitales 0-13).
  3. Que el modo de operación (OUTPUT / INPUT / INPUT_PULLUP) sea
     consistente con el uso posterior del pin (set -> OUTPUT,
     read -> INPUT o INPUT_PULLUP).
  4. Que todo identificador (pin o variable) usado ya haya sido
     declarado antes de su uso.
  5. Que los retardos (delay/repeat) usen literales o variables
     numéricas válidas, dentro de los límites del firmware.
  6. (Advertencia, no error) Si se usa un pin reservado por el
     hardware (0, 1 o 13), según el catálogo.

Ampliación de la Fase 2 (la gramática ahora admite expresiones,
asignaciones, `read ... into`, `if/si ... else/sino` y `while/mientras`):

  7. Toda variable usada en una expresión, asignación o `read ... into`
     debe estar declarada antes (en un `var` previo, en orden textual).
  8. Los literales enteros deben caber en 32 bits (rango de Arduino).
  9. No se permite dividir (/ o %) entre la constante literal 0.

Al finalizar, expone:
  - self.symbol_table  -> tabla de símbolos completa
  - self.errors        -> lista de errores semánticos (str)
  - self.warnings      -> lista de advertencias semánticas (str)

NOTA: este archivo depende de las clases generadas por ANTLR4
(ArduinoDSLParser.py y ArduinoDSLVisitor.py). Generalas primero
siguiendo el README.md antes de ejecutar este módulo.
"""

from ArduinoDSLVisitor import ArduinoDSLVisitor
from ArduinoDSLParser import ArduinoDSLParser
from symbol_table import SymbolTable
import hardware_catalog as hw


class SemanticAnalyzer(ArduinoDSLVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self._context = "expresión"   # sentencia que se está validando

    # ---------------------------------------------------------
    # Utilidades internas
    # ---------------------------------------------------------
    def _error(self, line: int, message: str):
        self.errors.append(f"Línea {line}: {message}")

    def _warning(self, line: int, message: str):
        self.warnings.append(f"Línea {line}: {message}")

    # ---------------------------------------------------------
    # pin <n> as <MODE>;
    # ---------------------------------------------------------
    def visitPinDeclaration(self, ctx: ArduinoDSLParser.PinDeclarationContext):
        number = ctx.INT().getText()
        mode = ctx.MODE().getText()
        line = ctx.start.line
        pin_num = int(number)

        # --- Validación contra el catálogo de hardware ---
        if not hw.is_valid_digital_pin(pin_num):
            self._error(
                line,
                f"el pin {number} está fuera de rango. El "
                f"{hw.BOARD_NAME} solo tiene pines digitales "
                f"{hw.DIGITAL_PIN_MIN}-{hw.DIGITAL_PIN_MAX}."
            )
            # Igual se registra en la tabla para no arrastrar más
            # errores de "pin no declarado" en el resto del análisis.
        else:
            motivo = hw.is_reserved(pin_num)
            if motivo:
                self._warning(
                    line,
                    f"el pin {number} está reservado por el hardware "
                    f"({motivo}); se puede usar, pero no es recomendable "
                    f"para propósito general."
                )

        error = self.symbol_table.declare_pin(number, mode, line)
        if error:
            self.errors.append(error)

        return self.visitChildren(ctx)

    # ---------------------------------------------------------
    # var <id> = <expr>;
    # ---------------------------------------------------------
    def visitVarDeclaration(self, ctx: ArduinoDSLParser.VarDeclarationContext):
        name = ctx.ID().getText()
        line = ctx.start.line

        # Primero se valida la expresión inicial: `var x = x + 1;` debe
        # fallar porque `x` todavía no existe en ese punto.
        self._visit_expr(ctx.expr(), "var")

        error = self.symbol_table.declare_var(
            name, self._constant_value(ctx.expr()), line)
        if error:
            self.errors.append(error)
        return None

    # ---------------------------------------------------------
    # <id> = <expr>;
    # ---------------------------------------------------------
    def visitAssignStatement(self, ctx: ArduinoDSLParser.AssignStatementContext):
        name = ctx.ID().getText()
        line = ctx.start.line
        if not self.symbol_table.is_var_declared(name):
            self._error(
                line,
                f"la variable '{name}' recibe una asignación pero no fue "
                f"declarada con 'var {name} = ...;'."
            )
        self._visit_expr(ctx.expr(), "asignación")
        return None

    # ---------------------------------------------------------
    # set <pin> = HIGH|LOW;
    # ---------------------------------------------------------
    def visitSetStatement(self, ctx: ArduinoDSLParser.SetStatementContext):
        number = ctx.INT().getText()
        line = ctx.start.line

        if not self.symbol_table.is_pin_declared(number):
            self._error(
                line,
                f"el pin {number} se usa en 'set' pero no fue declarado "
                f"con 'pin {number} as ...;'."
            )
        else:
            pin = self.symbol_table.get_pin(number)
            if pin.mode != "OUTPUT":
                self._error(
                    line,
                    f"el pin {number} fue declarado como {pin.mode} y no "
                    f"puede usarse en 'set' (requiere modo OUTPUT)."
                )

        self._visit_expr(ctx.expr(), "set")
        return None

    # ---------------------------------------------------------
    # read <pin>;
    # ---------------------------------------------------------
    def visitReadStatement(self, ctx: ArduinoDSLParser.ReadStatementContext):
        number = ctx.INT().getText()
        line = ctx.start.line

        if not self.symbol_table.is_pin_declared(number):
            self._error(
                line,
                f"el pin {number} se usa en 'read' pero no fue declarado "
                f"con 'pin {number} as ...;'."
            )
        else:
            pin = self.symbol_table.get_pin(number)
            if pin.mode == "OUTPUT":
                self._error(
                    line,
                    f"el pin {number} fue declarado como OUTPUT y no "
                    f"puede leerse con 'read' (requiere INPUT o "
                    f"INPUT_PULLUP)."
                )

        if ctx.ID() is not None:
            target = ctx.ID().getText()
            if not self.symbol_table.is_var_declared(target):
                self._error(
                    line,
                    f"la variable '{target}' usada en 'read ... into' no "
                    f"fue declarada con 'var {target} = ...;'."
                )
        return None

    # ---------------------------------------------------------
    # delay <expr>;
    # ---------------------------------------------------------
    def visitDelayStatement(self, ctx: ArduinoDSLParser.DelayStatementContext):
        self._visit_expr(ctx.expr(), "delay")
        return None

    # ---------------------------------------------------------
    # repeat <expr> times { ... }
    # ---------------------------------------------------------
    def visitRepeatStatement(self, ctx: ArduinoDSLParser.RepeatStatementContext):
        self._visit_expr(ctx.expr(), "repeat")
        self.visit(ctx.block())
        return None

    # ---------------------------------------------------------
    # if|si <expr> { ... } [else|sino { ... }]
    # ---------------------------------------------------------
    def visitIfStatement(self, ctx: ArduinoDSLParser.IfStatementContext):
        self._visit_expr(ctx.expr(), "if")
        for blk in ctx.block():
            self.visit(blk)
        return None

    # ---------------------------------------------------------
    # while|mientras <expr> { ... }
    # ---------------------------------------------------------
    def visitWhileStatement(self, ctx: ArduinoDSLParser.WhileStatementContext):
        self._visit_expr(ctx.expr(), "while")
        self.visit(ctx.block())
        return None

    # ---------------------------------------------------------
    # Expresiones
    # ---------------------------------------------------------
    def _visit_expr(self, expr_ctx, label: str):
        """Visita una expresión recordando en qué sentencia se usa
        (para que los mensajes de error digan, p. ej., "usada en
        'delay'")."""
        previous = self._context
        self._context = label
        try:
            self.visit(expr_ctx)
        finally:
            self._context = previous

    def visitIntExpr(self, ctx: ArduinoDSLParser.IntExprContext):
        value = int(ctx.INT().getText())
        if value > hw.DELAY_MAX_MS:     # 2^32 - 1: máximo entero de 32 bits
            self._error(
                ctx.start.line,
                f"el valor {value} usado en '{self._context}' excede "
                f"el máximo permitido por el firmware "
                f"({hw.DELAY_MAX_MS})."
            )
        return None

    def visitIdExpr(self, ctx: ArduinoDSLParser.IdExprContext):
        name = ctx.ID().getText()
        if not self.symbol_table.is_var_declared(name):
            self._error(
                ctx.start.line,
                f"la variable '{name}' usada en '{self._context}' no "
                f"fue declarada con 'var {name} = ...;'."
            )
        return None

    def visitMulExpr(self, ctx: ArduinoDSLParser.MulExprContext):
        right = ctx.expr(1)
        if (ctx.op.text in ("/", "%")
                and isinstance(right, ArduinoDSLParser.IntExprContext)
                and int(right.getText()) == 0):
            self._error(
                ctx.start.line,
                f"división entre la constante 0 en '{self._context}'."
            )
        return self.visitChildren(ctx)

    # visitParenExpr, visitNegExpr, visitAddExpr, visitRelExpr y
    # visitLevelExpr usan el comportamiento por defecto (visitChildren).

    @staticmethod
    def _constant_value(expr_ctx):
        """Valor entero de la expresión si es una constante simple
        (literal, HIGH/LOW o literal negado); None en otro caso."""
        if isinstance(expr_ctx, ArduinoDSLParser.IntExprContext):
            return int(expr_ctx.getText())
        if isinstance(expr_ctx, ArduinoDSLParser.LevelExprContext):
            return hw.LEVEL_CODES[expr_ctx.getText()]
        if (isinstance(expr_ctx, ArduinoDSLParser.NegExprContext)
                and isinstance(expr_ctx.expr(), ArduinoDSLParser.IntExprContext)):
            return -int(expr_ctx.expr().getText())
        return None
