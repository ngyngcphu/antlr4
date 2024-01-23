# ANTLR4 Cook Book

> My note for book The Definitive ANTLR 4 Reference - Terence Parr.

## I. Installing ANTLR (Ubuntu 22.04)
> I use antlr4 version 4.9.2.
### 1. Prerequisites
- `python3` >= v3.10.12
- `javac` >= v11.0.21
- `antlr` = v4.9.2
  - Dowload [antlr-4.9.2-complete.jar](https://www.antlr.org/download/antlr-4.9.2-complete.jar).
  - Move into `/usr/local/lib`.
- `antlr4-python3-runtime` = v4.9.2, use the command:
    ```
    pip3 install antlr4-python3-runtime==4.9.2
    ```
### 2. Set up environment variables
- **CLASSPATH**: With CLASSPATH set, Java can find both the ANTLR tool and the runtime library.
- **ANTLR_JAR**: Store jar file.

Add two variables into file `~/.profile`:
```
export ANTLR_JAR=/usr/local/lib/antlr-4.9.2-complete.jar
export CLASSPATH=".:/usr/local/lib/antlr-4.9.2-complete.jar:$CLASSPATH"
```
Check to see that ANTLR is installed correctly now by running the ANTLR tool without arguments:  
![](./assets/launch-org.antlr.v4.Tool.png)

### 3. Set up aliases
- **antlr4**: alternative to running java commands.
- **grun**: `TestRig` (testing tool) display lots of information about how a recognizer matches input from a file or standard input.

Add two aliases into file `~/.bashrc`:
```
alias antlr4='java -jar /usr/local/lib/antlr-4.9.2-complete.jar'
alias grun='java org.antlr.v4.runtime.misc.TestRig'
```
Check to see:  
![](./assets/antlr4-grun-aliases.png)

### 4. Execute ANTLR and Testing Recognizers
Simple grammar that recognizes phrases in `hello/Hello.g4`:
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
    javac *.java
    ```
- Print the tokens created during recognition (type Ctrl-D to terminate reading from standard input):
    ```
    grun Hello r -tokens
    ```
    ![](./assets/test-grun.png)