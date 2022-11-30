"""caesar"""


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    alph_caps = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    alph_small = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    ciphertext = ""
    for i, char in enumerate(plaintext):
        if plaintext[i].isalpha():
            if plaintext[i] == plaintext[i].upper():
                length = len(alph_caps)
                ciphertext += alph_caps[(alph_caps.index(char, 0, length) + shift) % length]
            else:
                length = len(alph_caps)
                ciphertext += alph_small[(alph_small.index(char, 0, length) + shift) % length]
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    alph_caps = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    alph_small = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    plaintext = ""
    for i, char in enumerate(ciphertext):
        if ciphertext[i].isalpha():
            if ciphertext[i] == ciphertext[i].upper():
                length = len(alph_caps)
                plaintext += alph_caps[(alph_caps.index(char, 0, length) - shift) % length]
            else:
                length = len(alph_small)
                plaintext += alph_small[(alph_small.index(char, 0, length) - shift) % length]
        else:
            plaintext += ciphertext[i]
    return plaintext
