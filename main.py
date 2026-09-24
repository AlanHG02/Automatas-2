"""
main.py
-------
Punto de entrada del analizador del DSL de Arduino Uno.

Uso (Windows, con el entorno virtual activado):

    python main.py ejemplos\\ejemplo_valido.dsl
    python main.py ejemplos\\ejemplo_con_errores.dsl

Flujo:
    1. Léxico + sintáctico: ANTLR4 tokeniza y parsea el archivo.
       Los errores léxicos/sintácticos se capturan con un
       ErrorListener personalizado (no lanzan excepciones).
    2. Semántico: SemanticAnalyzer recorre el árbol y valida pines,
       identificadores, modos y retardos (ver semantic_analyzer.py).
    3. Reporte: se imprime la tabla de símbolos y el listado de
       errores/advertencias (si los hay).

La función `analizar_texto` se reutiliza desde pruebas.py para poder
analizar fragmentos de código sin necesidad de escribir un archivo.
"""

import sys

from antlr4 import FileStream, InputStream, CommonTokenStream
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


def _analizar_stream(entrada):
    """Lógica común: corre lexer -> parser -> analizador semántico
    sobre un stream de entrada de ANTLR (de archivo o de texto)."""
    error_listener = CollectingErrorListener()

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


def analizar_archivo(ruta: str):
    """Analiza un archivo .dsl en disco."""
    return _analizar_stream(FileStream(ruta, encoding="utf-8"))


def analizar_texto(codigo: str):
    """Analiza un fragmento de código DSL dado como string (usado por
    pruebas.py)."""
    return _analizar_stream(InputStream(codigo))


def imprimir_tabla_simbolos(analyzer: SemanticAnalyzer):
    filas = analyzer.symbol_table.as_rows()
    print("\n=== TABLA DE SÍMBOLOS ===")
    if not filas:
        print("(vacía)")
        return

    encabezado = (f"{'ID':<10}{'TIPO':<10}{'MODO':<15}"
                  f"{'PIN FÍSICO':<12}{'VALOR':<8}{'LÍNEA':<6}")
    print(encabezado)
    print("-" * len(encabezado))
    for nombre, tipo, modo, pin_fisico, valor, linea in filas:
        print(f"{nombre:<10}{str(tipo):<10}{str(modo):<15}"
              f"{str(pin_fisico):<12}{str(valor):<8}{linea:<6}")


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
