from flask import Flask, render_template, request

app = Flask(__name__)

# AES S-Box
sbox = [
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15
]

rcon = [0x01, 0x02]

def rot_word(word):
    return word[1:] + word[:1]

def sub_word(word):
    return [sbox[b % len(sbox)] for b in word]

def to_hex(word):
    return " ".join([format(b, '02X') for b in word])

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():

    key_hex = request.form['key']

    key = list(bytes.fromhex(key_hex))

    w0 = key[0:4]
    w1 = key[4:8]
    w2 = key[8:12]
    w3 = key[12:16]

    steps = []

    steps.append("Initial Words")
    steps.append(f"W0 = {to_hex(w0)}")
    steps.append(f"W1 = {to_hex(w1)}")
    steps.append(f"W2 = {to_hex(w2)}")
    steps.append(f"W3 = {to_hex(w3)}")

    # ROUND 1
    steps.append("")
    steps.append("ROUND 1")

    temp = rot_word(w3)
    steps.append(f"RotWord(W3) = {to_hex(temp)}")

    temp = sub_word(temp)
    steps.append(f"SubWord = {to_hex(temp)}")

    temp[0] ^= rcon[0]
    steps.append(f"Rcon XOR = {to_hex(temp)}")

    w4 = [a ^ b for a,b in zip(w0,temp)]
    w5 = [a ^ b for a,b in zip(w1,w4)]
    w6 = [a ^ b for a,b in zip(w2,w5)]
    w7 = [a ^ b for a,b in zip(w3,w6)]

    steps.append(f"W4 = {to_hex(w4)}")
    steps.append(f"W5 = {to_hex(w5)}")
    steps.append(f"W6 = {to_hex(w6)}")
    steps.append(f"W7 = {to_hex(w7)}")

    # ROUND 2
    steps.append("")
    steps.append("ROUND 2")

    temp = rot_word(w7)
    steps.append(f"RotWord(W7) = {to_hex(temp)}")

    temp = sub_word(temp)
    steps.append(f"SubWord = {to_hex(temp)}")

    temp[0] ^= rcon[1]
    steps.append(f"Rcon XOR = {to_hex(temp)}")

    w8 = [a ^ b for a,b in zip(w4,temp)]
    w9 = [a ^ b for a,b in zip(w5,w8)]
    w10 = [a ^ b for a,b in zip(w6,w9)]
    w11 = [a ^ b for a,b in zip(w7,w10)]

    steps.append(f"W8 = {to_hex(w8)}")
    steps.append(f"W9 = {to_hex(w9)}")
    steps.append(f"W10 = {to_hex(w10)}")
    steps.append(f"W11 = {to_hex(w11)}")

    return render_template("index.html", steps=steps)

if __name__ == "__main__":
    app.run(debug=True)