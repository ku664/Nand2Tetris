#!/usr/bin/env python3
"""
Two-pass assembler for the 16-bit Nand2Tetris Hack computer.

Author: Kuber Sharma (Roll No. 2501730446, K = 06)
Required K-dependent feature (K mod 3 = 0): export resolved symbol table to symbols.txt.
"""
from pathlib import Path
import argparse
import json
import re
import sys

PREDEFINED = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    **{f"R{i}": i for i in range(16)},
}

DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}

SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


class AssemblerError(Exception):
    """Raised when an assembly source file contains invalid syntax."""


def clean_lines(source):
    """Strip comments and whitespace, returning (source_line_no, code) pairs."""
    path = Path(source)
    cleaned = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        code = raw.split("//", 1)[0].strip()
        if code:
            cleaned.append((line_no, re.sub(r"\s+", "", code)))
    return cleaned


def _format_errors(errors):
    return "\n".join(f"Line {line_no}: {msg}" for line_no, msg in errors)


def write_symbol_table(symbols, symbols_path):
    """Write all symbols (predefined, labels, variables) sorted by address to disk."""
    target = Path(symbols_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(symbols.items(), key=lambda entry: (entry[1], entry[0]))
    content = "".join(f"{name}\t{address}\n" for name, address in ordered)
    target.write_text(content, encoding="utf-8")


def assemble(source, k=6, symbols_path=None):
    """
    Assemble a Hack .asm source file into 16-bit binary instruction strings.

    Pass 1: Collect label declarations and map each label to its ROM address.
    Pass 2: Translate A- and C-instructions; allocate new variables from RAM[16].
    For K % 3 == 0 (K = 06 for Roll No. 2501730406), export the symbol table to symbols_path.
    """
    if not isinstance(k, int) or not 0 <= k <= 99:
        raise AssemblerError("K must be an integer from 0 to 99")

    lines = clean_lines(source)
    symbols = dict(PREDEFINED)
    rom_addr = 0
    warnings = []
    errors = []

    # Pass 1: record label -> ROM address mappings.
    for line_no, stmt in lines:
        if stmt.startswith("(") or stmt.endswith(")"):
            if not (stmt.startswith("(") and stmt.endswith(")")):
                errors.append((line_no, "malformed label declaration"))
                continue
            label = stmt[1:-1]
            if not SYMBOL_RE.fullmatch(label):
                errors.append((line_no, f"invalid label name: {label!r}"))
                continue
            if label in symbols:
                if label in PREDEFINED:
                    errors.append((line_no, f"label {label} conflicts with a predefined symbol"))
                else:
                    warnings.append(
                        f"Line {line_no}: duplicate label ({label}); first definition kept"
                    )
                continue
            symbols[label] = rom_addr
        else:
            rom_addr += 1

    # Pass 2: encode A-instructions and C-instructions.
    machine_code = []
    next_var_addr = 16

    for line_no, stmt in lines:
        if stmt.startswith("(") or stmt.endswith(")"):
            continue

        try:
            if stmt.startswith("@"):
                token = stmt[1:]
                if not token:
                    raise AssemblerError("missing A-instruction value")

                if token.isdecimal():
                    value = int(token)
                else:
                    if not SYMBOL_RE.fullmatch(token):
                        raise AssemblerError("invalid A-instruction symbol")
                    if token not in symbols:
                        symbols[token] = next_var_addr
                        next_var_addr += 1
                    value = symbols[token]

                if not 0 <= value <= 32767:
                    raise AssemblerError("A-instruction value must be between 0 and 32767")
                machine_code.append(f"{value:016b}")
                continue

            if stmt.count("=") > 1 or stmt.count(";") > 1:
                raise AssemblerError("malformed C-instruction")

            dest = ""
            jump = ""
            comp = stmt
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)

            if comp not in COMP:
                raise AssemblerError(f"invalid computation: {comp!r}")
            if dest not in DEST:
                raise AssemblerError(f"invalid destination: {dest!r}")
            if jump not in JUMP:
                raise AssemblerError(f"invalid jump: {jump!r}")

            machine_code.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])

        except AssemblerError as exc:
            errors.append((line_no, str(exc)))

    if errors:
        if k % 3 == 1:
            raise AssemblerError(_format_errors(errors))
        line_no, msg = errors[0]
        raise AssemblerError(f"Line {line_no}: {msg}")

    if symbols_path is not None:
        write_symbol_table(symbols, symbols_path)

    return machine_code, warnings, symbols


def main():
    parser = argparse.ArgumentParser(
        description="Translate Hack assembly (.asm) into 16-bit machine code (.hack)."
    )
    parser.add_argument("source", help="input .asm file")
    parser.add_argument("-o", "--output", help="output .hack file (default: same name as source)")
    parser.add_argument("--k", type=int, help="personal K: last two digits of university roll number")
    parser.add_argument(
        "--symbols",
        help="symbol-table output path (default: Part-B-Assembler/symbols.txt)",
    )
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    try:
        config = json.loads((project_dir / "config.json").read_text(encoding="utf-8"))
        k = args.k if args.k is not None else int(config.get("K", 6))
        output_path = Path(args.output) if args.output else Path(args.source).with_suffix(".hack")
        symbols_path = Path(args.symbols) if args.symbols else project_dir / "symbols.txt"

        words, warnings, _ = assemble(args.source, k=k, symbols_path=symbols_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(words) + "\n", encoding="utf-8")

        print(f"Success: wrote {len(words)} 16-bit instructions to {output_path}")
        if k % 3 == 0:
            print(f"Symbol table saved to {symbols_path}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        feature = (
            "save symbol table",
            "line-numbered invalid-instruction errors",
            "duplicate-label warnings",
        )[k % 3]
        print(f"K={k:02d}; required additional feature: {feature}")
    except (AssemblerError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ASSEMBLY FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
