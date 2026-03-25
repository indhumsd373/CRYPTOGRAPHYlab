from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Function to find modular inverse
def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/calculate', methods=['POST'])
def calculate():

    p = int(request.form['p'])
    q = int(request.form['q'])
    message = int(request.form['message'])

    # Step 1: compute n
    n = p * q

    # Step 2: compute phi
    phi = (p - 1) * (q - 1)

    # Step 3: choose e
    e = 2
    while e < phi:
        if math.gcd(e, phi) == 1:
            break
        e += 1

    # Step 4: compute d
    d = mod_inverse(e, phi)

    # Step 5: encryption
    c = pow(message, e, n)

    # Step 6: decryption
    m = pow(c, d, n)

    steps = [
        "STEP 1: Choose prime numbers",
        f"p = {p}",
        f"q = {q}",

        "",

        "STEP 2: Compute n",
        "n = p × q",
        f"n = {p} × {q} = {n}",

        "",

        "STEP 3: Compute Euler Totient",
        "φ(n) = (p − 1)(q − 1)",
        f"φ(n) = ({p}-1) × ({q}-1) = {phi}",

        "",

        "STEP 4: Choose public exponent e",
        f"e = {e}",

        "",

        "STEP 5: Compute private key d",
        "d × e mod φ(n) = 1",
        f"d = {d}",

        "",

        f"Public Key = ({e}, {n})",
        f"Private Key = ({d}, {n})",

        "",

        "STEP 6: Encryption",
        "C = M^e mod n",
        f"C = {message}^{e} mod {n} = {c}",

        "",

        "STEP 7: Decryption",
        "M = C^d mod n",
        f"M = {c}^{d} mod {n} = {m}",

        "",

        f"Final Decrypted Message = {m}"
    ]

    return render_template("index.html", steps=steps)


if __name__ == "__main__":
    app.run(debug=True)
