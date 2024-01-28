# Introduction
Our goal is to build an ANTLR grammar by reading the JSON reference manual and looking at its syntax diagram and existing grammar. We’ll pull out key phrases from the manual and figure out how to encode them as ANTLR rules, starting with the grammatical structures.

## I. Grammar
```antlr4
grammar JSON;

json: obj | array;

obj: 
    '{' pair (',' pair)* '}' 
    | '{' '}';  // empty object

pair: STRING ':' value;

array: 
    '[' value (',' value)* ']' 
    | '[' ']';  // empty array

value:
    STRING
    | NUMBER
    | obj       // recursion
    | array     // recursion
    | 'true'    // keywords
    | 'false'
    | 'null';

STRING: '"' (ESC | ~["\\])* '"';
fragment ESC: '\\' (["\\/bfnrt] | UNICODE);
fragment UNICODE: 'u' HEX HEX HEX HEX;
fragment HEX: [0-9a-fA-F];

NUMBER: 
    '-'? INT '.' INT EXP?   // 1.35, 1.35E-9, 0.3, -4.5
    | '-'? INT EXP          // 1e10 -3e4
    | '-' INT;              // -3, 45
fragment INT: '0' | [1-9][0-9]*;    // no leading zeros
fragment EXP: [Ee] [+\-]? INT;      // \- since - means "range" inside [...]

WS: [ \t\n\r] -> skip;
```

## Build and test
1. Build
    ```
    antlr4py3 JSON.g4
    ```
2. Test
- Generate tokens stream:
    ```
    pygrun JSON json --tokens t.json
    ->  [@0,0:0='{',<1>,1:0]
        [@1,3:13='"antlr.org"',<10>,2:1]
        [@2,14:14=':',<4>,2:12]
        [@3,16:16='{',<1>,2:14]
        [@4,20:27='"owners"',<10>,3:2]
        [@5,29:29=':',<4>,3:11]
        [@6,31:31='[',<5>,3:13]
        [@7,32:32=']',<6>,3:14]
        [@8,33:33=',',<2>,3:15]
        [@9,37:42='"live"',<10>,4:2]
        [@10,44:44=':',<4>,4:9]
        [@11,46:49='true',<7>,4:11]
        [@12,50:50=',',<2>,4:15]
        [@13,54:60='"speed"',<10>,5:2]
        [@14,62:62=':',<4>,5:10]
        [@15,64:68='1e100',<11>,5:12]
        [@16,69:69=',',<2>,5:17]
        [@17,73:79='"menus"',<10>,6:2]
        [@18,81:81=':',<4>,6:10]
        [@19,83:83='[',<5>,6:12]
        [@20,84:89='"File"',<10>,6:13]
        [@21,90:90=',',<2>,6:19]
        [@22,92:103='"Help\nMenu"',<10>,6:21]
        [@23,104:104=']',<6>,6:33]
        [@24,107:107='}',<3>,7:1]
        [@25,109:109='}',<3>,8:0]
        [@26,110:109='<EOF>',<-1>,8:1]
    ```
- Generate parser tree:
    ```
    pygrun JSON json --tree t.json
    -> (json 
            (obj { 
                (pair "antlr.org" : 
                    (value 
                        (obj { 
                        (pair "owners" : 
                            (value 
                                (array [ ]))) , 
                        (pair "live" : 
                            (value true)) , 
                        (pair "speed" : 
                            (value 1e100)) , 
                        (pair "menus" : 
                            (value 
                                (array [ 
                                    (value "File") , 
                                    (value "Help\nMenu") ]))) }))) }))
    ```