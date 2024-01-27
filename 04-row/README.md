# Introduction
We can compute values or print things out on-the-fly during parsing if we don’t want the overhead of building a parse tree.

## I. Grammar
The columns are tab-delimited, and each row ends with a newline character. Matching this kind of input is pretty simple grammatically.
```antlr4
grammar Rows;

@parser::members {          // add members to generated RowsParser
// Create a constructor so that we can pass in the column number we want (counting from 1).
@property
def column(self):
    return self._col

@column.setter
def column(self, value):
    self._col = value

}

rows: (row NL)+;

// The action within rule row accesses $i, the local variable defined with the locals clause.
// Use $STUFF.text to get the text for the most recently matched STUFF token.
row
	locals[i = 0]: ( 
		STUFF {
$i = $i + 1
if $i == self.column:
    print($STUFF.text)  
}                       // actions are code snippets surrounded by curly braces
	)+;

TAB: '\t' -> skip;      // match but don't pass to the parser
NL: '\r'? '\n';         // match and pass to the parser
STUFF: ~[\t\r\n]+;      // match any chars except tab, newline
```

## II. Integrating a Generated Parser into a Python Program
Pass in a column number to the parser using a custom constructor and telling the parser not to build a tree, see file `col.py`.
- Build:
    ```
    antlr4py3 -no-listener Rows.g4
    ```
- Test sequence, one test per column:
    ```
    python3 col.py 1 t.rows
    =>  parrt
        tombu
        bke
    python3 col.py 2 t.rows
    =>  Terence Parr
        Tom Burns
        Kevin Edgar
    python3 col.py 3 t.rows
    =>  101
        020
        008
    ```