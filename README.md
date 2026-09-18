# arithmetic-generator

一个命令行程序，用于生成小学四则运算题目，并支持批改答案。



## 功能

- 生成小学四则运算题目
- 支持自然数、真分数、带分数
- 每道题运算符不超过 3 个
- 减法结果非负
- 除法结果必须是真分数
- 自动去重
- 支持批改答案并统计对错
- 

## 运行环境

- Python 3.7+
- 无第三方依赖



## 用法

### 生成题目

```bash
python main.py -n <题目数量> -r <数值范围>
例：python main.py -n 10 -r 10
```

- `-n`：生成题目的数量
- `-r`：题目中数值的范围，所有自然数、分子、分母都小于该值

生成结果：

- `Exercises.txt`：题目
- `Answers.txt`：答案



### 批改答案

```bash
python main.py -e <题目文件> -a <答案文件>
例：python main.py -e Exercises.txt -a Answers.txt
```

生成结果：

- `Grade.txt`：对错统计

`Grade.txt`格式示例：

```text
Correct: 5 (1, 3, 5, 7, 9)
Wrong: 5 (2, 4, 6, 8, 10)
```



### 查看帮助

```bash
python main.py -h
```



## 打包成 exe

```bash
pip install pyinstaller
pyinstaller -F main.py -n Myapp
```

生成的 `dist/Myapp.exe` 可以直接运行。