#!/usr/bin/env python3
import string, base64
from itertools import product

# Remove "#" for your own specific usage.

cipher = "CIPHER TEXT" # \
      # SAME CYPHER, 2ND LINE"
#cipher2 ="2ND CIPHER"

# THM{/HTB{ / ctf{  : whatever you get the point
KNOW_PLAIN_TEXT = ""

def parse(cipher):
    cipher = cipher.strip().replace(" ", "").replace("\n", "")
    try:
        return bytes.fromhex(cipher)
    except Exception:
        pass
    try:
        return base64.b64decode(cipher)
    except Exception:
        pass
    return cipher.encode()

def xor_decrypt(cipher: bytes, key: bytes) -> str:
    return bytes([cipher[i] ^ key[i % len(key)] for i in range(len(cipher))]).decode(errors='replace')

def recover_key(cipher: bytes, known: str) -> bytes:
    kb = KNOW_PLAIN_TEXT.encode() # bytes
    return bytes([c ^ p for c, p in zip(cipher[:len(kb)], kb)])

def is_readable(text): # ASCII Characters
    return all(32 <= ord(c) <= 126 for c in text)

# ══════════════════════════════════════════════════════
#Main

cipher = parse(cipher)
print(f"[-] Cipher : {len(cipher)} bytes")

# Récupère la clé depuis le known plaintext
key = recover_key(cipher, KNOWN_PLAIN_TEXT)
print(f"[-] Key founded : {key}")

# Déchiffre le message
result = xor_decrypt(cipher, key)
print(f"[-] Result : {result}")

# ══════════════════════════════════════════════════════
# Option 1 :  If result is more than the key (weird string answer) : Missing bytes brute-force

# for combo in product(string.printable.encode(), repeat=ADD THE LENGTH ESTIMATED OF THE KEY LEFT (2 is like 2 bytes missing for example):
#     possible_key = key + bytes(combo)
#     decrypted = xor_decrypt(cipher, possible_key)
#     if is_readable(decrypted):
#         print(f"[-] Key : {possible_key}")
#         print(f"[-] Msg : {decrypted}")
#         break

# ══════════════════════════════════════════════════════
# Option 2 : If two messages has the same key : Multi-Time Pad. 


# cipher2 = parse(cipher2)
# xored = bytes([a ^ b for a, b in zip(cipher, cipher2)])
#
# for i in range(len(xored) - len(KNOWN_PLAIN_TEXT)):
#     fragment = bytes([xored[i+j] ^ ord(KNOWN_PLAIN_TEXT[j]) for j in range(len(KNOWN_PLAIN_TEXT))])
#     decoded = fragment.decode(errors='replace')
#     if is_readable(decoded):
#         print(f"Position {i:3d} → {decoded}")

# ══════════════════════════════════════════════════════
# Annexes : Decoding values based on their values :

# Binaire → bytes :
# cipher = bytes(int(cipher[i:i+8], 2) for i in range(0, len(cipher), 8))

# Decimal séparé par des virgules :
# cipher = bytes([int(x) for x in cipher.split(",")])

# Octal :
# cipher = bytes([int(x, 8) for x in cipher.split()])
