# Hack Computer Capstone Report

**Name:** Kuber Sharma  
**Roll number:** 2501730446  
**Personal K (last two digits):** 06  
**K mod 3:** 0 (Save symbol table to `symbols.txt`)  
**Box dimensions:** 48 pixels wide (3 words/row) × 20 rows high (`16 × ((6 mod 4) + 1) = 48`)  
**Top screen row:** 6 (First screen address = `16384 + 32 × 6 = 16576`)

## 1. Objective
The objective of this capstone is to build and test the Hack computer, implement a two-pass Hack assembler in Python, and write a Hack assembly program that displays a personalised black rectangle while a keyboard key is pressed.

## 2. Part A — Hardware implementation
Briefly explain `CPU.hdl`, `Memory.hdl` and `Computer.hdl`. Mention any lab chip replaced with a built-in chip.

**Evidence:** Insert genuine screenshots for `CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst` and `ComputerRect.tst`. Write Pass/Fail beside each.

## 3. Part B — Python assembler
Explain the two passes, predefined symbols, labels, variables starting at RAM address 16, A-instruction encoding and C-instruction encoding. Since `K = 06` (`K mod 3 = 0`), document how the assembler exports all resolved symbols to `symbols.txt`.

**Evidence:** Insert the Python test output, one successful assembly output, and a screenshot/snippet of `symbols.txt`. Compare output with the official assembler.

## 4. Part C — Personalised box
State the formula and calculate your actual dimensions:
- Top row = `K` = **6**
- Height = **20 rows**
- Words per row = `(K mod 4) + 1` = `(6 mod 4) + 1` = **3 words**
- Width = `16 × 3` = **48 pixels**
- First screen address = `16384 + 32 × 6` = **16576**

Explain how the program checks the keyboard (`@KBD`) and writes `-1` to draw and `0` to erase the selected screen memory words.

**Evidence:** Insert a screenshot of the visible box in the official CPU Emulator (and optionally the included Python demo emulator).

## 5. One mistake I fixed
Describe one real mistake you encountered, its cause, how you corrected it, and how you verified the fix (for example, fixing `Memory.hdl` address decoding so both `00` and `01` on `address[13..14]` route to `RAM16K` and `10` routes to `Screen`).

## 6. Conclusion
Summarise what you learned about hardware integration, binary instructions, symbol resolution, memory-mapped I/O and screen drawing.

## 7. Final evidence audit (complete before submission)
- Confirm that the name (`Kuber Sharma`) and roll number (`2501730446`) on this report belong to the submitting student.
- Confirm that `K = 06` equals the last two digits of that student's roll number.
- List the exact official test filenames and their actual outcomes.
- Attach original screenshots; do not use emulator mock-ups as Hardware Simulator evidence.
- State clearly which chips were built in earlier labs and which built-in chips were used.
