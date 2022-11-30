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
    alph_caps = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    alph_small = [chr(i) for i in range(ord('a'), ord('z') + 1)]

    new_key = keyword
    while len(new_key) < len(plaintext):
        new_key += keyword
    new_key = [i for i in new_key.lower()]
    for i in range(len(new_key)):
        new_key[i] = ord(new_key[i]) - ord('a')
    ciphertext = ""
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if plaintext[i] == plaintext[i].upper():
                ciphertext += alph_caps[(alph_caps.index(plaintext[i], 0, len(alph_caps)) + int(new_key[i])) % len(alph_caps)]
            else:
                ciphertext += alph_small[(alph_small.index(plaintext[i], 0, len(alph_small)) + int(new_key[i])) % len(alph_small)]
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
    alph_caps = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    alph_small = [chr(i) for i in range(ord('a'), ord('z') + 1)]

    new_key = keyword
    while len(new_key) < len(ciphertext):
        new_key += keyword
    new_key = [i for i in new_key.lower()]
    for i in range(len(new_key)):
        new_key[i] = ord(new_key[i]) - ord('a')

    plaintext = ""
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if ciphertext[i] == ciphertext[i].upper():
                plaintext += alph_caps[(alph_caps.index(ciphertext[i], 0, len(alph_caps)) - int(new_key[i])) % len(alph_caps)]
            else:
                plaintext += alph_small[(alph_small.index(ciphertext[i], 0, len(alph_small)) - int(new_key[i])) % len(alph_small)]
        else:
            plaintext += ciphertext[i]
    return plaintext
