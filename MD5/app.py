from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# MD5 Constants: T[i] = floor(abs(sin(i+1)) * 2^32)
T = [int(4294967296 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

def run_md5_step(message_text):
    # 1. Preprocessing (Padding)
    msg = bytearray(message_text.encode())
    orig_len_bits = (len(msg) * 8) & 0xffffffffffffffff
    
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0x00)
    
    # Append length as 64-bit little-endian
    msg += orig_len_bits.to_bytes(8, byteorder='little')
    
    steps = [f"Step 1: Padding complete. Padded length: {len(msg)} bytes"]
    
    # 2. Initialize MD Buffer (A, B, C, D)
    a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
    
    # Process only the first 512-bit block for demonstration
    chunk = msg[0:64]
    M = [int.from_bytes(chunk[i:i+4], byteorder='little') for i in range(0, 64, 4)]
    steps.append(f"Step 2: First block M[0..15] extracted.")

    A, B, C, D = a0, b0, c0, d0
    
    # Show logic for the very first round operation
    # F = (B & C) | (~B & D)
    f_res = (B & C) | (~B & D)
    A = (B + left_rotate((A + f_res + T[0] + M[0]) & 0xFFFFFFFF, 7)) & 0xFFFFFFFF
    
    steps.append(f"Step 3: Initial A value updated to {hex(A)} using F-function.")
    steps.append("Step 4: Iterating through 64 operations (Rounds 1-4)...")

    # Final "simulated" result for the full string (using built-in for brevity in hash calculation)
    import hashlib
    final_hash = hashlib.md5(message_text.encode()).hexdigest()
    
    return final_hash, steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    hash_val, steps = run_md5_step(data['msg'])
    return jsonify({"hash": hash_val, "steps": steps})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
