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
    alph_caps = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    alph_small = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    ciphertext = ""
    for ch in plaintext:
        if ch.isalpha():
            if ch == ch.upper():
                ciphertext += alph_caps[(alph_caps.index(ch, 0, len(alph_caps)) + shift) % len(alph_caps)]
            else:
                ciphertext += alph_small[(alph_small.index(ch, 0, len(alph_small)) + shift) % len(alph_small)]
        else:
            ciphertext += ch
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
    alph_caps = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    alph_small = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    plaintext = ""
    for ch in ciphertext:
        if ch.isalpha():
            if ch == ch.upper():
                plaintext += alph_caps[(alph_caps.index(ch, 0, len(alph_caps)) - shift) % len(alph_caps)]
            else:
                plaintext += alph_small[(alph_small.index(ch, 0, len(alph_small)) - shift) % len(alph_small)]
        else:
            plaintext += ch
    return plaintext
