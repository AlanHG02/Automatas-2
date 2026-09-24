# Generated from ArduinoDSL.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,21,90,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,1,0,5,0,22,8,0,10,0,12,0,25,9,0,1,0,1,
        0,1,1,1,1,1,1,1,1,1,1,1,1,3,1,35,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,6,
        1,6,1,6,1,6,1,7,1,7,1,7,3,7,66,8,7,1,7,1,7,1,8,1,8,1,8,3,8,73,8,
        8,1,8,1,8,1,8,5,8,78,8,8,10,8,12,8,81,9,8,1,8,1,8,1,9,3,9,86,8,9,
        1,9,1,9,1,9,0,0,10,0,2,4,6,8,10,12,14,16,18,0,1,2,0,15,15,17,17,
        89,0,23,1,0,0,0,2,34,1,0,0,0,4,36,1,0,0,0,6,44,1,0,0,0,8,46,1,0,
        0,0,10,52,1,0,0,0,12,58,1,0,0,0,14,62,1,0,0,0,16,69,1,0,0,0,18,85,
        1,0,0,0,20,22,3,2,1,0,21,20,1,0,0,0,22,25,1,0,0,0,23,21,1,0,0,0,
        23,24,1,0,0,0,24,26,1,0,0,0,25,23,1,0,0,0,26,27,5,0,0,1,27,1,1,0,
        0,0,28,35,3,4,2,0,29,35,3,8,4,0,30,35,3,10,5,0,31,35,3,12,6,0,32,
        35,3,14,7,0,33,35,3,16,8,0,34,28,1,0,0,0,34,29,1,0,0,0,34,30,1,0,
        0,0,34,31,1,0,0,0,34,32,1,0,0,0,34,33,1,0,0,0,35,3,1,0,0,0,36,37,
        5,1,0,0,37,38,5,16,0,0,38,39,5,2,0,0,39,40,3,6,3,0,40,41,5,3,0,0,
        41,42,5,13,0,0,42,43,5,4,0,0,43,5,1,0,0,0,44,45,7,0,0,0,45,7,1,0,
        0,0,46,47,5,5,0,0,47,48,5,16,0,0,48,49,5,2,0,0,49,50,3,18,9,0,50,
        51,5,4,0,0,51,9,1,0,0,0,52,53,5,6,0,0,53,54,5,16,0,0,54,55,5,2,0,
        0,55,56,5,14,0,0,56,57,5,4,0,0,57,11,1,0,0,0,58,59,5,7,0,0,59,60,
        5,16,0,0,60,61,5,4,0,0,61,13,1,0,0,0,62,65,5,8,0,0,63,66,3,18,9,
        0,64,66,5,16,0,0,65,63,1,0,0,0,65,64,1,0,0,0,66,67,1,0,0,0,67,68,
        5,4,0,0,68,15,1,0,0,0,69,72,5,9,0,0,70,73,3,18,9,0,71,73,5,16,0,
        0,72,70,1,0,0,0,72,71,1,0,0,0,73,74,1,0,0,0,74,75,5,10,0,0,75,79,
        5,11,0,0,76,78,3,2,1,0,77,76,1,0,0,0,78,81,1,0,0,0,79,77,1,0,0,0,
        79,80,1,0,0,0,80,82,1,0,0,0,81,79,1,0,0,0,82,83,5,12,0,0,83,17,1,
        0,0,0,84,86,5,18,0,0,85,84,1,0,0,0,85,86,1,0,0,0,86,87,1,0,0,0,87,
        88,5,17,0,0,88,19,1,0,0,0,6,23,34,65,72,79,85
    ]

class ArduinoDSLParser ( Parser ):

    grammarFileName = "ArduinoDSL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'pin'", "'='", "'as'", "';'", "'var'", 
                     "'set'", "'read'", "'delay'", "'repeat'", "'times'", 
                     "'{'", "'}'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'-'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "MODE", "LEVEL", "ANALOG_PIN", "ID", 
                      "INT", "MINUS", "WS", "LINE_COMMENT", "BLOCK_COMMENT" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_pinDeclaration = 2
    RULE_pinRef = 3
    RULE_varDeclaration = 4
    RULE_setStatement = 5
    RULE_readStatement = 6
    RULE_delayStatement = 7
    RULE_repeatStatement = 8
    RULE_number = 9

    ruleNames =  [ "program", "statement", "pinDeclaration", "pinRef", "varDeclaration", 
                   "setStatement", "readStatement", "delayStatement", "repeatStatement", 
                   "number" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    MODE=13
    LEVEL=14
    ANALOG_PIN=15
    ID=16
    INT=17
    MINUS=18
    WS=19
    LINE_COMMENT=20
    BLOCK_COMMENT=21

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ArduinoDSLParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ArduinoDSLParser.StatementContext)
            else:
                return self.getTypedRuleContext(ArduinoDSLParser.StatementContext,i)


        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = ArduinoDSLParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 994) != 0):
                self.state = 20
                self.statement()
                self.state = 25
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 26
            self.match(ArduinoDSLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pinDeclaration(self):
            return self.getTypedRuleContext(ArduinoDSLParser.PinDeclarationContext,0)


        def varDeclaration(self):
            return self.getTypedRuleContext(ArduinoDSLParser.VarDeclarationContext,0)


        def setStatement(self):
            return self.getTypedRuleContext(ArduinoDSLParser.SetStatementContext,0)


        def readStatement(self):
            return self.getTypedRuleContext(ArduinoDSLParser.ReadStatementContext,0)


        def delayStatement(self):
            return self.getTypedRuleContext(ArduinoDSLParser.DelayStatementContext,0)


        def repeatStatement(self):
            return self.getTypedRuleContext(ArduinoDSLParser.RepeatStatementContext,0)


        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = ArduinoDSLParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 34
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 28
                self.pinDeclaration()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 29
                self.varDeclaration()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 3)
                self.state = 30
                self.setStatement()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 4)
                self.state = 31
                self.readStatement()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 5)
                self.state = 32
                self.delayStatement()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 6)
                self.state = 33
                self.repeatStatement()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PinDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ArduinoDSLParser.ID, 0)

        def pinRef(self):
            return self.getTypedRuleContext(ArduinoDSLParser.PinRefContext,0)


        def MODE(self):
            return self.getToken(ArduinoDSLParser.MODE, 0)

        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_pinDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPinDeclaration" ):
                listener.enterPinDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPinDeclaration" ):
                listener.exitPinDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPinDeclaration" ):
                return visitor.visitPinDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def pinDeclaration(self):

        localctx = ArduinoDSLParser.PinDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_pinDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(ArduinoDSLParser.T__0)
            self.state = 37
            self.match(ArduinoDSLParser.ID)
            self.state = 38
            self.match(ArduinoDSLParser.T__1)
            self.state = 39
            self.pinRef()
            self.state = 40
            self.match(ArduinoDSLParser.T__2)
            self.state = 41
            self.match(ArduinoDSLParser.MODE)
            self.state = 42
            self.match(ArduinoDSLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PinRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(ArduinoDSLParser.INT, 0)

        def ANALOG_PIN(self):
            return self.getToken(ArduinoDSLParser.ANALOG_PIN, 0)

        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_pinRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPinRef" ):
                listener.enterPinRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPinRef" ):
                listener.exitPinRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPinRef" ):
                return visitor.visitPinRef(self)
            else:
                return visitor.visitChildren(self)




    def pinRef(self):

        localctx = ArduinoDSLParser.PinRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_pinRef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            _la = self._input.LA(1)
            if not(_la==15 or _la==17):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ArduinoDSLParser.ID, 0)

        def number(self):
            return self.getTypedRuleContext(ArduinoDSLParser.NumberContext,0)


        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_varDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarDeclaration" ):
                listener.enterVarDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarDeclaration" ):
                listener.exitVarDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDeclaration" ):
                return visitor.visitVarDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def varDeclaration(self):

        localctx = ArduinoDSLParser.VarDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_varDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(ArduinoDSLParser.T__4)
            self.state = 47
            self.match(ArduinoDSLParser.ID)
            self.state = 48
            self.match(ArduinoDSLParser.T__1)
            self.state = 49
            self.number()
            self.state = 50
            self.match(ArduinoDSLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ArduinoDSLParser.ID, 0)

        def LEVEL(self):
            return self.getToken(ArduinoDSLParser.LEVEL, 0)

        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_setStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetStatement" ):
                listener.enterSetStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetStatement" ):
                listener.exitSetStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetStatement" ):
                return visitor.visitSetStatement(self)
            else:
                return visitor.visitChildren(self)




    def setStatement(self):

        localctx = ArduinoDSLParser.SetStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_setStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.match(ArduinoDSLParser.T__5)
            self.state = 53
            self.match(ArduinoDSLParser.ID)
            self.state = 54
            self.match(ArduinoDSLParser.T__1)
            self.state = 55
            self.match(ArduinoDSLParser.LEVEL)
            self.state = 56
            self.match(ArduinoDSLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReadStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ArduinoDSLParser.ID, 0)

        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_readStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReadStatement" ):
                listener.enterReadStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReadStatement" ):
                listener.exitReadStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReadStatement" ):
                return visitor.visitReadStatement(self)
            else:
                return visitor.visitChildren(self)




    def readStatement(self):

        localctx = ArduinoDSLParser.ReadStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_readStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(ArduinoDSLParser.T__6)
            self.state = 59
            self.match(ArduinoDSLParser.ID)
            self.state = 60
            self.match(ArduinoDSLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DelayStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(ArduinoDSLParser.NumberContext,0)


        def ID(self):
            return self.getToken(ArduinoDSLParser.ID, 0)

        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_delayStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDelayStatement" ):
                listener.enterDelayStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDelayStatement" ):
                listener.exitDelayStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDelayStatement" ):
                return visitor.visitDelayStatement(self)
            else:
                return visitor.visitChildren(self)




    def delayStatement(self):

        localctx = ArduinoDSLParser.DelayStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_delayStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(ArduinoDSLParser.T__7)
            self.state = 65
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17, 18]:
                self.state = 63
                self.number()
                pass
            elif token in [16]:
                self.state = 64
                self.match(ArduinoDSLParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 67
            self.match(ArduinoDSLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RepeatStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(ArduinoDSLParser.NumberContext,0)


        def ID(self):
            return self.getToken(ArduinoDSLParser.ID, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ArduinoDSLParser.StatementContext)
            else:
                return self.getTypedRuleContext(ArduinoDSLParser.StatementContext,i)


        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_repeatStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRepeatStatement" ):
                listener.enterRepeatStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRepeatStatement" ):
                listener.exitRepeatStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRepeatStatement" ):
                return visitor.visitRepeatStatement(self)
            else:
                return visitor.visitChildren(self)




    def repeatStatement(self):

        localctx = ArduinoDSLParser.RepeatStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_repeatStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(ArduinoDSLParser.T__8)
            self.state = 72
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17, 18]:
                self.state = 70
                self.number()
                pass
            elif token in [16]:
                self.state = 71
                self.match(ArduinoDSLParser.ID)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 74
            self.match(ArduinoDSLParser.T__9)
            self.state = 75
            self.match(ArduinoDSLParser.T__10)
            self.state = 79
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 994) != 0):
                self.state = 76
                self.statement()
                self.state = 81
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 82
            self.match(ArduinoDSLParser.T__11)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(ArduinoDSLParser.INT, 0)

        def MINUS(self):
            return self.getToken(ArduinoDSLParser.MINUS, 0)

        def getRuleIndex(self):
            return ArduinoDSLParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)




    def number(self):

        localctx = ArduinoDSLParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==18:
                self.state = 84
                self.match(ArduinoDSLParser.MINUS)


            self.state = 87
            self.match(ArduinoDSLParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





