# Introduction
To demonstrate how to parse a programming language with syntax derived from C, we’re going to build a grammar for a language I conjured up called Cymbol. Cymbol is a simple non-object-oriented programming language that looks like C without structs. A grammar for this language serves as a good prototype for other new programming languages.

## I. Grammar
```antlr
grammar Cymbol;

program: (functionDecl | varDecl)+;

varDecl: typ ID ('=' expr)? ';';
typ: 'float' | 'int' | 'void';

functionDecl: typ ID '(' functionParameters? ')' block;
functionParameters: formalParameter (',' formalParamter)*;
formalParamter: typ ID;

block: '{' stat* '}';
stat:
    block
    | varDecl
    | 'if' expr 'then' stat ('else' stat)?
    | 'return' expr ';'
    | expr '=' expr ';'
    | expr ';'
    ;

expr:
    ID '(' exprList? ')'
    | expr '[' expr ']'
    | '-' expr
    | '!' expr
    | expr '*' expr
    | expr ('+' | '-') expr
    | expr '==' expr
    | ID
    | INT
    | '(' expr ')'
    ;
exprList: expr (',' expr)*;

ID: LETTER (LETTER | [0-9])*;
fragment LETTER: [a-zA-Z];

INT: [0-9]+;
WS: [ \t\n\r] -> skip;
SL_COMMENT: '//' .*? '\n' -> skip;
```

## II. Build and test
1. Build
    ```
    antlr4py3 Cymbol.g4
    ```
2. Test
- Generate tokens stream:
    ```
    pygrun Cymbol program --tokens t.cymbol
    ->  [@0,15:17='int',<4>,2:0]
        [@1,19:19='g',<22>,2:4]
        [@2,21:21='=',<1>,2:6]
        [@3,23:23='9',<23>,2:8]
        [@4,24:24=';',<2>,2:9]
        [@5,54:56='int',<4>,3:0]
        [@6,58:61='fact',<22>,3:4]
        [@7,62:62='(',<6>,3:8]
        [@8,63:65='int',<4>,3:9]
        [@9,67:67='x',<22>,3:13]
        [@10,68:68=')',<7>,3:14]
        [@11,70:70='{',<9>,3:16]
        [@12,98:99='if',<11>,4:4]
        [@13,101:101='x',<22>,4:7]
        [@14,102:103='==',<21>,4:8]
        [@15,104:104='0',<23>,4:10]
        [@16,106:109='then',<12>,4:12]
        [@17,111:116='return',<14>,4:17]
        [@18,118:118='1',<23>,4:24]
        [@19,119:119=';',<2>,4:25]
        [@20,125:130='return',<14>,5:4]
        [@21,132:132='x',<22>,5:11]
        [@22,134:134='*',<19>,5:13]
        [@23,136:139='fact',<22>,5:15]
        [@24,140:140='(',<6>,5:19]
        [@25,141:141='x',<22>,5:20]
        [@26,142:142='-',<17>,5:21]
        [@27,143:143='1',<23>,5:22]
        [@28,144:144=')',<7>,5:23]
        [@29,145:145=';',<2>,5:24]
        [@30,147:147='}',<10>,6:0]
        [@31,149:148='<EOF>',<-1>,7:0]
    ```
- Generate parser tree:
    ```
    pygrun Cymbol program --tree t.cymbol
    ->  (program 
            (varDecl 
                (typ int) g = 
                (expr 9) ;) 
            (functionDecl 
                (typ int) fact ( 
                (formalParameters 
                    (formalParameter 
                        (typ int) x)) ) 
            (block { 
                (stat if 
                    (expr 
                        (expr x) == 
                        (expr 0)) then 
                    (stat return 
                        (expr 1) ;)) 
                (stat return 
                    (expr 
                        (expr x) * 
                        (expr fact ( 
                        (exprList 
                            (expr 
                                (expr x) - 
                                (expr 1))) ))) ;) })))
    ```
