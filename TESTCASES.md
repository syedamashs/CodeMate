# CodeMate UI Test Cases

A collection of ready-to-use test cases across multiple programming languages and defect categories. Use these snippets to test and demonstrate the CodeMate Code Intelligence Workbench.

---

## 🐍 Python Test Cases

### 1. Syntax Error: Missing Colon & Unterminated String (Multi-Bug)
* **Language:** `Python`
* **Expected Bug Type:** `Syntax Error` (Severity: `CRITICAL`)
```python
def calculate_discount(price, rate)
    message = "Applying discount rate
    return price - (price * rate)
```

---

### 2. Runtime Error: Division by Zero with Missing Edge-Case Handling
* **Language:** `Python`
* **Expected Bug Type:** `Runtime Error` (Severity: `HIGH`)
* **Optional Error Message:** `ZeroDivisionError: division by zero`
```python
def calculate_average(scores):
    total = sum(scores)
    count = len(scores)
    return total / count

# Fails when an empty list is passed
result = calculate_average([])
```

---

### 3. Logical Error: Inverted Comparison in Maximum Finder
* **Language:** `Python`
* **Expected Bug Type:** `Logical Error` (Severity: `MEDIUM`)
```python
def find_highest_score(scores):
    highest = 0
    for score in scores:
        # Bug: comparison is inverted, tracking the minimum instead of maximum
        if score < highest:
            highest = score
    return highest

print(find_highest_score([45, 82, 19, 99, 64]))
```

---

### 4. Logical / Runtime Error: Recursion Missing Base Case (Infinite Recursion)
* **Language:** `Python`
* **Expected Bug Type:** `Runtime Error` / `Logical Error` (Severity: `HIGH`)
```python
def countdown(n):
    print(n)
    # Bug: Missing base case (if n <= 0: return)
    return countdown(n - 1)

countdown(5)
```

---

### 5. Runtime Error: Off-By-One List Index Error
* **Language:** `Python`
* **Expected Bug Type:** `Runtime Error` (Severity: `HIGH`)
* **Optional Error Message:** `IndexError: list index out of range`
```python
def print_elements(items):
    for i in range(len(items) + 1):
        print(f"Item {i}: {items[i]}")

print_elements(["apple", "banana", "cherry"])
```

---

## ☕ Java Test Cases

### 6. Syntax Error: Missing Semicolon & Bracket Mismatch
* **Language:** `Java`
* **Expected Bug Type:** `Syntax Error` (Severity: `CRITICAL`)
```java
public class Calculator {
    public static int add(int a, int b) {
        int result = a + b
        return result;
    }
```

---

### 7. Runtime Error: Null Pointer Risk
* **Language:** `Java`
* **Expected Bug Type:** `Runtime Error` (Severity: `HIGH`)
```java
public class StringHelper {
    public static int getLength(String text) {
        // Bug: Calling length() without checking if text is null
        return text.length();
    }
}
```

---

## ⚡ C / C++ Test Cases

### 8. Syntax Error: Missing Semicolon in Return Statement
* **Language:** `C`
* **Expected Bug Type:** `Syntax Error` (Severity: `CRITICAL`)
```c
#include <stdio.h>

int multiply(int x, int y) {
    return x * y
}

int main() {
    printf("%d\n", multiply(4, 5));
    return 0;
}
```

---

### 9. Logical Error: Array Out-of-Bounds in C++
* **Language:** `C++`
* **Expected Bug Type:** `Logical Error` / `Runtime Error` (Severity: `HIGH`)
```cpp
#include <iostream>
#include <vector>

void printVector(const std::vector<int>& vec) {
    // Bug: Loop condition <= vec.size() accesses out-of-bounds index
    for (size_t i = 0; i <= vec.size(); ++i) {
        std::cout << vec[i] << " ";
    }
}
```

---

## 🌐 JavaScript Test Cases

### 10. Logical Error: Strict Equality with Type Coercion Issue
* **Language:** `JavaScript`
* **Expected Bug Type:** `Logical Error` (Severity: `MEDIUM`)
```javascript
function checkUserRole(roleId) {
    const ADMIN_ROLE_ID = 1;
    // Bug: Comparing string prompt input to integer without conversion
    if (roleId === ADMIN_ROLE_ID) {
        return "Access Granted";
    }
    return "Access Denied";
}

console.log(checkUserRole("1")); // Returns Access Denied unexpectedly
```

---

### 11. Multi-Bug: Unclosed Template Literal & Undefined Variable
* **Language:** `JavaScript`
* **Expected Bug Type:** `Syntax Error` (Severity: `CRITICAL`)
```javascript
function greetUser(firstName, lastName) {
    const fullName = `${firstName ${lastName}`;
    console.log(msg);
    return fullName;
}
```

---

## ✅ Clean Code Test Case (Verify Zero False Positives)

### 12. Correct Implementation: Palindrome Checker
* **Language:** `Python`
* **Expected Bug Type:** `No obvious issue` (Severity: `CLEAN` or `LOW`)
```python
def is_palindrome(text: str) -> bool:
    clean_text = "".join(char.lower() for char in text if char.isalnum())
    return clean_text == clean_text[::-1]

print(is_palindrome("A man, a plan, a canal: Panama"))
```
