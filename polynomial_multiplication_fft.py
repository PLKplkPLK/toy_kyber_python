import numpy as np
from numpy.fft import fft, ifft


def multiply_polynomials(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    """Return polynomial result of multiplication of two polynomials."""

    if p1.shape != p2.shape:
        raise ValueError(
            "Polynomials must be the same degree (in this implementation xD)")
    
    # negacyclic multiplication trick
    coefficients_signs = np.array([(-1)**k for k in range(len(p1))])
    p1 = p1 * coefficients_signs
    p2 = p2 * coefficients_signs

    # fft, multiply, ifft
    fft1 = fft(p1)
    fft2 = fft(p2)
    multiplication_result = fft1 * fft2
    result = ifft(multiplication_result).real
    result = np.rint(result).astype(int)  # round because of values like 14.(9)
    result = result * coefficients_signs

    return result
