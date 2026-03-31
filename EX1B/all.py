import math
def euclidean_algorithm(a, b):
    print("\n--- Euclidean Algorithm (GCD) ---")
    print("Formula: gcd(a, b) = gcd(b, a mod b)\n")

    step = 1
    while b != 0:
        print(f"Step {step}:")
        print(f"gcd({a}, {b})")
        #print(f"{a} = {b} × {a // b} + {a % b}")
        print(f"gcd({b}, {a % b})\n")

        a, b = b, a % b
        step += 1

    print("Final Step:")
    print(f"gcd({a}, 0)")
    print(f"GCD = {a}")
def primality_test(n):
    print("\n--- Primality Testing ---")
    #print("Formula: n mod i ≠ 0 for all 2 ≤ i ≤ √n\n")

    if n <= 1:
        print(f"{n} is NOT a prime number")
        return

    step = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        print(f"Step {step}:")
        print(f"Check: {n} mod {i}")
        print(f"{n} mod {i} = {n % i}\n")

        if n % i == 0:
            print(f"{n} is NOT a prime number")
            return
        step += 1

    print(f"{n} is a PRIME number")

def main():
    print("Cryptography Algorithms")
    print("1. Euclidean Algorithm (GCD)")
    print("2. Primality Testing")

    choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        a = int(input("Enter first number (a): "))
        b = int(input("Enter second number (b): "))
        euclidean_algorithm(a, b)

    elif choice == 2:
        n = int(input("Enter a number (n): "))
        primality_test(n)

    else:
        print("Invalid choice!")


# Program execution starts here
main()
