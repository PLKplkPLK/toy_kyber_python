import numpy as np


class PolynomialMatrix():
    """Matrices of polynomials over Z_mod[x]/(x^n + 1)."""

    def __init__(self, q: int, n_rows: int, n_cols: int,
                 max_coefficient_value: int, polynomial_degree: int,
                 include_negative: bool = False):
        """Initialize m x n polynomial matrix Z_mod[x]/(x^n + 1).

        The coefficients are random (uniform distr.) [0, max_coef_value),
        or [-max_coef_value, max_coef_value] if include_negative is True.
        """
        self.q = q
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.max_coefficient_value = max_coefficient_value
        self.n = polynomial_degree

        if max_coefficient_value == 0:
            self.matrix = np.zeros((n_rows, n_cols, polynomial_degree))
        elif include_negative:
            self.matrix = np.random.randint(
                -max_coefficient_value, max_coefficient_value+1,
                (n_rows, n_cols, polynomial_degree))
        else:
            self.matrix = np.random.randint(
                0, max_coefficient_value, (n_rows, n_cols, polynomial_degree))

    def __repr__(self) -> str:
        """Print matrix of polynomials."""
        rows_repr = []
        for i in range(self.n_rows):
            row_polys = []
            for j in range(self.n_cols):
                coefs = self.matrix[i, j]
                poly_terms = []
                for power, coef in enumerate(coefs):
                    if power == 0:
                        poly_terms.append(f"{coef}")
                    elif power == 1:
                        poly_terms.append(f"{coef}x")
                    else:
                        poly_terms.append(f"{coef}x^{power}")
                poly_str = " + ".join(poly_terms) if poly_terms else "0"
                row_polys.append(poly_str)
            rows_repr.append("\t".join(row_polys))
        matrix_str = "\n".join(rows_repr)

        return f"PolynomialMatrix {self.n_rows}x{self.n_cols}:\n{matrix_str}"

    def copy(self) -> "PolynomialMatrix":
        """Copy the structure of PolynomialMatrix (with polynomial
        coefficients = 0)
        """
        return PolynomialMatrix(self.q, self.n_rows, self.n_cols, 0, self.n)

    def __add__(self, other: "PolynomialMatrix | int") -> "PolynomialMatrix":
        """If adding PolynomialMatrix: sum coefficients of polynomials
        (modulo q), if it's int: add a number to the bias of polynomials.
        """
        if isinstance(other, PolynomialMatrix):
            if self.n_rows != other.n_rows or self.n_cols != other.n_cols:
                raise ValueError("Matrix dimensions don't match.")

            A = self.matrix
            B = other.matrix

            # If polynomials degrees don't match, add padding to the smaller
            if A.shape[2] < B.shape[2]:
                A = np.pad(A, ((0, 0), (0, 0), (0, B.shape[2] - A.shape[2])),
                           mode='constant')
            elif A.shape[2] > B.shape[2]:
                B = np.pad(B, ((0, 0), (0, 0), (0, A.shape[2] - B.shape[2])),
                           mode='constant')
            values = (A + B) % self.q
        elif isinstance(other, int):
            values = self.matrix.copy()
            values[:, :, 0] = (self.matrix[:, :, 0] + other) % self.q
        else:
            raise TypeError("Unsupported operand type for + in "
                            "PolynomialMatrix. Only PolynomialMatrix"
                            "and int allowed.")

        result_pm = self.copy()
        result_pm.matrix = values
        return result_pm

    def __sub__(self, other: "PolynomialMatrix") -> "PolynomialMatrix":
        """Subtract two polynomial matrices."""
        if self.n_rows != other.n_rows or self.n_cols != other.n_cols:
            raise ValueError("Matrix dimensions don't match.")
        A = self.matrix
        B = other.matrix
        # if polynomials degrees don't match, add padding to the smaller
        if A.shape[2] < B.shape[2]:
            A = np.pad(A, ((0, 0), (0, 0), (0, B.shape[2] - A.shape[2])),
                       mode='constant')
        elif A.shape[2] > B.shape[2]:
            B = np.pad(B, ((0, 0), (0, 0), (0, A.shape[2] - B.shape[2])),
                       mode='constant')

        values = (A - B) % self.q
        result_pm = self.copy()
        result_pm.matrix = values
        return result_pm

    def __mul__(self, other: "PolynomialMatrix") -> "PolynomialMatrix":
        """Multiply matrices.

        Performs negacyclic convolution: coefficients with index >= n are
        folded into idx - n with a sign flip (x^n = -1).
        """
        if self.n_cols != other.n_rows:
            raise ValueError("Matrix dimensions don't match.")

        n = self.n
        values = np.zeros((self.n_rows, other.n_cols, n))

        for r in range(self.n_rows):
            for c in range(other.n_cols):
                # accumulate in a temp int64 array
                acc = np.zeros(n, dtype=np.int64)
                for m in range(self.n_cols):
                    a = self.matrix[r, m].astype(int)
                    b = other.matrix[m, c].astype(int)
                    # so cool that the polynomial multiplication is convolution
                    conv = np.convolve(a, b).astype(int)
                    # zamaist convolution można zrobić DCT, przemnożenie tych współczynników i potem odwrotna DCT
                    # fold using negacyclic rule
                    for idx, coef in enumerate(conv):
                        if idx < n:
                            acc[idx] = (acc[idx] + coef) % self.q
                        else:
                            # fold: x^{n + t} -> - x^t
                            t = idx - n
                            acc[t] = (acc[t] - coef) % self.q
                values[r, c] = acc % self.q

        result_pm = PolynomialMatrix(self.q, self.n_rows,
                                     other.n_cols, 0, self.n)
        result_pm.matrix = values
        return result_pm

    @property
    def T(self) -> "PolynomialMatrix":
        """Transpose polynomials matrix."""
        pm_transposed = PolynomialMatrix(self.q, self.n_cols,
                                         self.n_rows, 0, self.n)
        pm_transposed.matrix = np.transpose(self.matrix, (1, 0, 2))
        return pm_transposed
