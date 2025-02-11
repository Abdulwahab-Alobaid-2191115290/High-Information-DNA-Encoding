# Table of Contents

1. [Introduction](#introduction)
2. [Method](#method)
   - [Encoding](#encoding)
   - [Decoding](#decoding)
3. [Results and Discussion](#results-and-discussion)
   - [Lab Constraints](#lab-constraints)
   - [Storage](#storage)
   - [Error](#error)
4. [Future Directions](#future-directions)

# Introduction

In the field of DNA based data storage, information density is always a competitive measure which contributes to the effeciency of the storage method. As increasing information density reduces DNA synthesis and sequencing costs.

This work implements a significantly high information density encoding scheme. Which also comes with several limitations which make real life implementation challenging.


# Method

## Encoding

A data file is parsed in chunks, each chunk consists of 3 bytes. A simple max function is used to encode 3 bytes into a single base, this function can be replaced with any other function as long as it reads 3 bytes and outputs a DNA nucleotide. A separate codebook is used to store these values to allow decoding.

![image](https://github.com/user-attachments/assets/2b2d5d9f-e86c-42b2-bd1e-18a23841da76)

You will notice there is also an RGB image as output, since the main idea was motivated by an RGB pixel structure, the strand was converted to an image since we are at it.

## Decoding

Directly reading from the codebook in-order is enough to decode the strand. Decoding without the codebook is currently impossible, unless a specific variation is implemented for encoding.


# Results and Discussion

In terms of information density, this method surpases any existing coding scheme.

| Work  | Information Density |
| ------------- | ------------- |
| Organick et al.  | 1.10  |
| Bornholt et al.  | 0.85  |
| Grass et al.     | 1.26  |
| **This Work**    | **24.0** |


However, although high information density is achieved, real life implementation is an extreme limiting factor. Such limitations are discussed in the following section.

## Lab constraints

This work simply focuses on information density, and ignores biological details such as.

- GC content.
- Homopolymer avoidance. As repeated nucleotides are bad for sequencing.
- Avoidance of secondary structures and primer-dimer formations.
- Some implementations such as ones by Organick et al. implement random access, they do it through having a primer for each strand(each strand represents a file). So involve primer design in their discussion.

Although the current implementation does not adhere such constraints, the implemented algorithm acts as a placeholder, meaning it can be replaced with any other encoding method as long as produces a similiar codebook.


## Storage

The problem in the storage lies in the codebook size which is considered very large. The proposed way of storing the each codebook is shown in the following struct:

```c
typedef struct CodeBookEntry{

        char base;  // 1-byte

        mi_int1 r;  // 1-byte integer (0 - 255)
        mi_int1 g;
        mi_int1 b;
    } CodeBookEntry;
```

Given this struct, this means each base requires 4-bytes to store To calculate codebook size. To calculate the codebook size we look consider the resulting sequence length which is `NumberOfBases * 4`. Given the encoding scheme, the sequence length is `ciel(bytes/3)` where 3 is the tuple size. So for a Terabyte, the codebook size will be `ciel(bytes/3)*4` which is 1.3333 Terabytes. Even if appending the codebook using a simple encoding scheme 2 bits/base, the resulting information density drops all the way to 0.176 !

Thereby, there has to be a way to deal with the size of the codebook. Standard compression techniques achieve a compression rate of 30%, but is still not enough and does not solve the main problem.

A proposed idea, is to use high dimensional interpolation. If we consider the encoding function to be F(x, y, z, w), where x(first byte), y(second byte), z(third byte), and w to indicate the order of the nucleotide, as in 0, 1, 2, ... If such thing is possible, it might require only a certain amount of points to be stored in the codebook, then a continous interpolation is applied to derive the rest of the points retrieving the original codebook.

However, extra reading is required to verify:

- If this is possible in the first place.
- Will it really reduce the length of the codebook? If so by how much?
- Measure the accuracy of the interpolation, and what are the minimum points required for an accurate interpolation.
- How much time will it take? Is it possible to do it on a standard machine or parallel computation is required (GPU, distributed computing)?


## Error

Although high information is a good thing, it means 3 bytes are lost per base i.e. 24-bits per base. If compared with other work, the criticality of error rises significantly with bases lost as shown.

![image](https://github.com/user-attachments/assets/25c6a970-5d82-4a80-8d7c-d2f3ef869ff9)


So an effecient error correction is mandatory especially when coding rate increases. An alternate measure is to use sequencing coverage, but this is usually a costly process. It is also worth mentioning that applying error correction also impacts the code rate, because it adds redundancy to the data itself. An example of an effecient implementation of Reed-Solomon error correction in DNA storage is done by William H. et al. in https://github.com/whpress/hedges.

Additionally, one has to amount of redundancy required, this can also be influenced by different sequencing and synthesis technologies, as they have different indel(insertion, deletion) and subtitution error distributions.


# Future Directions

- Apply error correction using HEDGES paper implementation https://github.com/whpress/hedges.
- Identify error distributions (insertion%, deletion%, and substitution%), then identify exact tolerance for errors. This will help identify minimum redundancy required for this encoding method.
- See possibilities for random access, Organick et al. work is relevant.
- What are the implications of increasing information density? e.g. using RGBA instead of RGB, or any x-bits per nucleotide? We expect codebook and error correction to be directly affected.
- Real test of the encoding scheme (a later step, when lab constraints are met).
- DNA as an image wasn't an idea unique to this work, this work here applies studies on the image version of DNA https://github.com/MahdiKarimian/DIF, it might be possible to extend the work for this implementation.
- Analyse encoding time and memory usage.






