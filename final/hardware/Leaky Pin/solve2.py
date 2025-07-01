import board
import rp2pio
import adafruit_pioasm
import time
from leaky_gpio25 import secret_in_gpio25

# ——— Simple Counter replacement ———
def count_occurrences(seq):
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts

# ——— PIO program ———
pio_source = """
.program sampler
loop:
    in pins, 1
    jmp loop
"""
assembled = adafruit_pioasm.assemble(pio_source)

# ——— Set up SM ———
sm = rp2pio.StateMachine(
    assembled,
    frequency=150_000_000,
    first_in_pin=board.GP24,
    in_shift_right=False,
    push_threshold=32,
    auto_push=True
)

# ——— Capture ———
BUF_LEN = 8000
buf = bytearray(BUF_LEN)

time.sleep(0.01)
secret_in_gpio25()
sm.readinto(buf)
sm.deinit()

# ——— Count unique byte values ———
byte_counts = count_occurrences(buf)
print("\n📊 Unique byte values:")
for val in sorted(byte_counts):
    print("Byte 0x{:02X} ({}): {} times".format(val, val, byte_counts[val]))

# ——— Count unique 32-bit words ———
words = [int.from_bytes(buf[i:i+4], "big")
         for i in range(0, len(buf), 4)]
word_counts = count_occurrences(words)

print("\n📊 Unique 32-bit word values:")
for val in sorted(word_counts):
    print("Word 0x{:08X}: {} times".format(val, word_counts[val]))
