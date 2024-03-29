"""rsa"""
import random
import typing as tp
from math import ceil, sqrt


def is_prime(number: int) -> bool:
    """
    Tests to see if a number is prime.
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if number <= 0:
        return False
    if number == 1:
        return False
    if number == 2:
        return True
    for i in range(2, ceil(sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


def gcd(first: int, second: int) -> int:
    """
    Euclid's algorithm for determining the greatest common divisor.
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """

    minn = min(first, second)
    maxx = max(first, second)
    while minn:
        maxx, minn = minn, maxx % minn
    return abs(maxx)


def multiplicative_inverse(arg: int, phi: int) -> int:
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.
    >>> multiplicative_inverse(7, 40)
    23
    """
    arr = [[phi, arg, max(arg, phi) % min(arg, phi), max(arg, phi) // min(arg, phi), 0, 1]]
    i = 0
    while arr[i][2]:
        arr.append(
            [
                arr[i][1],
                arr[i][2],
                max(arr[i][1], arr[i][2]) % min(arr[i][1], arr[i][2]),
                max(arr[i][1], arr[i][2]) // min(arr[i][1], arr[i][2]),
                0,
                1,
            ]
        )
        i += 1
    for i in range(len(arr) - 2, -1, -1):
        arr[i][5] = arr[i + 1][4] - arr[i][3] * arr[i + 1][5]
        arr[i][4] = arr[i + 1][5]
    return arr[0][5] % phi


def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    """generates keys"""
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    if p == q:
        raise ValueError("p and q cannot be equal")

    # n = pq
    n = p * q

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    divider = gcd(e, phi)
    while divider != 1:
        e = random.randrange(1, phi)
        divider = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return (e, n), (d, n)


def encrypt(packed_key: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    """encrypting"""
    # Unpack the key into it's components
    key, num = packed_key
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % num for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(packed_key: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    """decrypting"""
    # Unpack the key into its components
    key, num = packed_key
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char**key) % num) for char in ciphertext]
    # Return the array of bytes as a string
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(str, encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
