"""
main.py
-------
Punto de entrada del analizador del DSL de Arduino Uno.

Uso (desde Windows, en la carpeta del proyecto y con el entorno
virtual activado):

    python main.py ejemplos\\ejemplo_valido.dsl
    python main.py ejemplos\\ejemplo_con_errores.dsl

Flujo:
    1. Léxico + sintáctico: ANTLR4 tokeniza y parsea el archivo.
       Los errores léxicos/sintácticos se capturan con un
       ErrorListener personalizado (no lanzan excepciones).
    2. Semántico: SemanticAnalyzer recorre el árbol y valida
       declaraciones, pines, modos, identificadores y retardos.
    3. Reporte: se imprime la tabla de símbolos y el listado de
       errores (si los hay).
"""

import sys

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from ArduinoDSLLexer import ArduinoDSLLexer
from ArduinoDSLParser import ArduinoDSLParser
from semantic_analyzer import SemanticAnalyzer


class CollectingErrorListener(ErrorListener):
    """Reemplaza el comportamiento por defecto de ANTLR (que imprime a
    stderr) para poder juntar los errores léxicos/sintácticos en una
    sola lista y mostrarlos en el reporte final."""

    def __init__(self):
        super().__init__()
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Línea {line}:{column} - {msg}")


def analizar_archivo(ruta: str):
    error_listener = CollectingErrorListener()

    entrada = FileStream(ruta, encoding="utf-8")

    lexer = ArduinoDSLLexer(entrada)
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    tokens = CommonTokenStream(lexer)

    parser = ArduinoDSLParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    arbol = parser.program()

    analyzer = SemanticAnalyzer()
    analyzer.visit(arbol)

    return error_listener.errors, analyzer


def imprimir_tabla_simbolos(analyzer: SemanticAnalyzer):
    filas = analyzer.symbol_table.as_rows()
    print("\n=== TABLA DE SÍMBOLOS ===")
    if not filas:
        print("(vacía)")
        return

    encabezado = f"{'NOMBRE':<10}{'TIPO':<8}{'MODO':<15}{'VALOR':<8}{'LÍNEA':<6}"
    print(encabezado)
    print("-" * len(encabezado))
    for nombre, tipo, modo, valor, linea in filas:
        print(f"{nombre:<10}{tipo:<8}{str(modo):<15}{str(valor):<8}{linea:<6}")


def imprimir_reporte_errores(errores_sintacticos, errores_semanticos, advertencias):
    total = len(errores_sintacticos) + len(errores_semanticos)
    print("\n=== REPORTE DE ERRORES ===")
    if total == 0:
        print("No se encontraron errores. El programa es válido. ✅")
    else:
        if errores_sintacticos:
            print(f"\nErrores léxicos/sintácticos ({len(errores_sintacticos)}):")
            for err in errores_sintacticos:
                print(f"  - {err}")

        if errores_semanticos:
            print(f"\nErrores semánticos ({len(errores_semanticos)}):")
            for err in errores_semanticos:
                print(f"  - {err}")

        print(f"\nTotal de errores: {total} ❌")

    if advertencias:
        print(f"\nAdvertencias ({len(advertencias)}):")
        for adv in advertencias:
            print(f"  - {adv}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.dsl>")
        sys.exit(1)

    ruta = sys.argv[1]
    errores_sintacticos, analyzer = analizar_archivo(ruta)

    imprimir_tabla_simbolos(analyzer)
    imprimir_reporte_errores(errores_sintacticos, analyzer.errors, analyzer.warnings)


if __name__ == "__main__":
    main()
