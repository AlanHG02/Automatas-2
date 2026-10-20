grammar ArduinoDSL;

// ============================================================
// REGLAS DEL PARSER
// ============================================================
// FASE 2: la gramática de la Fase 1 se amplió de forma
// retrocompatible (todo programa válido de la Fase 1 sigue siendo
// válido) para poder expresar lo que el generador de código
// intermedio debe traducir: expresiones aritméticas/relacionales,
// asignaciones, lectura hacia variable y las estructuras de control
// SI...SINO y MIENTRAS.
// ============================================================

// Programa: una secuencia de sentencias hasta fin de archivo
program
    : statement* EOF
    ;

statement
    : pinDeclaration
    | varDeclaration
    | assignStatement
    | setStatement
    | readStatement
    | delayStatement
    | repeatStatement
    | ifStatement
    | whileStatement
    ;

// Bloque de sentencias entre llaves
block
    : '{' statement* '}'
    ;

// Declaración de un pin y su modo:  pin 13 as OUTPUT;
pinDeclaration
    : 'pin' INT 'as' MODE ';'
    ;

// Declaración de una variable entera:  var espera = 500;  var t = a + 1;
varDeclaration
    : 'var' ID '=' expr ';'
    ;

// Asignación a una variable ya declarada:  espera = espera * 2;
assignStatement
    : ID '=' expr ';'
    ;

// Escritura digital sobre un pin:  set 13 = HIGH;  set 13 = x > 3;
setStatement
    : 'set' INT '=' expr ';'
    ;

// Lectura de un pin:  read 7;   o guardando el valor:  read 7 into s;
readStatement
    : 'read' INT ('into' ID)? ';'
    ;

// Retardo en milisegundos:  delay 1000;  delay espera * 2;
delayStatement
    : 'delay' expr ';'
    ;

// Bloque repetido N veces:  repeat 5 times { ... }
repeatStatement
    : 'repeat' expr 'times' block
    ;

// Condicional SI ... SINO  (se aceptan ambas formas de las palabras clave)
//   if s == HIGH { ... } else { ... }      si s == HIGH { ... } sino { ... }
ifStatement
    : ('if' | 'si') expr block (('else' | 'sino') block)?
    ;

// Bucle MIENTRAS:  while i < 10 { ... }     mientras i < 10 { ... }
whileStatement
    : ('while' | 'mientras') expr block
    ;

// Expresiones. El orden de las alternativas fija la precedencia
// (de mayor a menor): paréntesis, negación, * / %, + -, relacionales.
// Todo valor es un entero de 32 bits; una comparación produce 1 o 0
// (como en C), y HIGH/LOW valen 1 y 0.
expr
    : '(' expr ')'                                  # parenExpr
    | '-' expr                                      # negExpr
    | expr op=('*' | '/' | '%') expr                # mulExpr
    | expr op=('+' | '-') expr                      # addExpr
    | expr op=('<' | '<=' | '>' | '>=' | '==' | '!=') expr   # relExpr
    | INT                                           # intExpr
    | LEVEL                                         # levelExpr
    | ID                                            # idExpr
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
