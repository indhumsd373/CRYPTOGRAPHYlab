class Solution:
    def countPrimes(self, n: int) -> int:
        # Primes strictly less than n means we return 0 for n < 3
        if n < 3:
            return 0
        
        # Create a boolean array representing whether a number is prime
        # Initially, assume all numbers are prime (True)
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False # 0 and 1 are not prime
        
        # Sieve logic
        for i in range(2, int(n**0.5) + 1):
            if is_prime[i]:
                # Mark all multiples of i starting from i*i as not prime
                # Stepping by i effectively hits all multiples
                for multiple in range(i * i, n, i):
                    is_prime[multiple] = False
        
        # Return the count of True values in the array
        return sum(is_prime)
