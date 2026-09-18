import sys

from .generator import generate_problems, save_problems
from .grader import grade


def print_help():
    """
    打印帮助信息
    """
    print(
    """
    用法：
    main.py -n <题目数量> -r <数值范围>
      生成题目并保存到Exercises.txt和Answers.txt
    main.py -e <题目文件> -a <答案文件>
      批改答案，结果保存到Grade.txt

    参数：
      -n  生成题目的数量（正整数）
      -r  题目中数值的范围（正整数），所有自然数、分子、分母都小于该值
      -e  题目文件路径
      -a  答案文件路径
      -h  显示帮助信息

    示例：
      main.py -n 10 -r 10
      main.py -e Exercises.txt -a Answers.txt
    """)


def main():
    """
    程序主入口
    """
    
    argv = sys.argv[1:]

    # 如用户没有输入任何参数，或输入了-h/--help，打印帮助信息并返回
    if not argv or '-h' in argv or '--help' in argv:
        print_help()
        return

    # 保存解析后的参数
    opts = {}
    
    i = 0
    while i < len(argv):
        arg = argv[i]

        # 只支持 -n、-r、-e、-a 四种参数
        if arg in ('-n', '-r', '-e', '-a'):
            # 如果参数后面没有值，报错
            if i + 1 >= len(argv):
                print(f"错误：{arg} 缺少参数")
                print_help()
                sys.exit(1)
            # 参数名和参数值存入opts，然后跳过两个位置
            opts[arg] = argv[i + 1]
            i += 2
        else:
            # 未知参数，报错并退出
            print(f"错误：未知参数 {arg}")
            print_help()
            sys.exit(1)

    # 批改模式
    
    if '-e' in opts or '-a' in opts:
        # 批改模式必须同时有-e和-a
        if '-e' not in opts or '-a' not in opts:
            print("错误：批改模式需要同时指定-e和-a")
            print_help()
            sys.exit(1)

        try:
            # 调用grade函数，结果写入Grade.txt
            grade(opts['-e'], opts['-a'], 'Grade.txt')
            print("批改完成，结果已保存到Grade.txt")
        except Exception as e:
            # 如批改过程出错，打印错误并退出
            print(f"批改失败：{e}")
            sys.exit(1)
        return

    # 生成模式

    # 生成模式必须指定-n
    if '-n' not in opts:
        print("错误：生成模式需要指定-n")
        print_help()
        sys.exit(1)

    # 生成模式必须指定-r
    if '-r' not in opts:
        print("错误：必须指定-r参数")
        print_help()
        sys.exit(1)

    # 把-n和-r的值转成整数
    try:
        n = int(opts['-n'])
        r = int(opts['-r'])
    except ValueError:
        # 无法转成整数，说明用户输入的不是数字
        print("错误：-n和-r必须是整数")
        sys.exit(1)

    # 检查-n是否为正整数
    if n <= 0:
        print("错误：-n必须是正整数")
        sys.exit(1)

    # 检查-r是否为正整数
    if r <= 0:
        print("错误：-r必须是正整数")
        sys.exit(1)

    # 调用生成器生成题目并保存
    try:
        problems = generate_problems(n, r)
        save_problems(problems)
        print(f"成功生成{n}道题目，已保存到 "
              f"Exercises.txt和Answers.txt")
    except Exception as e:
        print(f"生成失败：{e}")
        sys.exit(1)
