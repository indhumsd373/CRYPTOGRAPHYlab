from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def sha256_manual(message):
    def rrot(n, b): return ((n >> b) | (n << (32 - b))) & 0xffffffff
    def shr(n, b): return n >> b

    # Constants and Initial Hash
    K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174]
    h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

    # Padding
    msg = bytearray(message, 'utf-8')
    length = (len(msg) * 8).to_bytes(8, 'big')
    msg.append(0x80)
    while (len(msg) * 8) % 512 != 448: msg.append(0x00)
    msg += length

    steps = [f"Padded Message: {msg.hex()[:100]}..."]

    # Simple processing of first block for demo
    for i in range(0, len(msg), 64):
        block = msg[i:i+64]
        w = [int.from_bytes(block[j:j+4], 'big') for j in range(0, 64, 4)]
        for j in range(16, 64):
            s0 = rrot(w[j-15], 7) ^ rrot(w[j-15], 18) ^ shr(w[j-15], 3)
            s1 = rrot(w[j-2], 17) ^ rrot(w[j-2], 19) ^ shr(w[j-2], 10)
            w.append((w[j-16] + s0 + w[j-7] + s1) & 0xffffffff)

        a, b, c, d, e, f, g, hh = h
        for j in range(64): # Showing first 8 rounds in logs
            S1 = rrot(e, 6) ^ rrot(e, 11) ^ rrot(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (hh + S1 + ch + (K[j%16]) + w[j]) & 0xffffffff
            S0 = rrot(a, 2) ^ rrot(a, 13) ^ rrot(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffff
            hh, g, f, e, d, c, b, a = g, f, e, (d + temp1) & 0xffffffff, c, b, a, (temp1 + temp2) & 0xffffffff
            if j < 8: steps.append(f"Round {j}: a={hex(a)}, e={hex(e)}")

        h = [(x + y) & 0xffffffff for x, y in zip(h, [a,b,c,d,e,f,g,hh])]
    
    return "".join(f"{x:08x}" for x in h), steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hash', methods=['POST'])
def generate_hash():
    data = request.json
    text = data.get("text", "")
    final_hash, steps = sha256_manual(text)
    return jsonify({"hash": final_hash, "steps": steps})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
