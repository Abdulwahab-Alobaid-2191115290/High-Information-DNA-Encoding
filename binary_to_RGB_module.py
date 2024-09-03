
from PIL import Image
import numpy as np
import math

# Decoding based on recipe
def decode(recipe, padding):
    ascii_str = ''
    # print("recipe: ", recipe)
    print(padding)
    # removing global padding from recipe
    if padding['global'] > 0:
        recipe = recipe.splitlines()[:(padding["global"])*-1]

    repixeled = []
    # removing global padding
    for line in recipe:
        rgb_str_list = line.strip('ATGCN(')[:-2].split(', ')
        rgb_int_list = [int(val) for val in rgb_str_list]
        repixeled.append(rgb_int_list)
        ascii_list = [chr(val) for val in rgb_int_list]
        ascii_str += "".join(ascii_list)

    # print("decoded: ")
    # for _ in repixeled:
    #     print(_)

    # removing local padding
    if padding["local"] > 0:
        return ascii_str[:(padding["local"]*-1)]
    return ascii_str

# Encoding function
# Idea: perhaps we can optimize encoding by removing the padding from the recipe file and only keep the global/local padding vals
def encode(pixel_matrix):

    dna = ""
    recipe = ""
    for pixel_array in pixel_matrix:
        for (a, b, c) in pixel_array:
            if a >= b and b >= c and a >= c:
                dna += "A"
            elif a <= b and b <= c and a <= c:
                dna += "T"
            elif a >= b and b <= c and a >= c:
                dna += "G"
            elif a >= b and b <= c and a <= c:
                dna += "C"
            else:
                # extra cases that affect the nucleotide distribution
                if a <= b and b >= c and a <= c:
                    dna += "N"
                elif a <= b and b >= c and a <= c:
                    dna += "N"
            recipe += f"{dna[-1]}({a}, {b}, {c}) \n"

    return dna, recipe


# turns an array of tuples it into a square matrix with fill_value as padding
def squarify(array, fill_value=(255, 255, 255)):
    num_elements = len(array)

    # get size of the square matrix
    matrix_size = math.ceil(math.sqrt(num_elements))

    # calculate global padding for decoding
    global_padding = matrix_size**2 - num_elements

    # initialize matrix with fill_value
    matrix = [[fill_value for _ in range(matrix_size)] for _ in range(matrix_size)]

    # fill the matrix with the values from the array
    for i in range(matrix_size):
        for j in range(matrix_size):
            index = i * matrix_size + j
            if index < num_elements:
                matrix[i][j] = array[index]

    return matrix, global_padding


# groups array elements into groups of 3 i.e. tuples. Padded with 255 when required
def tuplify(array, tuple_size, fill_value=255):
    # Create chunks of the specified size
    chunks = [tuple(array[i:i + tuple_size]) for i in range(0, len(array), tuple_size)]

    # Pad the last chunk if necessary
    if len(chunks) > 0 and len(chunks[-1]) < tuple_size:
        # Calculate how many elements to pad
        padding_needed = tuple_size - len(chunks[-1])
        # Pad the last chunk
        chunks[-1] += (fill_value,) * padding_needed

    return chunks


# converts text to png image
def txt_to_png(src):

    # getting the binary representation of the file
    src_ascii = []
    for char in src:
        src_ascii.append(ord(char))
    # print("characters: ", src_ascii, "\n")

    tuple_size = 3      # 3 for RGB, 4 for RGBA if required

    # local padding: used for decoding
    local_padding = tuple_size - (len(src_ascii) % tuple_size)
    # in case modulus gives 0, then padding will be = tuple size, which is wrong, hence we set padding = 0 to fix this bug
    local_padding = 0 if local_padding == tuple_size else local_padding

    # creating rgb tuples i.e. the pixels of the image
    pixels = tuplify(src_ascii, 3)
    # print("pixel tuples: ", pixels, "\n")

    # making sure the image is always a square, padding is added as required
    pixel_matrix, global_padding = squarify(pixels)

    # print the matrix
    print(f"pixel matrix {math.ceil(math.sqrt(len(pixels)))}x{math.ceil(math.sqrt(len(pixels)))} with (255, 255, 255) as padding: ")
    for _ in pixel_matrix:
        print(_)

    dna, recipe = encode(pixel_matrix)
    # print(dna)

    # writing files
    with open("recipe.txt", "w") as recipe_file:
        recipe_file.write(recipe)
        recipe_file.write(f"{local_padding}, {global_padding}")

    with open("encoded_data.fasta", "w") as fasta_file:
        fasta_file.write("> encoded_data \n")
        fasta_file.write(dna + " \n")

    # conversion from pixel matrix to image
    array = np.array(pixel_matrix, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save('new.png')

    padding = {"local": local_padding, "global": global_padding}

    return dna, recipe, padding


dna, recipe, padding = txt_to_png("hey, this is wahab as an imageoa")
decoded = decode(recipe, padding)

print(decoded)