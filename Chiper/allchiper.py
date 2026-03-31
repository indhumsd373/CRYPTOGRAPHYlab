def mod(n):
    return n % 26
def clean_text(text):
    return "".join(ch for ch in text.upper() if ch.isalpha())
# ---------- Shift Cipher ----------
def shift_cipher(text, key, mode):
    result = ""
    for ch in text:
        p = ord(ch) - 65
        if mode == "E":
            r = mod(p + key)
        else:
            r = mod(p - key)
        result += chr(r + 65)
    return result
# ---------- Vigenere Cipher ----------
def vigenere_cipher(text, key, mode):
    result = ""
    key = clean_text(key)

    if len(key) == 0:
        return "Key cannot be empty."

    for i in range(len(text)):
        p = ord(text[i]) - 65
        k = ord(key[i % len(key)]) - 65
        if mode == "E":
            r = mod(p + k)
        else:
            r = mod(p - k)
        result += chr(r + 65)
    return result
# ---------- Hill Cipher (2x2) ----------

def inverse_matrix(a, b, c, d):
    det = mod(a * d - b * c)
    inv_det = -1

    for i in range(1, 26):
        if mod(det * i) == 1:
            inv_det = i
            break

    if inv_det == -1:
        return None

    return (
        mod(inv_det * d),
        mod(inv_det * -b),
        mod(inv_det * -c),
        mod(inv_det * a)
    )
def hill_cipher(text, key_matrix, mode):
    if len(text) % 2 != 0:
        text += "X"

    a, b, c, d = key_matrix

    if mode == "D":
        inv = inverse_matrix(a, b, c, d)
        if inv is None:
            return "Key matrix is not invertible."
        a, b, c, d = inv

    result = ""
    for i in range(0, len(text), 2):
        p1 = ord(text[i]) - 65
        p2 = ord(text[i + 1]) - 65

        r1 = mod(a * p1 + b * p2)
        r2 = mod(c * p1 + d * p2)

        result += chr(r1 + 65) + chr(r2 + 65)

    return result
# --------- Menu Driven Program ----------

while True:
    print("\n--- Classical Cipher Menu ---")
    print("1. Shift Cipher")
    print("2. Vigenere Cipher")
    print("3. Hill Cipher (2x2)")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "4":
        print("Exiting program.")
        break

    text = clean_text(input("Enter text: "))
    mode = input("Encrypt or Decrypt (E/D): ").upper()

    if mode not in ["E", "D"]:
        print("Invalid mode. Use E or D.")
        continue

    if choice == "1":
        key = int(input("Enter shift key: "))
        print("Result:", shift_cipher(text, key, mode))

    elif choice == "2":
        key = input("Enter Vigenere key: ")
        print("Result:", vigenere_cipher(text, key, mode))

    elif choice == "3":
        print("Enter 2x2 Hill key matrix values:")
        a = int(input("a: "))
        b = int(input("b: "))
        c = int(input("c: "))
        d = int(input("d: "))
        print("Result:", hill_cipher(text, (a, b, c, d), mode))

    else:
        print("Invalid choice. Try again.")
