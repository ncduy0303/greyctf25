import numpy as np
from PIL import Image

# ── Step 0: Load the 60×8 image.
img = Image.open("subGB.png").convert("RGB")
arr = np.array(img)  # shape = (8, 60, 3)


# # ── Step 1: Build three 8×60 boolean masks.
R_mask = (arr[:, :, 0] > 0).astype(int)  # 1 if red pixel, else 0
G_mask = (arr[:, :, 1] > 0).astype(int)
B_mask = (arr[:, :, 2] > 0).astype(int)
masks = {"R": R_mask, "G": G_mask, "B": B_mask}
# print(f"R_mask: {R_mask}, "
#       f"G_mask: {G_mask}, "
#       f"B_mask: {B_mask}")

# For each mask, treat each column as a byte (8 bits), and convert to character.
def bits_to_char(bits):
    """Convert a list of 8 bits to a character."""
    return chr(int("".join(str(bit) for bit in bits), 2))
def convert_to_string(mask):
    """Convert an 8x60 bitarray to a string."""
    return ''.join(bits_to_char(mask[:, i]) for i in range(mask.shape[1]))
# Convert each mask to a string
for channel_name, mask in masks.items():
    result_string = convert_to_string(mask)
    print(f"Channel {channel_name} decodes to: {result_string}")

# # ── Step 2: Load (or define) a tiny 6×8 font dictionary.
# #    FONT_6x8 should map ASCII chars → 8×6 arrays of 0/1 bits.
# #    For example: FONT_6x8['A'] might be
# #       [[0,1,1,1,1,0],
# #        [1,0,0,0,0,1],
# #        [1,0,0,0,0,1],
# #        [1,1,1,1,1,1],
# #        [1,0,0,0,0,1],
# #        [1,0,0,0,0,1],
# #        [1,0,0,0,0,1],
# #        [1,0,0,0,0,1]]
# #
# #    You can find many 6×8 font arrays online.  Below is just a SMALL example:
# FONT_6x8 = {
#     "A": np.array([
#        [0,1,1,1,1,0],
#        [1,0,0,0,0,1],
#        [1,0,0,0,0,1],
#        [1,1,1,1,1,1],
#        [1,0,0,0,0,1],
#        [1,0,0,0,0,1],
#        [1,0,0,0,0,1],
#        [1,0,0,0,0,1],
#     ], dtype=int),
#     "B": np.array([
#        [1,1,1,1,0,0],
#        [1,0,0,0,1,0],
#        [1,0,0,0,1,0],
#        [1,1,1,1,0,0],
#        [1,0,0,0,1,0],
#        [1,0,0,0,1,0],
#        [1,0,0,0,1,0],
#        [1,1,1,1,0,0],
#     ], dtype=int),
#     # …and so on for C, D, E, …, Z, 0–9, '{', '}', '_', etc.
#     # You must fill in the rest of FONT_6x8 for all characters you might see.
# }

# # ── Step 3: A helper to match an 8×6 “block” to a character.
# def match_block_to_char(block, font_dict):
#     """
#     block: 8×6 numpy array of 0/1 bits.
#     font_dict: maps ASCII char → 8×6 array.
#     Returns the matching character, or '?' if no match.
#     """
#     for ch, glyph in font_dict.items():
#         if np.array_equal(block, glyph):
#             return ch
#     return "?"

# # ── Step 4: Try each channel in turn.  Split into ten 8×6 blocks.
# for channel_name, mask in masks.items():
#     guessed = []
#     for i in range(10):
#         block = mask[:, i*6 : (i+1)*6]     # shape = (8, 6)
#         c = match_block_to_char(block, FONT_6x8)
#         guessed.append(c)
#     result = "".join(guessed)
#     print(f"Channel {channel_name} decodes to: {result}")

#     # If you see something like "GREY{S0METHING...}", you’ve found your flag.
