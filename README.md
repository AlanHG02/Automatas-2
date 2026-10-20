# Compilador para un DSL de control de Arduino Uno

> **Fase 1:** análisis léxico, sintáctico y semántico (tabla de símbolos).
> **Fase 2:** generación de código intermedio (cuádruplos y LLVM IR) —
> ver la sección [Fase 2](#fase-2--generación-de-código-intermedio) al final.

## (Fase 1) Analizador semántico

Proyecto: gramática ANTLR4 + analizador semántico en Python 3 que
verifica declaraciones, pines, modos de operación, identificadores y
retardos de un pequeño lenguaje (DSL) para controlar un Arduino Uno,
generando una **tabla de símbolos** y un **reporte de errores**.

Esta guía asume Windows 10/11, con **Visual Studio Code** como único
programa ya instalado. Vas a instalar 3 cosas más: **Python**, **Java**
(lo necesita la herramienta ANTLR4, que está escrita en Java) y el
**.jar de ANTLR4** (no es un instalador, es un archivo que se descarga
y se usa con `java -jar`).

---

## 1. Instalar Python 3

1. Andá a https://www.python.org/downloads/ y descargá la última
   versión de Python 3 (3.11 o superior).
2. Ejecutá el instalador. **Muy importante:** marcá la casilla
   **"Add python.exe to PATH"** antes de darle a "Install Now".
3. Verificá la instalación abriendo una terminal (`cmd` o
   PowerShell) y escribiendo:
   ```
   python --version
   pip --version
   ```
   Deberían mostrar números de versión sin error.

## 2. Instalar Java (JDK)

ANTLR4 es una herramienta escrita en Java; la necesitás solo para
**generar** el lexer/parser a partir de la gramática (no para correr
el analizador en sí, eso es Python puro).

1. Descargá el instalador de Temurin (Adoptium), una distribución
   gratuita de Java: https://adoptium.net/ → elegí la versión **LTS
   más reciente (17 o 21)**, sistema **Windows**, instalador `.msi`.
2. Ejecutá el instalador con las opciones por defecto (asegurate de
   que la opción "Set JAVA_HOME" y "Add to PATH" queden marcadas).
3. Verificá abriendo una terminal nueva:
   ```
   java -version
   ```

## 3. Descargar la herramienta ANTLR4 (antlr.jar)

1. Creá la carpeta `C:\antlr`.
2. Descargá el archivo `antlr-4.13.2-complete.jar` desde la página
   oficial: https://www.antlr.org/download.html (sección "Downloads",
   link "Complete ANTLR 4.13.2 Java binaries jar").
3. Guardalo exactamente en `C:\antlr\antlr-4.13.2-complete.jar`
   (el `generar.bat` del proyecto ya apunta a esa ruta).

No hace falta instalar nada más: se invoca con `java -jar`.

## 4. Preparar el proyecto en VS Code

1. Copiá toda la carpeta `arduino_dsl` (la que te compartí) a algún
   lugar como `C:\Users\TU_USUARIO\arduino_dsl`.
2. Abrí VS Code → `File > Open Folder...` → seleccioná esa carpeta.
3. (Opcional pero recomendado) Instalá la extensión **Python** de
   Microsoft desde el panel de extensiones de VS Code (ícono de
   cuadraditos a la izquierda, buscá "Python").
4. Abrí una terminal integrada en VS Code: menú **Terminal > New
   Terminal**. Debe abrir PowerShell o cmd ya parado en la carpeta
   del proyecto.

## 5. Crear un entorno virtual e instalar dependencias

En la terminal de VS Code, dentro de la carpeta `arduino_dsl`:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Si todo salió bien, el prompt de la terminal debería empezar con
`(venv)`. Cada vez que abras una terminal nueva para trabajar en el
proyecto, hay que volver a correr `venv\Scripts\activate`.

## 6. Generar el lexer y el parser con ANTLR4

Con el entorno virtual activado y parado en la carpeta `arduino_dsl`,
corré el script incluido:

```
generar.bat
```

Esto ejecuta por dentro:

```
java -jar C:\antlr\antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor ArduinoDSL.g4
```

y va a generar, entre otros, estos archivos nuevos en la carpeta:

- `ArduinoDSLLexer.py`
- `ArduinoDSLParser.py`
- `ArduinoDSLVisitor.py`
- `ArduinoDSLListener.py`

Esos archivos generados **no se editan a mano**: si cambiás la
gramática (`ArduinoDSL.g4`), volvés a correr `generar.bat`.

## 7. Ejecutar el analizador

Con el entorno virtual activado:

```
python main.py ejemplos\ejemplo_valido.dsl
python main.py ejemplos\ejemplo_con_errores.dsl
```

El primero debería imprimir la tabla de símbolos y "No se encontraron
errores". El segundo va a mostrar la tabla de símbolos (con lo que sí
se pudo procesar) y un listado de errores semánticos, uno por cada
problema intencional que tiene ese archivo de ejemplo.

---

## Estructura del proyecto

```
arduino_dsl/
├── ArduinoDSL.g4          # Gramática ANTLR4 del DSL
├── generar.bat            # Genera lexer/parser/visitor con ANTLR4
├── requirements.txt        # Dependencias de Python (runtime de ANTLR4)
├── symbol_table.py         # Clase SymbolTable / Symbol
├── semantic_analyzer.py    # Visitor con las reglas semánticas
├── hardware_catalog.py     # Catálogo del Arduino Uno (+ API de Arduino, Fase 2)
├── quadruples.py           # FASE 2: AST -> cuádruplos
├── llvm_ir.py              # FASE 2: cuádruplos -> LLVM IR
├── validar_llvm.py         # FASE 2: validación con llvm-as / opt / lli + bitácora
├── main.py                 # Punto de entrada (CLI)
├── runtime/
│   └── arduino_stub.ll     # FASE 2: Arduino simulado (para ejecutar el IR con lli)
├── tests/
│   └── test_fase2.py       # FASE 2: pruebas de traducción
├── salida/                 # FASE 2: resultados de ejemplo (cuádruplos, .ll, bitácora)
├── ejemplos/
│   ├── ejemplo_valido.dsl
│   ├── ejemplo_fase2.dsl   # FASE 2: usa todas las construcciones
│   └── ejemplo_con_errores.dsl
└── (se generan al correr generar.bat)
    ├── ArduinoDSLLexer.py
    ├── ArduinoDSLParser.py
    ├── ArduinoDSLVisitor.py
    └── ArduinoDSLListener.py
```

## El DSL, en resumen

```
pin 13 as OUTPUT;        // declara el pin 13 como salida
pin 7 as INPUT;          // declara el pin 7 como entrada
pin 2 as INPUT_PULLUP;   // entrada con resistencia pull-up interna

var espera = 500;        // variable entera (para delays/repeticiones)

set 13 = HIGH;            // escribe HIGH/LOW en un pin OUTPUT
delay espera;              // espera en milisegundos (literal o variable)
delay 500;

read 7;                    // lee un pin INPUT / INPUT_PULLUP

repeat 5 times {           // bloque repetido N veces (literal o variable)
    set 13 = HIGH;
    delay 500;
    set 13 = LOW;
    delay 500;
}
```

## Qué valida el analizador semántico

| Categoría              | Regla implementada                                                               |
|-------------------------|-----------------------------------------------------------------------------------|
| Declaraciones           | No se puede declarar dos veces el mismo pin ni la misma variable.                |
| Pines                    | El número de pin debe estar en el rango físico del Arduino Uno (0-13).           |
| Modos de operación      | `set` exige que el pin haya sido declarado `OUTPUT`; `read` exige `INPUT`/`INPUT_PULLUP`. |
| Identificadores          | Todo pin o variable usado debe haber sido declarado antes (si no, error "no declarado"). |
| Retardos                 | `delay`/`repeat` aceptan un entero literal o una variable ya declarada; se valida rango del literal. |

Todo esto se implementa recorriendo el árbol de parseo con el patrón
**Visitor** (`SemanticAnalyzer` en `semantic_analyzer.py`), que va
llenando una **tabla de símbolos** (`symbol_table.py`) y acumulando
una lista de **errores semánticos**. Los errores léxicos y
sintácticos (por ejemplo, olvidarte un `;`) se capturan aparte, con un
`ErrorListener` personalizado en `main.py`, y se muestran en el mismo
reporte final bajo una sección separada.

## Extender el proyecto (ideas)

- Agregar pines analógicos (`A0`-`A5`) como un token separado.
- Detectar el uso del pin 13 (LED integrado) y emitir una advertencia
  en vez de un error.
- Soportar bloques `if` / condicionales sobre el resultado de `read`.
- Exportar el reporte de errores y la tabla de símbolos a un archivo
  `.txt` o `.json` además de imprimirlos en consola.


---

# Fase 2 — Generación de código intermedio

El generador recorre el **AST ya validado** en la Fase 1 y **reutiliza la
misma tabla de símbolos**; no vuelve a hacer análisis semántico. `main.py`
solo lo invoca si no hubo errores léxicos, sintácticos ni semánticos.

```
programa.dsl ──ANTLR4──▶ AST ──SemanticAnalyzer──▶ tabla de símbolos + errores
                          │                              │
                          └────────── (si no hay errores) ┘
                                      │
                      QuadrupleGenerator  (quadruples.py)
                                      │
                               cuádruplos ──▶ salida/<programa>.quads.txt
                                      │
                         LLVMGenerator  (llvm_ir.py)
                                      │
                                   LLVM IR ──▶ salida/<programa>.ll
```

## Cambios en el lenguaje (retrocompatibles)

La Fase 1 no tenía expresiones, asignaciones ni estructuras de control, que
la Fase 2 debe traducir. Se amplió la gramática sin romper ningún programa
válido de la Fase 1 (`ejemplo_valido.dsl` y `ejemplo_con_errores.dsl` dan
exactamente los mismos resultados que antes):

| Construcción | Sintaxis |
|---|---|
| Variable con expresión | `var x = a * 2 + 1;` |
| Asignación | `x = x - 1;` |
| Lectura a variable | `read 7 into s;` (`read 7;` sigue valiendo) |
| Escritura con expresión | `set 13 = HIGH;`  `set 13 = x > 3;` |
| Retardo / repetición con expresión | `delay espera / 2;`  `repeat n + 1 times { ... }` |
| SI ... SINO | `si cond { ... } sino { ... }` (también `if ... else ...`) |
| MIENTRAS | `mientras cond { ... }` (también `while`) |
| Operadores | `* / %`, `+ -`, `< <= > >= == !=`, `-x`, paréntesis (en ese orden de precedencia) |

Todo valor es un entero de 32 bits con signo; una comparación vale 1 o 0
(como en C) y `HIGH`/`LOW` valen 1 y 0. La semántica añadió: variables
declaradas antes de usarse en cualquier expresión, literales de 32 bits y
división entre la constante 0.

**Palabras reservadas nuevas:** `into`, `if`, `si`, `else`, `sino`, `while`,
`mientras`. Un programa de la Fase 1 que usara una de ellas como nombre de
variable debe renombrarla.

## Uso

```
python main.py ejemplos\ejemplo_fase2.dsl              # análisis + cuádruplos + .ll en salida\
python main.py ejemplos\ejemplo_fase2.dsl --validar    # además valida y ejecuta con LLVM
python main.py ejemplos\ejemplo_fase2.dsl --salida otra_carpeta
python main.py ejemplos\ejemplo_fase2.dsl --solo-analisis   # solo Fase 1
python validar_llvm.py salida\ejemplo_fase2.ll          # solo la validación
python -m unittest discover -s tests -v                 # pruebas
```

## Cuádruplos

Formato `(op, arg1, arg2, resultado)`; `_` significa "vacío". Los temporales
(`t1`, `t2`...) se asignan una sola vez.

| Operador | Significado |
|---|---|
| `+ - * / %` | `resultado = arg1 op arg2` |
| `< <= > >= == !=` | `resultado = 1` si se cumple, `0` si no |
| `UMINUS` | `resultado = -arg1` |
| `=` | `resultado = arg1` (asignación a variable) |
| `PARAM` | empuja `arg1` como argumento de la siguiente llamada |
| `CALL` | `resultado = arg1(últimos arg2 PARAM)`; sin resultado si la función no devuelve valor |
| `LABEL` / `GOTO` | define una etiqueta / salto incondicional |
| `IF_FALSE` | si `arg1 == 0` salta a la etiqueta; si no, continúa |
| `FUNC_BEGIN` / `RETURN` / `FUNC_END` | el programa se envuelve en `main` |

Las "llamadas a funciones" son las del núcleo de Arduino (`pinMode`,
`digitalWrite`, `digitalRead`, `delay`; definidas en `hardware_catalog.ARDUINO_API`):

| DSL | Cuádruplos |
|---|---|
| `pin 13 as OUTPUT;` | `PARAM 13` `PARAM OUTPUT` `CALL pinMode, 2` |
| `set 13 = e;` | (cálculo de `e`) `PARAM 13` `PARAM e` `CALL digitalWrite, 2` |
| `read 7 into s;` | `PARAM 7` `CALL digitalRead, 1, t` `= t, _, s` |
| `delay e;` | (cálculo de `e`) `PARAM e` `CALL delay, 1` |

Estructuras de control (las etiquetas llevan un número único por construcción):

```
si c { A } sino { B }          mientras c { A }             repeat n times { A }

    <c>                        while_cond_1:                    = n, _, $rep1
    IF_FALSE c, if_else_1          <c>                      repeat_cond_1:
  if_then_1:                       IF_FALSE c, while_end_1      > $rep1, 0, t
    A                          while_body_1:                    IF_FALSE t, repeat_end_1
    GOTO if_end_1                  A                        repeat_body_1:
  if_else_1:                       GOTO while_cond_1            A
    B                          while_end_1:                     - $rep1, 1, t2 ; = t2, _, $rep1
  if_end_1:                                                     GOTO repeat_cond_1
                                                            repeat_end_1:
```

`repeat` evalúa el conteo **una sola vez** y lo copia a un contador oculto
(`$rep1`, nombre imposible para un ID del DSL); `n <= 0` no ejecuta nada.

## LLVM IR

| Concepto | LLVM IR |
|---|---|
| Programa | `define i32 @main()` |
| Variable (y contador de `repeat`) | `alloca i32` en `entry` (inicializada a 0); `load` / `store` |
| Temporal `tN` | valor SSA `%tN` |
| `+ - * / %` | `add sub mul sdiv srem` |
| Comparación | `icmp slt/sle/sgt/sge/eq/ne` (i1); si se usa como número, además `zext` a i32 |
| Etiqueta / `GOTO` / `IF_FALSE` | bloque básico / `br label` / `br i1 %c, label %v, label %f` |
| `PARAM` + `CALL` | `call` a funciones externas declaradas con `declare` |

Se usan punteros opacos (`ptr`): **se requiere LLVM 15 o superior**.
No se fija `target triple`, para poder ejecutarlo en el equipo con `lli`.

## Validación del LLVM IR

`validar_llvm.py` (o `main.py --validar`) ejecuta y registra en
`salida/<programa>.validacion.log` la fecha, el sistema, la versión de cada
herramienta, cada comando y su resultado:

```
llvm-as    programa.ll -o programa.bc                  # ensambla y verifica
opt        -passes=verify -disable-output programa.ll  # verificador
opt        -passes=mem2reg,verify -S programa.ll -o programa.mem2reg.ll
llvm-link  programa.ll runtime/arduino_stub.ll -S -o programa.linked.ll
lli        programa.linked.ll                          # ejecuta; guarda la traza
```

Las herramientas se buscan en el PATH (con o sin sufijo de versión, p. ej.
`llvm-as-18`) o en la carpeta de la variable de entorno `LLVM_BIN`.
`runtime/arduino_stub.ll` simula Arduino: cada función imprime su llamada y
`digitalRead` alterna 0, 1, 0, 1... Así la ejecución produce una **traza**
comparable con la esperada.

Instalación de LLVM: Ubuntu/Debian `sudo apt install llvm`; Windows: instalador
de https://github.com/llvm/llvm-project/releases (marcar "Add LLVM to PATH");
macOS `brew install llvm`.

**Resultados obtenidos** (LLVM 18.1.3, Ubuntu 24.04; ver `salida/*.validacion.log`):
`ejemplo_valido.dsl` y `ejemplo_fase2.dsl` pasan los cinco pasos, y las trazas
coinciden con las calculadas a mano.

## Pruebas

`tests/test_fase2.py` (48 pruebas, solo biblioteca estándar) cubre:
expresiones (precedencia, paréntesis, asociatividad, `/ % -x`), relacionales,
asignaciones, E/S (`pinMode`, `digitalWrite`, `digitalRead`, `delay`),
`si/sino` (con y sin `sino`, anidados), `mientras` (anidados, controlado por
una lectura), `repeat`, estructura del IR (bloques, terminadores, `zext`),
rechazo de programas con errores, verificación con LLVM y comparación de la
traza de ejecución con la esperada. Las de LLVM se omiten si no está instalado.

## Limitaciones conocidas

- Los enteros son `i32` con signo. Un literal entre 2^31 y 2^32-1 (permitido
  por compatibilidad con el `unsigned long` de `delay`) se interpreta en
  complemento a dos en comparaciones y en `repeat`.
- Dividir entre una variable que vale 0 en ejecución es comportamiento
  indefinido en LLVM (`sdiv`/`srem`); solo se detecta el divisor literal `0`.
- Las funciones "de usuario" no existen en el DSL: las llamadas son siempre
  a la API externa de Arduino.
- `ArduinoDSLParser.py` y compañía se regeneraron con ANTLR 4.11.1 (el único
  disponible al desarrollar) y se ajustó la cadena de versión a 4.13.2; el
  código es equivalente. Para obtener la salida canónica, ejecute `generar.bat`
  con su `antlr-4.13.2-complete.jar`.
