import numpy as np

from kyber import KyberPKE
from polynomial_algebra import PolynomialMatrix


np.random.seed(42)


def demo_polynomial_matrices() -> None:
    """Show how the PolynomialMatrix class works."""
    pm1 = PolynomialMatrix(10, 2, 2, 2)
    pm2 = PolynomialMatrix(10, 2, 2, 2)
    print(pm1)
    print(pm2)

    pm_added = pm1 + pm2
    print('Added matrices of polynomials:')
    print(pm_added)

    pm_multiplied = pm1 * pm2
    print('Multiplied matrices of polynomials:')
    print(pm_multiplied)


def demo_kyber_pke() -> None:
    """Show how KyberPKE class works."""
    kyber = KyberPKE(n=4)
    print('Public key:')
    print(kyber.public_key)
    print('Private key:')
    print(kyber.private_key)


if __name__ == '__main__':
    #demo_polynomial_matrices()
    demo_kyber_pke()
