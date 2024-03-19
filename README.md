# Nanoscript 🛠️

Nanoscript is a minimalist programming language crafted entirely from scratch using **pure Python** without relying on external libraries like `ply` or `pybison`.

## Features 

- **Variables**:
    - Declaration: Utilize `let` and `const` to define variables.
    - Assignment: Currently supports numbers and numeric expressions.
    - Scoping: Manage variable visibility and accessibility within designated scopes.

- **Numeric Expression Evaluation**: Evaluate numeric expressions like `4 * (3 + 2 - (3 % 4))`, etc

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

Big thanks to [@tlaceby]('https://github.com/tlaceby) for initiating the guide-to-interpreter series. I absolutely loved it 💛. Your work inspired me to create a Python port, building upon your foundation, with the hope of making it even better.