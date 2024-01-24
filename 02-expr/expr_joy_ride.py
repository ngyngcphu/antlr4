__author__ = 'jszheng'

import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from target.ExprLexer import ExprLexer
from target.ExprParser import ExprParser

if __name__ == '__main__':
    
    # create an input stream of characters for the lexer
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.readline())

    # create the lexer and parser objects and a token stream “pipe” between them
    lexer = ExprLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ExprParser(token_stream)
    
    # parse; start at prog
    tree = parser.prog()

    lisp_tree_str = tree.toStringTree(recog=parser)
    print(lisp_tree_str)