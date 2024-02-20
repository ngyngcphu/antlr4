# Introduction
R is an expressive domain-specific programming language for describing statistical problems. 

## I. Grammar
```antlr
grammar R;

program: (expr_or_assign (';' | NL) | NL)* EOF;

expr_or_assign: expr ('<-' | '=' | '<<-') expr_or_assign | expr;

expr:
    expr '[[' sublist ']' ']'
    | expr '[' sublist ']'
    | expr ('::' | ':::') expr
    | expr ('$' | '@') expr
    | <assoc=right> expr '^' expr
    | ('-' | '+') expr
    | expr ':' expr
    | expr USER_OF expr
    | expr ('*' | '/') expr
    | expr ('+' | '-') expr
    | expr ('>' | '>=' | '<' | '<=' | '==' | '!=') expr
    | '!' expr
    | expr ('&' | '&&') expr
    | expr ('|' | '||') expr
    | '~' expr
    | expr '~' expr
    | expr ('->' | '->>' | ':=') expr
    | 'function' '(' formlist? ')' expr
    | expr '(' sublist ')'
    | '{' exprlist '}'
    | 'if' '(' expr ')' expr
    | 'if' '(' expr ')' 'else' expr
    | 'for' '(' ID 'in' expr ')' expr
    | 'while' '(' expr ')' expr
    | 'repeat' expr
    | '?' expr
    | 'next'
    | 'break'
    | '(' expr ')'
    | ID
    | STRING
    | HEX
    | INT
    | FLOAT
    | COMPLEX
    | 'NULL'
    | 'NA'
    | 'Inf'
    | 'NaN'
    | 'TRUE'
    | 'FALSE';

exprlist: expr_or_assign ((';' | NL) expr_or_assign?)* |;

formlist: form (',' form)*;
form: ID | ID '=' expr | '...';

sublist: sub (',' sub)*;
sub:
    expr
    | ID '='
    | ID '=' expr
    | STRING '='
    | STRING '=' expr
    | 'NULL' '='
    | 'NULL' '=' expr
    | '...'
    |;

ID:
    '.' (LETTER | '_' | '.') (LETTER | DIGIT | '_' '.')*
    | LETTER (LETTER | DIGIT | '_' '.')*;
fragment LETTER: [a-zA-Z];

HEX: '0' ('x' | 'X') HEXDIGIT+ [Ll]?;
fragment HEXDIGIT: '0'..'9' | 'a'..'f' | 'A'..'F';

INT: DIGIT+ [Ll]?;

FLOAT:
    DIGIT+ '.' DIGIT* EXP? [Ll]?
    | DIGIT+ EXP? [Ll]?
    | '.' DIGIT+ EXP? [Ll]?;
fragment DIGIT: '0'..'9';
fragment EXP: ('E' | 'e') ('+' | '-')? INT;

COMPLEX: INT 'i' | FLOAT 'i';

STRING: '"' (ESC | ~[\\"])*? '"' | '\'' (ESC | ~[\\'])*? '\'';
fragment ESC:
    '\\' ([abtnfrv] | '"' | '\'')
    | UNICODE_ESCAPE
    | HEX_ESCAPE
    | OCTAL_ESCAPE;

fragment UNICODE_ESCAPE:
    '\\' 'u' HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT
    | '\\' 'u' '{' HEXDIGIT HEXDIGIT HEXDIGIT HEXDIGIT '}';

fragment OCTAL_ESCAPE:
    '\\' [0-3] [0-7] [0-7]
    | '\\' [0-7] [0-7]
    | '\\' [0-7];

fragment HEX_ESCAPE: '\\' HEXDIGIT HEXDIGIT?;

USER_OP: '%' .*? '%';
COMMENT: '#' .*? '\r'? '\n' -> type(NL)

NL: '\r'? '\n';
WS: [ \t] -> skip;
```

## II. Build and test
1. Build
    ```
    antlr4py3 R.g4
    ```
2. Test
- Generate tokens stream:
    ```
    pygrun R program --tokens t.R
    ->  [@0,0:4='addMe',<55>,1:0]
        [@1,6:7='<-',<2>,1:6]
        [@2,9:16='function',<33>,1:9]
        [@3,17:17='(',<34>,1:17]
        [@4,18:18='x',<55>,1:18]
        [@5,19:19=',',<53>,1:19]
        [@6,20:20='y',<55>,1:20]
        [@7,21:21=')',<35>,1:21]
        [@8,23:23='{',<36>,1:23]
        [@9,25:30='return',<55>,1:25]
        [@10,31:31='(',<34>,1:31]
        [@11,32:32='x',<55>,1:32]
        [@12,33:33='+',<14>,1:33]
        [@13,34:34='y',<55>,1:34]
        [@14,35:35=')',<35>,1:35]
        [@15,37:37='}',<37>,1:37]
        [@16,38:38='\n',<62>,1:38]
        [@17,39:43='addMe',<55>,2:0]
        [@18,44:44='(',<34>,2:5]
        [@19,45:45='x',<55>,2:6]
        [@20,46:46='=',<3>,2:7]
        [@21,47:47='1',<57>,2:8]
        [@22,48:48=',',<53>,2:9]
        [@23,49:49='2',<57>,2:10]
        [@24,50:50=')',<35>,2:11]
        [@25,51:51='\n',<62>,2:12]
        [@26,52:52='r',<55>,3:0]
        [@27,54:55='<-',<2>,3:2]
        [@28,57:57='1',<57>,3:5]
        [@29,58:58=':',<15>,3:6]
        [@30,59:59='5',<57>,3:7]
        [@31,60:60='\n',<62>,3:8]
        [@32,61:60='<EOF>',<-1>,4:0]
    ```
- Generate parser tree:
    ```
    pygrun R program --tree t.R
    ->  (program 
            (expr_or_assign 
                (expr addMe) <- 
                (expr_or_assign 
                    (expr function ( 
                        (formlist 
                        (form x) , 
                        (form y)) ) 
                    (expr { 
                        (exprlist 
                        (expr_or_assign 
                            (expr 
                                (expr return) ( 
                                (sublist 
                                    (sub 
                                    (expr 
                                        (expr x) + 
                                        (expr y)))) )))) })))) \n 
            (expr_or_assign 
                (expr 
                    (expr addMe) ( 
                    (sublist 
                        (sub x = 
                        (expr 1)) , 
                        (sub 
                        (expr 2))) ))) \n 
            (expr_or_assign 
                (expr r) <- 
                (expr_or_assign 
                    (expr 
                        (expr 1) : 
                        (expr 5)))) \n <EOF>)
    ```