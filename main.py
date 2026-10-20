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
    4. (Fase 2) Si el programa es válido, se genera código intermedio
       a partir del AST ya validado y de la misma tabla de símbolos:
         - cuádruplos            -> <salida>/<programa>.quads.txt
         - LLVM IR               -> <salida>/<programa>.ll
       Con --validar se verifica el IR con las herramientas de LLVM
       (ver validar_llvm.py) y se guarda la bitácora.

Opciones de la Fase 2:
    --salida DIR       carpeta de salida (por defecto: salida)
    --solo-analisis    solo Fase 1 (no genera código intermedio)
    --validar          valida y ejecuta el .ll con llvm-as/opt/llvm-link/lli
"""

import argparse
import os
import sys

from antlr4 import FileStream, InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from ArduinoDSLLexer import ArduinoDSLLexer
from ArduinoDSLParser import ArduinoDSLParser
from semantic_analyzer import SemanticAnalyzer
from quadruples import QuadrupleGenerator, format_quadruples
from llvm_ir import generate_llvm_ir


class CollectingErrorListener(ErrorListener):
    """Reemplaza el comportamiento por defecto de ANTLR (que imprime a
    stderr) para poder juntar los errores léxicos/sintácticos en una
    sola lista y mostrarlos en el reporte final."""

    def __init__(self):
        super().__init__()
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Línea {line}:{column} - {msg}")


def analizar(entrada):
    """Léxico + sintáctico + semántico sobre un InputStream/FileStream.
    Devuelve (errores_sintacticos, analyzer, arbol)."""
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

    return error_listener.errors, analyzer, arbol


def analizar_archivo(ruta: str):
    """Compatibilidad con la Fase 1: devuelve (errores_sintacticos, analyzer)."""
    errores, analyzer, _ = analizar(FileStream(ruta, encoding="utf-8"))
    return errores, analyzer


def analizar_texto(codigo: str):
    """Igual que `analizar`, pero sobre una cadena (útil en pruebas)."""
    return analizar(InputStream(codigo))


def generar_codigo_intermedio(arbol, analyzer: SemanticAnalyzer, nombre: str):
    """FASE 2. Traduce el AST validado a cuádruplos y a LLVM IR reutilizando
    la tabla de símbolos del analizador (no se repite la validación).
    Devuelve (lista_de_cuadruplos, texto_llvm_ir)."""
    quads = QuadrupleGenerator(analyzer.symbol_table).generate(arbol)
    ir = generate_llvm_ir(quads, analyzer.symbol_table, nombre)
    return quads, ir


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
    ap = argparse.ArgumentParser(
        description="Compilador del DSL de Arduino Uno: análisis (Fase 1) "
                    "y código intermedio (Fase 2).")
    ap.add_argument("archivo", help="programa .dsl")
    ap.add_argument("--salida", default="salida", help="carpeta de salida (por defecto: salida)")
    ap.add_argument("--solo-analisis", action="store_true",
                    help="solo análisis (Fase 1); no genera código intermedio")
    ap.add_argument("--validar", action="store_true",
                    help="valida y ejecuta el LLVM IR con las herramientas de LLVM")
    args = ap.parse_args()

    ruta = args.archivo
    errores_sintacticos, analyzer, arbol = analizar(FileStream(ruta, encoding="utf-8"))

    imprimir_tabla_simbolos(analyzer)
    imprimir_reporte_errores(errores_sintacticos, analyzer.errors, analyzer.warnings)

    if errores_sintacticos or analyzer.errors:
        if not args.solo_analisis:
            print("\nNo se generó código intermedio: el programa tiene errores.")
        sys.exit(1)
    if args.solo_analisis:
        return

    # ---------------- Fase 2 ----------------
    nombre = os.path.splitext(os.path.basename(ruta))[0]
    quads, ir = generar_codigo_intermedio(arbol, analyzer, os.path.basename(ruta))

    os.makedirs(args.salida, exist_ok=True)
    ruta_quads = os.path.join(args.salida, nombre + ".quads.txt")
    ruta_ll = os.path.join(args.salida, nombre + ".ll")
    tabla = format_quadruples(quads)
    with open(ruta_quads, "w", encoding="utf-8") as f:
        f.write(tabla + "\n")
    with open(ruta_ll, "w", encoding="utf-8") as f:
        f.write(ir)

    print("\n=== CUÁDRUPLOS ===")
    print(tabla)
    print(f"\nCuádruplos guardados en {ruta_quads}")
    print(f"LLVM IR guardado en      {ruta_ll}")

    if args.validar:
        from validar_llvm import validar
        print()
        ok = validar([ruta_ll], os.path.join(args.salida, nombre + ".validacion.log"))
        sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
