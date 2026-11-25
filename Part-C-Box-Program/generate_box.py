#!/usr/bin/env python3
"""
Generate the personalised key-controlled rectangle Hack assembly program.

Author: Anubhav (Roll No. 2501730406, K = 06)
For K = 6: top row = 6, height = 20 rows, words/row = (6 mod 4) + 1 = 3 (48 pixels),
first screen word = 16384 + 32 * 6 = 16576.
"""
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
CONFIG = HERE.parent / "Part-B-Assembler" / "config.json"


def generate(k: int) -> str:
    """Return Hack assembly source for a key-controlled rectangle parametrised by K."""
    if not 0 <= k <= 99:
        raise ValueError("K must be between 0 and 99")

    words_per_row = (k % 4) + 1
    first_screen_addr = 16384 + 32 * k
    width_px = words_per_row * 16

    lines = [
        f"// Personal K = {k}",
        f"// Top row = {k}; height = 20 rows; width = {width_px} pixels ({words_per_row} words).",
        f"// First screen address = {first_screen_addr} (16384 + 32 * {k})",
        "(CHECK_KEY)",
        "@KBD",
        "D=M",
        "@DRAW",
        "D;JGT",
        "@ERASE",
        "0;JMP",
        "(DRAW)",
        f"@{first_screen_addr}",
        "D=A",
        "@ROW",
        "M=D",
        "@20",
        "D=A",
        "@COUNT",
        "M=D",
        "(DRAW_ROW)",
        "@ROW",
        "D=M",
        "@PTR",
        "M=D",
        f"@{words_per_row}",
        "D=A",
        "@WIDTH",
        "M=D",
        "(DRAW_WORD)",
        "@PTR",
        "A=M",
        "M=-1",
        "@PTR",
        "M=M+1",
        "@WIDTH",
        "MD=M-1",
        "@DRAW_WORD",
        "D;JGT",
        "@ROW",
        "D=M",
        "@32",
        "D=D+A",
        "@ROW",
        "M=D",
        "@COUNT",
        "MD=M-1",
        "@DRAW_ROW",
        "D;JGT",
        "@CHECK_KEY",
        "0;JMP",
        "(ERASE)",
        f"@{first_screen_addr}",
        "D=A",
        "@ROW",
        "M=D",
        "@20",
        "D=A",
        "@COUNT",
        "M=D",
        "(ERASE_ROW)",
        "@ROW",
        "D=M",
        "@PTR",
        "M=D",
        f"@{words_per_row}",
        "D=A",
        "@WIDTH",
        "M=D",
        "(ERASE_WORD)",
        "@PTR",
        "A=M",
        "M=0",
        "@PTR",
        "M=M+1",
        "@WIDTH",
        "MD=M-1",
        "@ERASE_WORD",
        "D;JGT",
        "@ROW",
        "D=M",
        "@32",
        "D=D+A",
        "@ROW",
        "M=D",
        "@COUNT",
        "MD=M-1",
        "@ERASE_ROW",
        "D;JGT",
        "@CHECK_KEY",
        "0;JMP",
    ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Generate personalised Box.asm from K in config.json."
    )
    parser.add_argument("--k", type=int, help="override personal K (0..99)")
    args = parser.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    k = args.k if args.k is not None else int(cfg["K"])
    asm_text = generate(k)
    (HERE / "Box.asm").write_text(asm_text, encoding="utf-8")
    words = (k % 4) + 1
    print(
        f"Generated Box.asm for K={k:02d}: top row {k}, 20 rows high, "
        f"{words * 16} pixels wide ({words} words), start address {16384 + 32 * k}."
    )


if __name__ == "__main__":
    main()
