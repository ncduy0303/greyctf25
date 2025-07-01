from sage.all import *
import json

data = json.load(open('dist-meow-log-meow-log-meow-e/chall.json'))
n, e, c1, c2, po = data['n'], data['e'], data['c1'], data['c2'], data['po']

def e_power(x, field, terms):
    """
    Compute e^x in a finite field using Taylor series approximation.
    
    Args:
        x: element in the finite field
        field: the finite field (e.g., GF(p) or GF(p^n))
        terms: number of Taylor series terms to compute
    
    Returns:
        approximation of e^x in the finite field as 1 + x + x^2/2! + x^3/3! + ... + x^(terms-1)/(terms-1)!
    """
    result = field(1)  # Start with e^0 = 1
    x_power = field(1)  # x^0 = 1
    factorial = 1
    
    for n in range(1, terms):
        x_power *= x  # x^n
        factorial *= n  # n!
        
        # In finite fields, we need the multiplicative inverse of factorial
        try:
            factorial_inv = field(factorial)^(-1)
            term = x_power * factorial_inv
            result += term
        except ZeroDivisionError:
            # If factorial is not invertible (divisible by char(field)), skip this term
            continue
    
    return result

from tqdm import tqdm

def naive_gcd(a, b, *, show_progress=True):
    """
    Compute the GCD of two polynomials using the naive method,
    optionally showing a tqdm progress bar.
    """
    if show_progress:
        # estimate total as degree of the smaller polynomial
        total = min(a.degree(), b.degree())
        pbar = tqdm(total=total, desc="GCD steps", unit="step")
    try:
        while b != 0:
            a, b = b, a % b
            if show_progress:
                pbar.update(1)
        return a
    finally:
        if show_progress:
            pbar.close()

# Convert to polynomial ring
F = Zmod(n)
R.<x> = PolynomialRing(F)

# Create polynomials from the ciphertexts
a0 = x^e - c1
a1 = e_power(x, F, po)^e - c2

# Compute the GCD
gcd = naive_gcd(a0, a1)
gcd = gcd.monic()

print(gcd)
assert gcd.degree() == 1, "GCD is not linear"
if gcd.degree() == 1:
    print(f"Found monic linear polynomial at degree {po}: {gcd[0]}")
    m = int(-gcd[0] % n)
    print(f"Message (m): {long_to_bytes(m)}")
