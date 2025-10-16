import numpy as np

from kyber import KyberPKE
from polynomial_algebra import PolynomialMatrix


np.random.seed(42)


def demo_polynomial_matrices() -> None:
    """Show how the PolynomialMatrix class works."""
    pm1 = PolynomialMatrix(10, 2, 2, 10, 3)
    pm2 = PolynomialMatrix(10, 2, 2, 10, 3)
    print(pm1)
    print(pm2)

    pm_added = pm1 + pm2
    print('Added matrices of polynomials:')
    print(pm_added)

    pm_added_number = pm1 + 3
    print("Added number to polynomials:")
    print(pm_added_number)

    pm_multiplied = pm1 * pm2
    print('Multiplied matrices of polynomials:')
    print(pm_multiplied)

    print("Transposing:")
    pmt = pm1.T
    print(pm1)
    print(" \\/ \\/ \\/ \\/ \\/ ")
    print(pmt)


def demo_kyber_pke() -> None:
    """Show how KyberPKE class works."""

    # Alice
    kyber = KyberPKE(n=256)
    public_key, private_key = kyber.generate_keys()
    print('Public key:')
    print(public_key)
    print('Private key:')
    print(private_key)

    # Bob
    message = "Who's the monster?"
    # the message in binary can be have as many bits as
    # degree of polynomials (which is parameter "n") + 1
    encrypted_message = kyber.encrypt_message(message, public_key)
    print('Encrypted message:')
    print(encrypted_message)

    # Alice
    decrypted_message = kyber.decrypt_message(encrypted_message, private_key)
    print('Decrypted message:')
    print(decrypted_message)


def test_operations() -> None:
    kyber = KyberPKE(n=10)
    public_key, private_key = kyber.generate_keys()
    A, t = public_key
    s = private_key
    print((A * s) - t)


if __name__ == '__main__':
    # demo_polynomial_matrices()
    demo_kyber_pke()
    # test_operations()
