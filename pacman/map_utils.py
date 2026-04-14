#!/usr/bin/env python3

from pathlib import Path

BORDER_SYMBOL = ["═", "║", "╔", "╗", "╚", "╝", "*"]
BORDERS = ['═', '║', '╔', '╗', '╚', '╝']

def load_map(file_pathname):
    """Loads map lines from a file."""
    file = Path(file_pathname)
    if not file.is_file():
        raise ValueError(f"'{file_pathname}' is not a valid file path.")

    with file.open("r", encoding="utf-8") as f:
        # Use rstrip to remove trailing newlines while keeping leading spaces
        pacman_map = [line.rstrip('\n') for line in f if line.strip()]

    return pacman_map

def simplify_map(pacman_map):
    """Converts visual borders back to generic '*' symbols."""
    if not isinstance(pacman_map, list):
        raise TypeError("'pacman_map' must be a list")

    simplified_map = []
    mapping = {
        "═": "*", "║": "*", "╔": "*", 
        "╗": "*", "╚": "*", "╝": "*",
        "·": ".", "•": "o"
    }
    
    for line in pacman_map:
        newline = "".join(mapping.get(char, char) for char in line)
        simplified_map.append(newline)
    
    return simplified_map

def prettify_map(pacman_map):
    """
    Transforms a simplified map (*) into a visually accurate 
    bordered map using neighbor detection.
    """
    if not isinstance(pacman_map, list):
        raise TypeError("'pacman_map' must be a list")

    height = len(pacman_map)
    first_stage = []

    # Stage 1: Basic Border Detection
    for r in range(height):
        newline = ""
        width = len(pacman_map[r])
        for c in range(width):
            char = pacman_map[r][c]
            if char == ".":
                newline += "·"
            elif char == "o":
                newline += "•"
            elif char == "*":
                # Check neighbors (Up, Down, Left, Right)
                u = r > 0 and pacman_map[r-1][c] == "*"
                d = r < height - 1 and pacman_map[r+1][c] == "*"
                l = c > 0 and pacman_map[r][c-1] == "*"
                r_side = c < width - 1 and pacman_map[r][c+1] == "*"

                # Logic for basic corners and lines
                if (l or r_side) and not (u or d): newline += "═"
                elif (u or d) and not (l or r_side): newline += "║"
                elif r_side and d: newline += "╔"
                elif l and d: newline += "╗"
                elif r_side and u: newline += "╚"
                elif l and u: newline += "╝"
                else: newline += "═" # Default
            else:
                newline += char
        first_stage.append(newline)

    return first_stage

def compress_map_with_rle(pacman_map):
    """Compresses map using Run-Length Encoding."""
    if not isinstance(pacman_map, list):
        raise TypeError("'pacman_map' must be a list")

    rle_map = []
    for line in pacman_map:
        if not line:
            rle_map.append("")
            continue
            
        newline = ""
        current_char = line[0]
        count = 0
        
        for char in line:
            if char == current_char:
                count += 1
            else:
                newline += f"{count}{current_char}"
                current_char = char
                count = 1
        
        # Append the final group
        newline += f"{count}{current_char}"
        rle_map.append(newline)
    
    return rle_map

def uncompress_map_with_rle(compressed_map):
    """Restores an RLE map to its full string representation."""
    if not isinstance(compressed_map, list):
        raise TypeError("'compressed_map' must be a list")

    uncompressed_map = []
    for line in compressed_map:
        newline = ""
        number_str = ""
        for char in line:
            if char.isdigit():
                number_str += char
            else:
                if number_str:
                    newline += char * int(number_str)
                    number_str = ""
        uncompressed_map.append(newline)
    
    return uncompressed_map

def save_map(pacman_map, file_pathname):
    """Saves map to file."""
    path = Path(file_pathname)
    if path.exists():
        raise ValueError(f"File '{file_pathname}' already exists.")
    
    with path.open("w", encoding="utf-8") as f:
        for line in pacman_map:
            f.write(line + '\n')
