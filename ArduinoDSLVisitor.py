# Generated from ArduinoDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ArduinoDSLParser import ArduinoDSLParser
else:
    from ArduinoDSLParser import ArduinoDSLParser

# This class defines a complete generic visitor for a parse tree produced by ArduinoDSLParser.

class ArduinoDSLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ArduinoDSLParser#program.
    def visitProgram(self, ctx:ArduinoDSLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#statement.
    def visitStatement(self, ctx:ArduinoDSLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#pinDeclaration.
    def visitPinDeclaration(self, ctx:ArduinoDSLParser.PinDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#varDeclaration.
    def visitVarDeclaration(self, ctx:ArduinoDSLParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#setStatement.
    def visitSetStatement(self, ctx:ArduinoDSLParser.SetStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#readStatement.
    def visitReadStatement(self, ctx:ArduinoDSLParser.ReadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#delayStatement.
    def visitDelayStatement(self, ctx:ArduinoDSLParser.DelayStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#repeatStatement.
    def visitRepeatStatement(self, ctx:ArduinoDSLParser.RepeatStatementContext):
        return self.visitChildren(ctx)



del ArduinoDSLParser