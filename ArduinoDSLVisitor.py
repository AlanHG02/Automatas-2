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


    # Visit a parse tree produced by ArduinoDSLParser#block.
    def visitBlock(self, ctx:ArduinoDSLParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#pinDeclaration.
    def visitPinDeclaration(self, ctx:ArduinoDSLParser.PinDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#varDeclaration.
    def visitVarDeclaration(self, ctx:ArduinoDSLParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#assignStatement.
    def visitAssignStatement(self, ctx:ArduinoDSLParser.AssignStatementContext):
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


    # Visit a parse tree produced by ArduinoDSLParser#ifStatement.
    def visitIfStatement(self, ctx:ArduinoDSLParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#whileStatement.
    def visitWhileStatement(self, ctx:ArduinoDSLParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#intExpr.
    def visitIntExpr(self, ctx:ArduinoDSLParser.IntExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#addExpr.
    def visitAddExpr(self, ctx:ArduinoDSLParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#negExpr.
    def visitNegExpr(self, ctx:ArduinoDSLParser.NegExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#levelExpr.
    def visitLevelExpr(self, ctx:ArduinoDSLParser.LevelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#mulExpr.
    def visitMulExpr(self, ctx:ArduinoDSLParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#relExpr.
    def visitRelExpr(self, ctx:ArduinoDSLParser.RelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#parenExpr.
    def visitParenExpr(self, ctx:ArduinoDSLParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArduinoDSLParser#idExpr.
    def visitIdExpr(self, ctx:ArduinoDSLParser.IdExprContext):
        return self.visitChildren(ctx)



del ArduinoDSLParser