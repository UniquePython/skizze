# skizze

**Skizze** is a small, expression-based, dynamically typed, interpreted language — written in Python.

## Installation

```bash
pip install -e .
```

## Usage

```bash
skizze <file.skz>
```

## Syntax Guide

### Variables

```
let var = value
```

### Functions

Functions return the last statement implicitly.

```
fn func_name(param_a, param_b)
{
    let c = param_a * param_b
    let d = param_a * 2 + 1
    c - d
}
```

### Control Flow

#### If-Else

```
let a = 10
if a > 25 {
    print(a + " is greater than 25")
} else {
    print("nope")
}
```

#### While

```
let i = 0
while i <= 5 {
    print(i)
    i = i + 1
}
```

### Print

```
let name = "mark"
print("Hello, " + name + "!")
```

## Example

```
fn greet(name) {
    print("Hello, " + name)
}

greet("user")

let i = 1
while i <= 5 {
    print(i)
    i = i + 1
}
```