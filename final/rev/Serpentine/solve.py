def m():
    # Check if Python version hash matches expected value (anti-tamper/version check)
    if __import__("hashlib").sha1(__import__("sys").version.encode()).hexdigest() != "aa7f8dbc4108c4188deae171641908d3ed37e455":
        return
    # Import ctypes for low-level memory manipulation
    ct = __import__("ctypes")
    # Import random for shuffling operations
    r = __import__("random")
    # Get reference to memmove function for memory copying
    mm = ct.memmove
    # Get memory address from int type object + 96 bytes offset
    t = ct.cast(id(int) + 96, ct.POINTER(ct.c_uint64)).contents.value
    # Load C library for system calls
    l = ct.CDLL(None)
    # Align memory address to page boundary (clear lower 12 bits)
    p = t & (~0xfff)
    # Make memory page writable using mprotect syscall (10=mprotect, 7=RWX permissions)
    l.syscall(10, ct.c_uint64(p), 0x1000, 7)
    # Calculate various memory offsets for manipulation
    a = t + 112
    b = t
    c = t + 96
    d = t + 112
    # Custom character mapping table (substitution cipher)
    f = b':0oECk`XP6?YMK^t~gu[GW/}wmn\\U>j%$Hr]hiD=eJ9+QI_AN&y58l2pzSO;d{RT(<\'vaLs"-!bxq|Vf37FB*@1Z.#,4)c'
    # Get memory address of the character table + 32 bytes offset
    e = id(f) + 32
    # Overwrite ASCII character representations in memory with custom mapping
    for i in range(33, 127):  # ASCII printable characters
        mm(id(i)+24, e, 1)    # Copy 1 byte from custom table to character object
        e += 1                # Move to next character in table
    # Declare global variable to override built-in 'reversed' function
    global reversed
    def g(l):
        # Seed random number generator with fixed value for reproducible shuffling
        r.seed(69)
        # Shuffle the input list in-place
        r.shuffle(l)
        # Copy 8 bytes of memory between calculated addresses (memory manipulation)
        mm(c, d, 8)
        mm(a, b, 8)
        # Right-shift each list element by specific amounts (data obfuscation)
        l[2] >>= 120   # Shift element at index 2 right by 120 bits
        l[3] >>= 36    # Shift element at index 3 right by 36 bits
        l[8] >>= 83    # Shift element at index 8 right by 83 bits
        l[0] >>= 78    # Shift element at index 0 right by 78 bits
        l[13] >>= 0    # Shift element at index 13 right by 0 bits (no change)
        l[7] >>= 61    # Shift element at index 7 right by 61 bits
        l[4] >>= 79    # Shift element at index 4 right by 79 bits
        l[12] >>= 49   # Shift element at index 12 right by 49 bits
        l[6] >>= 87    # Shift element at index 6 right by 87 bits
        l[10] >>= 82   # Shift element at index 10 right by 82 bits
        l[11] >>= 112  # Shift element at index 11 right by 112 bits
        l[1] >>= 99    # Shift element at index 1 right by 99 bits
        l[15] >>= 101  # Shift element at index 15 right by 101 bits
        l[14] >>= 106  # Shift element at index 14 right by 106 bits
        l[9] >>= 49    # Shift element at index 9 right by 49 bits
        l[5] >>= 35    # Shift element at index 5 right by 35 bits
        return l

    # Replace built-in 'reversed' function with custom function 'g'
    reversed = g
# Execute the memory manipulation and function override
m()

# Helper function to pad string on the left with specified character
def leftpad(x,n,c=" "):
    return c * (n-len(x)) + x

# Helper function to pad string on the right with specified character
def rightpad(x,n,c=" "):
    return x + c * (n-len(x))


# Flag to track if any validation fails
fail = False
try:
    # Attempt to read the flag file
    with open("./flag.txt", "rb") as f:
        b = f.read()
        b = b.strip()  # Remove whitespace
        # Check if flag starts with "grey{"
        if b[:5] != b"grey{":
            fail = True
        # Check if flag ends with "}"
        if b[-1] != ord('}'):
            fail = True
        # Extract flag content (remove "grey{" and "}")
        b = b[5:-1]
except:
    # If file reading fails, mark as failure
    fail = True
# Check if flag content is exactly 16 bytes long
if len(b) != 16:
    fail = True

# If all validations pass, process the flag
if not fail:
    # XOR each byte with 42, then apply custom 'reversed' function (which is actually function 'g')
    b = bytes(reversed([x ^ 42 for x in b]))

    # Write the processed data back to flag.txt
    with open("./flag.txt", "wb") as f:
        f.write(b)