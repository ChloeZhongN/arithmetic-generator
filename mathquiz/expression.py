from .rational import Rational

# 定义运算符的优先级
# 数字越大优先级越高
PRIORITY = {'+': 1, '-': 1, '×': 2, '÷': 2}


class Expr:
    """
    所有表达式节点的基类
    """
    
    def eval(self):
        """
        计算这个表达式的值，返回一个rational分数
        """
        raise NotImplementedError

    def priority(self):
        """
        返回这个表达式的优先级，用于决定输出时是否加括号
        """
        raise NotImplementedError

    def to_string(self):
        """
        把表达式转成可读字符串
        """
        raise NotImplementedError

    def canonical(self):
        """
        返回规范式的字符串，判断两道题是否重复
        """
        raise NotImplementedError


class Num(Expr):
    """
    数字节点
    """
    
    def __init__(self, value):
        """
        构造一个数字节点
        :param value：必须是一个rational对象
        """
        self.value = value

    def eval(self):
        """
        数字节点的值是它自己
        """
        return self.value

    def priority(self):
        """
        数字的优先级最高，设为3
        """
        return 3

    def to_string(self):
        """
        把数字转成字符串
        调用Rational的__str__方法
        """
        return str(self.value)

    def canonical(self):
        """
        数字节点的规范形式
        用'N'开头，后面跟分子/分母
        例:1/2变成'N1/2'
        """
        return f"N{self.value.num}/{self.value.den}"


class Op(Expr):
    """
    运算符节点
    """
    
    def __init__(self, op, left, right):
        """
        构造一个运算符节点
        :param op：运算符(+ - * /)
        :param left：左子表达式，是一个Expr对象
        :param right：右子表达式，是一个Expr对象
        """
        self.op = op
        self.left = left
        self.right = right

    def eval(self):
        """
        递归计算整个表达式的值
        """
        # 计算左子表达式的值l和右子表达式的值r
        l = self.left.eval()
        r = self.right.eval()

        # 根据运算符，对l和r做相应的运算
        if self.op == '+':
            return l + r
        if self.op == '-':
            return l - r
        if self.op == '×':
            return l * r
        if self.op == '÷':
            return l / r

        # 运算符不是+ - * /，则出错
        raise ValueError(f"未知运算符: {self.op}")

    def priority(self):
        """
        返回当前运算符的优先级
        """
        return PRIORITY[self.op]

    def to_string(self):
        """
        把表达式转成字符串，在需要的地方加括号
        """
        
        my_pri = PRIORITY[self.op]

        # 递归得到左子右子表达式的字符串
        l = self.left.to_string()
        r = self.right.to_string()

        # 左子表达式优先级更低，加括号
        if self.left.priority() < my_pri:
            l = f"({l})"

        # 右子表达式优先级更低，或同优先级但父节点是 - / ÷，加括号
        r_pri = self.right.priority()
        if r_pri < my_pri or (r_pri == my_pri and self.op in ('-', '÷')):
            r = f"({r})"

        # 拼接成"左 运算符 右"的形式
        return f"{l} {self.op} {r}"

    def canonical(self):
        """
        返回规范形式
        """
        l = self.left.canonical()
        r = self.right.canonical()

        # 加法和乘法满足交换律，可以交换左右
        if self.op in ('+', '×') and l > r:
            l, r = r, l

        return f"({l}{self.op}{r})"
