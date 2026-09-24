grammar ArduinoDSL;

// ============================================================
// REGLAS DEL PARSER
// ============================================================

// Estructura del programa: una secuencia de sentencias hasta EOF
program
    : statement* EOF
    ;

statement
    : pinDeclaration
    | varDeclaration
    | setStatement
    | readStatement
    | delayStatement
    | repeatStatement
    ;

// Declaración de pines:  pin led = 13 as OUTPUT;   pin sensor = A0 as INPUT;
// El identificador (ID) es el nombre simbólico con el que luego se
// referencia el pin en 'set' / 'read'. pinRef es el pin físico real.
pinDeclaration
    : 'pin' ID '=' pinRef 'as' MODE ';'
    ;

pinRef
    : INT          // pin digital, p. ej. 13
    | ANALOG_PIN   // pin analógico, p. ej. A0
    ;

// Declaración de variable:  var espera = 500;   var ajuste = -50;
varDeclaration
    : 'var' ID '=' number ';'
    ;

// Instrucción de salida (escritura digital):  set led = HIGH;
setStatement
    : 'set' ID '=' LEVEL ';'
    ;

// Instrucción de entrada (lectura digital):  read boton;
readStatement
    : 'read' ID ';'
    ;

// Retardo, en milisegundos. Acepta un literal con signo o una variable:
//   delay 500;   delay -100;   delay espera;
delayStatement
    : 'delay' (number | ID) ';'
    ;

// Bloque repetido N veces:  repeat 5 times { ... }
repeatStatement
    : 'repeat' (number | ID) 'times' '{' statement* '}'
    ;

// Número entero con signo opcional (permite representar retardos
// negativos para que el analizador semántico pueda detectarlos y
// reportarlos como error).
number
    : MINUS? INT
    ;

// ============================================================
// REGLAS DEL LEXER
// (el orden importa: ante un empate de longitud, ANTLR4 elige la
//  regla definida primero; por eso MODE, LEVEL y ANALOG_PIN van
//  antes que ID)
// ============================================================

MODE
    : 'OUTPUT'
    | 'INPUT_PULLUP'
    | 'INPUT'
    ;

LEVEL
    : 'HIGH'
    | 'LOW'
    ;

// Pines analógicos del Arduino Uno: A0-A5
ANALOG_PIN
    : 'A' [0-5]
    ;

ID
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

INT
    : [0-9]+
    ;

MINUS
    : '-'
    ;

WS
    : [ \t\r\n]+ -> skip
    ;

LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;
