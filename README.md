# ANTLR4 Cook Book

> My note for book The Definitive ANTLR 4 Reference - Terence Parr. I use antlr4 version 4.9.2 and antlr4-python3-runtime version 4.9.2.

## I. Installing ANTLR (Ubuntu 22.04)

### 1. Prerequisites
- `javac` >= v11.0.21
- `antlr` = v4.9.2
  - Dowload [antlr-4.9.2-complete.jar](https://www.antlr.org/download/antlr-4.9.2-complete.jar).
  - Move into `/usr/local/lib`.
### 2. Set up environment variables
- **CLASSPATH**: With CLASSPATH set, Java can find both the ANTLR tool and the runtime library.
- **ANTLR_JAR**: Store jar file.

Add two variables into file `~/.profile` (Please log out and log back in to your computer to activate environment variables):
```
export ANTLR_JAR=/usr/local/lib/antlr-4.9.2-complete.jar
export CLASSPATH=".:/usr/local/lib/antlr-4.9.2-complete.jar:$CLASSPATH"
```
Check to see that ANTLR is installed correctly now by running the ANTLR tool without arguments:  
![](./assets/launch-org.antlr.v4.Tool.png)

### 3. Set up aliases
- **antlr4**: alternative to running java commands.
- **grun**: `TestRig` (testing tool) display lots of information about how a recognizer matches input from a file or standard input.

Add two aliases into file `~/.bashrc` (Please log out and log back in to your computer to activate aliases):
```
alias antlr4='java -jar /usr/local/lib/antlr-4.9.2-complete.jar -o target'
alias grun='java org.antlr.v4.runtime.misc.TestRig'
```
Check to see:  
![](./assets/antlr4-grun-aliases.png)

### 4. Execute ANTLR and Testing Recognizers
> This is code from the book with Lexer and Parser generated from the antlr4 java runtime, it is for testing purposes only. All other exercises will be coded in python, using antlr4-python3-runtime.

Simple grammar that recognizes phrases in `test-hello/Hello.g4`:
```antlr4
grammar Hello;
r: 'hello' ID;
ID: [a-z]+;
WS: [ \t\r\n]+ -> skip;
```
- Generate parser and lexer:
    ```
    antlr4 Hello.g4
    ```
- Compile ANTLR-generated code:
    ```
    javac target/*.java
    ```
- Print the tokens created during recognition (type Ctrl-D to terminate reading from standard input):
    ```
    cd target && grun Hello r -tokens
    ```
    ![](./assets/test-grun.png)

## II. A Starter ANTLR Project

### 1. Prerequisites
- `python3` >= v3.10.12
- Run this command to install all dependencies:
    ```
    pip3 install -r requirement.txt
    ```

### 2. Testing tool
A tool like `grun` but written in Python. I put it in `bin/pygrun`.

### 3. Set up aliases
- **antlr4py3**: Run ANTLR tool with Python3 target.
- **pygrun**: Path to testing tool.

Add aliases into file `~/.bashrc` (Please log out and log back in to your computer to activate aliases):
```
alias antlr4py3='java org.antlr.v4.Tool -Dlanguage=Python3 -o target'
alias installdir='dirname "$(pwd)"'
alias pygrun='python3 "$(installdir)"/bin/pygrun'
```

#### Once fully installed, go [here](./01-array/) to view the exercise.

## III. Matching an Arithmetic Expression Language
Only the basic arithmetic operators (add, subtract, multiply, and divide), parenthesized expressions, integer numbers, and variables.
#### Click [here](./02-expr/) to see details.

## IV. Building a Calculator Using a Visitor
Get the previous arithmetic expression parser to compute values, this example shows:
- Visitor pattern.
- Use of Alternative Label.
#### Click [here](./03-calc/) to see details.

## V. Embedding Arbitrary Actions in a Grammar
Build a program that prints out a specific column from rows of data, this example shows:
- Embedded python actions.
- Local variable and initialization.
- Get column from command line and set in parser.
- Do not build tree.
#### Click [here](./04-row/) to see details.

## VI. Altering the Parse with Semantic Predicates
We can demonstrate the power of semantic predicates with a simple example, this example shows:
- Pass parameter to rule.
- Local variable.
- Semantic predication: 1st data decide the number of data followed
#### Click [here](./05-sempred/) to see details.

## VII. Island Grammars: Dealing with Different Formats in the Same File
ANTLR provides a well-known lexer feature called lexical modes that lets us deal easily with files containing mixed formats. The basic idea is to have the lexer switch back and forth between modes when it sees special sentinel character sequences.  
XML is a good example, this example shows:
- Lexer Only, call nextToken() method till end of file (Token.EOF).
- Switch Mode.
#### Click [here](./06-xml/) to see details.

## VIII. Exploring Some Real Grammars
1. **Parsing Common-Separated Values**  
The first language we’ll look at is the comma-separated-value (CSV) format used by spreadsheets and databases. CSV is a great place to start because it’s simple and yet widely applicable.
    #### Click [here](./07-csv/) to see details.
2. **Parsing JSON**  
The second language is also a data format, called JSON, that has nested data elements, which lets us explore the use of rule recursion in a real language.
    #### Click [here](./08-json/) to see details.
3. **Parsing DOT**  
Next, we’ll look at a declarative language called DOT for describing graphs (networks). In a declarative language, we express logical constructions without specifying control flow. DOT lets us explore more complicated lexical structures, such as case-insensitive keywords.
    #### Click [here](./09-dot/) to see details.
4. **Parsing Cymbol**  
Our fourth language is a simple non-object-oriented programming language called Cymbol. It’s a prototypical grammar we can use as a reference or starting point for other imperative programming languages (those composed of functions, variables, statements, and expressions).
    #### Click [here](./10-cymbol/) to see details.
5. **Parsing R**  
Finally, we’ll build a grammar for the R functional programming language.(Functional languages compute by evaluating expressions.) R is a statistical programming language increasingly used for data analysis.
    #### Click [here](./11-R/) to see details.

## IX. Decoupling Grammars from Application-Specific Code
We’re going to learn how to use parse-tree listeners and visitors to build language applications. A listener is an object that responds to rule entry and exit events (phrase recognition events) triggered by a parse-tree walker as it discovers and finishes nodes. To support situations where an application must control how a tree is walked, ANTLR-generated parse trees also support the well-known tree visitor pattern.
    #### Click [here](./12-propfile/) to see details.

# References:
#### I. Lexer starter kit
1. Punctuation
    ```antlr4
    call: ID '(' exprList ')';
    ```
    or
    ```antlr4
    call: ID LP exprList RP;
    LP: '(';
    RP: ')';
    ```
2. Keywords
    ```antlr4
    returnStat: 'return' expr ';';
    ```
3. Indentifiers
    ```antlr4
    ID: ID_LETTER (ID_LETTER | DIGIT)*; // From C language
    fragment ID_LETTER: 'a'..'z' | 'A'..'Z' | '_';
    fragment DIGIT: '0'..'9';
    ```
4. Numbers
    ```antlr4
    INT: DIGIT+;
    FLOAT: DIGIT+ '.' DIGIT*
        | '.' DIGIT+
        ;
    ```
5. Strings
    ```antlr4
    STRING: '"' (ESC | .)*? '"';
    fragment ESC: '\\' [btnr"\\]; // \b, \t, \n etc...
    ```
6. Comments:
    ```antlr4
    LINE_COMMENT: '//' .*? '\n' -> skip;
    COMMENT: '/*' .*? '*/' -> skip;
    ```
7. Whitespace:
    ```antlr4
    WS: [ \t\n\r]+ -> skip;
    ```