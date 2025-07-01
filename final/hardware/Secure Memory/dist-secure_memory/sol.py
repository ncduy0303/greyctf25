import board
import digitalio
import time
import hardware.fpga

# The bitstream is already loaded, so we can comment this out or skip it.
# hardware.hw_state["fpga_overlay"].deinit()
# if input("type something to update fpga: ") != "":
#     h = hardware.fpga.upload_bitstream("/hardware/bitstreams/main.bit")
#     h.deinit()

# These are the 8 pins from the microcontroller (RP2040) to the FPGA.
# They are used to send control signals and the memory address.
fpga_interconnect_pins = [
    board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15
]

# These are the 8 pins from the FPGA back to the microcontroller.
# The FPGA will place the data from the memory onto these pins.
# The pin numbers (16, 17, etc.) are read directly from the board's silkscreen.
fpga_output_pins = [
    board.GP16, board.GP17, board.GP18, board.GP19,
    board.GP20, board.GP21, board.GP22, board.GP24
]

# Configure FPGA Interconnect pins as OUTPUTS (RP2040 -> FPGA)

def setup_interconnect_pins():
    dio = []
    for p in fpga_interconnect_pins:
        d = digitalio.DigitalInOut(p)
        d.direction = digitalio.Direction.OUTPUT
        dio.append(d)
    return dio

# Configure PMOD ECPS pins as INPUTS (FPGA -> RP2040)


def setup_output_pins():
    dio = []
    for p in fpga_output_pins:
        d = digitalio.DigitalInOut(p)
        d.direction = digitalio.Direction.INPUT
        dio.append(d)
    return dio


interconnect = setup_interconnect_pins()
data_in = setup_output_pins()

# --- THE BYPASS ---
# The default mode is 2 (0b010), which is the "secure" memory challenge.
# We are changing the mode to 1 (0b001) to talk to the regular memory directly.
# interconnect[7] is the most significant bit of the mode.
print("Setting FPGA mode to 1 (Regular Memory Access)...")
interconnect[7].value = 0  # Mode bit 2
interconnect[6].value = 0  # Mode bit 1
interconnect[5].value = 1  # Mode bit 0

# --- DATA EXTRACTION ---
# The flag is stored across 32 addresses (2^5).
# We will loop through each address, read the byte, and store it.
flag_bytes = []
print("Reading memory from addresses 0 to 31...")

for address in range(32):
    # Set the 5 address pins (interconnect[4:0])
    for i in range(5):
        # This is a neat trick to set each pin based on the bits of the address
        # (address >> i) & 1 gets the i-th bit of the address
        interconnect[i].value = (address >> i) & 1

    # Give the FPGA a tiny amount of time to put the data on the output pins
    time.sleep(0.01)

    # Read the 8 data pins and assemble the byte
    byte_val = 0
    for i in range(8):
        if data_in[i].value:
            # If the pin is high (True), add its value to our byte
            # (1 << i) is the same as 2**i
            byte_val |= (1 << i)

    flag_bytes.append(byte_val)

# Convert the collected bytes into a readable string
flag = "".join(map(chr, flag_bytes))

print("\n----------------------------------")
print("Extraction Complete!")
print(f"Flag: {flag}")
print("----------------------------------")
