# Generated from ArduinoDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ArduinoDSLParser import ArduinoDSLParser
else:
    from ArduinoDSLParser import ArduinoDSLParser

# This class defines a complete listener for a parse tree produced by ArduinoDSLParser.
class ArduinoDSLListener(ParseTreeListener):

    # Enter a parse tree produced by ArduinoDSLParser#program.
    def enterProgram(self, ctx:ArduinoDSLParser.ProgramContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#program.
    def exitProgram(self, ctx:ArduinoDSLParser.ProgramContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#statement.
    def enterStatement(self, ctx:ArduinoDSLParser.StatementContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#statement.
    def exitStatement(self, ctx:ArduinoDSLParser.StatementContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#block.
    def enterBlock(self, ctx:ArduinoDSLParser.BlockContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#block.
    def exitBlock(self, ctx:ArduinoDSLParser.BlockContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#pinDeclaration.
    def enterPinDeclaration(self, ctx:ArduinoDSLParser.PinDeclarationContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#pinDeclaration.
    def exitPinDeclaration(self, ctx:ArduinoDSLParser.PinDeclarationContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#varDeclaration.
    def enterVarDeclaration(self, ctx:ArduinoDSLParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#varDeclaration.
    def exitVarDeclaration(self, ctx:ArduinoDSLParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#assignStatement.
    def enterAssignStatement(self, ctx:ArduinoDSLParser.AssignStatementContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#assignStatement.
    def exitAssignStatement(self, ctx:ArduinoDSLParser.AssignStatementContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#setStatement.
    def enterSetStatement(self, ctx:ArduinoDSLParser.SetStatementContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#setStatement.
    def exitSetStatement(self, ctx:ArduinoDSLParser.SetStatementContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#readStatement.
    def enterReadStatement(self, ctx:ArduinoDSLParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#readStatement.
    def exitReadStatement(self, ctx:ArduinoDSLParser.ReadStatementContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#delayStatement.
    def enterDelayStatement(self, ctx:ArduinoDSLParser.DelayStatementContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#delayStatement.
    def exitDelayStatement(self, ctx:ArduinoDSLParser.DelayStatementContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#repeatStatement.
    def enterRepeatStatement(self, ctx:ArduinoDSLParser.RepeatStatementContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#repeatStatement.
    def exitRepeatStatement(self, ctx:ArduinoDSLParser.RepeatStatementContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#ifStatement.
    def enterIfStatement(self, ctx:ArduinoDSLParser.IfStatementContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#ifStatement.
    def exitIfStatement(self, ctx:ArduinoDSLParser.IfStatementContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#whileStatement.
    def enterWhileStatement(self, ctx:ArduinoDSLParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#whileStatement.
    def exitWhileStatement(self, ctx:ArduinoDSLParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#intExpr.
    def enterIntExpr(self, ctx:ArduinoDSLParser.IntExprContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#intExpr.
    def exitIntExpr(self, ctx:ArduinoDSLParser.IntExprContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#addExpr.
    def enterAddExpr(self, ctx:ArduinoDSLParser.AddExprContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#addExpr.
    def exitAddExpr(self, ctx:ArduinoDSLParser.AddExprContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#negExpr.
    def enterNegExpr(self, ctx:ArduinoDSLParser.NegExprContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#negExpr.
    def exitNegExpr(self, ctx:ArduinoDSLParser.NegExprContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#levelExpr.
    def enterLevelExpr(self, ctx:ArduinoDSLParser.LevelExprContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#levelExpr.
    def exitLevelExpr(self, ctx:ArduinoDSLParser.LevelExprContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#mulExpr.
    def enterMulExpr(self, ctx:ArduinoDSLParser.MulExprContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#mulExpr.
    def exitMulExpr(self, ctx:ArduinoDSLParser.MulExprContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#relExpr.
    def enterRelExpr(self, ctx:ArduinoDSLParser.RelExprContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#relExpr.
    def exitRelExpr(self, ctx:ArduinoDSLParser.RelExprContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#parenExpr.
    def enterParenExpr(self, ctx:ArduinoDSLParser.ParenExprContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#parenExpr.
    def exitParenExpr(self, ctx:ArduinoDSLParser.ParenExprContext):
        pass


    # Enter a parse tree produced by ArduinoDSLParser#idExpr.
    def enterIdExpr(self, ctx:ArduinoDSLParser.IdExprContext):
        pass

    # Exit a parse tree produced by ArduinoDSLParser#idExpr.
    def exitIdExpr(self, ctx:ArduinoDSLParser.IdExprContext):
        pass



del ArduinoDSLParser