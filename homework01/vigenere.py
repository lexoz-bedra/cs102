"""vigenere"""


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    alph_caps = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    alph_small = [chr(i) for i in range(ord("a"), ord("z") + 1)]

    key = keyword
    while len(key) < len(plaintext):
        key += keyword
    new_key = list(key.lower())
    for i, char in enumerate(new_key):
        new_key[i] = int(ord(char) - ord("a"))  # type: ignore
    ciphertext = ""
    for i, char in enumerate(plaintext):
        if plaintext[i].isalpha():
            if plaintext[i] == plaintext[i].upper():
                length = len(alph_caps)
                index = (alph_caps.index(char, 0, length) + new_key[i]) % length  # type: ignore
                ciphertext += alph_caps[index]
            else:
                length = len(alph_caps)
                index = (alph_small.index(char, 0, length) + new_key[i]) % length  # type: ignore
                ciphertext += alph_small[index]
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    alph_caps = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    alph_small = [chr(i) for i in range(ord("a"), ord("z") + 1)]

    key = keyword
    while len(key) < len(ciphertext):
        key += keyword
    new_key = list(key.lower())
    for i, char in enumerate(new_key):
        new_key[i] = int(ord(char) - ord("a"))  # type: ignore

    plaintext = ""
    for i, char in enumerate(ciphertext):
        if ciphertext[i].isalpha():
            if ciphertext[i] == ciphertext[i].upper():
                length = len(alph_caps)
                index = (alph_caps.index(char, 0, length) - new_key[i]) % length  # type: ignore
                plaintext += alph_caps[index]
            else:
                length = len(alph_small)
                index = (alph_small.index(char, 0, length) - new_key[i]) % length  # type: ignore
                plaintext += alph_small[index]
        else:
            plaintext += ciphertext[i]
    return plaintext
