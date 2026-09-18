import random
from .rational import Rational
from .expression import Num, Op

def rand_operand(r):
    """
    随机生成一个操作数，所有数值都<r
    :return：一个Rational对象，表示随机生成的操作数
    """
    randint = random.randint

    # 范围太小，返回0
    if r <= 1:
        return Rational(0, 1)

    # 如果 r <= 2，无法生成真分数和带分数（分母范围不够），必须强制只能生成自然数 (kind = 0)
    if r <= 2:
        kind = 0
    else:
        kind = randint(0, 2)

    if kind == 0:
        # 自然数：随机生成0到r-1之间的整数
        return Rational(randint(0, r - 1), 1)

    if kind == 1:
        # 真分数
        # 分母
        d = randint(2, r - 1)
        # 分子
        a = randint(1, d - 1)
        return Rational(a, d)

    # 带分数
    # 分母
    d = randint(2, r - 1)
    # 分子
    a = randint(1, d - 1)
    # 整数部分
    k = randint(1, r - 1)
    return Rational(k * d + a, d)


def _build(r, num_ops):
    """
    递归构建表达式树，失败返回None
    :param r：取值范围
    :param num_ops：当前子树需要的运算符个数
    """
    randint = random.randint
    choice = random.choice

    # 递归终止条件
    if num_ops == 0:
        return Num(rand_operand(r))

    # 随机分配左右子树的运算符数量
    left_ops = randint(0, num_ops - 1)
    right_ops = num_ops - 1 - left_ops

    # 递归构建左子树
    left = try_build(r, left_ops)
    if left is None:
        return None

    # 递归构建右子树
    right = try_build(r, right_ops)
    if right is None:
        return None

    # 计算左右子树的值，判断哪些运算符合法
    lv = left.eval()
    rv = right.eval()

    # 收集所有合法运算符
    # 加法和乘法永远合法
    valid_ops = ['+', '×']

    # 减法：左值>=右值
    if lv >= rv:
        valid_ops.append('-')

    # 除法：右值不为0，结果必须是真分数
    if not rv.is_zero():
        res = lv / rv
        if res.is_proper_fraction():
            valid_ops.append('÷')

    # 从合法运算符中随机选择一个
    op = choice(valid_ops)
    # 组合成运算符节点并返回
    return Op(op, left, right)


def try_build(r, num_ops, max_tries=30):
    """
    尝试构建一个表达式树，最多尝试max_tries次构建，失败返回None
    :param r: 数值范围
    :param num_ops: 需要的运算符个数
    :param max_tries: 最大尝试次数，默认30次
    """
    for _ in range(max_tries):
        result = _build(r, num_ops)
        if result is not None:
            return result
    return None


def generate_problems(n, r):
    """
    生成n道不重复的题目
    :param n: 需要生成的题目数量
    :param r: 数值范围，所有数值都小于r
    :return：一个列表，里面是n个Expr对象
    """
    # 用于去重的集合
    seen = set()
    # 存储生成的题目
    problems = []
    # 连续失败次数
    fail_streak = 0
    # 最大允许连续失败次数
    max_fail = max(10000, n * 10)

    while len(problems) < n:
        # 如果连续失败太多次，说明范围太小，无法生成足够多的不重复题目
        if fail_streak >= max_fail:
            raise RuntimeError(
                f"无法生成 {n} 道不重复题目"
                f"（已生成 {len(problems)} 道），请增大 -r"
            )

        # 随机选择运算符个数
        num_ops = random.randint(1, 3)
        # 尝试构建表达式树
        expr = try_build(r, num_ops, max_tries=20)

        # 如果构建失败，增加失败计数，继续下一轮
        if expr is None:
            fail_streak += 1
            continue

        # 获取题目的规范形式
        key = expr.canonical()

        # 如果这个题目已经生成过，增加失败计数，继续下一轮
        if key in seen:
            fail_streak += 1
            continue

        # 成功生成一道新题目
        seen.add(key)
        fail_streak = 0
        problems.append(expr)

    return problems


def save_problems(problems,
                  ex_file='Exercises.txt',
                  ans_file='Answers.txt'):
    """
    将题目和答案写入文件（新增行号 1. 2. …）
    """
    # 同时打开两个文件，分别用于写题目和答案
    with open(ex_file, 'w', encoding='utf-8') as fe, \
         open(ans_file, 'w', encoding='utf-8') as fa:
        for idx, p in enumerate(problems, start=1):
            fe.write(f"{idx}. {p.to_string()} = \n")
            fa.write(f"{idx}. {str(p.eval())}\n")

