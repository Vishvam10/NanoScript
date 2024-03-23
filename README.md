# Nanoscript 🛠️

Nanoscript is a minimalist programming language crafted entirely from scratch using **pure Python** without relying on external libraries like `ply` or `pybison`.

## Features 

- **Numeric Expression Evaluation**: Evaluate numeric expressions like `4 * (3 + 2 - (3 % 4))`, etc

- **Variables**:
    - Declaration: Utilize `let` and `const` to define variables.
    - Assignment: Currently supports numbers and numeric expressions.
    - Scoping: Manage variable visibility and accessibility within designated scopes.
    - Example :

        ```javascript
            const a = 5;
            let b = 10;
            let x = y = x = 12;

            b = 5;      // works
            a = 10;     // throws an error

            const c;    // throws an error

            let a = 12; // throws an error
        ```

## Some Notes On Grammar

```
Order of precedence : 

    lower in the tree or the call stack has the highest precedence

    |    Stmt                          (lowest)
    |    Expr | VariableDecl
    |    AssignmentExpr
    |    ObjectExpr
    |    AdditiveExpr
    |    MultiplicativeExpr
    |    CallExpr
    |    MemberExpr
    v    PrimaryExpr                    (highest)

    more precedence = further down the tree

    so, additive calls multiplicative. multiplicative calls primary.
    similarly, assignment calls object expression, and so on

    At any level of the stack described above, the expr that the parser 
    currently points at will always :
        
        - return something or
        - call itself or
        - call an expr that has a lower precedence
        - call an expr that has a one level higher precedence

    At no point, an expr calls another expr that has more than one level of 
    precedence difference. It always passes through the above order. 
    So, for example :

        VariableDecl can not directly call PrimaryExpr  or say
        AdditiveExpr can not directly call MemberExpr
 

Technically speaking, this would be the grammar of this language at this point :

    Stmt                := Expr | VariableDecl
    Expr                := AssignmentExpr
    AssignmentExpr      := AssignmentExpr | ObjectExpr
    ObjectExpr          := Expr | AdditiveExpr
    AdditiveExpr        := MultiplicativeExpr
    MultiplicativeExpr  := PrimaryExpr
    
```

**Note :** 

- The grammar created here is based on the parser implementation.
- Ideally, it would the other way around - we write the rules and code a 
'meta program' to auto-generate the parser file. For the time being, this is what we will be working with the former.
- This is bound to change in the future 






## Getting Started 

To dive into Nanoscript, simply clone this repository and start experimenting with the language. 

To execute your Nanoscript code use the provided REPL .

```bash
git clone https://github.com/Vishvam10/NanoScript

cd src

python repl.py
```

## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements 

Big thanks to [@tlaceby](https://github.com/tlaceby/) for initiating the guide-to-interpreter series. I absolutely loved it 💛. Your work inspired me to create a Python port, building upon your foundation, with the hope of making it even better.
