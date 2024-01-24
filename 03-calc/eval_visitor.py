__author__ = 'jszheng'

from target.LabeledExprVisitor import LabeledExprVisitor
from target.LabeledExprParser import LabeledExprParser

class EvalVisitor(LabeledExprVisitor):
    
    # "memory" for our calculator; variable/value pairs go here
    def __init__(self):
        self.memory = {}

    # ID '=' expr NEWLINE
    def visitAssign(self, ctx):
        name = ctx.ID().getText()           # id is left-hand side of '='
        value = self.visit(ctx.expr())      # compute value of expression on right
        self.memory[name] = value           # store it in our memory
        return value

    # expr NEWLINE
    def visitPrintExpr(self, ctx):
        value = self.visit(ctx.expr())      # evaluate the expr child
        print(value)                        # print the result
        return 0                            # return dummy value

    # INT
    def visitInt(self, ctx):
        return ctx.INT().getText()

    # ID
    def visitId(self, ctx):
        name = ctx.ID().getText()
        if name in self.memory:
            return self.memory[name]
        return 0

    # expr op=('*'|'/') expr
    def visitMulDiv(self, ctx):
        left = int(self.visit(ctx.expr(0)))         # get value of left subexpression
        right = int(self.visit(ctx.expr(1)))        # get value of right subexpression
        if ctx.getChild(1).getSymbol().type == LabeledExprParser.MUL:
            return left * right
        return left / right

    # expr op=('+'|'-') expr
    def visitAddSub(self, ctx):
        left = int(self.visit(ctx.expr(0)))         # get value of left subexpression
        right = int(self.visit(ctx.expr(1)))        # get value of right subexpression
        if ctx.getChild(1).getSymbol().type == LabeledExprParser.ADD:
            return left + right
        return left - right

    # '(' expr ')'
    def visitParens(self, ctx):
        return self.visit(ctx.expr())               # return child expr's value