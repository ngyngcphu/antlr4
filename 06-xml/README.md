# Introduction
An XML parser treats everything other than tags and entity references (such as *\&pound*;) as text chunks. When the lexer sees <, it switches to “inside” mode and switches back to the default mode when it sees > or />. The following grammar demonstrates how this works.

## I. Grammar
```antlr4
lexer grammar XMLLexer;

OPEN        :   '<'                 -> pushMode(INSIDE);
COMMENT     :   '<!--' .*? '-->'    -> skip; 
ENTITYREF   :   '&' [a-z]+ ';';
TEXT        :   ~('<' | '&')+;

mod INSIDE;

CLOSE       :   '>'                 -> popMode;
SLASH_CLOSE :   '/>'                -> popMode;
EQUALS      :   '=';
STRING      :   '"' .*? '"';
SLASHNAME   :   '/' NAME;
NAME        :   ALPHA (ALPHA | DIGIT)*;
S           :   [ \t\r\n]           -> skip;

fragment
ALPHA       :   [a-zA-Z]+;

fragment
DIGIT       :   [0-9]+;
```

## II. Build and test
1. Build:
    ```
    antlr4py3 XMLLexer.g4
    ```
2. Test:
    - Input:
        ```xml
        <!--
        ! Excerpted from "The Definitive ANTLR 4 Reference",
        ! published by The Pragmatic Bookshelf.
        ! Copyrights apply to this code. It may not be used to create training material, 
        ! courses, books, articles, and the like. Contact us if you are in doubt.
        ! We make no guarantees that this code is fit for any purpose. 
        ! Visit http://www.pragmaticprogrammer.com/titles/tpantlr2 for more book information.
        -->
        <tools>
            <tool name="ANTLR">A parser generator</tool>
        </tools>
        ```
    - Output:
        ```
        0 8 3 413 413 4 \n
        0 9 0 414 414 1 <
        0 9 1 415 419 10 tools
        0 9 6 420 420 5 >
        0 9 7 421 422 4 \n\t
        0 10 1 423 423 1 <
        0 10 2 424 427 10 tool
        0 10 7 429 432 10 name
        0 10 11 433 433 7 =
        0 10 12 434 440 8 "ANTLR"
        0 10 19 441 441 5 >
        0 10 20 442 459 4 A parser generator
        0 10 38 460 460 1 <
        0 10 39 461 465 9 /tool
        0 10 44 466 466 5 >
        0 10 45 467 467 4 \n
        0 11 0 468 468 1 <
        0 11 1 469 474 9 /tools
        0 11 7 475 475 5 >
        ```