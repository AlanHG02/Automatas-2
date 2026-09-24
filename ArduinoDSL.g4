grammar ArduinoDSL;

// ============================================================
// REGLAS DEL PARSER
// ============================================================

// Programa: una secuencia de sentencias hasta fin de archivo
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

// Declaración de un pin y su modo:  pin 13 as OUTPUT;
pinDeclaration
    : 'pin' INT 'as' MODE ';'
    ;

// Declaración de una variable entera:  var espera = 500;
varDeclaration
    : 'var' ID '=' INT ';'
    ;

// Escritura digital sobre un pin:  set 13 = HIGH;
setStatement
    : 'set' INT '=' LEVEL ';'
    ;

// Lectura de un pin:  read 7;
readStatement
    : 'read' INT ';'
    ;

// Retardo en milisegundos, con literal o variable:  delay 1000;  delay espera;
delayStatement
    : 'delay' (INT | ID) ';'
    ;

// Bloque repetido N veces:  repeat 5 times { ... }
repeatStatement
    : 'repeat' (INT | ID) 'times' '{' statement* '}'
    ;

// ============================================================
// REGLAS DEL LEXER
// (el orden importa: las reglas explícitas se prueban en el
//  orden en que aparecen, por eso MODE y LEVEL van antes que ID)
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

ID
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

INT
    : [0-9]+
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
