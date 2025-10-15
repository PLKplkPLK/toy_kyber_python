import numpy as np

class PolynomialMatrix():
    """Matrices and vectors of polynomials."""
    def __init__(self, max_coef_value: int, n_rows: int, n_cols: int = 1, polynomial_degree: int = 256):
        """Initialize m x n polynomial matrix (or vector if n_cols=1) with polynomials with random (uniform distr.) coeficcients [0, q)."""
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.max_coef_value = max_coef_value
        self.polynomial_degree = polynomial_degree

        self.matrix = np.random.randint(0, max_coef_value, (n_rows, n_cols, polynomial_degree + 1))

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


    def __add__(self, other: "PolynomialMatrix") -> "PolynomialMatrix":
        """Add coefficients of polynomials (modulo max_coef_value)."""
        if self.n_rows != other.n_rows or self.n_cols != other.n_cols:
            raise ValueError("Matrix dimensions don't match.")
        
        values = (self.matrix + other.matrix) % self.max_coef_value
        result_pm = PolynomialMatrix(self.max_coef_value, self.n_cols, self.n_cols, self.polynomial_degree)
        result_pm.matrix = values

        return result_pm
    
    def __mul__(self, other: "PolynomialMatrix") -> "PolynomialMatrix":
        """Multiply matrices: coefficients and degrees of polynomials must be included."""
        if self.n_cols != other.n_rows:
            raise ValueError("Matrix dimensions don't match.")
        
        values = np.zeros((self.n_rows, other.n_cols, self.polynomial_degree + 1))
        for result_row in range(self.n_rows):
            for result_col in range(other.n_cols):
                for polynomial_indx in range(self.n_cols):
                    # That's so cool that the polynomial multiplication works like convolution
                    conv = np.convolve(self.matrix[result_row, polynomial_indx], other.matrix[polynomial_indx, result_col])
                    for idx, coef in enumerate(conv):
                        values[result_row, result_col, idx % (self.polynomial_degree + 1)] = \
                            (values[result_row, result_col, idx % (self.polynomial_degree + 1)] + coef) % self.max_coef_value


        result_pm = PolynomialMatrix(self.max_coef_value, self.n_rows, other.n_cols, self.polynomial_degree)
        result_pm.matrix = values
        return result_pm
