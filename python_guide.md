# Python Programming Guide

## Variables and Data Types

Python supports several built-in data types:

### Basic Data Types
- **int**: Integer numbers (e.g., 42, -10, 0)
- **float**: Decimal numbers (e.g., 3.14, -2.5, 1.0)
- **str**: Text strings (e.g., "Hello", 'World', """Multi-line""")
- **bool**: Boolean values (True, False)

### Collections
- **list**: Ordered, mutable collection [1, 2, 3]
- **tuple**: Ordered, immutable collection (1, 2, 3)
- **dict**: Key-value pairs {"name": "John", "age": 30}
- **set**: Unordered unique elements {1, 2, 3}

## Functions

### Defining Functions
```python
def greet(name):
    """Function to greet a person"""
    return f"Hello, {name}!"

# Call the function
message = greet("Alice")
print(message)  # Output: Hello, Alice!
```

### Lambda Functions
```python
# Anonymous function
square = lambda x: x ** 2
print(square(5))  # Output: 25

# Using with map
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # Output: [1, 4, 9, 16, 25]
```

## Classes and Objects

### Basic Class Definition
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old."

# Create an instance
person = Person("Bob", 25)
print(person.introduce())
```

## File Operations

### Reading Files
```python
# Read entire file
with open('file.txt', 'r') as f:
    content = f.read()

# Read line by line
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())
```

### Writing Files
```python
# Write to file
with open('output.txt', 'w') as f:
    f.write("Hello, World!")

# Append to file
with open('log.txt', 'a') as f:
    f.write("New log entry\n")
```

## Error Handling

### Try-Except Blocks
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Cleanup code here")
```

## List Comprehensions

### Basic Syntax
```python
# Create a list of squares
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Filter even numbers
evens = [x for x in range(20) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

## Modules and Imports

### Importing Modules
```python
import math
from datetime import datetime
import numpy as np

# Using imported functions
print(math.pi)
print(datetime.now())
```

This guide covers essential Python programming concepts for beginners and intermediate developers.