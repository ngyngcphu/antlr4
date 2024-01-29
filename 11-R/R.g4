grammar R;

program: (expr_or_assign (';' | NL) | NL)* EOF;

expr_or_assign: expr ('<-' | '=' | '<<-') expr_or_assign | expr;
expr:
	expr '[[' sublist ']' ']'
	| expr '[' sublist ']'
	| expr ('::' | ':::') expr
	| expr ('$' | '@') expr
	| <assoc = right> expr '^' expr
	| ('-' | '+') expr
	| expr ':' expr
	| expr USER_OP expr
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
	'.' (LETTER | '_' | '.') (LETTER | DIGIT | '_' | '.')*
	| LETTER (LETTER | DIGIT | '_' | '.')*;
fragment LETTER: [a-zA-Z];

HEX: '0' ('x' | 'X') HEXDIGIT+ [Ll]?;
fragment HEXDIGIT: '0' ..'9' | 'a' ..'f' | 'A' ..'F';

INT: DIGIT+ [Ll]?;

FLOAT:
	DIGIT+ '.' DIGIT* EXP? [Ll]?
	| DIGIT+ EXP? [Ll]?
	| '.' DIGIT+ EXP? [Ll]?;

fragment DIGIT: '0' ..'9';
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
COMMENT: '#' .*? '\r'? '\n' -> type(NL);

NL: '\r'? '\n';
WS: [ \t] -> skip;