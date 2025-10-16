from polynomial_algebra import PolynomialMatrix


class KyberPKE():
    """Kyber PKE class.
    
    Example usage:
        kyber_object = KyberPKE()
        public, private = kyber_object.generate_keys()
        encrypted_message = kyber_object.encrypt_message("secret", public)
        decrypted_message = kyber_object.decrypt_message(encrypted_message, private)
    """

    def __init__(self, n: int = 256, q: int = 3329, k: int = 3, eta1: int = 2, eta2: int = 2) -> None:
        """Create KyberPKE object to use generate_keys, encrypt_message, decrypt_message methods.
        
        Think of this object as an implementation of Kyber.
        The default parameters are ML-KEM-768 implementation.

        Parameters:
            n - degree of polynomials
            q - modulo q coefficients of matrices
            k - dimensions of matrices
            eta1 - max value of vector s (private key) coefficients
            eta2 - max value of vector e (errors) coefficients
        """
        self.n = n
        self.q = q
        self.k = k
        self.eta1 = eta1
        self.eta2 = eta2

    def generate_keys(self) -> tuple[tuple[PolynomialMatrix, PolynomialMatrix], PolynomialMatrix]:
        """Generate public and private key.
        
        Returns public key: (A, s) and private key: s.
        """
        
        A = PolynomialMatrix(self.q, self.k, self.k, self.n)
        s = PolynomialMatrix(self.eta1, self.k, 1, self.n, include_negative=True)
        e = PolynomialMatrix(self.eta2, self.k, 1, self.n, include_negative=True)
        t = (A * s) + e

        return (A, t), s

    def encrypt_message(self, message: str, public_key: 
                        tuple[PolynomialMatrix, PolynomialMatrix]) -> tuple[PolynomialMatrix, PolynomialMatrix]:
        """Encrypt the message, given public key as (A, t).
        
        Returns encrypted message as a tuple of vector u and polynomial v."""

        A = public_key[0]
        t = public_key[1]

        r = PolynomialMatrix(self.eta1, self.k, polynomial_degree=self.n, include_negative=True)
        e1 = PolynomialMatrix(self.eta2, self.k, polynomial_degree=self.n, include_negative=True)
        e2 = PolynomialMatrix(self.eta2, 1, 1, polynomial_degree=self.n, include_negative=True)

        # scaling replaces all the "1" coefficients with q/2 and leaves 0 coefficients
        scaling_factor = round(self.q / 2)
        polynomial_message = self._transform_message_to_polynomial(message, scaling_factor)

        u = A.T * r + e1
        v = t.T * r + e2 + polynomial_message
        return u, v

    def decrypt_message(self, encrypted_message: tuple[PolynomialMatrix, PolynomialMatrix],
                        private_key: PolynomialMatrix) -> str:
        """Decrypt message, return string."""
        u, v = encrypted_message
        message_polynomial = v - (private_key.T * u)
        # print('message poly and binary:')
        # print(message_polynomial)
        message_binary = self._transform_polynomial_to_binary_string(message_polynomial)
        # print(message_binary)
        message = self._transform_binary_string_to_text(message_binary)
        return message

    def _transform_message_to_polynomial(self, message: str, scaling_factor: int) -> "PolynomialMatrix":
        """Transform message from string to PolynomialMatrix object."""
        binary_message = self._transform_message_to_binary(message)
        # print('message before encyption')
        # print(binary_message)
        polynomial_message = PolynomialMatrix(self.q, 1, 1, self.n)
        polynomial_message.matrix[0][0] = [scaling_factor * int(c) for c in binary_message]
        #print(polynomial_message)
        return polynomial_message

    def _transform_message_to_binary(self, message: str) -> str:
        """Transform message to binary form and take only the first n characters."""
        # If n=256 is used, you can encrypt 256 bytes
        n_characters = self.n
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        return binary_message[:n_characters+1]

    def _transform_polynomial_to_binary_string(self, poly_message: PolynomialMatrix) -> str:
        """Transform decrypted message polynomial to a string, binary representation."""
        coefficients = poly_message.matrix[0][0]
        rounded_coefficients = list(map(self._rounding, coefficients))
        return ''.join([str(b) for b in rounded_coefficients])

    def _rounding(self, x: int) -> int:
        """Perform Kyber rounding on a number (using saved q)."""
        return 0 if -self.q/4 < x < self.q/4 else 1

    @staticmethod
    def _transform_binary_string_to_text(binary_string: str) -> str:
        """Transform binary string ("100101") to text."""
        return ''.join(chr(int(binary_string[i*8:i*8+8],2)) for i in range(len(binary_string)//8))
