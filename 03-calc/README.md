# Introduction
Use the well-known Visitor pattern to implement our little calculator.

## I. Grammar
Label the alternatives of the rules. Labels appear on the right edge of alternatives and start with the # symbol in our new grammar, `LabeledExpr`:

```anltr
stat: expr NEWLINE              # printExpr             
    | ID '=' expr NEWLINE       # assign
    | NEWLINE                   # blank
    ;

expr:
	expr ('*' | '/') expr       # MulDiv
	| expr ('+' | '-') expr     # AddSub
	| INT                       # int
	| ID                        # id
	| '(' expr ')'              # parens
    ;
```

Define some token names for the operator literals:

```anltr
MUL: '*';
DIV: '/';
ADD: '+';
SUB: '-';
```

## II. Start coding calculator
Our main program in file `calc.py` is nearly identical to `expr_joy_ride.py` from earlier. The first difference is that we create lexer and parser objects derived from grammar `LabeledExpr`, not `Expr`.
```py
lexer = LabeledExprLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = LabeledExprParser(token_stream)
tree = parser.prog()
```
The other difference is that we create an instance of our visitor class, `EvalVisitor`. To start walking the parse tree returned from method `prog()`, we call `visit()`.
```py
visitor = EvalVisitor()
visitor.visit(tree)
```
ANTLR generates a visitor interface with a method for each labeled alternative name when we type:
```
antlr4py3 -no-listener -visitor LabeledExpr.g4
```
To implement the calculator, we override the methods associated with statement and expression alternatives in `LabeledExprVisitor` interface, see `eval_visitor.py`.  
And here is the build and test sequence that evaluates expressions in `t.expr`:
```
antlr4py3 -no-listener -visitor LabeledExpr.g4
python3 calc.py t.expr
```
Result:
```
193
17
9
```