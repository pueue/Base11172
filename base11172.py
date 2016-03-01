# base11172.py
import itertools
from enum import IntEnum

BASE = 10


class Sign(IntEnum):
    Positive = 1
    Zero = 0
    Negative = -1


class Base11172:

    def __init__(self, data, sign=0):
        sign = Sign(sign)

        if isinstance(data, int):
            assert -BASE < data < BASE
            sign = 1 if data > 0 else 0 if data == 0 else -1
            data = [abs(data)]
        elif isinstance(data, list):
            for x in data:
                assert -BASE < x < BASE
            assert sign != 0
            data = list(reversed(data))
        else:
            assert False

        # Properties
        self.sign = sign
        self.data = data

        self.clear_zero()

    # Represent
    def __repr__(self):
        if self.sign == 1:
            return '+' + str(self.data[::-1])
        elif self.sign == 0:
            return '0'
        else:   # self.sign == -1:
            return '-' + str(self.data[::-1])

    def __str__(self):
        if self.sign == 1:
            return '+' + str(self.data[::-1])
        elif self.sign == 0:
            return '0'
        else:   # self.sign == -1:
            return '-' + str(self.data[::-1])

    # Index & Slice
    def __len__(self):
        return len(self.data)

    def __getitem__(self, degree):
        return self.data[degree]

    def __setitem__(self, degree, coefficient):
        self.data[degree] = coefficient

    def __delitem__(self, degree):
        self.data.__delitem__(degree)

    # Shift
    def __lshift__(self, move):
        return Base11172(self.data[::-1] + [0] * move, self.sign)

    def __rshift__(self, move):
        if len(self) <= move:
            return Base11172(0, 0)
        return Base11172(self.data[move:], self.sign)

    # Compare
    def __cmp__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # Same object
        if id(self) == id(other):
            return 0

        # Different sign
        if self.sign > other.sign:
            return 1
        elif self.sign < other.sign:
            return -1
        # Same sign
        else:
            if self.sign == 1:
                return self.compare_data(other)
            elif self.sign == 0:
                return 0
            else:   # self.sign == -1
                return self.compare_data(other) * -1

    def __eq__(self, other):
        compare = self.__cmp__(other)
        if compare == 0:
            return True
        return False

    def __ne__(self, other):
        compare = self.__cmp__(other)
        if compare != 0:
            return True
        return False

    def __lt__(self, other):
        compare = self.__cmp__(other)
        if compare < 0:
            return True
        return False

    def __gt__(self, other):
        compare = self.__cmp__(other)
        if compare > 0:
            return True
        return False

    def __le__(self, other):
        compare = self.__cmp__(other)
        if compare <= 0:
            return True
        return False

    def __ge__(self, other):
        compare = self.__cmp__(other)
        if compare >= 0:
            return True
        return False

    def compare_data(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        if id(self) == id(other):
            return 0

        # different length
        if len(self) > len(other):
            return 1
        elif len(self) < len(other):
            return -1
        # Same length
        else:
            for i in range(len(self)-1, -1, -1):
                if self.data[i] > other.data[i]:
                    return 1
                elif self.data[i] < other.data[i]:
                    return -1
            return 0

    # Unary
    def __pos__(self):
        return Base11172(self.data[::-1], self.sign)

    def __neg__(self):
        if self.sign == 0:
            Base11172(0)
        return Base11172(self.data[::-1], self.sign*-1)

    def __abs__(self):
        return Base11172(self.data[::-1], 1)

    # Mathematics
    def __add__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # One of both is Zero
        if self.sign == 0:
            return other
        elif other.sign == 0:
            return self

        # Different sign means subtract
        if self.sign != other.sign:
            data = self.sub_data(other)
            if self.compare_data(other) == 1:
                sign = self.sign
            else:   # self.compare_data(other) == -1
                sign = other.sign

        else:   # Self.sign == Other.sign
            data = self.add_data(other)
            sign = self.sign
        return Base11172(data, sign)

    def add_data(self, other):
        size = max(len(self), len(other))
        data = [0] * (size+1)
        carry = 0
        for i, (a, b) in enumerate(itertools.zip_longest(*(self.data, other.data), fillvalue=0)):
            carry, data[i] = divmod(a+b+carry, BASE)
        data[-1] = carry
        return data[::-1]

    def __sub__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # One of both is Zero
        if self.sign == 0:
            return -other
        elif other.sign == 0:
            return self

        if self.sign != other.sign:
            data = self.add_data(other)
            if self.compare_data(other) == 1:
                sign = self.sign
            else:   # self.compare_data(other) == -1
                sign = other.sign

        else:   # Self.sign == Other.sign
            if self.compare_data(other) < 0:
                data = other.sub_data(self)
                sign = -1
            else:
                data = self.sub_data(other)
                sign = self.sign
        return Base11172(data, sign)

    def sub_data(self, other):
        size = max(len(self), len(other))
        data = [0] * (size+1)
        carry = 0
        for i, (a, b) in enumerate(itertools.zip_longest(*(self.data, other.data), fillvalue=0)):
            carry, data[i] = divmod(a-b+carry, BASE)
        data[-1] = carry
        return data[::-1]

    def __mul__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other, 0)

        # One of both is Zero
        if self.sign == 0 or other.sign == 0:
            return 0
        if self.sign == other.sign:
            sign = 1
        else:
            sign = -1

        data = self.mul_data(other)
        return Base11172(data, sign)

    def mul_data(self, other):
        temps = []
        for i, x in enumerate(other.data):
            tmp = [0] * (i + 1 + len(self))
            carry = 0
            for j, y in enumerate(self.data):
                carry, tmp[i+j] = divmod(x*y+carry, BASE)
            tmp[-1] = carry
            if tmp[-1] == 0:
                del tmp[-1]
            temps.append(tmp)

        size = len(self) + len(other)
        data = [0] * size
        carry = 0
        for i, x in enumerate(itertools.zip_longest(*temps, fillvalue=0)):
            carry, data[i] = divmod(sum(x)+carry, BASE)
        if data[-1] == 0:
            data[-1] = carry
        return data[::-1]

    def __floordiv__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        quotient, remind = [], []

        # One of both is Zero
        if self.sign == 0:
            return 0
        elif other.sign == 0:
            raise ZeroDivisionError
        if self.sign != other.sign:
            sign = -1
        else:
            sign = 1

        if self.compare_data(other) == 0:
            quotient, remind = [1], [0]
        elif self.compare_data(other) == -1:
            quotient, remind = [0], self.data
        else:   # self.compare_data(other) == 1
            dividend, divisor, quotient = self, other, []

            pointer = len(dividend)-1
            sub_dividend = []
            while pointer >= 0:
                sub_dividend = Base11172(sub_dividend[::-1]+[dividend[pointer]], 1)

                if sub_dividend.compare_data(divisor) != 1:
                    quotient.insert(0, 0)
                    pointer -= 1
                    sub_dividend.data.insert(0, dividend[pointer])
                if pointer < 0:
                        break

                sub_quotient = 0
                while sub_dividend.compare_data(divisor) >= 0:
                    sub_quotient += 1
                    sub_dividend = Base11172(sub_dividend.sub_data(divisor), 1)
                quotient.insert(0, sub_quotient)
                pointer -= 1
                # remind is sub_dividend
                remind = sub_dividend.data

        quotient = Base11172(quotient[::-1], sign)
        if remind != [0]:
            if sign == -1:
                quotient -= 1
        return quotient

    # def __mod__(self, other):
    #     pass

    def clear_zero(self):
        for i in range(len(self)-1, -1, -1):
                if i != 0 and self.data[i] == 0:
                    del self.data[i]
                else:
                    break


def test():
    a = Base11172([5,5,5,5,5,5], 1)
    b = Base11172([9, 1, 1], 1)
    print(a//b, 555555//911)
    a = Base11172([5, 4, 3, 2, 1], 1)
    b = Base11172([9, 9, 9], -1)
    print(a//b, 54321//-999)
    x = Base11172([1, 0, 2, 8], 1)
    print(x*b)

    c = Base11172([1, 2, 3, 2, 1], 1)
    d = Base11172([1, 1], 1)
    print(c//d, 12321//11)

    e = Base11172([7, 7, 7, 7, 7], 1)
    f = Base11172([9, 9], 1)
    print(e//f, 77777//99)
    # print(a+b)
    # print(a == (a+b)-b)
    # print(a*b)
    # print(b*a)
    print()


if __name__ == '__main__':
    # cProfile.run("test()")
    test()
