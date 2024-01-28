# Introduction
Basic CSV grammar

## I. Grammar
```antlr4
grammar CSV;

top: hdr row+;
hdr: row;

row: field (',' field)* '\r'? '\n';
field: TEXT | STRING | ;

TEXT: ~[,\n\r"]+;
STRING: '"' ('""' | ~'"')* '"';     // quote-quote is an escaped quote in file CSV

// We can’t use a nongreedy loop with the wildcard, ('""'|.)*?, because it would stop at the first " it saw after the start of the string. 
// Input like "x""y" would match two strings, not one string with "" inside it.
```
## II. Build and test
1. Build
    ```
    antlr4py3 CSV.g4
    ```
2. Test
- Generate tokens stream:
    ```
    pygrun CSV top --tokens data.csv
    ->  [@0,0:6='Details',<4>,1:0]
        [@1,7:7=',',<1>,1:7]
        [@2,8:12='Month',<4>,1:8]
        [@3,13:13=',',<1>,1:13]
        [@4,14:19='Amount',<4>,1:14]
        [@5,20:20='\n',<3>,1:20]
        [@6,21:29='Mid Bonus',<4>,2:0]
        [@7,30:30=',',<1>,2:9]
        [@8,31:34='June',<4>,2:10]
        [@9,35:35=',',<1>,2:14]
        [@10,36:43='"$2,000"',<5>,2:15]
        [@11,44:44='\n',<3>,2:23]
        [@12,45:45=',',<1>,3:0]
        [@13,46:52='January',<4>,3:1]
        [@14,53:53=',',<1>,3:8]
        [@15,54:64='"""zippo"""',<5>,3:9]
        [@16,65:65='\n',<3>,3:20]
        [@17,66:78='Total Bonuses',<4>,4:0]
        [@18,79:79=',',<1>,4:13]
        [@19,80:81='""',<5>,4:14]
        [@20,82:82=',',<1>,4:16]
        [@21,83:90='"$5,000"',<5>,4:17]
        [@22,91:91='\n',<3>,4:25]
        [@23,92:91='<EOF>',<-1>,5:0]
    ```
- Generate parser tree:
    ```
    pygrun CSV top --tree data.csv
    ->  (top 
            (hdr 
                (row 
                    (field Details) , 
                    (field Month) , 
                    (field Amount) \n)) 
            (row 
                (field Mid Bonus) , 
                (field June) , 
                (field "$2,000") \n) 
            (row field , 
                (field January) , 
                (field """zippo""") \n) 
            (row 
                (field Total Bonuses) , 
                (field "") , 
                (field "$5,000") \n))
    ```