# Introduction
A grammar that reads in sequences of integers. The trick is that part of the input specifies how many integers to group together. We don’t know until runtime how many integers to match.

## I. Grammar
```antlr
grammar Data;

top: group+;

group: INT sequence[$INT.int];

sequence[n]
    locals[i=0]: ({$i < $n}? INT {$i = $i + 1})*;    // match n integers

INT: [0-9]+;
WS: [ \t\n\r] -> skip;
```
## II. Build and test
- Build:
    ```
    antlr4py3 Data.g4
    ```
- Test:
    ```
    python3 test.py t.data
    ```
    - Input:
        ```
        2 9 10 3 1 2 3
        ```
    - Output:
        ```
        (top (group 2 (sequence 9 10)) (group 3 (sequence 1 2 3)))
        ```