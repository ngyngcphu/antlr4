import sys

# import ANTLR's runtime library, Lexer and Parser generated from ANTLR tool
from antlr4 import *
from target.ArrayInitLexer import ArrayInitLexer
from target.ArrayInitParser import ArrayInitParser
from short_to_unicode_string import ShortToUnicodeString

def main(argv):
    
    # create a FileStream that reads from input file
    istream = FileStream(argv[1])
    
    # create a lexer that feeds off of input FileStream
    lexer = ArrayInitLexer(istream)
    
    # create a buffer of tokens pulled from the lexer
    stream = CommonTokenStream(lexer)
    
    # create a parser that feeds off the tokens buffer
    parser = ArrayInitParser(stream)
    
    # begin parsing at init rule
    tree = parser.init()
    
    # print LISP-style tree
    print(tree.toStringTree(recog=parser))
    
    # create a generic parse tree walker that can trigger callbacks
    walker = ParseTreeWalker()

    # Walk the tree created during the parse, trigger callbacks
    walker.walk(ShortToUnicodeString(), tree)
    print()
    
if __name__ == '__main__':
    main(sys.argv)