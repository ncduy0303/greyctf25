import numpy as np
from PIL import Image

img = Image.open("subGB.png").convert("RGB")
arr = np.array(img)  # shape = (8, 60, 3)

R_mask = (arr[:, :, 0] > 0).astype(int)  # 1 if red pixel, else 0
G_mask = (arr[:, :, 1] > 0).astype(int)
B_mask = (arr[:, :, 2] > 0).astype(int)
masks = {"R": R_mask, "G": G_mask, "B": B_mask}
# print(f"R_mask: {R_mask}, "
#       f"G_mask: {G_mask}, "
#       f"B_mask: {B_mask}")

