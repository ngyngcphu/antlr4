import sys
from antlr4 import *

from target.PropertyFileLexer import PropertyFileLexer
from target.PropertyFileParser import PropertyFileParser
from target.PropertyFileVisitor import PropertyFileVisitor

class PropertyFileLoader(PropertyFileVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.props = {}
        
    def visitProp(self, ctx: PropertyFileParser.PropContext):
        self.props[ctx.ID().getText()] = ctx.STRING().getText()
        
    def show(self):
        for (key, value) in self.props.items():
            print(key, '=>', value)
            
if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(sys.stdin.read())
    
    lexer = PropertyFileLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PropertyFileParser(token_stream)
    tree = parser.top()
    
    visitor = PropertyFileLoader()
    visitor.visit(tree)
    
    visitor.show()