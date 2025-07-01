#!/usr/bin/env python3
import os

INPUT_FILE = 'rockyou.txt'
OUTPUT_TEMPLATE = 'rockyou_part{}.txt'  # will generate part1…part4

def count_lines(filepath):
    """Return total number of lines in the file."""
    with open(filepath, 'rb') as f:
        return sum(1 for _ in f)

def split_into_four(input_file):
    total_lines = count_lines(input_file)
    base_size = total_lines // 4
    remainder = total_lines % 4

    # Determine the size of each part (first 'remainder' parts get +1 line)
    sizes = [
        base_size + (1 if i < remainder else 0)
        for i in range(4)
    ]

    # Open four output files and write the label
    out_files = []
    for i, sz in enumerate(sizes, start=1):
        fname = OUTPUT_TEMPLATE.format(i)
        f = open(fname, 'w', encoding='utf-8')
        out_files.append((f, sz))

    # Now distribute lines
    with open(input_file, 'r', encoding='latin-1', errors='ignore') as src:
        part_idx = 0
        written = 0
        for line in src:
            f, sz = out_files[part_idx]
            f.write(line)
            written += 1
            if written >= sz:
                f.close()
                part_idx += 1
                written = 0
                if part_idx >= 4:
                    break  # should be done

    # Close any remaining files (in case)
    for i in range(part_idx, 4):
        out_files[i][0].close()

    print("Done splitting into 4 parts.")

if __name__ == '__main__':
    if not os.path.isfile(INPUT_FILE):
        print(f"Error: '{INPUT_FILE}' not found.")
    else:
        split_into_four(INPUT_FILE)
