from dataclasses import dataclass

from curve import EllipticCurve
from field import FieldElement

inf = float("inf")


@dataclass
class Point:
    x: int
    y: int

    curve: EllipticCurve

    def __post_init__(self):
        # Ignore validation for I
        if self.x is None and self.y is None:
            return

        # Encapsulate int coordinates in FieldElement
        self.x = FieldElement(self.x, self.curve.field)
        self.y = FieldElement(self.y, self.curve.field)

        # Verify if the point satisfies the curve equation
        if self not in self.curve:
            raise ValueError

    def __add__(self, other):
        assert self.curve == other.curve
        I = Point(x=None, y=None, curve=self.curve)

        #################################################################
        # Point Addition for P₁ or P₂ = I   (identity)                  #
        #                                                               #
        # Formula:                                                      #
        #     P + I = P                                                 #
        #     I + P = P                                                 #
        #################################################################
        if self == I:
            return other

        if other == I:
            return self

        #################################################################
        # Point Addition for X₁ = X₂   (additive inverse)               #
        #                                                               #
        # Formula:                                                      #
        #     P + (-P) = I                                              #
        #     (-P) + P = I                                              #
        #################################################################
        if self.x == other.x and self.y == (-1 * other.y):
            return I

        #################################################################
        # Point Addition for X₁ ≠ X₂   (line with slope)                #
        #                                                               #
        # Formula:                                                      #
        #     S = (Y₂ - Y₁) / (X₂ - X₁)                                 #
        #     X₃ = S² - X₁ - X₂                                         #
        #     Y₃ = S(X₁ - X₃) - Y₁                                      #
        #################################################################
        if self.x != other.x:
            x1, x2 = self.x, other.x
            y1, y2 = self.y, other.y

            s = (y2 - y1) / (x2 - x1)
            x3 = s ** 2 - x1 - x2
            y3 = s * (x1 - x3) - y1

            return self.__class__(x=x3.value, y=y3.value, curve=self.curve)

        #################################################################
        # Point Addition for P₁ = P₂   (vertical tangent)               #
        #                                                               #
        # Formula:                                                      #
        #     S = ∞                                                     #
        #     (X₃, Y₃) = I                                              #
        #################################################################
        if self == other and self.y == inf:
            return I

        #################################################################
        # Point Addition for P₁ = P₂   (tangent with slope)             #
        #                                                               #
        # Formula:                                                      #
        #     S = (3X₁² + a) / 2Y₁         .. ∂(Y²) = ∂(X² + aX + b)    #
        #     X₃ = S² - 2X₁                                             #
        #     Y₃ = S(X₁ - X₃) - Y₁                                      #
        #################################################################
        if self == other:
            x1, y1, a = self.x, self.y, self.curve.a

            s = (3 * x1 ** 2 + a) / (2 * y1)
            x3 = s ** 2 - 2 * x1
            y3 = s * (x1 - x3) - y1

            return self.__class__(x=x3.value, y=y3.value, curve=self.curve)

    def __rmul__(self, scalar: int) -> "Point":
        I = Point(x=None, y=None, curve=self.curve)
        # Naive approach:
        #
        # result = I
        # for _ in range(scalar):  # or range(scalar % N)
        #     result = result + self
        # return result

        # Optimized approach using binary expansion
        current = self
        result = I
        while scalar:
            if scalar & 1:  # same as scalar % 2
                result = result + current
            current = current + current  # point doubling
            scalar >>= 1  # same as scalar / 2
        return result
