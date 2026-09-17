# 求最大公约数，实现分数约分
from math import gcd

class Rational:
    """
    分数类。
    1.用整数分子和分母表示分数
    2.构造时自动约分
    3.分母始终为正，负号统一放在分子上
    4.支持加、减、乘、除、比较、格式化输出、字符串解析
    """

    def __init__(self, num, den=1):
        """
        构造一个分数。
        :param num: 分子(整数)
        :param den：分母(整数，默认1)
        """
        if den == 0:
            raise ValueError("分母不能为 0")

        # 保证分母为正
        if den < 0:
            num, den = -num, -den

        # 求最大公约数，用于约分
        g = gcd(abs(num), den)

        # 约分后保存分子和分母
        self.num = num // g
        self.den = den // g

    # 四则运算
    
    def __add__(self, o):
        """
        加法：a/b + c/d = (a*d + c*b) / (b*d)
        """
        return Rational(self.num * o.den + o.num * self.den,
                        self.den * o.den)

    def __sub__(self, o):
        """
        减法：a/b - c/d = (a*d - c*b) / (b*d)
        """
        return Rational(self.num * o.den - o.num * self.den,
                        self.den * o.den)

    def __mul__(self, o):
        """
        乘法：a/b × c/d = (a*c) / (b*d)
        """
        return Rational(self.num * o.num, self.den * o.den)

    def __truediv__(self, o):
        """
        除法：a/b ÷ c/d = (a*d) / (b*c)
        """
        if o.num == 0:
            raise ZeroDivisionError("除数为 0")
        return Rational(self.num * o.den, self.den * o.num)

    # 比较运算

    def __eq__(self, o):
        """
        判断两个分数是否相等
        不是Rational类型，返回False
        """
        return isinstance(o, Rational) and \
               self.num == o.num and self.den == o.den

    def __lt__(self, o):
        """
        小于比较：a/b < c/d 等价于 a*d < c*b
        """
        return self.num * o.den < o.num * self.den

    def __le__(self, o):
        """
        小于等于比较
        """
        return self.num * o.den <= o.num * self.den

    def __gt__(self, o):
        """
        大于比较
        """
        return self.num * o.den > o.num * self.den

    def __ge__(self, o):
        """
        大于等于比较
        """
        return self.num * o.den >= o.num * self.den

    def __hash__(self):
        """
        让Rational可以被放入set或作为dict的key
        """
        return hash((self.num, self.den))

    # 工具方法

    def is_zero(self):
        """
        判断是否为0
        """
        return self.num == 0

    def is_proper_fraction(self):
        """
        判断是否是真分数
        分子>0且分子<分母
        """
        return self.num > 0 and self.num < self.den

    # 格式化输出

    def __str__(self):
        """
        按题目要求输出
        """
        # 分母为1，是整数
        if self.den == 1:
            return str(self.num)

        # 分子绝对值小于分母，是真分数
        if abs(self.num) < self.den:
            return f"{self.num}/{self.den}"

        # 带分数
        sign = -1 if self.num < 0 else 1
        n = abs(self.num)
        # 整数部分
        k = n // self.den
        # 余数，作为新的分子
        r = n % self.den

        # 余数为0，是整数
        if r == 0:
            return str(sign * k)

        # 拼接带分数，如2’3/8
        return f"{sign * k}’{r}/{self.den}"

    # 字符串解析
    
    @staticmethod
    def parse(s):
        """
        把字符串解析成Rational
        """
        s = s.strip().replace("'", "’")

        # 允许前导加号，如"+3/5"
        if s.startswith('+'):
            s = s[1:]

        # 带分数：如2’3/8
        if "’" in s:
            k_str, frac = s.split("’")
            a_str, b_str = frac.split("/")
            k, a, b = int(k_str), int(a_str), int(b_str)

            # 带分数若整数部分为负，值应为k-a/b
            if k < 0:
                return Rational(k * b - a, b)

            # 整数部分非负，值应为k+a/b
            return Rational(k * b + a, b)

        # 普通分数，如3/5
        if "/" in s:
            a_str, b_str = s.split("/")
            return Rational(int(a_str), int(b_str))

        # 整数
        return Rational(int(s))
