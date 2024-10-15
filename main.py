import numpy as np
from ciphertxt_types import *

if __name__ == '__main__':
    # GLWE ciphertext parameters
    q = 64  # cipher text modulus
    p = 4   # plaintext modulus
    delta = int(q/p)  # scaling factor, lift the message to MSB
    # when instantiate GLWE with k = n, N = 1, get LWE
    # when instantiate GLWE with k = 1 and N = 2**m, get RLWE
    N = 4  # the degree of M (message)'s polynomial
    k = 2  # the number of secret key's polynomials. k < N
    # Original message polynomial with N coefficients under modulo 64, modular reductions are centered around zero
    M = np.random.randint(-q/2, q/2, size=N)

    # Call the function with the given parameters
    encrypt_n_decrypt_veri(M, N, k, q, delta)

    # homomorphic multiplication verification
    M_1 = np.random.randint(-q/2, q/2, size=N)
    lambda_1 = [-1, 0, 2, 3]
    M_1_mul_lambda_1 = cyclic_poly_mul(M_1, lambda_1, N)

    B_1, A_1, S_1 = glwe_encrypt(N, q, k, M_1, delta)
    B_1_mul_lambda_1 = cyclic_poly_mul(B_1, lambda_1, N)
    A_1_mul_lambda_1 = [[0] * N] * k
    for i in range(k):
        A_1_mul_lambda_1[i] = cyclic_poly_mul(A_1[i], lambda_1, N)
    dec_M_1_mul_lambda_1 = glwe_decrypt(N, B_1_mul_lambda_1, A_1_mul_lambda_1, S_1, delta)
    if np.array_equal(M_1_mul_lambda_1, dec_M_1_mul_lambda_1):
        print("Encryption and decryption worked correctly!")
    else:
        print("There's a mismatch between the original and decrypted messages.")
        print("Differences:", M_1_mul_lambda_1 - dec_M_1_mul_lambda_1)
    pass