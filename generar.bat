@echo off


setlocal

set ANTLR_JAR=C:\antlr\antlr-4.13.2-complete.jar

if not exist "%ANTLR_JAR%" (
    echo ERROR: no se encontro %ANTLR_JAR%
    echo Revisar el archivo
    exit /b 1
)

echo Generando lexer/parser/visitor en Python3 a partir de ArduinoDSL.g4 ...
java -jar "%ANTLR_JAR%" -Dlanguage=Python3 -visitor ArduinoDSL.g4

if %errorlevel% neq 0 (
    echo ERROR: fallo la generacion con ANTLR4
    exit /b 1
)

echo.
echo Listo. Se generaron los archivos ArduinoDSL*.py
endlocal
