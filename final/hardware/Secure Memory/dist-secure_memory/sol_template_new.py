import board, digitalio, time, hardware.fpga

# 1) Drop the overlay so we control the pins
hardware.hw_state["fpga_overlay"].deinit()
if input("↪ press Enter to load bitstream…"):
    h = hardware.fpga.upload_bitstream("/hardware/bitstreams/main.bit")
    h.deinit()

# 2) Pin assignments
addr_pins = [board.GP8, board.GP9, board.GP10, board.GP11, board.GP12]
mode_pins = [board.GP13, board.GP14, board.GP15]          # fixed = 0b010
data_pins = [board.GP27, board.GP16, board.GP23, board.GP25,
             board.GP26, board.GP28, board.GP22, board.GP24]

# configure the 5 address outputs
addr_io = []
for p in addr_pins:
    d = digitalio.DigitalInOut(p)
    d.direction = digitalio.Direction.OUTPUT
    addr_io.append(d)

# configure the 3 mode bits to 0,1,0
for p, v in zip(mode_pins, (0,1,0)):
    d = digitalio.DigitalInOut(p)
    d.direction = digitalio.Direction.OUTPUT
    d.value = v

# configure the 8 data inputs
data_io = []
for p in data_pins:
    d = digitalio.DigitalInOut(p)
    d.direction = digitalio.Direction.INPUT
    data_io.append(d)

# 3) Drive address=31 *once*, as fast as possible
def latch_address(addr=31):
    bits = [(addr >> i) & 1 for i in range(5)]
    for i, b in enumerate(bits):
        addr_io[i].value = b
    # give the FPGA a few microseconds to propagate
    time.sleep(0.001)

# 4) Read the bus as an integer
def read_bus():
    v = 0
    for i, pin in enumerate(data_io):
        if pin.value:
            v |= 1 << i
    return v

# ——————————————————————————————————————————————
# 5) Busy-wait for every change, record it immediately
# ——————————————————————————————————————————————
latch_address()

prev = read_bus()
flag = []

print("Streaming flag… (hit Ctrl-C to abort)")

while True:
    cur = read_bus()
    if cur != prev:
        # stop on 0x00 or “?”
        if cur == 0 or cur == 0x3F:
            break
        flag.append(chr(cur))
        print(chr(cur), end="")
        prev = cur
    # no sleep! keep polling as fast as possible

print("\n\nRecovered flag:", "".join(flag))
