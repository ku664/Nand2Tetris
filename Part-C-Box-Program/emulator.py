#!/usr/bin/env python3
"""
Lightweight Hack CPU emulator with a 512x256 tkinter display.

Author: Kuber Sharma (Roll No. 2501730446, K = 06)
"""
from pathlib import Path
import argparse
import tkinter as tk

COMP_OPS = {
    0b0101010: lambda d, a, m: 0,
    0b0111111: lambda d, a, m: 1,
    0b0111010: lambda d, a, m: -1,
    0b0001100: lambda d, a, m: d,
    0b0110000: lambda d, a, m: a,
    0b1110000: lambda d, a, m: m,
    0b0001101: lambda d, a, m: ~d,
    0b0110001: lambda d, a, m: ~a,
    0b1110001: lambda d, a, m: ~m,
    0b0001111: lambda d, a, m: -d,
    0b0110011: lambda d, a, m: -a,
    0b1110011: lambda d, a, m: -m,
    0b0011111: lambda d, a, m: d + 1,
    0b0110111: lambda d, a, m: a + 1,
    0b1110111: lambda d, a, m: m + 1,
    0b0001110: lambda d, a, m: d - 1,
    0b0110010: lambda d, a, m: a - 1,
    0b1110010: lambda d, a, m: m - 1,
    0b0000010: lambda d, a, m: d + a,
    0b1000010: lambda d, a, m: d + m,
    0b0010011: lambda d, a, m: d - a,
    0b1010011: lambda d, a, m: d - m,
    0b0000111: lambda d, a, m: a - d,
    0b1000111: lambda d, a, m: m - d,
    0b0000000: lambda d, a, m: d & a,
    0b1000000: lambda d, a, m: d & m,
    0b0010101: lambda d, a, m: d | a,
    0b1010101: lambda d, a, m: d | m,
}


def mask16(value: int) -> int:
    return value & 0xFFFF


class HackMachine:
    """Minimal software model of the 16-bit Hack CPU + memory-mapped I/O."""

    def __init__(self, words):
        self.rom = list(words)
        self.ram = [0] * 32768
        self.a = 0
        self.d = 0
        self.pc = 0
        self.key = 0

    def step(self):
        if not 0 <= self.pc < len(self.rom):
            self.pc = 0
            return

        ins = self.rom[self.pc]
        old_a = self.a
        self.pc += 1

        if (ins >> 15) == 0:
            self.a = ins & 0x7FFF
            return

        comp = (ins >> 6) & 0x7F
        dest = (ins >> 3) & 0x7
        jump = ins & 0x7

        if comp not in COMP_OPS:
            raise ValueError(f"Unsupported comp bits {comp:07b} at ROM {self.pc - 1}")

        mem_val = self.key if old_a == 24576 else (self.ram[old_a] if old_a < len(self.ram) else 0)
        out = mask16(COMP_OPS[comp](self.d, self.a, mem_val))
        signed_out = out if out < 32768 else out - 65536

        if (dest & 1) and old_a < 24576:
            self.ram[old_a] = out
        if dest & 2:
            self.d = out
        if dest & 4:
            self.a = out

        take_jump = {
            0: False,
            1: signed_out > 0,
            2: signed_out == 0,
            3: signed_out >= 0,
            4: signed_out < 0,
            5: signed_out != 0,
            6: signed_out <= 0,
            7: True,
        }[jump]
        if take_jump:
            self.pc = old_a


def main():
    parser = argparse.ArgumentParser(description="Run a .hack binary on the local Hack emulator.")
    parser.add_argument("hack", nargs="?", default=str(Path(__file__).with_name("Box.hack")))
    parser.add_argument("--steps", type=int, default=200000)
    args = parser.parse_args()

    words = [int(line.strip(), 2) for line in Path(args.hack).read_text(encoding="utf-8").splitlines() if line.strip()]
    machine = HackMachine(words)

    root = tk.Tk()
    root.title("Hack Computer — Box Program (Kuber Sharma | Roll No. 2501730446)")
    root.geometry("720x560")

    info = tk.Label(
        root,
        text="Hold any key inside this window to draw the box. Release to erase it.",
        font=("Segoe UI", 11),
    )
    info.pack(pady=8)

    canvas = tk.Canvas(
        root, width=512, height=256, bg="white", highlightthickness=1, highlightbackground="#777"
    )
    canvas.pack(padx=10, pady=8)

    status = tk.Label(root, text="Keyboard: released | Screen: blank", font=("Consolas", 10))
    status.pack(pady=5)

    running = True

    def render_screen():
        canvas.delete("pixel")
        for row in range(256):
            row_base = 16384 + row * 32
            for word in range(32):
                value = machine.ram[row_base + word]
                if value == 0xFFFF:
                    x = word * 16
                    canvas.create_rectangle(x, row, x + 16, row + 1, fill="black", outline="black", tags="pixel")
                elif value:
                    for bit in range(16):
                        if value & (1 << (15 - bit)):
                            x = word * 16 + bit
                            canvas.create_rectangle(x, row, x + 1, row + 1, fill="black", outline="black", tags="pixel")
        state = "pressed" if machine.key else "released"
        status.config(text=f"Keyboard: {state} | PC: {machine.pc} | Hold a key to draw")

    def tick():
        if not running:
            return
        for _ in range(1500):
            machine.step()
        render_screen()
        root.after(30, tick)

    def on_key_down(_event):
        machine.key = 65

    def on_key_up(_event):
        machine.key = 0

    def on_close():
        nonlocal running
        running = False
        root.destroy()

    root.bind("<KeyPress>", on_key_down)
    root.bind("<KeyRelease>", on_key_up)
    root.focus_force()
    root.protocol("WM_DELETE_WINDOW", on_close)

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
