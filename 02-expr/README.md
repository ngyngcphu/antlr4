# Introduction
Simple Arithmetic Expression Language, include:
- Basic arithmetic operators: add, subtract, multiply, and divide.
- Parenthesized expressions.
- Integer numbers.
- Variables

## I. Grammar
```antlr4
grammar Expr;

prog: stat+ EOF;

stat: expr NEWLINE | ID '=' expr NEWLINE | NEWLINE;

expr: 
    expr ('*' | '/') expr
    | expr ('+' | '-') expr
    | INT
    | ID
    | '(' expr ')'
    ;

ID: [a-zA-Z];
INT: [0-9]+;
NEWLINE: '\r'? '\n';
WS: [ \t] -> skip;
```
Build and test sequence on the grammar file
```
antlr4py3 Expr.g4
pygrun Expr prog --tree t.expr
```
Result:
```
(prog 
   (stat 
      (expr 193) \n) 
   (stat a = 
      (expr 5) \n) 
   (stat b = 
      (expr 6) \n) 
   (stat 
      (expr 
         (expr a) + 
         (expr 
            (expr b) * 
            (expr 2))) \n) 
   (stat 
      (expr 
         (expr ( 
            (expr 
               (expr 1) + 
               (expr 2)) )) * 
      (expr 3)) \n) <EOF>)
```

## II. Integrating a Generated Parser into a Python Program
The main program `expr_joy_ride.py` shows the code necessary to create all necessary objects and launch our expression language parser starting at rule prog.  
Run on input file `t.expr`:
```
python3 expr_joy_ride.py t.expr
```
Result:
```
(prog (stat (expr 193) \n) (stat a = (expr 5) \n) (stat b = (expr 6) \n) (stat (expr (expr a) + (expr (expr b) * (expr 2))) \n) (stat (expr (expr ( (expr (expr 1) + (expr 2)) )) * (expr 3)) \n) <EOF>)
```