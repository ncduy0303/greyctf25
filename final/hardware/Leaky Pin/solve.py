import board
import rp2pio
import adafruit_pioasm
import time
from leaky_gpio25 import secret_in_gpio25

# ——— PIO program: sample 1 bit continuously ———
pio_source = """
.program sampler
loop:
    in pins, 1
    jmp loop
"""
assembled = adafruit_pioasm.assemble(pio_source)

# ——— Instantiate the PIO StateMachine on GP24 ———
sm = rp2pio.StateMachine(
    assembled,
    frequency=150_000_000,   # 150 MHz sample clock
    first_in_pin=board.GP24, # now wired to GPIO25 via jumper
    in_shift_right=False,    # shift direction (new bits enter LSB)
    push_threshold=32,       # push every 32 bits
    auto_push=True           # auto-push when threshold reached
)

# ——— Prepare a buffer for 1000 words (32 bits each) ———
buf = bytearray(4000)  # 1000 * 4 bytes

# Give the SM a moment to spin up
time.sleep(0.01)

# ——— 1) Trigger the secret leak ———
print("❯ Leaking secret on GPIO25 → please wait…")
secret_in_gpio25()

# ——— 2) Capture into our buffer ———
print("❯ Capturing on GP24…")
sm.readinto(buf)
print("❯ Capture complete.")

# ——— Tidy up ———
sm.deinit()

# ——— Decode the captured bits ———
# Convert each 4-byte chunk → 32-bit word → 32-bit binary string
bitstream = "".join(
    f"{int.from_bytes(buf[i:i+4], 'big'):032b}"
    for i in range(0, len(buf), 4)
)

# Pack bits into bytes
flag_bytes = bytearray(
    int(bitstream[i:i+8], 2)
    for i in range(0, len(bitstream), 8)
    if len(bitstream[i:i+8]) == 8
)

# ——— Print it out ———
try:
    decoded = flag_bytes.decode("utf-8", errors="ignore")
    print("\nDecoded string:")
    print(decoded)
    # Try to extract grey{…}
    if "grey{" in decoded.lower():
        start = decoded.lower().find("grey{")
        end   = decoded.find("}", start) + 1
        print(f"\n🏁 Flag: {decoded[start:end]}")
except Exception as e:
    print("⚠️ Decode error:", e)
    print("Raw bytes:", flag_bytes)
