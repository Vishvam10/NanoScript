# Nanoscript 🛠️

Nanoscript is a minimalist programming language crafted entirely from 
scratch using **pure Python** without relying on external 
libraries like `ply` or `pybison`.

## Features 

- **Arithmetic Expression Evaluation**

    ```
    Evaluate numeric expressions like `4 * (3 + 2 - (3 % 4))`, etc
    ```

- **Variables**
  
    ```
        - Syntax : Use the `let` and `const` to define variables.
        - Assignment: Currently supports numbers and arithmetic expressions.
        - Scoping: Support global and function scoping

    ```

    ```javascript
        // Example

        const a = 5;
        let b = 10;
        let x = y = x = 12;

        b = 5;      // works
        a = 10;     // throws an error

        const c;    // throws an error

        let a = 12; // throws an error
    ```
        

- **Objects, Nested Objects and Accessors**

    ```
        - Syntax : Similar to JS objects, use curly braces `{}`
        - Assignment : Currently supports only numbers and arithmetic expressions
        - Scoping : Every property inside the object belongs to the object and are scoped to it
        - Accessors : Use the dot operator (.) to access properties inside an object. For nested properties, see the example below
    ```


    ```javascript

        // Example

        let obj = {
            a : 32,
            b : 39 + 23 - 5 * 4 % 2
            nested : {
                foo : {
                    bar : 1
                }
            }
        };

        a = b + 15          // throws : Cannot resolve b as it does not exist
        obj.a = obj.b + 15  // this is valid

        // accessing nested properties
        obj.nested.foo.bar = 2

    ```


- **Global and User Defined Functions** 

    ```
        - Syntax : 
            - Use the `fn` keyword to create user defined function. 
            - Use the `make_native_fn` macro to create global methods. See `create_global_env()` method in `runtime/environment.py`
        - Note :
            - `return` statement is yet to be implemented. In the 
            current implementation, the last statement / expr in 
            the function declaration is returned
    ```

   
    ```javascript
        fn add(x, y) {
            const res = x + y;
            res                     // res is returned
        }

        let a = add(10, 2);

    ```
    


- **Nested Functions and Nested Call Expressions** :

    ```
        - Syntax : Just like the normal function, use the `fn` keyword and create functions within functions
        - Scoping : Inner functions have access to outer function's scope but not vice-versa. See the example below to understand better about scoping
    ```

    ```javascript
        let res;                    // A. this is in global scope
        let a;                      // A. this is in global scope
        let b;                      // A. this is in global scope
        
        fn calc(x, y) {
            let res;                // B. this is in the 'calc' function's scope
        
            fn add(x, y) {
                const VAL = 1; 
                res = x + y         // refers to B.
                res   
            }
        
            fn sub(x, y) {
                res = x - y         // refers to B.
                res   
            }

            res = {                 // refers to B
                a : add(x, y),
                b : sub(
                    add(x, y), 10
                ) 
            }

            // throws : Cannot resolve VAL as it does not exist    
            print(VAL)              

        }

        // refers to A (although, in this case the program terminates 
        // since we are accessing VAL from outer scope)
        print(res)

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
    - Ideally, it would the other way around - we write the rules and code a 'meta program' to auto-generate the parser file. For the time being, this is what we will be working with the former.
    - This is bound to change in the future.






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
