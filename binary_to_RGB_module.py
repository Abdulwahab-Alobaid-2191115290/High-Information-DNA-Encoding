
from PIL import Image
import numpy as np
import math

# Decoding based on recipe
def decode(recipe):
    ascii_str = ''
    for line in recipe.splitlines():
        rgb_str_list = line.strip('ATGCN(')[:-2].split(', ')
        rgb_int_list = [int(val) for val in rgb_str_list]

        ascii_list = [chr(val) for val in rgb_int_list]
        ascii_str += "".join(ascii_list)

    return ascii_str

# Encoding function
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

    # initialize matrix with fill_value
    matrix = [[fill_value for _ in range(matrix_size)] for _ in range(matrix_size)]

    # fill the matrix with the values from the array
    for i in range(matrix_size):
        for j in range(matrix_size):
            index = i * matrix_size + j
            if index < num_elements:
                matrix[i][j] = array[index]

    return matrix


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

    # creating rgb tuples i.e. the pixels of the image
    pixels = tuplify(src_ascii, 3)
    # print("pixel tuples: ", pixels, "\n")

    # making sure the image is always a square, padding is added as required
    pixel_matrix = squarify(pixels)

    # print the matrix
    # print(f"pixel matrix {math.ceil(math.sqrt(len(pixels)))}x{math.ceil(math.sqrt(len(pixels)))} with (255, 255, 255) as padding: ")
    # for _ in pixel_matrix:
    #     print(_)

    dna, recipe = encode(pixel_matrix)
    # print(dna)

    # writing files
    with open("recipe.txt", "w") as recipe_file:
        recipe_file.write(recipe)
    with open("encoded_data.fasta", "w") as fasta_file:
        fasta_file.write("> encoded_data \n")
        fasta_file.write(dna + " \n")

    # conversion from pixel matrix to image
    array = np.array(pixel_matrix, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save('new.png')

    return dna, recipe


dna, recipe = txt_to_png("hey, this is wahab as an image")
decoded = decode(recipe)

print(decoded)