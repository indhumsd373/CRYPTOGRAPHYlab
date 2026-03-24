from flask import Flask, render_template, request

app = Flask(__name__)

P10 = [3,5,2,7,4,10,1,9,8,6]
P8  = [6,3,7,4,8,5,10,9]

IP = [2,6,3,1,4,8,5,7]
IP_INV = [4,1,3,5,7,2,8,6]

EP = [4,1,2,3,2,3,4,1]
P4 = [2,4,3,1]

S0 = [
[1,0,3,2],
[3,2,1,0],
[0,2,1,3],
[3,1,3,2]
]

S1 = [
[0,1,2,3],
[2,0,1,3],
[3,0,1,0],
[2,1,0,3]
]


def permute(bits, table):
    return ''.join(bits[i-1] for i in table)

def left_shift(bits):
    return bits[1:] + bits[0]

def xor(a,b):
    return ''.join('0' if i==j else '1' for i,j in zip(a,b))

def sbox(bits, box):
    row = int(bits[0] + bits[3],2)
    col = int(bits[1] + bits[2],2)
    return format(box[row][col],'02b')


def generate_keys(key,steps):

    p10 = permute(key,P10)
    steps.append("P10 : "+p10)

    left = p10[:5]
    right = p10[5:]

    left = left_shift(left)
    right = left_shift(right)

    k1 = permute(left+right,P8)
    steps.append("K1 : "+k1)

    left = left_shift(left)
    left = left_shift(left)

    right = left_shift(right)
    right = left_shift(right)

    k2 = permute(left+right,P8)
    steps.append("K2 : "+k2)

    return k1,k2


def f_function(bits,key,steps):

    L = bits[:4]
    R = bits[4:]

    steps.append("L : "+L)
    steps.append("R : "+R)

    ep = permute(R,EP)
    steps.append("EP : "+ep)

    x = xor(ep,key)
    steps.append("XOR : "+x)

    left = x[:4]
    right = x[4:]

    s0 = sbox(left,S0)
    s1 = sbox(right,S1)

    steps.append("S0 : "+s0)
    steps.append("S1 : "+s1)

    p4 = permute(s0+s1,P4)
    steps.append("P4 : "+p4)

    newL = xor(L,p4)

    return newL + R


def encrypt(pt,key):

    steps = []

    k1,k2 = generate_keys(key,steps)

    ip = permute(pt,IP)
    steps.append("IP : "+ip)

    r1 = f_function(ip,k1,steps)

    swap = r1[4:] + r1[:4]
    steps.append("SWAP : "+swap)

    r2 = f_function(swap,k2,steps)

    cipher = permute(r2,IP_INV)

    steps.append("CIPHERTEXT : "+cipher)

    return steps


@app.route('/',methods=['GET','POST'])
def index():

    steps=[]
    error=""

    if request.method == 'POST':

        plaintext = request.form['plaintext']
        key = request.form['key']

        if len(plaintext)!=8 or len(key)!=10:
            error="Plaintext must be 8 bits and key must be 10 bits"
        else:
            steps = encrypt(plaintext,key)

    return render_template("index.html",steps=steps,error=error)


if __name__ == "__main__":
    app.run(debug=True)