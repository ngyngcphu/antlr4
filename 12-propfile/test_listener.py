import sys

from antlr4 import *
from target.PropertyFileLexer import PropertyFileLexer
from target.PropertyFileParser import PropertyFileParser
from target.PropertyFileListener import PropertyFileListener

class PropertyFileLoader(PropertyFileListener):
    def __init__(self) -> None:
        super().__init__()
        self.props = {}
    
    def exitProp(self, ctx: PropertyFileParser.PropContext):
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
    
    walker = ParseTreeWalker()
    listener = PropertyFileLoader()
    walker.walk(listener, tree)
    
    listener.show()