from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- MANUAL AES-128 IMPLEMENTATION ---
SBOX = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0] # truncated for brevity, use full in prod

def aes_encrypt(block, key):
    # Simplified AES Round for demonstration of steps
    state = [b ^ k for b, k in zip(block, key)]
    # Step: SubBytes (Simplified)
    state = [SBOX[b % 32] for b in state] 
    return bytes(state)

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def bitwise_shift_left(data):
    int_val = int.from_bytes(data, 'big')
    res = (int_val << 1) & (2**128 - 1)
    return res.to_bytes(16, 'big')

# --- CMAC LOGIC ---
def run_cmac(key_hex, message_text):
    key = bytes.fromhex(key_hex).ljust(16, b'\x00')[:16]
    msg = message_text.encode()
    steps = []

    # 1. Subkey Generation
    L = aes_encrypt(b'\x00' * 16, key)
    steps.append(f"Step 1: L = AES_Encrypt(0^128) -> {L.hex()}")

    # Derive K1
    if (L[0] & 0x80) == 0:
        K1 = bitwise_shift_left(L)
        steps.append(f"Step 2: MSB of L is 0. K1 = L << 1 -> {K1.hex()}")
    else:
        K1 = xor_bytes(bitwise_shift_left(L), b'\x00'*15 + b'\x87')
        steps.append(f"Step 2: MSB of L is 1. K1 = (L << 1) XOR Rb -> {K1.hex()}")

    # Derive K2
    if (K1[0] & 0x80) == 0:
        K2 = bitwise_shift_left(K1)
        steps.append(f"Step 3: MSB of K1 is 0. K2 = K1 << 1 -> {K2.hex()}")
    else:
        K2 = xor_bytes(bitwise_shift_left(K1), b'\x00'*15 + b'\x87')
        steps.append(f"Step 3: MSB of K1 is 1. K2 = (K1 << 1) XOR Rb -> {K2.hex()}")

    # 2. Padding and XORing
    n = (len(msg) + 15) // 16
    if n == 0: n = 1
    
    is_complete = (len(msg) > 0 and len(msg) % 16 == 0)
    
    if is_complete:
        M_last = xor_bytes(msg[(n-1)*16:], K1)
        steps.append(f"Step 4: Message is block-aligned. XOR last block with K1.")
    else:
        # Padding: add 0x80 then 0x00s
        padding = b'\x80' + b'\x00' * (16 - (len(msg) % 16) - 1)
        target = msg[(n-1)*16:] + padding
        M_last = xor_bytes(target, K2)
        steps.append(f"Step 4: Message not aligned. Padded block: {(msg[(n-1)*16:] + padding).hex()}")
        steps.append(f"Step 5: XOR padded block with K2 -> {M_last.hex()}")

    # 3. Final Tag Generation
    tag = aes_encrypt(M_last, key)
    steps.append(f"Step 6: Final AES Encryption of XORed block -> {tag.hex()}")

    return tag.hex(), steps

@app.route('/')
def index(): return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    tag, steps = run_cmac(data['key'], data['msg'])
    return jsonify({"tag": tag, "steps": steps})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
