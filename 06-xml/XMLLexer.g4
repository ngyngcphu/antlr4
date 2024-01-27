lexer grammar XMLLexer;

// Default "mode": Everything OUTSIDE of a tag
OPEN        :       '<'                 -> pushMode(INSIDE);
COMMENT     :       '<!--' .*? '-->'    -> skip;
ENTITYREF   :       '&' [a-z]+ ';';
TEXT        :       ~('<' | '&')+;       // match any 16 bit char minus < and &

// ----------------- Everything INSIDE of a tag ---------------------
mode INSIDE;

CLOSE       :       '>'                 -> popMode;     // back to default mode
SLASH_CLOSE :       '/>'                -> popMode;
EQUALS      :       '=';
STRING      :       '"' .*? '"';
SLASHNAME   :       '/' NAME;
NAME        :       ALPHA (ALPHA | DIGIT)*;
S           :       [ \t\n\r]   -> skip;

fragment
ALPHA       :       [a-zA-Z]+;

fragment
DIGIT       :       [0-9]+;