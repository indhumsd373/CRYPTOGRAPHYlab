from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():

    p = int(request.form['p'])
    g = int(request.form['g'])
    a = int(request.form['a'])
    b = int(request.form['b'])

    # Step 1: Public keys
    A = pow(g, a, p)
    B = pow(g, b, p)

    # Step 2: Shared secret
    KA = pow(B, a, p)
    KB = pow(A, b, p)

    steps = [
        f"Public Prime (p) = {p}",
        f"Generator (g) = {g}",
        "",
        "Step 1: Alice chooses private key a",
        f"a = {a}",
        "",
        "Step 2: Bob chooses private key b",
        f"b = {b}",
        "",
        "Step 3: Alice computes public key",
        f"A = g^a mod p",
        f"A = {g}^{a} mod {p} = {A}",
        "",
        "Step 4: Bob computes public key",
        f"B = g^b mod p",
        f"B = {g}^{b} mod {p} = {B}",
        "",
        "Step 5: Exchange public keys",
        "Alice sends A to Bob",
        "Bob sends B to Alice",
        "",
        "Step 6: Compute shared secret",
        f"Alice: K = B^a mod p = {B}^{a} mod {p} = {KA}",
        f"Bob:   K = A^b mod p = {A}^{b} mod {p} = {KB}",
        "",
        f"Final Shared Secret Key = {KA}"
    ]

    return render_template("index.html", steps=steps)

if __name__ == "__main__":
    app.run(debug=True)
