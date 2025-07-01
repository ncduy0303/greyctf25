import ctypes as ct

def debug_int_type_pointers():
    # Get the same addresses as in the original code
    t = ct.cast(id(int) + 96, ct.POINTER(ct.c_uint64)).contents.value
    
    a = t + 112  # Source address 1
    b = t        # Destination address 1  
    c = t + 96   # Source address 2 (same as t)
    d = t + 112  # Destination address 2 (same as a)
    
    print(f"Base address t: 0x{t:016x}")
    print(f"Address a (t+112): 0x{a:016x}")
    print(f"Address b (t+0): 0x{b:016x}")
    print(f"Address c (t+96): 0x{c:016x}")
    print(f"Address d (t+112): 0x{d:016x}")
    print()
    
    # Read the actual function pointers at these addresses
    ptr_at_b = ct.cast(b, ct.POINTER(ct.c_uint64)).contents.value
    ptr_at_c = ct.cast(c, ct.POINTER(ct.c_uint64)).contents.value  
    ptr_at_a = ct.cast(a, ct.POINTER(ct.c_uint64)).contents.value
    
    print(f"Function pointer at address b (t+0): 0x{ptr_at_b:016x}")
    print(f"Function pointer at address c (t+96): 0x{ptr_at_c:016x}")
    print(f"Function pointer at address a (t+112): 0x{ptr_at_a:016x}")
    print()
    
    # Map these to PyTypeObject fields (approximate offsets for CPython 3.x)
    print("Likely PyTypeObject fields:")
    print(f"  b (t+0): Likely tp_name or object header field")
    print(f"  c (t+96): Likely tp_dictoffset or tp_weaklistoffset") 
    print(f"  a (t+112): Likely tp_iter or tp_methods")
    
    # Try to get the int type object and examine its structure
    int_type = type(int)
    print(f"\nint type object: {int_type}")
    print(f"int type id: 0x{id(int):016x}")
    
    # Calculate the actual base of the int type object
    int_base = id(int)
    print(f"So t (id(int)+96) points to offset 96 in the int type object")
    print(f"Original t value was: 0x{t:016x}")
    print(f"Which should be at: 0x{int_base + 96:016x}")

# Run the debugging
debug_int_type_pointers()

# To see what functions these might be, you can also try:
def examine_int_methods():
    print("\nint type methods and attributes:")
    for attr in dir(int):
        if not attr.startswith('_'):
            print(f"  {attr}")
    
    # Check specific methods that might be at these offsets
    print(f"\nint.as_integer_ratio: {getattr(int, 'as_integer_ratio', 'Not found')}")
    print(f"int.real: {getattr(int, 'real', 'Not found')}")

examine_int_methods()