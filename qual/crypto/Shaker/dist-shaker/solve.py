from pwn import remote, success, warn, info, context # type: ignore
import hashlib

# Set up pwntools context
context.log_level = 'info' # Use 'debug' for more verbose output

# Server details
HOST = "challs.nusgreyhats.org"
PORT = 33302

# Attempt to connect to the server
try:
    io = remote(HOST, PORT)
except Exception as e:
    print(f"Failed to connect to server: {e}")
    exit(1)

# --- Collect samples ---
# Each call to option '2' uses one "shake" internally during reset.
# MAX_SHAKES is 200. We can make up to 200 calls to option '2'.
num_samples = 100  # Number of samples to collect.
list_of_Y_outputs = [] # To store the 64-byte outputs (as lists of ints)

info(f"Collecting {num_samples} samples...")
for i in range(num_samples):
    try:
        io.sendlineafter(b"> ", b"2") # Choose "See inside"
        # Receive the output line, e.g., "Result: aabbcc..."
        line = io.recvline().strip().decode()
        
        if "Result: " not in line:
            warn(f"Unexpected line format on sample {i+1}: {line}")
            # Attempt to read another line, in case of an extra message
            line = io.recvline().strip().decode()
            if "Result: " not in line:
                io.close()
                exit(1)
        
        hex_output = line.split("Result: ")[1]
        Y_k = bytes.fromhex(hex_output)
        
        if len(Y_k) != 64:
            print(f"Output length for sample {i+1} is not 64 bytes: {len(Y_k)}. Aborting.")
            io.close()
            exit(1)
            
        list_of_Y_outputs.append(list(Y_k)) # Store as list of byte values (integers)
        if (i + 1) % 25 == 0 or i == num_samples - 1: # Progress update
            info(f"Collected sample {i+1}/{num_samples}")

    except EOFError:
        print("Connection closed unexpectedly by server while collecting samples. Aborting.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while collecting sample {i+1}: {e}. Aborting.")
        io.close()
        exit(1)

if len(list_of_Y_outputs) != num_samples:
    print(f"Failed to collect all {num_samples} samples. Only got {len(list_of_Y_outputs)}. Aborting.")
    io.close()
    exit(1)

# --- Determine the XOR key x ---
recovered_x = [-1] * 64 # Initialize with -1 to indicate not found
possible_x_byte_values = list(range(256))
# Standard printable ASCII range for flag characters
CHARACTER_WHITELIST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"

info("Determining the 64-byte XOR key 'x'...")
all_x_j_uniquely_determined = True
for j in range(64):  # For each byte position/column of x
    # S_j contains all observed bytes at this position 'j' across all samples
    S_j = [Y_k[j] for Y_k in list_of_Y_outputs]
    
    candidate_x_values_for_j = []
    for guess_x_val in possible_x_byte_values:
        is_plausible_x_byte = True
        for y_byte_in_S_j in S_j:
            # If guess_x_val is correct, then y_byte_in_S_j ^ guess_x_val should be a flag character
            decrypted_char_code = y_byte_in_S_j ^ guess_x_val
            if decrypted_char_code not in map(ord, CHARACTER_WHITELIST):
                is_plausible_x_byte = False
                break
        if is_plausible_x_byte:
            candidate_x_values_for_j.append(guess_x_val)
    
    if len(candidate_x_values_for_j) == 1:
        recovered_x[j] = candidate_x_values_for_j[0]
    else:
        warn(f"Byte x[{j}] has {len(candidate_x_values_for_j)} candidates: {candidate_x_values_for_j}.")
        all_x_j_uniquely_determined = False
        if candidate_x_values_for_j: # If there are candidates, pick the first one (a guess)
            recovered_x[j] = candidate_x_values_for_j[0]
            warn(f"  Using the first candidate for x[{j}]: {recovered_x[j]}")
        else: # No candidates found
            print(f"  No valid candidate found for x[{j}]. This is problematic.")
            # recovered_x[j] remains -1

if not all_x_j_uniquely_determined:
    warn("Some bytes of 'x' were not uniquely determined. The derived flag might be incorrect.")
if any(val == -1 for val in recovered_x):
    print("Failed to determine all bytes of 'x'. Cannot proceed to flag recovery.")
    io.close()
    exit(1)

info(f"Recovered x (first 16 bytes hex): {bytes(recovered_x[:16]).hex()}...")

# --- Calculate the candidate flag ---
# Y_0 is the first output collected: list_of_Y_outputs[0]
# Y_0 = F ^ x  =>  F = Y_0 ^ x
Y_0 = list_of_Y_outputs[0] 
candidate_flag_bytes_list = [Y_0[j] ^ recovered_x[j] for j in range(64)]
candidate_flag_bytes = bytes(candidate_flag_bytes_list)

# --- Verify the flag ---
target_md5 = "4839d730994228d53f64f0dca6488f8d"
info(f"Target MD5: {target_md5}")

md5_hash_of_candidate = hashlib.md5(candidate_flag_bytes).hexdigest()
info(f"MD5 of candidate flag: {md5_hash_of_candidate}")

try:
    candidate_flag_str = candidate_flag_bytes.decode('ascii')
    info(f"Candidate flag string: {candidate_flag_str}")
    # Additional check: ensure all characters are in the assumed range
    if not all(char_range_min <= ord(c) <= char_range_max for c in candidate_flag_str):
        warn("Warning: Recovered flag contains characters outside the assumed printable range [32, 126].")

except UnicodeDecodeError:
    warn(f"Candidate flag is not valid ASCII. Hex: {candidate_flag_bytes.hex()}")
    candidate_flag_str = "" # Cannot be the flag if not ASCII and printable generally

if md5_hash_of_candidate == target_md5:
    success(f"🎉 Flag successfully recovered: {candidate_flag_str}")
else:
    print("Flag verification failed. MD5 hash does not match.")
    print("This could be due to non-unique x_j determination or incorrect character range assumption.")

# --- Exit gracefully ---
try:
    io.sendlineafter(b"> ", b"3")
    io.close()
except EOFError:
    info("Connection already closed by server.")
except Exception as e:
    warn(f"Error during cleanup: {e}")