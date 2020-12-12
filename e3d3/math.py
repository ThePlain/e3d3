import copy
from math import *


class Vector:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @property
    def values(self):
        return [self.x, self.y, self.z, self.w]

    @property
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2)

    @property
    def normalized(self):
        length = self.length

        if length == 0:
            return Vector()

        return Vector(
            self.x / length,
            self.y / length,
            self.z / length,
            self.w / length,
        )

    @property
    def copy(self):
        return copy.deepcopy(self)


class Quaternion:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @property
    def values(self):
        return [self.x, self.y, self.z, self.w]

    @property
    def copy(self):
        return copy.deepcopy(self)


IDENTITY = [
    1.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 1.0,
]


class Matrix:
    def __init__(self, *values):
        self.values = values or IDENTITY

    def __mul__(self, mat):
        return Matrix(
            self._11 * mat._11 + self._12 + mat._21 + self._13 * mat._31 + self._14 * mat._41,
            self._11 * mat._12 + self._12 + mat._22 + self._13 * mat._32 + self._14 * mat._42,
            self._11 * mat._13 + self._12 + mat._23 + self._13 * mat._33 + self._14 * mat._43,
            self._11 * mat._14 + self._12 + mat._24 + self._13 * mat._34 + self._14 * mat._44,

            self._21 * mat._11 + self._22 + mat._21 + self._23 * mat._31 + self._24 * mat._41,
            self._21 * mat._12 + self._22 + mat._22 + self._23 * mat._32 + self._24 * mat._42,
            self._21 * mat._13 + self._22 + mat._23 + self._23 * mat._33 + self._24 * mat._43,
            self._21 * mat._14 + self._22 + mat._24 + self._23 * mat._34 + self._24 * mat._44,

            self._31 * mat._11 + self._32 + mat._21 + self._33 * mat._31 + self._34 * mat._41,
            self._31 * mat._12 + self._32 + mat._22 + self._33 * mat._32 + self._34 * mat._42,
            self._31 * mat._13 + self._32 + mat._23 + self._33 * mat._33 + self._34 * mat._43,
            self._31 * mat._14 + self._32 + mat._24 + self._33 * mat._34 + self._34 * mat._44,

            self._41 * mat._11 + self._42 + mat._21 + self._43 * mat._31 + self._44 * mat._41,
            self._41 * mat._12 + self._42 + mat._22 + self._43 * mat._32 + self._44 * mat._42,
            self._41 * mat._13 + self._42 + mat._23 + self._43 * mat._33 + self._44 * mat._43,
            self._41 * mat._14 + self._42 + mat._24 + self._43 * mat._34 + self._44 * mat._44,
        )

    @property
    def copy(self):
        return copy.deepcopy(self)

    @staticmethod
    def from_components(location, rotation, scale):
        raise NotImplementedError

    @property
    def _11(self):
        return self.values[0]

    @_11.setter
    def _11(self, value):
        self.values[0] = value

    @property
    def _12(self):
        return self.values[1]

    @_12.setter
    def _12(self, value):
        self.values[1] = value

    @property
    def _13(self):
        return self.values[2]

    @_13.setter
    def _13(self, value):
        self.values[2] = value

    @property
    def _14(self):
        return self.values[3]

    @_14.setter
    def _14(self, value):
        self.values[3] = value

    @property
    def _21(self):
        return self.values[4]

    @_21.setter
    def _21(self, value):
        self.values[4] = value

    @property
    def _22(self):
        return self.values[5]

    @_22.setter
    def _22(self, value):
        self.values[5] = value

    @property
    def _23(self):
        return self.values[6]

    @_23.setter
    def _23(self, value):
        self.values[6] = value

    @property
    def _24(self):
        return self.values[7]

    @_24.setter
    def _24(self, value):
        self.values[7] = value

    @property
    def _31(self):
        return self.values[8]

    @_31.setter
    def _31(self, value):
        self.values[8] = value

    @property
    def _32(self):
        return self.values[9]

    @_32.setter
    def _32(self, value):
        self.values[9] = value

    @property
    def _33(self):
        return self.values[10]

    @_33.setter
    def _33(self, value):
        self.values[10] = value

    @property
    def _34(self):
        return self.values[11]

    @_34.setter
    def _34(self, value):
        self.values[11] = value

    @property
    def _41(self):
        return self.values[12]

    @_41.setter
    def _41(self, value):
        self.values[12] = value

    @property
    def _42(self):
        return self.values[13]

    @_42.setter
    def _42(self, value):
        self.values[13] = value

    @property
    def _43(self):
        return self.values[14]

    @_43.setter
    def _43(self, value):
        self.values[14] = value

    @property
    def _44(self):
        return self.values[15]

    @_44.setter
    def _44(self, value):
        self.values[15] = value
