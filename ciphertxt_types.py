#%%
import numpy as np
def cyclic_poly_mul(A, B, N):
    product = np.polymul(A, B)
    # Reduce modulo x^N + 1
    product_N = np.pad(product[N:], (0, N - len(product[N:])))  # Pad with zeros to length N
    reduced = product[:N] - product_N
    return reduced

def glwe_encrypt(N, q, k, M, delta):
    # Create the secret key S as k polynomials of degree smaller than N
    # Each polynomial has N coefficients, uniformly distributed in {0, 1}
    S = [np.random.randint(0, 2, size=N) for _ in range(k)]

    # Create two polynomials A[0], A[1] with N random coefficients each
    A = [np.random.randint(-q/2, q/2, size=N) for _ in range(k)]

    # Create a discrete Gaussian error E with N coefficients
    E = np.round(np.random.normal(0, 0.5, size = N)).astype(int)  # Using a small sigma:0.5 for small values
    # Compute the body B = A0 * S0 + A1 * S1 + delta*M + E
    B = np.zeros(N, dtype=int)

    # Polynomial multiplication for A0 * S0 and A1 * S1 modulo x^N + 1 and q
    for i in range(k):
        product = cyclic_poly_mul(A[i], S[i], N)
        # Reduce modulo x^N + 1
        B = (B + product)

    # Add scaled message and error
    B = (B + delta * np.array(M)) # M: cleartext; delta * M: plaintext
    B = (B + E) 

    return B, A, S


# Decryption process
def glwe_decrypt(N, B, A, S, delta):
    # Initialize the result
    result = np.array(B)
    
    # Subtract A[i] * S[i] for each i
    for i in range(len(A)):
        product = cyclic_poly_mul(A[i], S[i], N)
        result = result - product
    
    # Divide by delta and round to nearest integer
    decrypted = np.round(result / delta).astype(int)
    
    return decrypted

def encrypt_n_decrypt_veri(M, N, k, q, delta):
    # Perform encryption
    B, A, S = glwe_encrypt(N, q, k, M, delta)

    # Perform decryption
    decrypted_message = glwe_decrypt(N, B, A, S, delta)

    # Compare M and decrypted_message
    print("Original message M:", M)
    print("Decrypted message:", decrypted_message)

    if np.array_equal(M, decrypted_message):
        print("Encryption and decryption worked correctly!")
    else:
        print("There's a mismatch between the original and decrypted messages.")
        print("Differences:", M - decrypted_message)
