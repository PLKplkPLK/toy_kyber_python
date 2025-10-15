import numpy as np

class Lattice:
    def __init__(self, dimension: int, q: int):
        """Initialize lattice with dimension and modulo parameter: q."""
        self.dimension = dimension
        self.q = q

    def mod_q(self, x: int) -> int:
        """Return x modulo q."""
        return np.mod(x, self.q)
