#!/usr/bin/env python

import parse_sbox
import random
import sys

inv_he = {
    'ACAT': 'a',
    'ACTG': 'b',
    'ACCC': 'c',
    'ACGA': 'd',
    'TCAT': 'e',
    'TCTG': 'f',
    'TCCG': 'g',
    'TCGT': 'h',
    'CCAG': 'i',
    'CCTA': 'j',
    'AAAA': 'y',
    'CCCG': 'k',
    'CCGG': 'l',
    'GCAA': 'm',
    'GCTA': 'w',
    'GCTT': 'n',
    'GCCG': 'o',
    'GCGC': 'p',
    'ACCG': 'r',
    'TCCC': 't',
    'ACTC': 'q',
    'TCTC': 's',
    'CCTT': 'u',
    'CCCC': 'v',
    'AATT': 'z',
    'GCCC': 'x',
    'GGGG': '',
}

def decode_from_blocks(blocks):
    decoded = []
    for pb in blocks:
        tmp = ''
        tmp2 = ''
        for b in pb:
            tmp += b
            if len(tmp) == 4:
                tmp2 += inv_he[tmp]
                tmp = ''
        decoded.append(tmp2)

    return decoded


inverse_sbox = parse_sbox.inverse_sbox
# DNA base to binary
binary = {
    'A': '00',
    'C': '01',
    'G': '10',
    'T': '11',
}

# Binary to DNA
dnab = {
    '00': 'A',
    '01': 'C',
    '10': 'G',
    '11': 'T',
}

# Timin v Uracil, ostalo enako
inv_mRNA = {
    'G': 'G',
    'C': 'C',
    'U': 'T',
    'A': 'A',
}

# komplementi baz
inv_tRNA = {
    'C': 'G',
    'G': 'C',
    'U': 'A',
    'A': 'U',
}

inv_permute = {
    1 : 40,
    2 : 8,
    3 : 48,
    4 : 16,
    5 : 56,
    6 : 24,
    7 : 64,
    8 : 32,
    9 : 39,
    10 : 7,
    11 : 47,
    12 : 15,
    13 : 55,
    14 : 23,
    15 : 63,
    16 : 31,
    17 : 38,
    18 : 6,
    19 : 46,
    20 : 14,
    21 : 54,
    22 : 22,
    23 : 62,
    24 : 30,
    25 : 37,
    26 : 5,
    27 : 45,
    28 : 13,
    29 : 53,
    30 : 21,
    31 : 61,
    32 : 29,
    33 : 36,
    34 : 4,
    35 : 44,
    36 : 12,
    37 : 52,
    38 : 20,
    39 : 60,
    40 : 28,
    41 : 35,
    42 : 3,
    43 : 43,
    44 : 11,
    45 : 51,
    46 : 19,
    47 : 59,
    48 : 27,
    49 : 34,
    50 : 2,
    51 : 42,
    52 : 10,
    53 : 50,
    54 : 18,
    55 : 58,
    56 : 26,
    57 : 33,
    58 : 1,
    59 : 41,
    60 : 9,
    61 : 49,
    62 : 17,
    63 : 57,
    64 : 25,
}

def change_timin_to_uracil(blocks):
    dna = []
    for p in blocks:
        tmp = p.replace('T', 'U')
        dna.append(tmp)

    return dna

def convert_binary_to_dna(blocks):
    dna_text = []
    for s in blocks:
        tmp = ''
        tmp2 = ''
        for b in s:
            tmp += b
            if len(tmp) == 2:
                tmp2 += dnab[tmp]
                tmp = ''
        dna_text.append(tmp2)

    return dna_text

def inv_mrna_trna(blocks):
    perm = []
    for sb in blocks:
        tmp = ''
        for c in sb:
            tmp += inv_mRNA[inv_tRNA[c]]
        perm.append(tmp)

    return perm

def convert_dna_to_binary(blocks):
    binary_text = []
    for p in blocks:
        tmp = ''
        for c in p:
            tmp += binary[c]
        binary_text.append(tmp)

    return binary_text

def xor(blocks, key):
    xored = []
    for b in blocks:
        y = int(b,2) ^ int(key,2)
        bino = '{0:0{1}b}'.format(y,len(b))
        assert 64 == len(bino)
        xored.append(bino)

    return xored

def inv_permutation(blocks):
    perm = []
    for p in blocks:
        tmp = ''
        for i, c in enumerate(p):
            tmp += p[inv_permute[i+1] - 1]
        perm.append(tmp)
        tmp = ''

    return perm

def inv_substitution(blocks):
    sub_text = []
    for pb in blocks:
        tmp = ''
        tmp2 = ''
        for b in pb:
            tmp += b
            if len(tmp) == 4:
                # prva dva znaka row
                # druga dva znaka column
                tmp2 += inverse_sbox[tmp[0:2]][tmp[2:4]]
                tmp = ''
        sub_text.append(tmp2)

    return sub_text

def print_blocks(blocks):
    for b in blocks:
        print(b)

def generate_round_keys(src):
    num_keys = 16
    round_keys = []
    for k in range(num_keys):
        random.seed(src + k)
        x = random.getrandbits(64)
        bino = '{0:0{1}b}'.format(x,64)
        assert len(bino) == 64
        round_keys.append(bino)

    return round_keys

def remove_padding(blocks):
    unpadded = []
    for pb in blocks:
        tmp = ''
        tmp2 = ''
        for b in pb:
            tmp += b
            if len(tmp) == 4:
                if tmp != 'GGTG':
                    tmp2 += tmp
                tmp = ''
        unpadded.append(tmp2)

    return unpadded

if __name__ == '__main__':
    # DNA cipher text
    ct = [sys.argv[2]]
    # encodeing
    key = int.from_bytes(sys.argv[1].encode("utf-8"), byteorder='big')
    round_keys = round_keys = generate_round_keys(key)

    for r in reversed(round_keys):
        # Convert DNA to binary
        bina = convert_dna_to_binary(ct)
        #print_blocks(bin)

        # XOR with key
        xored = xor(bina, r)
        #print_blocks(xored)

        # Inverse permutation
        perm = inv_permutation(xored)
        #print_blocks(perm)

        # Convert back to DNA
        rna = convert_binary_to_dna(perm)
        #print_blocks(rna)

        # Change Timin to Uracil
        dna = change_timin_to_uracil(rna)
        #print_blocks(dna)

        # Inverse tRNA and mRNA
        inv = inv_mrna_trna(dna)
        #print_blocks(inv)

        # Inverse Substitution
        invsub = inv_substitution(inv)
        #print_blocks(invsub)

        ct = invsub

    # Remove padding
    unpadded = remove_padding(invsub)
    #print_blocks(unpadded)

    # Decode text
    decoded = decode_from_blocks(unpadded)
    print_blocks(decoded)
