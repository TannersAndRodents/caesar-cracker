"""Encypt text with the caesar method."""

ALPHABET_STR = "abcdefghijklmnopqrstuvwxyz"

def encode_character(s: str) -> int:

    encoding_dict = {"a": 0,
                    "b": 1,
                    "c": 2,
                    "d": 3,
                    "e": 4,
                    "f": 5,
                    "g": 6,
                    "h": 7,
                    "i": 8,
                    "j": 9,
                    "k": 10,
                    "l": 11,
                    "m": 12,
                    "n": 13,
                    "o": 14,
                    "p": 15,
                    "q": 16,
                    "r": 17,
                    "s": 18,
                    "t": 19,
                    "u": 20,
                    "v": 21,
                    "w": 22,
                    "x": 23,
                    "y": 24,
                    "z": 25}

    return encoding_dict[s]

def decode_character(encoded_s: int) -> str:

    decoding_dict = {0: "a",
                     1: "b",
                     2: "c",
                     3: "d",
                     4: "e",
                     5: "f",
                     6: "g",
                     7: "h",
                     8: "i",
                     9: "j",
                     10: "k",
                     11: "l",
                     12: "m",
                     13: "n",
                     14: "o",
                     15: "p",
                     16: "q",
                     17: "r",
                     18: "s",
                     19: "t",
                     20: "u",
                     21: "v",
                     22: "w",
                     23: "x",
                     24: "y",
                     25: "z"}

    return decoding_dict[encoded_s]

def encrypt_character(s: str, o: int) -> str:
    """

    Parameters:
    ----------
    s: str
        the character to encode
    o: int
        the offset used for caesar
    """

    encoded_s = encode_character(s)
    encoded_encrypted_s = (encoded_s + o) % 26
    encrypted_s = decode_character(encoded_encrypted_s)

    return encrypted_s

def encrypt_text(s: str, o: int) -> str:

    s = s.lower()
    encrypted_s = ""
    for char in s:
        if char in ALPHABET_STR:
            encrypted_s += encrypt_character(char, o)
        else:
            encrypted_s += char
    return encrypted_s

def decrypt_text(s: str) -> str:
    shift = detect_offset(s)
    return encrypt_text(s, shift)

def detect_offset(s: str) -> int:

    s = s.lower()
    letter_count = 0
    letter_dict = {}
    for char in s:
        if char in ALPHABET_STR:
            letter_count += 1
            if not char in letter_dict.keys():
                letter_dict[char] = 1
            else:
                letter_dict[char] += 1

    letter_frequencies = {}
    for key in letter_dict.keys():
        letter_frequencies[key] = letter_dict[key] / letter_count
    letter_frequencies_values = []
    for char in ALPHABET_STR:
        if char in letter_dict.keys():
            letter_frequencies_values.append(letter_frequencies[char])
        else:
            letter_frequencies_values.append(0)

    expected_letter_frequencies = {"a": 0.082,
                                   "b": 0.015,
                                   "c": 0.028,
                                   "d": 0.043,
                                   "e": 0.127,
                                   "f": 0.022,
                                   "g": 0.02,
                                   "h": 0.061,
                                   "i": 0.07,
                                   "j": 0.0015,
                                   "k": 0.0077,
                                   "l": 0.04,
                                   "m": 0.024,
                                   "n": 0.067,
                                   "o": 0.075,
                                   "p": 0.019,
                                   "q": 0.00095,
                                   "r": 0.06,
                                   "s": 0.063,
                                   "t": 0.091,
                                   "u": 0.028,
                                   "v": 0.0098,
                                   "w": 0.024,
                                   "x": 0.0015,
                                   "y": 0.02,
                                   "z": 0.00074}
    min_error_at_shift = 0
    min_error = 26
    for i in range(0, 26):
        error = shift_mean_square_error(letter_frequencies_values, list(expected_letter_frequencies.values()), i)
        if error < min_error:
            min_error = error
            min_error_at_shift = i

    return min_error_at_shift

def shift_mean_square_error(l1_original, l2, offset):

    l1 = []
    for x in l1_original:
        l1.append(x)

    error = 0

    for i in range(0, offset):
        element = l1.pop()
        l1.insert(0, element)

    for entry1, entry2 in zip(l1, l2):
        error += (entry1 - entry2)**2

    return error
