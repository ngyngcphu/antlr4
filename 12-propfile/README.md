# Introduction
To demonstrate the reusability of the refactored grammar, let’s build two different “applications,” starting with one that just prints out the properties as it encounters them. As a second application, let’s load the properties into a map instead of printing
them out.

## I. Grammar
> This decoupling makes the grammar reusable for different applications, but the grammar is still tied to Python because of the method calls. Demo in [test_print.py](./test_print.py) and [test_map.py](./test_map.py).
```antlr
grammar PropertyFile;

@members {
def startFile(self):
    pass
def finishFile(self):
    pass
def defineProperty(self, name, value):
    pass
}

top: {self.startFile()} prop+ {self.finishFile()};
prop: ID '=' STRING '\n' {self.defineProperty($ID, $STRING)};
ID: [a-z]+;
STRING: '"' .*? '"';
```

## II. Listener
Implementing Applications with Parse-Tree Listeners - [test_print.py](./test_listener.py)

## III. Visitor
Implementing Applications with Visitors - [test_visitor.py](./test_visitor.py)