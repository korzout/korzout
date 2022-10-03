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
    ciphertext = ""
    alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(plaintext)):
        if plaintext[i] in alphabet_lower:
            k = keyword[i % len(keyword)].lower()
            shift = alphabet_lower.index(k)
            ciphertext = (
                ciphertext
                + alphabet_lower[(alphabet_lower.index(plaintext[i]) + shift) % len(alphabet_lower)]
            )
        elif plaintext[i] in alphabet_upper:
            k = keyword[i % len(keyword)].upper()
            shift = alphabet_upper.index(k)
            ciphertext = (
                ciphertext
                + alphabet_upper[(alphabet_upper.index(plaintext[i]) + shift) % len(alphabet_upper)]
            )
        else:
            ciphertext = ciphertext + plaintext[i]
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
    plaintext = ""
    alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(ciphertext)):
        if ciphertext[i] in alphabet_lower:
            k = keyword[i % len(keyword)].lower()
            shift = alphabet_lower.index(k)
            plaintext = (
                plaintext
                + alphabet_lower[
                    (alphabet_lower.index(ciphertext[i]) - shift) % len(alphabet_lower)
                ]
            )
        elif ciphertext[i] in alphabet_upper:
            k = keyword[i % len(keyword)].upper()
            shift = alphabet_upper.index(k)
            plaintext = (
                plaintext
                + alphabet_upper[
                    (alphabet_upper.index(ciphertext[i]) - shift) % len(alphabet_upper)
                ]
            )
        else:
            plaintext = plaintext + ciphertext[i]
    return plaintext
