# Question 1 – Encryption and Decryption Program

## Introduction
This program was developed to demonstrate a custom encryption and decryption process using Python. The system reads input from a file, applies rule-based transformations to encrypt the text, and then reverses those transformations to recover the original content. A verification step is also included to ensure the decrypted output matches the original file exactly.  

The main challenge in this task was designing a method that remains reversible despite using multiple transformation rules.

---

## Encryption Process
The encryption function reads the contents of `raw_text.txt` and applies different rules depending on the type and position of each character:

### Lowercase Letters
- Characters between **a–m** are shifted forward by `(shift1 × shift2)`
- Characters between **n–z** are shifted backward by `(shift1 + shift2)`

### Uppercase Letters
- Characters between **A–M** are shifted backward by `shift1`
- Characters between **N–Z** are shifted forward by `(shift2²)`

### Other Characters
- Spaces, numbers, punctuation, and newline characters remain unchanged

The encrypted result is written to `encrypted_text.txt`.

---

## Issue with Reversibility
During implementation, it was identified that the encryption method is not inherently reversible. This is because different original characters can produce the same encrypted output, making it impossible to determine which rule was applied during decryption.

---

## Solution Implemented
To resolve this issue, an additional file named `rules.txt` was introduced. This file records the rule used for each character during encryption:

- `"1"` → First rule set  
- `"2"` → Second rule set  
- `"0"` → Unchanged characters  

This ensures that during decryption, the program knows exactly which transformation to reverse for each character.

---

## Decryption Process
The decryption function reads both:
- `encrypted_text.txt`
- `rules.txt`

Using the rule information, it applies the inverse operation for each character:
- Reverses forward shifts by subtracting values  
- Reverses backward shifts by adding values  
- Leaves non-alphabetic characters unchanged  

The decrypted output is written to `decrypted_text.txt`.

---

## Verification Process
To confirm correctness, the program compares the original file (`raw_text.txt`) with the decrypted file (`decrypted_text.txt`).

- If both files match → Decryption is successful  
- If not → The program identifies the exact mismatch position and characters  

This ensures the integrity of the encryption and decryption process.

---

## Program Behaviour
When executed, the program performs the following steps:

1. Prompt the user to input `shift1` and `shift2`  
2. Read and encrypt the original text file  
3. Store the encrypted output and rule data  
4. Decrypt the encrypted file using stored rules  
5. Verify that the decrypted text matches the original  

---

## Reference
![Program Output](https://github.com/Shishireno/software-now/blob/6334b02754e9ef366f97f077d022822b192d0b54/Q1.png)

---

## Conclusion
This implementation successfully demonstrates a rule-based encryption system while addressing the challenge of reversibility. By introducing a rule-tracking mechanism, the program ensures accurate decryption and maintains data integrity. The inclusion of verification further strengthens the reliability of the solution.
