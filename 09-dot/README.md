# Introduction
DOT is a declarative language for describing graphs such as network diagrams, trees, or state machines. It’s a generically useful graphing tool, particularly if you have a program that needs to generate images.

## I. Grammar
```antlr4
grammar DOT;

graph: STRICT? (GRAPH | DIGRAPH) iden? '{' stmt_list '}';
stmt_list: (stmt ';'?)*;
stmt:
	node_stmt
	| edge_stmt
	| attr_stmt
	| iden '=' iden
	| subgraph;

attr_stmt: (GRAPH | NODE | EDGE) attr_list;
attr_list: ('[' a_list? ']')+;
a_list: (iden ('=' iden)? ','?)+;

edge_stmt: (node_id | subgraph) edgeRHS attr_list?;
edgeRHS: (edgeop (node_id | subgraph))+;
edgeop: '->' | '--';

node_stmt: node_id attr_list?;
node_id: iden port?;
port: ':' iden (':' iden)?;

subgraph: (SUBGRAPH iden?)? '{' stmt_list '}';
iden: ID | STRING | HTML_STRING | NUMBER;

// "The keywords node, edge, graph, digraph, subgraph, and strict are
// case-independent"
STRICT: [Ss][Tt][Rr][Ii][Cc][Tt];
GRAPH: [Gg][Rr][Aa][Pp][Hh];
DIGRAPH: [Dd][Ii][Gg][Rr][Aa][Pp][Hh];
NODE: [Nn][Oo][Dd][Ee];
EDGE: [Ee][Dd][Gg][Ee];
SUBGRAPH: [Ss][Uu][Bb][Gg][Rr][Aa][Pp][Hh];

/** "Any string of alphabetic ([a-zA-Z\200-\377]) characters, underscores
 *  ('_') or digits ([0-9]), not beginning with a digit"
 */
ID: LETTER (LETTER | DIGIT)*;
fragment LETTER: [a-zA-Z\u0080-\u00FF_];

/** "a numeral [-]?(.[0-9]+ | [0-9]+(.[0-9]*)? )" */
NUMBER: '-'? ('.' DIGIT+ | DIGIT+ ('.' DIGIT*)?);
fragment DIGIT: [0-9];

/** "any double-quoted string ("...") possibly containing escaped quotes" */
STRING: '"' ('\\"' | .)*? '"';

/** "HTML strings, angle brackets must occur in matched pairs, and
 *  unescaped newlines are allowed."
 */
HTML_STRING: '<' (TAG | ~[<>])* '>';
fragment TAG: '<' .*? '>';

COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' .*? '\r'? '\n' -> skip;

/** "a '#' character is considered a line output from a C preprocessor (e.g.,
 *  # 34 to indicate line 34 ) and discarded"
 */
PREPOC: '#' .*? '\n' -> skip;
WS: [ \t\n\r] -> skip;
```

## II. Build and test
1. Build
    ```
    antlr4py3 DOT.g4
    ```
2. Test
- Generate tokens stream:
    ```
    pygrun DOT graph --tokens t.dot
    ->  [@0,0:6='digraph',<13>,1:0]
        [@1,8:8='G',<17>,1:8]
        [@2,10:10='{',<1>,1:10]
        [@3,16:22='rankdir',<17>,2:4]
        [@4,23:23='=',<4>,2:11]
        [@5,24:25='LR',<17>,2:12]
        [@6,26:26=';',<3>,2:14]
        [@7,32:35='main',<17>,3:4]
        [@8,37:37='[',<5>,3:9]
        [@9,38:42='shape',<17>,3:10]
        [@10,43:43='=',<4>,3:15]
        [@11,44:46='box',<17>,3:16]
        [@12,47:47=']',<6>,3:19]
        [@13,48:48=';',<3>,3:20]
        [@14,54:57='main',<17>,4:4]
        [@15,59:60='->',<8>,4:9]
        [@16,62:62='f',<17>,4:12]
        [@17,64:65='->',<8>,4:14]
        [@18,67:67='g',<17>,4:17]
        [@19,68:68=';',<3>,4:18]
        [@20,112:112='f',<17>,5:4]
        [@21,114:115='->',<8>,5:6]
        [@22,117:117='f',<17>,5:9]
        [@23,119:119='[',<5>,5:11]
        [@24,120:124='style',<17>,5:12]
        [@25,125:125='=',<4>,5:17]
        [@26,126:131='dotted',<17>,5:18]
        [@27,132:132=']',<6>,5:24]
        [@28,134:134=';',<3>,5:26]
        [@29,158:158='f',<17>,6:4]
        [@30,160:161='->',<8>,6:6]
        [@31,163:163='h',<17>,6:9]
        [@32,164:164=';',<3>,6:10]
        [@33,195:195='}',<2>,7:0]
        [@34,196:195='<EOF>',<-1>,7:1]
    ```
- Generate parser tree:
    ```
    pygrun DOT graph --tree t.dot
    ->  (graph digraph 
            (iden G) { 
            (stmt_list 
                (stmt 
                    (iden rankdir) = 
                    (iden LR)) ; 
                (stmt 
                    (node_stmt 
                        (node_id 
                        (iden main)) 
                        (attr_list [ 
                        (a_list 
                            (iden shape) = 
                            (iden box)) ]))) ; 
                (stmt 
                    (edge_stmt 
                        (node_id 
                        (iden main)) 
                        (edgeRHS 
                        (edgeop ->) 
                        (node_id 
                            (iden f)) 
                        (edgeop ->) 
                        (node_id 
                            (iden g))))) ; 
                (stmt 
                    (edge_stmt 
                        (node_id 
                        (iden f)) 
                        (edgeRHS 
                        (edgeop ->) 
                        (node_id 
                            (iden f))) 
                        (attr_list [ 
                        (a_list 
                            (iden style) = 
                            (iden dotted)) ]))) ; 
                (stmt 
                    (edge_stmt 
                        (node_id 
                        (iden f)) 
                        (edgeRHS 
                        (edgeop ->) 
                        (node_id 
                            (iden h))))) ;) })
    ```