"""
validar_llvm.py
----------------
FASE 2 - Validación del código intermedio con las herramientas de LLVM.

Para cada archivo .ll ejecuta, en orden:

  1. llvm-as    <f>.ll -o <f>.bc              ensambla (parsea) y verifica
  2. opt        -passes=verify -disable-output  pasada de verificación
  3. opt        -passes=mem2reg,verify -S       promoción de memoria a SSA
                                                (comprueba que el uso de
                                                alloca/load/store es correcto)
  4. llvm-link  <f>.ll runtime/arduino_stub.ll  enlaza con el runtime simulado
  5. lli        <f>.linked.ll                   EJECUTA el programa y guarda la
                                                traza (llamadas a Arduino)

y registra en un archivo de bitácora: fecha, sistema, versión de cada
herramienta, cada comando exacto, su código de salida y su salida.

Uso:
    python validar_llvm.py salida/ejemplo.ll [otro.ll ...] [--log bitacora.log]

Las herramientas se buscan en el PATH (con o sin sufijo de versión, p. ej.
`llvm-as` o `llvm-as-18`) o en la carpeta indicada por la variable de
entorno LLVM_BIN. Código de salida 0 si todo pasó.
"""

import argparse
import datetime
import os
import platform
import shutil
import subprocess
import sys
from typing import List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
STUB = os.path.join(HERE, "runtime", "arduino_stub.ll")
TOOLS = ["llvm-as", "opt", "llvm-link", "lli"]
VERSION_SUFFIXES = [""] + [f"-{v}" for v in range(22, 12, -1)]


def _rel(path: str) -> str:
    """Ruta relativa al directorio actual si es posible (bitácora portable)."""
    try:
        return os.path.relpath(path)
    except ValueError:                       # otra unidad en Windows
        return path


def find_tool(name: str) -> Optional[str]:
    """Ruta de la herramienta LLVM `name` (prueba LLVM_BIN y el PATH, con
    sufijos de versión)."""
    dirs = [os.environ["LLVM_BIN"]] if os.environ.get("LLVM_BIN") else []
    for suffix in VERSION_SUFFIXES:
        for d in dirs:
            p = shutil.which(name + suffix, path=d)
            if p:
                return p
        p = shutil.which(name + suffix)
        if p:
            return p
    return None


def tool_version(path: str) -> str:
    try:
        r = subprocess.run([path, "--version"], capture_output=True,
                           text=True, timeout=30)
        lines = [l.strip() for l in (r.stdout or r.stderr).splitlines()
                 if "version" in l.lower()]
        return lines[0] if lines else "(versión no reportada)"
    except Exception as e:                                # pragma: no cover
        return f"(error al consultar versión: {e})"


class Bitacora:
    """Acumula el texto de la bitácora y lo imprime a la vez."""

    def __init__(self):
        self.lines: List[str] = []

    def write(self, text: str = ""):
        self.lines.append(text)
        print(text)

    def save(self, path: str):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines) + "\n")


def _run(log: Bitacora, title: str, cmd: List[str],
         save_stdout_to: Optional[str] = None) -> bool:
    log.write(f"\n--- {title} ---")
    shown_cmd = [os.path.basename(cmd[0])] + cmd[1:]
    log.write("$ " + " ".join(shown_cmd))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        log.write(f"RESULTADO: FALLÓ (no se pudo ejecutar: {e})")
        return False
    log.write(f"código de salida: {r.returncode}")
    if r.stdout.strip():
        shown = r.stdout.rstrip()
        log.write("salida estándar:")
        log.write("\n".join("    " + l for l in shown.splitlines()))
    if r.stderr.strip():
        log.write("salida de error:")
        log.write("\n".join("    " + l for l in r.stderr.rstrip().splitlines()))
    if save_stdout_to:
        with open(save_stdout_to, "w", encoding="utf-8") as f:
            f.write(r.stdout)
        log.write(f"(salida guardada en {save_stdout_to})")
    ok = r.returncode == 0
    log.write("RESULTADO: " + ("OK" if ok else "FALLÓ"))
    return ok


def validar(ll_files: List[str], log_path: Optional[str] = None) -> bool:
    log = Bitacora()
    log.write("=== VALIDACIÓN DE LLVM IR ===")
    log.write(f"Fecha:    {datetime.datetime.now().isoformat(timespec='seconds')}")
    log.write(f"Sistema:  {platform.platform()}")
    log.write(f"Python:   {platform.python_version()}")

    log.write("\n--- Herramientas LLVM ---")
    paths = {}
    for t in TOOLS:
        p = find_tool(t)
        paths[t] = p
        log.write(f"{t:<10} {p or 'NO ENCONTRADA'}"
                  + (f"  ->  {tool_version(p)}" if p else ""))

    missing = [t for t, p in paths.items() if p is None]
    if missing:
        log.write("\nERROR: faltan herramientas de LLVM: " + ", ".join(missing))
        log.write("Instale LLVM (paquete llvm / clang) o defina LLVM_BIN.")
        if log_path:
            log.save(log_path)
        return False

    all_ok = True
    for ll in ll_files:
        ll = _rel(ll)
        base = os.path.splitext(ll)[0]
        stub = _rel(STUB)
        log.write(f"\n==================== {os.path.basename(ll)} ====================")
        steps = [
            _run(log, "1. Ensamblar y verificar (llvm-as)",
                 [paths["llvm-as"], ll, "-o", base + ".bc"]),
            _run(log, "2. Verificador (opt -passes=verify)",
                 [paths["opt"], "-passes=verify", "-disable-output", ll]),
            _run(log, "3. Promoción a SSA (opt -passes=mem2reg,verify)",
                 [paths["opt"], "-passes=mem2reg,verify", "-S", ll,
                  "-o", base + ".mem2reg.ll"]),
            _run(log, "4. Enlazar con el runtime simulado (llvm-link)",
                 [paths["llvm-link"], ll, stub, "-S", "-o", base + ".linked.ll"]),
        ]
        if all(steps):
            steps.append(_run(log, "5. Ejecutar (lli) y guardar la traza",
                              [paths["lli"], base + ".linked.ll"],
                              save_stdout_to=base + ".trace.txt"))
        ok = all(steps) and len(steps) == 5
        all_ok &= ok
        log.write(f"\nRESULTADO GLOBAL para {os.path.basename(ll)}: "
                  + ("VÁLIDO ✅" if ok else "CON ERRORES ❌"))

    if log_path:
        log.save(log_path)
        print(f"\nBitácora guardada en {log_path}")
    return all_ok


def main():
    ap = argparse.ArgumentParser(description="Valida archivos LLVM IR con las herramientas de LLVM.")
    ap.add_argument("archivos", nargs="+", help="archivos .ll a validar")
    ap.add_argument("--log", default=None, help="ruta de la bitácora (por defecto: junto al primer .ll)")
    args = ap.parse_args()
    log_path = args.log or os.path.splitext(args.archivos[0])[0] + ".validacion.log"
    sys.exit(0 if validar(args.archivos, log_path) else 1)


if __name__ == "__main__":
    main()
