from polynomial_algebra import PolynomialMatrix


class KyberPKE():
    """Kyber PKE generation class."""

    def __init__(self, n: int = 256, q: int = 3329, k: int = 3, eta1: int = 3, eta2: int = 3) -> None:
        """Create Kyber idk.
        
        Parameters:
            n - degree of polynomials
            q - modulo q coefficients of matrices
            k - dimensions of matrices
            eta1 - max value of vector s (private key) coefficients
            eta2 - max value of vector e (errors) coefficients
        """
        public_key, private_key = self.generate_keys(n, q, k, eta1, eta2)
        self.public_key = public_key
        self.private_key = private_key

    @staticmethod
    def generate_keys(n: int, q: int, k: int, eta1: int, eta2: int) -> tuple[tuple, PolynomialMatrix]:
        """Generate public and private key.
        
        Returns tuple(public key: (A, t), private key: s)
        """
        
        A = PolynomialMatrix(q, k, k, n)
        s = PolynomialMatrix(eta1, k, polynomial_degree=n)
        e = PolynomialMatrix(eta2, k, polynomial_degree=n)
        t = (A * s) + e

        return (A, t), s
