import re
# 解析题目字符串
from .parser import Parser
# 解析答案字符串
from .rational import Rational

def grade(ex_file, ans_file, out_file='Grade.txt'):
    """
    读取题目和答案文件，比对后写入Grade.txt
    """
    # 打开题目文件，逐行读取。
    with open(ex_file, 'r', encoding='utf-8') as f:
        ex_lines = [line.rstrip('\n') for line in f if line.strip()]

    # 读取答案文件
    with open(ans_file, 'r', encoding='utf-8') as f:
        ans_lines = [line.rstrip('\n') for line in f if line.strip()]

    # 如果两个文件行数不一致，打印警告
    if len(ex_lines) != len(ans_lines):
        print(f"警告：题目数 {len(ex_lines)} 与答案数 {len(ans_lines)} 不一致")

    # 记录正确的题号和错误的题号
    correct = []
    wrong = []

    # 取两个文件行数的较大值，防止漏题
    total = max(len(ex_lines), len(ans_lines))

    # 逐题批改
    for i in range(total):
        idx = i + 1

        # 如果题目文件或答案文件缺了这一行，判为错误
        if i >= len(ex_lines) or i >= len(ans_lines):
            wrong.append(idx)
            continue

        # 取出这一行的题目和答案
        ex_str = ex_lines[i].strip()
        ans_str = ans_lines[i].strip()

        # 新增：移除行开头 "1. " 这类序号，兼容带序号输出的文件
        ex_str = re.sub(r'^\d+\.\s*', '', ex_str)
        ans_str = re.sub(r'^\d+\.\s*', '', ans_str)

        # 去掉题目末尾的=
        if ex_str.endswith('='):
            ex_str = ex_str[:-1].rstrip()

        # 计算标准答案
        try:
            expr = Parser(ex_str).parse()
            expected = expr.eval()
        except Exception:
            # 解析失败，判为错误，跳到下一题
            wrong.append(idx)
            continue

        # 解析用户答案
        try:
            got = Rational.parse(ans_str)
        except Exception:
            # 答案格式不对，判为错误，跳到下一题
            wrong.append(idx)
            continue

        # 比较标准答案和用户答案
        if expected == got:
            # 相等记录到正确列表
            correct.append(idx)
        else:
            # 不相等记录到错误列表
            wrong.append(idx)

    # 写入结果文件
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(f"Correct: {len(correct)} "
                f"({', '.join(map(str, correct))})\n")
        f.write(f"Wrong: {len(wrong)} "
                f"({', '.join(map(str, wrong))})\n")
