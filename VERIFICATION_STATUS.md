# Verification status

## Personalisation
- Student: Anubhav
- University roll number: 2501730406
- Personal number: K = 06 (numeric value 6)
- K mod 3 = 0: save labels and variables with their addresses in `symbols.txt`
- K mod 4 = 2: 48-pixel width, three 16-bit screen words per row
- Starting row = 6; height = 20 rows
- First screen word = 16384 + (32 × 6) = 16576

## Verified locally
- 13 Python assembler unit tests passed (including `K = 6` / `K mod 3 = 0` symbol-table export).
- 2 box-generator tests passed.
- Add, Max and Rect local assembler outputs matched their checked-in `.hack` files.
- `Box.asm`, `Box.hack`, and `symbols.txt` regenerated for `K = 06`.
- Local teaching-emulator draw and erase checks passed for the 48×20 pixel box at row 6 (`SCREEN + 192 = 16576`).

## Still required before final submission
- Run official CPU, Memory and Computer HDL tests in the Nand2Tetris Hardware Simulator.
- Compare against the official Add, Max, Rect and Pong programs using the official assembler. The bundled Pong file is only a smoke test.
- Demonstrate `Box.hack` in the official CPU Emulator.
- Insert genuine screenshots of the official HDL tests, assembler comparison, and box visible/cleared states into the report.
- Complete the report's programming mistake and correction section with a real example from your own debugging work.
