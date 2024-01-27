__author__ = 'jszheng'

import sys
from antlr4 import *

from target.RowsLexer import RowsLexer
from target.RowsParser import RowsParser

if __name__ == '__main__':
    if len(sys.argv) > 1:
        col_num = int(sys.argv[1])
        input_stream = FileStream(sys.argv[2])
    else:
        print('Usage: python col.py #col file')
        exit(1)

    lexer = RowsLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = RowsParser(token_stream)
    parser.column = col_num         # pass column number!
    parser.buildParseTrees = False  # don't waste time bulding a tree
    tree = parser.rows()