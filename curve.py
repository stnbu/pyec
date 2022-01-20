from dataclasses import dataclass

from field import FieldElement, PrimeGaloisField


@dataclass
class EllipticCurve:
    a: int
    b: int
    field: PrimeGaloisField

    def __contains__(self, point: "Point") -> bool:
        x, y = point.x, point.y
        return y ** 2 == x ** 3 + self.a * x + self.b

    def __post_init__(self):
        # Encapsulate int parameters in FieldElement
        self.a = FieldElement(self.a, self.field)
        self.b = FieldElement(self.b, self.field)

        # Check for membership of curve parameters in the field.
        if self.a not in self.field or self.b not in self.field:
            raise ValueError
