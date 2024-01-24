__author__ = 'jszheng'

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from target.LabeledExprLexer import LabeledExprLexer
from target.LabeledExprParser import LabeledExprParser
from eval_visitor import EvalVisitor

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())

    lexer = LabeledExprLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = LabeledExprParser(token_stream)
    tree = parser.prog()

    visitor = EvalVisitor()
    visitor.visit(tree)