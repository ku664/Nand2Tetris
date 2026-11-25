# Hack Computer Capstone — Nand2Tetris

An individual capstone implementation organised into the three required parts:

- **Student:** Kuber Sharma (Roll No. 2501730446; K = 06).
- **Part A:** Hack CPU, Memory and Computer HDL.
- **Part B:** two-pass Python assembler with the K-dependent symbol-table export feature (`symbols.txt`).
- **Part C:** generated keyboard-controlled rectangle program and an optional Python teaching emulator.

## Personal configuration

`Part-B-Assembler/config.json` is configured with `K = 6`, which is the last two digits of Kuber Sharma's university roll number (`2501730446`).

For this configuration:

- `K mod 3 = 0` → save labels and variables with their addresses in `symbols.txt`.
- `K mod 4 = 2` → 3 words per row (`(6 mod 4) + 1 = 3`).
- Box width = **48 pixels** (`16 × 3`).
- Top row = **6**; height = **20 rows** (rows 6 to 25).
- First screen address = `16384 + 32 × 6 = 16576`.

## Requirements

- Python 3.10 or newer.
- Official Nand2Tetris Software Suite for Hardware Simulator and CPU Emulator.
- Official course test scripts and reference programs for final hardware verification and exact assembler comparisons.

## Run local verification

From the repository root in PowerShell:

```powershell
python verify_project.py
```

This runs the Python assembler unit tests, assembles the locally included sample programs, regenerates the personalised box, and checks draw/erase behaviour in the included teaching emulator.

## Run individual parts

### Part A — Hardware

Open `Part-A-Computer/CPU.hdl`, `Memory.hdl`, and `Computer.hdl` in the official Hardware Simulator. Run the course-provided CPU, Memory and Computer test scripts. Save genuine passing screenshots in `Part-A-Computer/tests/evidence/`.

The official `.tst` and `.cmp` files are not bundled. Do not report Part A as passed until those tests have actually run successfully.

### Part B — Assembler

```powershell
cd Part-B-Assembler
python -m unittest discover -s tests -v
python assembler.py programs/Add.asm
python assembler.py programs/Max.asm
python assembler.py programs/Rect.asm
python assembler.py programs/Pong.asm
```

`programs/Pong.asm` is explicitly a **smoke test**, not the official Pong game. For the assignment's exact comparison requirement, use the official `Pong.asm` supplied with the course distribution and compare its generated `.hack` output against the official assembler.

### Part C — Box program

```powershell
cd Part-C-Box-Program
python generate_box.py
cd ..\Part-B-Assembler
python assembler.py ..\Part-C-Box-Program\Box.asm -o ..\Part-C-Box-Program\Box.hack
cd ..\Part-C-Box-Program
python emulator.py Box.hack
```

Hold a key while the emulator window is focused to draw the box; release it to erase. This optional Python emulator is useful for local logic checks, but it does **not** replace the required official Nand2Tetris CPU Emulator demonstration.

## Submission checklist

- [x] Confirm the student's name (`Kuber Sharma`), roll number (`2501730446`), and `K = 06` in the report and configuration.
- [ ] Run and capture official CPU, Memory and Computer HDL tests.
- [ ] Compare Add, Max, Rect and the official Pong program against official assembler output.
- [ ] Demonstrate `Box.hack` in the official CPU Emulator with key press and release.
- [ ] Add genuine screenshots and complete the report's actual mistake/correction section.
- [ ] Practise explaining the HDL, assembler passes, screen memory and K-dependent feature in the viva.

## Evidence integrity

`VERIFICATION_STATUS.md` records what was tested locally and what still requires the official course tools. Screenshots and test results must be captured from real executions; this repository does not fabricate official pass evidence.
