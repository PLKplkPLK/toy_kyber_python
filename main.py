from timeit import timeit

import numpy as np
import matplotlib.pyplot as plt

import polynomial_algebra
from kyber import KyberPKE
from polynomial_algebra import PolynomialMatrix
from polynomial_multiplication_fft import multiply_polynomials


# np.random.seed(42)


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
    kyber = KyberPKE(n=1024, eta1=3)  # changing the eta can induce errors
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


def test_polynomial_multiplication_fft() -> None:
    pm1 = PolynomialMatrix(10, 1, 1, 10, 3)
    pm2 = PolynomialMatrix(10, 1, 1, 10, 3)
    result = PolynomialMatrix(10, 1, 1, 0, 3)
    print(pm1)
    print(pm2)

    result.matrix[0][0] = multiply_polynomials(
        pm1.matrix[0][0], pm2.matrix[0][0])
    print('FFT multiplication result:')
    print(result)


def run_kyber_pke() -> None:
    kyber = KyberPKE(n=1024, eta1=3)
    public_key, private_key = kyber.generate_keys()
    message = "Who's the monster?"
    encrypted_message = kyber.encrypt_message(message, public_key)
    kyber.decrypt_message(encrypted_message, private_key)


def check_times() -> None:
    polynomial_algebra.USE_DFT_INSTEAD_OF_CONVOLUTION = False
    t = timeit(run_kyber_pke, number=500)
    print('Convolution:')
    print(round(t, 3), "s")

    polynomial_algebra.USE_DFT_INSTEAD_OF_CONVOLUTION = True
    t = timeit(run_kyber_pke, number=500)
    print('FFT:')
    print(round(t, 3), "s")


def plot_times() -> None:
    runs = [1, 10, 50, 100, 200, 500]
    conv_times = np.array([])
    fft_times = np.array([])

    for n_runs in runs:
        polynomial_algebra.USE_DFT_INSTEAD_OF_CONVOLUTION = False
        conv_time = timeit(run_kyber_pke, number=n_runs)
        polynomial_algebra.USE_DFT_INSTEAD_OF_CONVOLUTION = True
        fft_time = timeit(run_kyber_pke, number=n_runs)

        conv_times = np.append(conv_times, conv_time)
        fft_times = np.append(fft_times, fft_time)

    plt.plot(runs, conv_times, label='Conv', marker='o')
    plt.plot(runs, fft_times, label='FFT', marker='o')
    plt.legend()
    plt.xlabel('Number of runs')
    plt.ylabel('Time [s]')
    plt.savefig('times.png')


if __name__ == '__main__':
    # demo_polynomial_matrices()
    # demo_kyber_pke()
    # test_operations()
    # test_polynomial_multiplication_fft()
    check_times()
    # plot_times()
