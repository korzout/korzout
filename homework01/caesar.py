import typing as tp


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
    ciphertext = ""
    for i in range(len(plaintext)):
        if 65 <= ord(plaintext[i]) and ord(plaintext[i]) <= 90:
            ciphertext = ciphertext + chr((ord(plaintext[i]) - 65 + shift) % 26 + 65)
        elif 97 <= ord(plaintext[i]) and ord(plaintext[i]) <= 122:
            ciphertext = ciphertext + chr((ord(plaintext[i]) - 97 + shift) % 26 + 97)
        else:
            ciphertext = ciphertext + plaintext[i]
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
    plaintext = ""
    for i in range(len(ciphertext)):
        if 65 <= ord(ciphertext[i]) and ord(ciphertext[i]) <= 90:
            plaintext = plaintext + chr((ord(ciphertext[i]) - 65 - shift) % 26 + 65)
        elif 97 <= ord(ciphertext[i]) and ord(ciphertext[i]) <= 122:
            plaintext = plaintext + chr((ord(ciphertext[i]) - 97 - shift) % 26 + 97)
        else:
            plaintext = plaintext + ciphertext[i]
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    maxcounter = -1
    for shift in range(26):
        message = decrypt_caesar(ciphertext)
        counter = 0
        for word in message.split():
            counter += word in dictionary
        if counter > maxcounter:
            best_shift = shift
    return best_shift
