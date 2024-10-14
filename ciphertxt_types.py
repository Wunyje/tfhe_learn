#%%
import numpy as np

def glwe_encrypt(M, S, A, E):
    # Compute the body B = A0 * S0 + A1 * S1 + delta*M + E
    B = np.zeros(N, dtype=int)

    # Polynomial multiplication for A0 * S0 and A1 * S1 modulo x^N + 1 and q
    for i in range(k):
        product = np.polymul(A[i], S[i])
        # Reduce modulo x^N + 1
        product_N = np.pad(product[N:], (0, N - len(product[N:])))  # Pad with zeros to length N
        reduced = product[:N] - product_N
        B = (B + reduced)

    # Add scaled message and error
    B = (B + delta * np.array(M))
    B = (B + E) 

    return B


# Decryption process
def glwe_decrypt(B, A, S, delta):
    # Initialize the result
    result = np.array(B)
    
    # Subtract A[i] * S[i] for each i
    for i in range(len(A)):
        product = np.polymul(A[i], S[i])
        # Reduce modulo x^N + 1
        product_N = np.pad(product[N:], (0, N - len(product[N:])))
        reduced = product[:N] - product_N
        result = result - reduced
    
    # Divide by delta and round to nearest integer
    decrypted = np.round(result / delta).astype(int)
    
    return decrypted



# GLWE ciphertext parameters
q = 64  # cipher text modulus
p = 4   # plaintext modulus
delta = int(q/p)  # scaling factor
# when instantiate GLWE with k = n, N = 1, get LWE
# when instantiate GLWE with k = 1 and N = 2**m, get RLWE
N = 4  # the degree of M (message)'s polynomial
k = 2  # the number of secret key's polynomials. k < N

# Original message polynomial with N coefficients under modulo 64
M = np.random.randint(-32, 32, size=N)

# Create the secret key S as k polynomials of degree smaller than N
# Each polynomial has N coefficients, uniformly distributed in {0, 1}
S = [np.random.randint(0, 2, size=N) for _ in range(k)]

# Create two polynomials A[0], A[1] with N random coefficients each
A = [np.random.randint(-32, 32, size=N) for _ in range(k)]

# Create a discrete Gaussian error E with N coefficients
E = np.round(np.random.normal(0, 0.5, size = N)).astype(int)  # Using a small sigma:0.5 for small values
print("E:", E)

# Perform encryption
B = glwe_encrypt(M, S, A, E)

# Perform decryption
decrypted_message = glwe_decrypt(B, A, S, delta)

# Compare M and decrypted_message
print("Original message M:", M)
print("Decrypted message:", decrypted_message)

if np.array_equal(M, decrypted_message):
    print("Encryption and decryption worked correctly!")
else:
    print("There's a mismatch between the original and decrypted messages.")
    print("Differences:", M - decrypted_message)


# # Ensure the result is within the ciphertext modulus q
# B = B % q

pass
