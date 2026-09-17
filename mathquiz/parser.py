
from .rational import Rational
from .expression import Num, Op

class Parser:
    """
    解析器类
    """
    
    def __init__(self, s):
        """
        构造解析器
        :param s：要解析的字符串
        :param self.s：保存这个字符串
        :param self.pos：当前解析到字符串的哪个位置，从0开始
        """
        self.s = s
        self.pos = 0

    def parse(self):
        """
        解析整个表达式，返回表达式树的根节点
        3. 如果还有剩余字符，说明有无法解析的内容，抛出异常。
        """
        # 调用_parse_expr()解析一个表达式
        expr = self._parse_expr()
        self._skip_ws()
        # 如果有剩余字符，则有无法解析的内容，抛出异常
        if self.pos < len(self.s):
            raise ValueError(f"无法解析的字符: '{self.s[self.pos]}' 位置 {self.pos}")
        return expr

    def _skip_ws(self):
        """
        跳过空格和制表符
        """
        while self.pos < len(self.s) and self.s[self.pos] in ' \t':
            self.pos += 1

    def _peek(self):
        """
        查看当前字符，但不移动位置
        如果到字符串末尾，返回None
        """
        # 跳过空格
        self._skip_ws()
        if self.pos < len(self.s):
            return self.s[self.pos]
        return None

    def _parse_expr(self):
        """
        解析表达式
        """
        # 解析第一个项，作为左操作数
        left = self._parse_term()
        
        while True:
            c = self._peek()
            if c in ('+', '-'):
                # 消耗掉运算符
                self.pos += 1
                # 解析右边的项
                right = self._parse_term()
                # 组合成运算符节点
                left = Op(c, left, right)
            else:
                break
                
        return left

    def _parse_term(self):
        """
        解析项
        """
        left = self._parse_factor()
        
        while True:
            c = self._peek()
            if c in ('×', '÷'):
                self.pos += 1
                right = self._parse_factor()
                left = Op(c, left, right)
            else:
                break
                
        return left

    def _parse_factor(self):
        """
        解析因子
        """
        c = self._peek()
        
        if c == '(':
            # 消耗(
            self.pos += 1
            # 递归解析括号里面的表达式
            expr = self._parse_expr()
            # 检查是否有)
            if self._peek() != ')':
                raise ValueError("缺少右括号")
            # 消耗掉)
            self.pos += 1
            # 直接返回括号里面的表达式
            return expr

        # 不是括号，就解析数字
        return self._parse_number()

    def _parse_number(self):
        """
        解析一个数字
        """
        self._skip_ws()
        start = self.pos

        # 一直读到遇到空格、运算符或括号停下
        while self.pos < len(self.s) and self.s[self.pos] not in ' \t+-×÷()':
            self.pos += 1

        # 截取数字字符串
        token = self.s[start:self.pos]
        
        if not token:
            raise ValueError(f"期望数字，位置 {self.pos}")

        # 用Rational.parse解析数字，用Num包装
        return Num(Rational.parse(token))
