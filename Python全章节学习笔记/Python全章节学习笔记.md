# Python 全章节学习笔记

> 面向 Python 3.x，算法章节示例基于 Jupyter Notebook。

## 目录

- **第一部分 基础语法与数据结构**
  - [1. 数字](#1-数字)
  - [2. 字符串详解](#2-字符串详解)
  - [3. 列表](#3-列表)
  - [4. 列表解析](#4-列表解析)
  - [5. 序列](#5-序列)
  - [6. 字典](#6-字典)
  - [7. 集合](#7-集合)
  - [8. 拷贝问题（深浅拷贝）](#8-拷贝问题深浅拷贝)
- **第二部分 Python 常用模块**
  - [9. 模块与导入](#9-模块与导入)
  - [10. collections 模块](#10-collections-模块)
  - [11. 随机数模块](#11-随机数模块)
  - [12. 时间处理](#12-时间处理)
- **第三部分 函数与函数式编程**
  - [13. 函数基础详解](#13-函数基础详解)
  - [14. 匿名函数与函数式编程](#14-匿名函数与函数式编程)
  - [15. 递归函数](#15-递归函数)
  - [16. 闭包](#16-闭包)
  - [17. 装饰器](#17-装饰器)
  - [18. 生成器函数](#18-生成器函数)
- **第四部分 文件与数据持久化**
  - [19. 文件详解](#19-文件详解)
  - [20. CSV 文件详解](#20-csv-文件详解)
  - [21. Excel 文件详解](#21-excel-文件详解)
  - [22. JSON 与 Pickle](#22-json-与-pickle)
  - [23. INI 配置文件处理](#23-ini-配置文件处理)
  - [24. OS 模块目录处理](#24-os-模块目录处理)
- **第五部分 正则表达式**
  - [25. 正则表达式](#25-正则表达式)
- **第六部分 错误和异常**
  - [26. 错误和异常](#26-错误和异常)
- **第七部分 面向对象编程**
  - [27. 面向对象编程](#27-面向对象编程)
  - [28. 面向对象基础（课上练习）](#28-面向对象基础课上练习)
  - [29. 继承与反射](#29-继承与反射)
  - [30. 班级练习（Jupyter）](#30-班级练习jupyter)
- **第八部分 并发编程**
  - [31. 多进程详解与应用](#31-多进程详解与应用)
  - [32. 多线程详解与应用](#32-多线程详解与应用)
- **第九部分 数据库**
  - [33. MySQL 数据库操作](#33-mysql-数据库操作)
- **第十部分 数据分析**
  - [34. NumPy](#34-numpy)
  - [35. Matplotlib](#35-matplotlib)
- **第十一部分 算法与数据结构**
  - [36. 逻辑强化（算法入门练习）](#36-逻辑强化算法入门练习)
  - [37. 递归问题](#37-递归问题)
  - [38. 回溯算法](#38-回溯算法)
  - [39. 动态规划](#39-动态规划)
  - [40. 贪心算法](#40-贪心算法)
  - [41. 分治算法](#41-分治算法)

---
## 第一部分 基础语法与数据结构
### 1. 数字

#### 3 数字类型

主要类型：

| 类型 | 说明 | 样例 |
|---|---|---|
| int | 整数 | 1, 2, 3, 100... |
| float | 浮点 | 3.14, 2.1... |
| complex | 复数 | complex(1, 2) |
| bool | 布尔值 | 只有 True 与 False |

定义数字变量：

```python
pi = 3.14
r = 5
b = False
```

#### 4 数字计算与类型转换

#### 4.1 数字相关运算符

数字支持比较、算术、逻辑运算符：

```python
# 帽子销量100，T-shirt销量120，对比销量
hat_total = 100
tshirt_total = 120
hat_total > tshirt_total    # False

# 计算销售额
hat_price = 40
tshirt_price = 30
hat_sales = hat_price * hat_total          # 4000
tshirt_sales = tshirt_price * tshirt_total # 3600
```

#### 4.2 不同数字类型进行计算，结果如何？

- 整数与浮点数运算，结果为浮点数（浮点运算存在精度误差）
- 布尔值参与运算时按整数处理：True 相当于 1，False 相当于 0

```python
2 * pi * r    # 31.400000000000002
1 + True      # 2
1 == True     # True
1.0 == True   # True
```

#### 4.3 默认转换规则

运算时按 complex > float > int > bool 的顺序向高精度类型转换。

#### 4.4 数字类型强制转换

| 方法 | 说明 | 示例 |
|---|---|---|
| int([x]) | 将 x 转成整数 | int(3.14) -> 3 |
| int(x, base=10) | 将数字字符串转整数 | int('3') -> 3 |
| float(x=0) | 将数字或字符串转浮点 | float('3') -> 3.0 |
| bool(x) | 将任意对象转成 bool | bool(1) -> True |

```python
r = 5
pi = 3.14
tmp = pi * (r ** 2)    # 78.5，圆面积只保留整数
int(tmp)               # 78
int(pi)                # 3
bool(pi)               # True
bool(0.0)              # False
int("10", base=16)     # 16
```

#### 5 数字相关函数

#### 5.1 基本函数

| 函数 | 说明 |
|---|---|
| round(number, ndigits=None) | 指定小数后位数 |
| pow(x, y, z=None) | x**y 或 x**y % z |
| abs(x) | x 的绝对值 |

```python
tmp = 2 * pi * r    # 31.400000000000002
round(tmp, 1)       # 31.4
pow(2, 3)           # 8
a = -1
abs(a)              # 1
```

#### 5.2 math 模块

```python
import math
```

#### 5.3 数学常数

| 常数 | 说明 |
|---|---|
| math.pi | 圆周率，3.141592653589793 |
| math.e | 自然对数的底，2.718281828459045 |

#### 5.4 三角函数

| 函数 | 说明 |
|---|---|
| math.sin(x) / math.cos(x) | 返回 x 弧度的正弦/余弦值 |
| math.asin(x) / math.acos(x) | 返回 x 的反正弦/反余弦弧度值 |
| math.tan(x) | 返回 x 弧度的正切值 |
| math.atan(x) | 返回 x 的反正切弧度值 |

#### 5.5 指数函数等

| 函数 | 说明 |
|---|---|
| math.factorial(x) | 计算阶乘，返回 x! |
| math.sqrt(x) | 返回 x 的平方根 |
| math.floor(x) | 取最接近 x 的整数，返回整数 < x |
| math.log(x[, base]) | 以 base 为底的 x 的对数 |
| math.log10(x) | 以 10 为底的 x 的对数 |
| math.log2(x) | 以 2 为底的 x 的对数 |

```python
math.sin(0.3)    # 0.29552020666133955
```

#### 6 强化练习

#### 6.1 给定数字，计算其对应的阶乘

n! = n * (n-1) * (n-2) * ... * 1，例如 5! = 5*4*3*2*1。

```python
def func(n):
    ret = 1
    for i in range(1, n + 1):
        ret *= i
    return ret
```

```python
def func(n):
    ret = 1
    while n > 0:
        ret *= n
        n -= 1
    return ret
```

#### 6.2 将给定的整数倒序输出

示例：23456 -> 65432；230 -> 032；1 -> 1。

```python
def reverse_digit(num):
    if num < 10:
        print(num)
    else:
        while num > 0:
            tmp = num % 10
            print(tmp, end="")
            num //= 10

reverse_digit(23456)    # 输出 65432
```

---

### 2. 字符串详解
#### 2 定义字符串

字符串：用单引号（'）、双引号（"）、三引号（'''、"""）开头结尾。例如：

```python
s1 = "Python"
s2 = 'hat'
s3 = """project"""
```

常见错误：引号前后不一致（`s = "qimao'` → SyntaxError: EOL while scanning string literal）、引号中包含相同引号（`s = 'it's me'` → SyntaxError: invalid syntax）。解决：外层换用另一种引号，或使用转义符：

```python
s = "it's me"
s = 'it\'s me'
```

#### 3 字符串类型

1. 普通字符串：引号开头结尾，如 `"this"`；
2. 原字符串：`r` 开头，如 `r'c\c++\Python'`，不对转义符进行转义；
3. Byte 类型：`b` 开头，如 `b'test'`，一般处理编码数据、媒体数据（图片、音乐等）。

```python
s = r'c\c++\Python'
s1 = r"it\'s me"   # 不转义，结果为 "it\\'s me"
```

#### 4 编码格式

Unicode 为每个字符设定了统一且唯一的二进制编码，是 Python 3 默认编码格式。常见编码格式：gbk、utf-8、utf-16、gb2312 等。编码与解码必须使用一致的格式：

```python
s = "香蕉"
s1 = s.encode('utf-8')        # 编码：str -> bytes
print(type(s1), s1)           # <class 'bytes'> b'\xe9\xa6\x99\xe8\x95\x89'
print(s1.decode('utf-8'))     # 解码格式不一致报 UnicodeDecodeError
```

#### 5 创建字符串

#### 5.1 使用 % 格式化

`%s`、`%d` 等为占位符：

```python
user_info = "name=%s, age=%d" % ("sun", 14)
```

| 占位符 | 说明 |
|---|---|
| %s | 对象 str 方法的返回值（一般选择这种方式） |
| %r | 对象 repr 方法的返回值 |
| %d、%i | 数字格式化 |
| %f | 浮点数格式化 |
| %.nf | 浮点数保留 n 位小数 |
| %x、%X | 数字格式化为 16 进制（x/X 大小写） |
| %c | 格式化字符及其 ASCII 码 |
| %e | 科学计数法表示的浮点数 |

```python
s = '%.2f' % (1 / 3)   # '0.33'
```

#### 5.2 f 字符串

Python 3.6 新增语法，字符串以 f 或 F 开头，`f'{var}'` 中的变量必须已定义：

```python
hero_names = ["程咬金", "马超", "蔡文姬", "王昭君", "曹操"]
hero_types = ["坦克", "刺客", "游走", "法师", "战士"]
for name, t in zip(hero_names, hero_types):
    print(f"{name}:{t}")
```

#### 6 字符串相关函数

| 函数 | 说明 |
|---|---|
| str(object='') | 将对象转成字符串对象 |
| sorted(iterable, key=None, reverse=False) | 对迭代对象排序，返回列表 |
| ord(c) | 将字符转成 ASCII 码 |
| chr(i) | 将 ASCII 码转成字符 |
| int(str) / float(str) | 将字符串转成数字/浮点数 |

```python
str(10)          # '10'
for char in ['a', 'z', 'c']:
    print(char, ord(char))
```

```python
def func(start, end):
    s = ""
    for val in range(ord(start), ord(end) + 1):
        s += chr(val)
    return s

func("d", "z")   # 'defghijklmnopqrstuvwxyz'
```

#### 7 字符串相关方法

#### 7.1 查找

| 方法 | 说明 |
|---|---|
| S.find(sub[, start[, end]]) | 从前向后查找，返回 sub 第一次出现的位置，不存在返回 -1 |
| S.rfind(sub[, start[, end]]) | 从后向前查找，功能同上 |
| S.index(sub[, start[, end]]) | 功能同 find，区别：子串不存在时抛异常 |
| S.count(sub[, start[, end]]) | 返回子串在 S 中出现的次数 |

start 与 end 用于限定查找范围。示例：解析小米 11 的价格。

```python
phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'
start = phoneprice.find("小米11:")
end = phoneprice.find(",", 13)
phoneprice[start + len("小米11:"):end]   # '3599'
```

#### 7.2 替换

| 方法 | 说明 |
|---|---|
| S.replace(old, new[, count]) | 将 old 用 new 替换，count 为替换数量，默认替换所有 |

```python
s = "age:9899"
s.replace("9", "*", 1)   # 'age:*899'
```

#### 7.3 切分

| 方法 | 说明 |
|---|---|
| S.split(sep=None, maxsplit=-1) | 从前向后通过 sep 切分，返回子串组成的列表 |
| S.rsplit(sep=None, maxsplit=-1) | 从后向前切分，功能同上 |
| sep | 分隔符，默认为所有空字符 |
| maxsplit | 指定切分数量，默认全部切分 |

```python
skills = "python C++ C Java Mysql Hive"
len(skills.split())   # 6

url = "http://i1.umei.cc/uploads/tu/201711/9999/6e312a86a7.jpg"
pic_name = url.rsplit("/", 1)[-1]   # '6e312a86a7.jpg'
pic_name.split(".")[-1]             # 'jpg'
```

#### 7.4 拼接

| 方法 | 说明 |
|---|---|
| S.join(iterable) | 使用 S 将迭代对象中的字符串元素拼接成新字符串 |

```python
skills = ['c++', 'Python', 'Java']
"/".join(skills)   # 'c++/Python/Java'
```

#### 7.5 strip 方法

| 方法 | 说明 |
|---|---|
| S.strip(chars=None) | 从 S 头尾删除在 chars 中的元素，遇到不在 chars 中的元素停止 |
| S.lstrip(chars=None) / S.rstrip(chars=None) | 从开始/结尾位置处理，功能同上 |
| chars | 指定字符集，默认为空白字符 |

```python
s = " \n msg "
s.strip()   # 'msg'

s = "#-msg#-"
s.strip("-#")    # 'msg'
s.lstrip("#-")   # 'msg#-'
```

#### 7.6 开头结尾判断

| 方法 | 说明 |
|---|---|
| S.startswith(prefix[, start[, end]]) | S 以指定子串开头返回 True，否则返回 False |
| S.endswith(suffix[, start[, end]]) | S 以指定子串结尾返回 True，否则返回 False |

示例：过滤出所有小米手机。

```python
listphone = ['xiaomi11', 'huaweimeta20', 'xiaomi11Pro', 'xiaomi10']
for phone in listphone:
    if phone.startswith('xiaomi'):
        print(phone)
```

#### 7.7 大小写转换

| 方法 | 说明 |
|---|---|
| S.lower() / S.upper() | 全部转为小写/大写 |
| S.title() | 每个单词首字母大写，其他小写 |
| S.capitalize() | 首字母大写，其他小写 |
| S.swapcase() | 大小写互换 |

```python
s = 'Python CookBook'
s.lower()   # 'python cookbook'
s.title()   # 'Python Cookbook'
```

#### 7.8 format 方法

1. 使用 `{}` 代替 `%`，参数位置与个数不受限制；
2. 指定位置 `{n}` 对应第 n 个参数；
3. 指定参数名 `{name}`。

```python
f = '{} age is {}'
print(f.format('sun', 18))   # sun age is 18

f = '{1} age is {0}'         # {1}对应zhang，{0}对应20
print(f.format(20, 'zhang'))   # zhang age is 20

f = '{name} age is {age}'    # 指定参数名
print(f.format(name='zhao', age=20))   # zhao age is 20
```

#### 7.9 字符串判断方法

| 方法 | 说明 |
|---|---|
| S.isalpha() | 判断所有字符是否为字母 |
| S.isdigit() | 判断所有字符是否为数字 |
| S.islower() / S.isupper() | 判断所有字符是否为小/大写字母 |
| S.isspace() | 判断所有字符是否为空格 |
| S.istitle() | 判断所有单词首字母是否大写且其他字母小写 |

```python
"12345".isdigit()   # True
"abcd1".isalpha()   # False
```

---

### 3. 列表
#### 2 列表基础

1. 定义方式：`[value1, value2, ...]`
2. 列表是容器，可存放任意对象，支持修改、插入、删除（可变数据结构）。

#### 2.1 列表创建方式

1. 直接定义：`list1 = [1, '1', '2', 3]`
2. 多维列表：`list2 = [1, 2, 3, ['a', 'b', 'c']]`
3. 使用 `list` 函数：`list(iterable=(), /)`

#### 2.2 列表遍历

1. `while` + 索引或 `for` 循环遍历；
2. 多维列表访问：`list2[3][0]`。

#### 2.3 列表修改

列表可变，修改元素不改变列表对象本身。

#### 3 列表相关函数

| 函数 | 说明 |
|---|---|
| `list(iterable=(), /)` | 将可迭代对象转成列表 |
| `max/min(iterable, [key=func])` | 获取最大/最小值 |
| `len(obj)` | 获取长度 |
| `sum(iterable, start=0, /)` | 迭代对象求和，元素必须为数字 |

#### 4 列表相关方法

#### 4.1 列表中添加元素

| 方法 | 说明 |
|---|---|
| `l.append(obj)` | 在列表尾部添加元素 |
| `l.insert(index, obj)` | 在指定索引插入元素 |
| `l.extend(iterable)` | 将可迭代对象元素添加到尾部 |

#### 4.2 列表统计与查找

| 方法 | 说明 |
|---|---|
| `L.count(value)` | 统计 value 出现次数 |
| `L.index(value, [start, [stop]])` | 返回第一次出现的位置，不存在抛异常 |

#### 4.3 列表删除

| 方法 | 说明 |
|---|---|
| `l.pop(index=-1, /)` | 删除并返回对应值，默认 -1（尾部） |
| `l.remove(value, /)` | 删除第一次出现的 value，不存在抛异常 |
| `l.clear()` | 清空列表 |

#### 4.4 列表陷阱

遍历时动态删除元素达不到预期，正确方式：while + 内层循环，删除后重新扫描。

#### 5 元组

元组与列表类似，但不可变。

#### 5.1 创建元组

1. `t1 = (1, 2, 3)`（括号可省略：`1, 2, 3`）
2. `t2 = tuple("123")`

#### 5.2 元组常用的方法

| 方法 | 说明 |
|---|---|
| `T.count(value)` | 统计 value 出现次数 |
| `T.index(value, [start, [stop]])` | 返回第一次出现的位置，不存在抛异常 |

#### 5.3 为什么使用元组？

元组不可变，数据不希望被修改时使用。

#### 6 列表强化练习

#### 6.1 练习 1：有序列表插入元素

```python
def insert_value(listnum, val):
    for index, item in enumerate(listnum):
        if val <= item:
            listnum.insert(index, val)
            break
    else:
        listnum.append(val)
```

#### 6.2 练习 2：数字转成数字列表

```python
def num_to_list(num):
    result = []
    for value in str(num):
        result.append(int(value))
    return result
```

#### 6.3 练习 3：合并两个有序列表

要求不使用默认排序算法：

```python
def merge_list(n1, n2):
    result = []
    index1 = index2 = 0
    while index1 < len(n1) and index2 < len(n2):
        if n1[index1] <= n2[index2]:
            result.append(n1[index1])
            index1 += 1
        else:
            result.append(n2[index2])
            index2 += 1
    result.extend(n1[index1:] if index1 < len(n1) else n2[index2:])
    return result
```

---

### 4. 列表解析

#### 1 列表解析详解

列表解析：在一个序列上应用表达式，并将结果保存到列表中。

#### 2 列表解析基本使用方式

基本语法：

```python
[expr for iter in iterable]
```

| 参数 | 说明 |
| --- | --- |
| iterable | 迭代对象 |
| iter | iterable 中的元素 |
| expr | 表达式 |

执行流程：依次取出 iterable 中的每个元素作为 iter，对其执行 expr，结果依次放入新列表。

示例：

```python
[val for val in range(1, 6)]      # [1, 2, 3, 4, 5]
[val ** 2 for val in range(1, 6)] # [1, 4, 9, 16, 25]
[str(val) for val in range(0, 6)] # ['0', '1', '2', '3', '4', '5']
[int(val) for val in str(520)]    # [5, 2, 0]
```

#### 3 列表解析与判断条件

基本语法：

```python
[expr(value) for value in iter if cond_expr(value)]
```

执行过程：依次取出 iter 中的元素，先判断 cond_expr(value)，条件成立才执行 expr(value) 并放入新列表。

生成 1~100 之间的偶数：

```python
[val for val in range(1, 101) if val % 2 == 0]
```

过滤出成绩大于等于 60 的成绩：

```python
scores = [59, 100, 20, 30, 80]
[score for score in scores if score >= 60]  # [100, 80]
[score >= 60 for score in scores]           # [False, True, False, False, True]
```

统计歌词中每个单词的长度与总长：

```python
words = """When I was young I'd listen to the radio
Waiting for my favorite songs
When they played I'd sing along,
It made me smile."""

word_len = [len(word) for word in words.split()]
sum(word_len)  # 98
```

#### 4 多重循环列表解析

基本语法：

```python
[expr(v1, v2) for v1 in iters1 for v2 in iters2]
```

执行过程：
1. 取 v1；
2. 依次取 v2；
3. 执行 expr(v1, v2)；
4. 重复步骤 1~3。

示例：

```python
[(v1, v2) for v1 in range(1, 4) for v2 in range(1, 4)]
# [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

[v1 * v2 for v1 in range(1, 4) for v2 in range(1, 4)]
# [1, 2, 3, 2, 4, 6, 3, 6, 9]
```

使用列表解析生成 1~9 乘法口诀：

```python
res = [f"{j}*{i}={i * j}" for i in range(1, 10) for j in range(1, 10) if i >= j]
# ['1*1=1', '1*2=2', '2*2=4', '1*3=3', ..., '9*9=81']
```

---

### 5. 序列

#### 2 序列

#### 2.2 序列结构

注意：

1. 索引起始值为：0
2. 索引最大值：(序列长度)-1
3. 负向索引，最后一个元素索引为：-1

#### 2.3 序列访问方式

基本语法：

```python
s = "helloCoCo"
s[0]    # 第一个元素
s[-1]   # 最后一个元素
s[:2]   # 切片操作
s[2:]
```

注意：

1. 序列访问不能越界（越界抛出 IndexError: string index out of range）
2. 重点理解切片操作，灵活使用索引

#### 2.5 序列遍历

遍历方式：

1. 使用 for 循环
2. 使用 while 循环

```python
for val in s:
    print(val)
```

#### 2.6 序列运算符

常见操作：

1. 比较运算符
2. not 操作
3. 加法操作
4. 乘法操作

#### 2.7 序列相关函数

序列支持通用函数：

| 函数 | 说明 |
|---|---|
| len(obj) | 获取可迭代对象长度 |
| max(iterable, *[, default=obj, key=func]) | 获取可迭代对象中最大值，func 为元素处理函数 |
| min(iterable, *[, default=obj, key=func]) | 获取可迭代对象中最小值，func 为元素处理函数 |
| val in seq | val 在 seq 中返回 True，否则返回 False |
| val not in seq | val 不在 seq 中返回 True，否则返回 False |
| all(iterable, /) | 若 iter 中每个对象 x 的 bool(x) 都为真，返回 True，否则返回 False |
| any(iterable, /) | 若 iter 中至少一个对象 x 的 bool(x) 为真，返回 True，否则返回 False |
| zip(*iterables) | 将多个可迭代对象合并，返回 zip 对象 |
| sorted(iterable, /, *, key=None, reverse=False) | 对可迭代对象排序，默认从小到大，返回列表 |

#### 2.8 理解 max、min 中的 key

```python
vals = [1, -10, 3, -11, 8, -3]
max(vals, key=abs), max(vals)
```

对 key 的理解：

1. 设置 key 函数
2. 每个元素使用 key 函数进行处理
3. max、min 函数根据处理后的结果选择最大或最小值
4. 返回最大最小值对应的元素

---

### 6. 字典

#### 字典介绍

- 字典是 Python 中唯一的映射型数据结构，定义形式为 `{key1: value, key2: value}`，key 在字典中唯一；
- 字典是可变容器，可存储任意类型对象；
- Python 3.6+ 中字典保持插入顺序。

```python
user_info = {"name": "张", "sex": "male", "age": "28"}
user_info["name"]   # '张'
```

#### 字典 key 要求

key 必须唯一且可 hash（不可变类型）；重复 key 后者覆盖前者；hash 值相同的 key（如 1 与 1.0）视为同一 key。

```python
info = {"id": "8001", "port": 80, "port": 8001}
info                # {'id': '8001', 'port': 8001}

dvalue = {1: 'one', 1.0: '1'}
dvalue              # {1: '1'}，hash(1) == hash(1.0)

d = {[]: 1}         # TypeError: unhashable type: 'list'
```

#### 字典访问

- 访问单个元素：`d[key]`，key 不存在时抛出 KeyError；
- 遍历：`for key in d:` 依次遍历所有 key。

```python
info["id"]          # '8001'
info["sex"]         # KeyError: 'sex'

for key in info:
    print(key, info[key])
```

#### 字典修改

语法 `d[key] = value`：key 存在则更新，不存在则添加。

```python
info = {"id": "8001", "port": 8001}
info["id"] = 800
info                # {'id': 800, 'port': 8001}
```

#### 字典相关函数

创建字典：

- `dict()`：创建空字典；
- `dict(mapping)`：由可迭代对象创建字典（每个子元素必须恰好包含两个元素）。

```python
d = {}
d['id'] = 9527

d1 = dict([['name', 'sun'], ['score', 90]])  # 二维列表
d3 = dict([(1, 2), (3, 4)])                  # 元组列表
d2 = dict(['12', '34'])                      # 字符串列表
dict(zip(["name", "age"], ["li", 18]))       # {'name': 'li', 'age': 18}
```

其他函数：

| 函数 | 说明 |
|---|---|
| len(obj) | 返回字典长度 |
| sum(iterable) | 对字典所有 key 求和 |
| max/min(iterable, key=func) | 获取字典 key 的最大值/最小值 |
| key in dict | 判断 key 是否在字典中 |

```python
d = dict([(1, 2), (3, 4)])
len(d)      # 2
sum(d)      # 4
max(d)      # 3
1 in d      # True
5 not in d  # True
```

#### 字典相关方法

#### fromkeys

`dict.fromkeys(iterable, value=None, /)`：以可迭代对象的每个元素为 key 创建字典，value 为所有 key 的默认值（默认 None）。

```python
dict.fromkeys(range(1, 10), 0)   # {1: 0, 2: 0, ..., 9: 0}
dict.fromkeys("abc", 1)          # {'a': 1, 'b': 1, 'c': 1}
```

#### 获取 key 和 value

| 方法 | 说明 |
|---|---|
| D.keys() | 获取字典所有 key |
| D.values() | 获取字典所有 value |
| D.items() | 获取所有键值对 |

```python
user_info = dict([('name', 'sun'), ('age', 18)])
list(user_info.keys())          # ['name', 'age']
user_info.values()              # dict_values(['sun', 18])
for k, v in user_info.items():
    print(k, v)

user_kpi = {"Q1": 90, "Q2": 80, "Q3": 89, "Q4": 85}
sum(user_kpi.values()) / len(user_kpi)   # 86.0
```

#### get

`dict.get(key, default=None)`：返回 key 对应的值，key 不存在时返回 default（不抛异常）。

```python
user_kpi = {"Q1": 90, "Q2": 80, "Q3": 89}
user_kpi.get("Q1")      # 90
user_kpi.get("Q4", -1)  # -1
user_kpi["Q4"]          # KeyError: 'Q4'
```

#### setdefault

`dict.setdefault(key, default=None)`：key 存在则返回其值且不修改；key 不存在则添加 {key: default} 并返回 default。

```python
user_kpi = {"Q1": 90, "Q2": 80, "Q3": 89}
user_kpi.setdefault("Q1", 80)   # 90，已存在不修改
user_kpi.setdefault("Q4", 96)   # 96，添加 {'Q4': 96}
user_kpi                        # {'Q1': 90, 'Q2': 80, 'Q3': 89, 'Q4': 96}
```

#### 删除

| 方法 | 说明 |
|---|---|
| D.pop(k[, d]) | 返回并删除 k 对应的元素；k 不存在且给出 d 时返回 d，否则抛 KeyError |
| D.popitem() | 返回并删除一组键值对 |
| D.clear() | 清空字典 |

```python
order_info = {"id": 8566, "product_name": "pc", "channel": "douyin", "price": 999}
order_info.pop("price")       # 999
order_info.pop("price", -1)   # -1（k 不存在返回默认值）
```

#### 更新

`D.update([E, ]**F)`：用字典 E 或可迭代键值对更新/添加多个元素。

```python
user_kpi = {"Q1": 90, "Q2": 80, "Q3": 89}
new_kpi = {"Q1": 80, "Q4": 90}
user_kpi.update(new_kpi)
user_kpi    # {'Q1': 80, 'Q2': 80, 'Q3': 89, 'Q4': 90}
```

#### 练习

#### 统计字符出现次数

```python
def count_char(s):
    cinfo = {}
    for c in s:
        if cinfo.get(c, 0):
            cinfo[c] += 1
        else:
            cinfo[c] = 1
    return cinfo

count_char("aabbccccddddeeee")
# {'a': 2, 'b': 2, 'c': 4, 'd': 4, 'e': 4}
```

#### 删除字典中指定数据

删除 KPI 评分小于 6 的员工信息（遍历时修改字典需先复制 key 列表）。

```python
kpi_info = {
    1001: {"score": 8.9, "name": "sun"},
    1002: {"score": 8, "name": "zhang"},
    1003: {"score": 5.9, "name": "zhao"},
    1004: {"score": 4.2, "name": "li"},
    1005: {"score": 7, "name": "hao"},
}

for k in list(kpi_info.keys()):
    if kpi_info[k]["score"] < 6:
        kpi_info.pop(k)
```

---

### 7. 集合

#### 2 集合

集合是一个无序的不重复元素序列。

#### 2.1 定义集合

```python
s1 = {val1, val2, val3, ...}
s2 = set(iter)
```

集合要点：

1. 集合元素不重复；
2. 集合不支持索引与切片操作。

#### 2.2 集合基本操作

```python
s = {'apple', 'banana', 'pear'}
# 集合长度
print(len(s))
# 判断是否存在
print('banana' in s)
# 遍历集合
for val in s:
    print(val)
```

利用集合元素不重复的特性可以对列表去重，`list(set(vlist))` 结果为 `[1, 2, 3, 5]`：

```python
vlist = [1, 1, 2, 3, 5, 5]
list(set(vlist))
```

#### 3 集合相关方法

| 方法 | 说明 |
|---|---|
| add(x) | 在集合中添加元素 |
| discard(x) | 删除集合中元素x |
| pop() | 随机删除一个元素 |
| remove(x) | 删除集合中指定元素，x必须存在于S中 |
| clear() | 清空集合 |
| copy() | 拷贝集合 |
| difference(S1, S2, ...) | 返回S与其他集合的差 |
| difference_update(S1, S2, ...) | 更新S为S与S1, S2, ...的差 |
| intersection(S1, S2, ...) | 返回S与其他集合的交集 |
| intersection_update(S1, S2, ...) | 更新S为S与其他集合的交集 |
| isdisjoint(S1) | 两个集合有交集返回False，否则返回True |
| issubset(S1) | 判断当前集合是否是S1的子集 |
| issuperset(S1) | 判断S1是否是当前集合的子集 |
| symmetric_difference(S1) | 返回S与S1中不重复元素 |
| symmetric_difference_update(S1) | 更新S为S与S1中不重复元素 |
| union(S1, S2, ...) | 返回S与S1, S2, ...的并集 |
| update(S1, S2, ...) | 更新集合S |

---

### 8. 拷贝问题（深浅拷贝）
#### 1 Copy 问题
- 浅拷贝：只拷贝父对象，不拷贝对象内部的子对象（子对象仍是共享引用）
- 深拷贝：完全拷贝父对象及其所有子对象

#### 2 copy 模块
使用前需 `import copy`。

| 函数 | 说明 |
|---|---|
| `copy.copy(x)` | 浅拷贝 |
| `copy.deepcopy(x, memo=None, _nil=[])` | 深拷贝 |

#### 2.1 例子 1：列表构造与赋值
```python
v1 = [1, 2, 3]
v2 = list(v1)   # list() 构造新列表，相当于浅拷贝
v3 = v2         # 直接赋值，v3 与 v2 指向同一对象
```
- `id(v1) != id(v2) == id(v3)`：`list(v1)` 生成新对象，`v3 = v2` 只是新增引用。
- 修改 `v1[1] = 10` 后：`v1 = [1, 10, 3]`，`v2 = v3 = [1, 2, 3]`，修改 v1 不影响 v2、v3。

#### 2.2 例子 2：浅拷贝的问题（子对象共享）
```python
v4 = [1, "test", [2, 3, 4]]
v5 = list(v4)   # 浅拷贝
```
- `id(v4) != id(v5)`：外层是独立的新对象。
- `v4[0] = -1` 不影响 `v5[0]`，`v5 = [1, 'test', [2, 3, 4]]`。
- `v4[2][0] = 10` 会同时改变 `v5[2][0]`：内层 `[2, 3, 4]` 是 v4、v5 共享的同一个子对象，修改后 `v4 = v5 = [1, 'test', [10, 3, 4]]`。

#### 2.3 例子 3：深拷贝
```python
import copy

tmp1 = [1, [2, 3]]
tmp2 = copy.deepcopy(tmp1)
```
- `id(tmp1[1]) != id(tmp2[1])`：内层子对象也被完整复制，不再共享。
- `tmp1[1][0] = -10` 后：`tmp1 = [1, [-10, 3]]`，`tmp2 = [1, [2, 3]]`，互不影响。

## 第二部分 Python 常用模块
### 9. 模块与导入
#### 2 模块与导入
模块：每个 Python 文件都是一个独立的模块。工作中可以将相同功能的代码放到一个文件中，不同功能放到不同文件中，便于代码维护；模块引入命名空间与作用域。

#### 2.1 导入方式
语法：

| 语句 | 说明 |
|---|---|
| `import 模块` | 导入整个模块 |
| `from 模块 import xxx` | 导入指定的属性 |
| `from 模块 import xxx, xxx` | 导入多个属性 |
| `import 模块 as 别名` | 导入后起别名 |
| `from 模块 import xxx as 别名1, xxx as 别名2` | 导入指定属性并起别名 |

```python
import os
from functools import reduce
import time as tm
from random import randint, randrange
from os.path import join as os_join
```

#### 2.2 导入过程
模块导入要点：
1. 模块在导入时会被加载，加载过程中会被执行；
2. 模块可以被导入多次，但是只会加载 1 次。

问题：模块中一般带有测试代码，如何使测试代码在导入时不执行？（见 2.4 __name__ 变量）

#### 2.3 导入搜索路径
查找过程：
1. 在当前目录下搜索该模块；
2. 在环境变量 PYTHONPATH 指定的路径列表中依次搜索；
3. 在 Python 安装路径的 lib 库中搜索。

具体可查看 `sys.path` 的值：

```python
import sys
sys.path
```

程序运行时需要导入指定模块，可以将路径添加到 `sys.path` 中。

#### 2.4 __name__ 变量
1. 文件被执行时：`__name__` 值为 `__main__`；
2. 文件被导入时：`__name__` 值为模块名。

需求：文件被执行时执行测试代码，作为模块被导入时不执行测试代码：

```python
def func_add(x, y):
    return x + y

# 通过 __name__ 的值判断是否被导入
if __name__ == "__main__":
    print("test func_add(1, 2)=%d" % func_add(1, 2))
```

#### 3 包
#### 3.1 包的概念
包：是一个包含 `__init__.py` 文件的文件夹，作用：更好地管理源码。

#### 3.2 相对导入与绝对导入
绝对导入语法：

```python
import 模块
from 模块 import 属性
```

相对导入：在包内部进行导入，基本语法：

```python
from . 模块 import xxx
from .. 模块 import xxx
```

注意：
- `.` 代表当前目录
- `..` 代表上一级目录
- `...` 代表上上级目录，依次类推

绝对导入：一个模块只能导入自身的子模块，或和它的顶层模块同级别的模块及其子模块；
相对导入：一个模块必须有包结构，且只能导入它的顶层模块内部的模块。

---

### 10. collections 模块

collections 模块扩展了 dict、list、set、tuple，主要介绍 Counter、defaultdict、OrderedDict、namedtuple。

#### Counter

Counter 是字典的子类，提供可哈希对象的计数功能。

| 方法 | 说明 |
|---|---|
| c = Counter(*args, **kwds) | 创建 Counter 对象 |
| c.elements() | 所有元素的迭代器，按出现次数排序 |
| c.most_common(n=None) | 出现次数最多的前 N 个元素 |
| c.subtract(*args, **kwds) | 从迭代对象减去元素 |
| c.update(*args, **kwds) | 从迭代对象增加元素 |

#### defaultdict

defaultdict(default_factory)：为查询不存在的 key 提供默认值。

```python
from collections import defaultdict
d = defaultdict(int)  # 默认值 0
print(d['A'])         # 不存在的 key 返回 0
d['B'] += 1
```

#### OrderedDict

Python 中字典无序；OrderedDict 保留添加顺序，操作与 dict 类似。

```python
from collections import OrderedDict
d = OrderedDict()
d['key1'] = 'value1'
d['key2'] = 'value2'
d['key3'] = 'value3'
print(d)
```

#### namedtuple

namedtuple：使用属性方式访问元素。

```python
from collections import namedtuple
Person = namedtuple('Person', ['name', 'age'])
Man = namedtuple('Man', 'name,age')
Woman = namedtuple('Woman', 'name age')
p = Person('sun', 15)
print(p.name, p.age)
```

---

### 11. 随机数模块

#### 1.1 模块导入

```python
import xxx          # 导入模块
from xxxx import xx # 在模块中导入某个属性
import xxxx as xx   # 导入之后起别名
```

#### 1.2 random模块主要方法

| 方法 | 说明 |
|---|---|
| random() | 产生 [0,1] 之间随机浮点数 |
| uniform(a, b) | 产生 (min(a,b), max(a,b)) 之间随机浮点数 |
| randint(a, b) | 产生 [a,b] 之间随机整数 |
| seed(a=None, version=2) | 设置随机数生成器的种子 |
| randrange([start], stop[, step]) | 在指定范围内，按 step 递增的集合中取一个随机数，step 缺省值为 1 |

```python
random.random()
random.uniform(10, 1)
random.seed(0)
random.randint(0, 10)
random.randrange(0, 11, 2)
```

#### 2 猜数字小游戏

1. 游戏开始每次产生随机数字
2. 读取用户输入，如果猜中，提示中奖
3. 如果猜错，进行合理的提示

```python
def guess_num():
    x = randint(1, 100)
    while True:
        tmp = input("输入数字：")
        tmp = int(tmp)
        if tmp == x:
            print("猜中了")
            break
        elif tmp > x:
            print("输入过大")
        else:
            print("输入过小")
```

#### 3 生成4随机数字验证码

#### 3.2 使用PIL模块生成随机码图片

安装：`pip install pillow`

```python
from PIL import Image, ImageDraw, ImageFont

def getRandomColor():
    '''获取一个随机颜色(r,g,b)格式的'''
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return (c1, c2, c3)

def createRandomImage(s):
    # 获取一个Image对象，参数:RGB模式,宽,高，随机颜色
    image = Image.new('RGB', (100, 30), getRandomColor())
    # 创建一个Draw对象
    draw = ImageDraw.Draw(image)
    # 创建字体，字体与字体大小
    font = ImageFont.truetype(r"C:\Windows\Fonts\Arial\arial.ttf", size=32)
    # 在图片上写东西,参数是：定位，字符串，颜色，字体
    draw.text((15, 0), s, getRandomColor(), font=font)
    return image

createRandomImage("1235")
```

---

### 12. 时间处理

#### time 模块

| 方法 | 说明 |
|---|---|
| time.time() / time.time_ns() | 返回当前时间戳，浮点数 / 纳秒时间戳，整数 |
| time.localtime([secs]) / time.gmtime([secs]) | 时间戳转 struct_time（本时区 / UTC 0 时区），secs 为空时取当前时间 |
| time.mktime(tuple) | struct_time 转时间戳 |
| time.strptime(string, format) / time.strftime(format[, tuple]) | 字符串转 struct_time / struct_time 转字符串 |
| time.asctime([tuple]) / time.ctime(seconds) | 转可读时间字符串，如 'Fri Jan 21 18:06:51 2022' |

struct_time 字段：

| 字段 | 说明 |
|---|---|
| tm_year / tm_mon / tm_mday | 年 / 月 / 日 |
| tm_hour / tm_min / tm_sec | 时 / 分 / 秒 |
| tm_wday / tm_yday | 星期（0-6，周日为 0）/ 今年第几天 |
| tm_isdst | 是否夏令时 |

strftime / strptime 的 format 格式：

| 格式 | 说明 |
|---|---|
| %Y / %y | 年份 [xxxx] / [xx] |
| %m / %d | 月份 [01, 12] / 日期 [01, 31] |
| %H / %I / %S | 小时 [00, 23] / [00, 12] / 秒数 [00, 59] |
| %p / %w | AM 或 PM / 星期（0-6，0：周日） |
| %x / %X | 日期（月/日/年）/ 时间（时:分:秒） |
| %A / %a | 本地完整 / 简化星期名称 |
| %B / %b | 本地完整 / 简化月份名称 |

```python
import time

st = time.localtime()   # 当前时间 struct_time
s = time.strftime("%Y-%m-%d %H:%M:%S", st)  # 转字符串
ts = time.mktime(st)    # 转时间戳
st2 = time.strptime(s, "%Y-%m-%d %H:%M:%S") # 字符串转回
```

#### datetime 模块

| 类 | 说明 |
|---|---|
| datetime.date | 表示日期，属性：year、month、day |
| datetime.time | 表示时间，属性：hour、minute、second、microsecond |
| datetime.datetime | 表示日期时间 |
| datetime.timedelta | 两个 date、time、datetime 实例之间的时间间隔，分辨率可达微秒 |
| datetime.timezone | 时区相关类 |

```python
from datetime import datetime

dt_now = datetime.now()                   # 当前时间
dt_delta = dt_now - datetime(2022, 1, 23) # 时间差（timedelta）
s = dt_now.strftime("%Y-%m-%d %H:%M:%S")  # datetime -> 字符串
datetime.strptime(s, "%Y-%m-%d %H:%M:%S") # 字符串 -> datetime
```

#### calendar 模块

```python
import calendar

calendar.calendar(2022)       # 某一年日历
calendar.isleap(2018)         # 是否闰年
calendar.month(2022, 1)       # 指定年月日历
calendar.weekday(2022, 1, 1)  # 指定年月日是星期几
```

#### 案例：统计用户订单量

用户订单 CSV 文件（user_pay_order.csv），支付时间字段 order_paytime，格式如 "2019/3/28 8:32"。

注意点：utf-8 方式打开出现 \ufeff 时，编码改为 UTF-8-sig。

需求 1：按年月统计订单量。

```python
import csv
import time
from collections import Counter

def count_order_by_month(fpath):
    counter = Counter()
    f = open(fpath, encoding="UTF-8-sig")
    csv_reader = csv.DictReader(f)
    for line in csv_reader:
        ts = line.get("order_paytime")
        pay_date = time.strftime("%Y-%m", time.strptime(ts, "%Y/%m/%d %H:%M"))
        counter[pay_date] += 1
    f.close()
    return counter

for month, total in count_order_by_month(r"E:\vscode_dir\python_file\user_pay_order.csv").items():
    print(month, total)
```

需求 2：给定日期（时间字符串），统计其前后三天（共 7 天）的订单量。

过滤条件：
- 方式 1：| 给定时间日期 - 订单时间日期 | <= 3，以日期为准；
- 方式 2：| 给定时间的时间戳 - 订单时间戳 | <= 3*24*60*60，以时间戳为准，更精准。

```python
import csv
import time
from datetime import datetime

def sdate_to_date(s, format="%Y/%m/%d %H:%M"):
    return datetime.strptime(s, format).date()

def sdate_to_ts(s, format="%Y/%m/%d %H:%M"):
    return time.mktime(time.strptime(s, format))

def is_seven_interval_days(sdate, order_time, cmp_type="DAY"):
    if cmp_type == "DAY":
        return abs(sdate_to_date(sdate) - sdate_to_date(order_time)).days <= 3
    return abs(sdate_to_ts(sdate) - sdate_to_ts(order_time)) <= 3 * 24 * 60 * 60

def count_order_by_setdate(date, fpath):
    order_num = 0
    with open(fpath, encoding="UTF-8-sig") as f:
        for line in csv.DictReader(f):
            if is_seven_interval_days(date, line.get("order_paytime")):
                order_num += 1
    return order_num

count_order_by_setdate("2019/3/27 00:00", r"E:\vscode_dir\python_file\user_pay_order.csv")
```

## 第三部分 函数与函数式编程
### 13. 函数基础详解

#### 2 函数基础

#### 2.1 函数三要素与作用

三要素：函数名、参数、返回值（默认 None）。作用：封装复用。

#### 2.2 函数定义与使用

```python
def my_add(x, y):
    return x + y
```
调用需传参；接收返回值。

#### 2.3 函数名

- 规则：小写字母与下划线；函数名体现作用。
```python
# 不推荐
def func(x):
    pass
# 推荐
def is_odd(x):
    pass
```

#### 2.4 函数参数

参数类型：无参、有参、带默认值、可变长。

#### 2.4.1 无参函数

```python
import time
def get_timestamp():
    return time.time()
```

#### 2.4.2 形参函数

```python
def str_to_int(s):
    return int(s.strip()) if s.strip() else 0
```

#### 2.4.3 带默认值参数

参数可带默认值，调用时可省略（如 open）。

```python
def str_to_int(s, base=10):
    return int(s, base)
```

#### 2.4.4 位置参数与关键字参数

1. 位置参数：按定义位置传；
2. 关键字参数：按键-值传，调用更清晰。
```python
def calculate_remainder(m, n):
    return m % n
```

#### 2.4.5 可变长非关键字参数 *args

个数不定时用；`*args` 打包 tuple，调用处 `*` 拆包。

```python
def func(*args):
    pass
func(1, 2, *[3, 4])
```

#### 2.4.6 可变长关键字参数 **kwargs

个数不定时用；`**kwargs` 打包 dict，调用处 `**` 拆包。

```python
def func(**kwargs):
    pass
func(**{"name": "sun"})
```

#### 2.4.7 参数顺序

定义顺序：位置参数、`*args`、默认值参数、`**kwargs`。

```python
def func(x, y, *args, z=10, **kwargs):
    pass
```
报错：`SyntaxError: positional argument follows keyword argument`

#### 2.4.8 函数参数陷阱

默认参数只创建一次：可变对象作默认值会多次共享。

```python
def test_func(value, listv=[]):
    listv.append(value)
    return listv
```

#### 2.5 函数返回值

#### 2.5.1 默认返回值

函数默认返回 None。

```python
def func():
    pass
```

#### 2.5.2 return 返回单个结果

```python
def foo(x, y):
    return x + y
```

#### 2.5.3 返回多个对象

返回多个值实际是元组，可解包。

```python
def count_max_min(x, y, *args):
    return max(x, y, *args), min(x, y, *args)
```

#### 2.6 函数作用域

变量可应用范围；函数、类引入作用域。

#### 2.6.1 一个例子

```python
x = 10
def func():
    x = 1
    print("in:", x)
func()
print("out:", x)
```
函数内局部变量不影响全局变量。

#### 2.6.2 LEGB 原则

查找规则：Local → Enclosed → Global → Builtin。

| 名称 | 说明 |
| --- | --- |
| L | 函数内部 |
| E | 嵌套外层（闭包） |
| G | 模块全局 |
| B | 内建 |

函数内重新定义同名变量屏蔽外层变量。

#### 2.6.3 命名空间

名称到对象的映射，便于查找。

| 命名空间类别 | 记录值 |
| --- | --- |
| 局部 | 函数参数与局部变量 |
| 模块 | 全局变量、函数、导入模块 |
| 内置 | 内置函数及异常 |

`locals()`/`globals()` 查看局部/全局命名空间。

#### 2.6.4 作用域陷阱

```python
x = 10
def func():
    print(x)
    x = 20
func()
```
报错：`UnboundLocalError: local variable 'x' referenced before assignment`

原因：解释器视 x 为局部变量，但未初始化。

#### 2.6.5 global 与 nonlocal 关键字

- `global`：声明全局变量，函数内修改；
- `nonlocal`：声明嵌套外层变量，仅用于嵌套函数。
```python
x = 10
y = 10
def g_test():
    global x
    x = 20
    y = 30
g_test()
print(x, y)
```

---

### 14. 匿名函数与函数式编程

#### 1 匿名函数（lambda）

lambda 为关键字，用于定义匿名函数，基本语法：

```python
# 定义语法
func = lambda: pass
# 调用方法
func()
```

说明：

1. lambda 为关键字，其他语言（如 Java）中也有此语法；
2. 匿名函数没有名称，返回值为函数对象；
3. 匿名函数中的表达式只能由一条语句；
4. 匿名函数调用后返回值为表达式结果；
5. 匿名函数不要太复杂，要考虑后期维护。

#### 1.1 无参匿名函数

需求：返回当前的时间戳：

```python
import time
get_ts = lambda: time.time()
```

#### 1.2 带参数匿名函数

计算两个数的和、判断成绩是否及格（大于等于 60）：

```python
my_add = lambda m, n: m + n
is_pass = lambda value: True if value >= 60 else False
```

#### 1.3 可变长参数匿名函数

给定一系列数字求和：

```python
my_sum = lambda x, y, *args: x + y + sum(args)
res = my_sum(1, 2, 3, 4, 5, 6)
print(res)
```

#### 2 匿名函数应用

#### 2.1 列表排序

需求：给定数字列表，按每个元素与 5 的差的绝对值从小到大排序：

```python
nums = [-3, 2, 1, 9, 10]
nums.sort(key=lambda value: abs(5 - value), reverse=False)
print(nums)
```

#### 2.2 字典列表排序

需求：给定用户信息，按年龄从小到大排序：

```python
user_info = [
    {'name': 'sun', 'age': 15},
    {'name': 'li', 'age': 12},
    {'name': 'zhao', 'age': 13},
]
user_info.sort(key=lambda item: item.get('age'))
```

#### 3 函数式编程

三个重要函数：

| 函数 | 签名 | 作用 |
| --- | --- | --- |
| map | `map(func, *iterables)` | 对可迭代对象每个元素调用 func 处理，返回 map 对象 |
| reduce | `reduce(function, sequence[, initial])` | 依次累积归并序列元素，返回单个结果 |
| filter | `filter(function or None, iterable)` | 按条件过滤元素，返回 filter 迭代器 |

#### 3.1 map 函数

map 为惰性求值：调用 map 时并不立即计算，迭代（list()、next() 等）时才执行；传入多个 iterable 时以最短者为准，func 接收对应个数的参数。

需求：将字符串列表 ['1', '2', '3'] 转成整数列表：

```python
l = ['1', '2', '3']
r = map(int, l)
list(r)
```

需求：给定两个成绩列表，计算每个学生的总成绩：

```python
math = [90, 80, 40]
chinese = [88, 92, 77, 88]
res = map(lambda x, y, *args: x + y + sum(args), math, chinese, math)
list(res)
```

需求：根据消费记录计算消费金额：

```python
bill = ['Apple 20', 'Pear 5', 'Banana 10']
res = sum(map(lambda val: int(val.split()[-1]), bill))
```

#### 3.2 reduce 函数

```python
from functools import reduce

reduce(function, sequence[, initial])
```

基本规则：

1. function 的参数为 2 个；
2. 依次从 sequence 中取一个元素，和上一次 function 的结果作为参数，再次调用 function；
3. 设置 initial 时，第一次调用 function 的参数为 sequence 的第一个元素和 initial；
4. 未设置 initial 时，第一次调用 function 的参数为 sequence 的前两个元素。

需求：计算 1~10 的累加和与阶乘：

```python
from functools import reduce
res = reduce(lambda x, y: x + y, range(1, 11))
print(f"sum res:", res)
res = reduce(lambda x, y: x * y, range(1, 11))
print(f"factorial res:", res)
```

需求：给定一组消费数据，计算累积销售额：

```python
order_list = [
    {"数量": 2, "单价": 15},
    {"数量": 1, "单价": 10},
    {"数量": 7, "单价": 12},
    {"数量": 4, "单价": 13},
]

def count_amount(value, order):
    amount = order.get("数量") * order.get("单价")
    return value + amount

reduce(count_amount, order_list, 0)
```

#### 3.3 filter 函数

filter 使用 function 对 iterable 每个元素处理，将返回值为真的保留，返回 filter 迭代器；function 为 None 时，根据 iterable 中的元素本身判断真假。

需求：过滤列表中的偶数；过滤平均分及格（大于等于 60）的成绩：

```python
l = [1, 2, 3, 4, 5, 6]
res = filter(lambda val: val % 2 == 0, l)

report = [[90, 80], [55, 70], [50, 45]]
res = filter(lambda item: sum(item) / len(item) >= 60, report)
```

---

### 15. 递归函数
#### 1 递归基本原理

递归函数：函数在函数体内部调用自身。

特性：自己调用自己；有明确的结束条件；每层递归问题规模减小；过深会栈溢出。

优点：逻辑简单清晰；缺点：调用过深会栈溢出。

```python
def func():
    print("call func")
    func()
```

#### 2 阶乘实现

计算 1 * 2 * ... * n。

```python
def recursion(num):
    if num == 1:
        return 1
    return num * recursion(num - 1)

recursion(5)
```

#### 3 斐波那契数列

斐波那契数列：1、1、2、3、5、8、13、21、34、……，从第 3 项起每项为前两项之和。

```python
def fibo(n):
    if n <= 2:
        return 1
    return fibo(n - 1) + fibo(n - 2)
```

#### 4 遍历多维列表

遍历多维列表中的每个元素（子元素可能是列表、字符、数字）。

```python
data = [1, 2, 3, ['a', 'b', 'c', ['d', 'e', 'f']], [4, 5, 6, [7, 8, 9]]]

def sort_list(items):
    for item in items:
        if isinstance(item, list):
            sort_list(item)
        else:
            print(item, end=" ")

sort_list(data)
```

---

### 16. 闭包
#### 1 闭包

#### 1.1 基本概念

内部函数中，对在外部作用域（但不是在全局作用域）的变量进行引用，那么内部函数就被认为是闭包（closure）。

```python
# foo为外部函数
def foo():
    # m相对于bar，是外部变量
    m = 10
    # bar为内部函数
    def bar(n):
        return n * m
    # foo函数返回值：内部函数
    return bar
```

#### 1.2 闭包理解

1. 函数内部定义函数；
2. 内部函数引用外部变量；
3. 函数返回值为函数。

#### 1.3 带着问题去理解

```python
def foo():
    m = 10
    def bar(n):
        return n * m
    print("id(bar):", id(bar))
    return bar

res = foo()
print(id(res))
print(res(2))
```

#### 2 闭包应用场景

#### 2.1 n次幂计算

需求：定义一组函数，计算指定数值N次幂。

#### 2.2 新需求

传入参数可以为数字字符串；若多个类似函数都需转换，逐个修改过于繁琐。

#### 2.3 引入闭包

```python
def make_pow(m):
    def inner(n):
        return pow(int(n), m)
    return inner

make_new_pow2 = make_pow(2)
make_new_pow10 = make_pow(10)
print(make_new_pow2(2))
print(make_new_pow10(2))
```

#### 2.4 闭包应用场景

1. 封装，代码复用；
2. 装饰器。

#### 2.5 可变长参数

```python
def logfunc(level='info'):
    def logmsg(msg, *args, **kwargs):
        print(f'{level}--> : {msg}, {args},{kwargs}')
    return logmsg

debug_func = logfunc('debug')
info_func = logfunc('info')
error_func = logfunc('error')

debug_func("test", 1, 2, 3, y=10)
info_func("info")
error_func("error")
```

#### 2.6 __closure__属性

闭包函数的 `__closure__` 属性实质为元组，用于记录外部变量。

```python
attr = info_func.__closure__
print(type(attr), attr)
print("外部变量值：", attr[0].cell_contents)
```

---

### 17. 装饰器

装饰器：对函数进行处理，并返回新的函数。

#### 1 再看闭包

```python
def deco_func(level='info'):
    def foo(msg):
        print(f'{level}:{msg}')
    return foo

f = deco_func()
f('test')  # info:test
```

#### 2 一个需求

需求：定义一系列函数，对函数进行检验，前两个参数必须为整数。将重复的参数检查提取到装饰器中，避免每个函数重复编写：

```python
def deco_func(f):
    print("call deco_func")
    def inner(x, y, *args):
        print("call here inner")
        if isinstance(x, int) and isinstance(y, int):
            return f(x, y, *args)
    return inner

def make_pow(x, y, *args):
    print("call make_pow")
    return x ** y

make_pow = deco_func(make_pow)  # 手动装饰
make_pow(2, 3, 3)  # 8
```

#### 3 使用装饰器

装饰器基本语法：

```python
def deco_func(f):
    def inner():
        return f()
    return inner

@deco_func
def foo():
    pass
```

注意：

1. deco_func 为装饰器函数；
2. foo 为被装饰函数；
3. 运行此代码时 deco_func 被调用，过程：foo = deco_func(foo)；
4. 结果：foo 成为 inner 函数的外部变量，foo 指向 inner 函数。

一个案例：

```python
# 装饰器函数
def deco_func(f):
    print("call deco_func")
    def inner(x, y, *args):
        print("call here inner")
        if isinstance(x, int) and isinstance(y, int):
            return f(x, y, *args)
    return inner

# 被装饰函数，@deco_func 为装饰器语法糖
@deco_func
def make_pow(x, y, *args):
    print("call make_pow")
    return x ** y

make_pow(2, 3)  # 8
```

#### 4 装饰器带参数

需求：定义一组 log 输出函数，log 的等级分为 info、debug、error。通过外层函数接收参数并返回装饰器：

```python
def level_func(level):
    def deco_func(f):
        def inner(msg):
            msg = level + " msg:" + msg
            f(msg)
        return inner
    return deco_func

# 调用过程：1. 调用 level_func 返回 deco_func；2. @deco_func 对 log_info 进行装饰，返回 inner
@level_func("info")
def log_info(msg):
    print(msg)

@level_func("error")
def log_error(msg):
    print(msg)

log_info("this is test")   # info msg:this is test
log_error("this is test")  # error msg:this is test
```

#### 5 wraps

问题：使用装饰器后，函数名及说明会被 inner 函数覆盖。使用 functools.wraps 保留原函数元信息：

```python
from functools import wraps

def deco_func(f):
    # 使用 wraps 装饰 f，保留原函数名与文档
    @wraps(f)
    def bar():
        'this bar func'
        f()
    return bar

@deco_func
def test():
    'this is test func, do nothing'
    pass
```

---

### 18. 生成器函数

#### 1.1 带yield关键字函数

带 `yield` 关键字的函数称为生成器函数：

```python
def func():
    print("--> step 1")
    yield "hello"
    print("--> step 2")
    yield "world"
    print("--> step 3")
```

调用说明：

1. 调用 `func()` 并不会执行函数体，而是返回一个生成器对象；
2. 可以使用 `next()` 函数或 `for` 循环对生成器进行操作；

```python
gen = func()
next(gen)   # --> step 1，返回 'hello'
next(gen)   # --> step 2，返回 'world'
next(gen)   # --> step 3，抛出 StopIteration
```

#### 1.2 理解yield调用过程

1. 第一次调用 `next(gen)`，执行到 `yield` 关键字，返回其对应的对象，并保存现场；
2. 再次调用 `next(gen)`，从 `yield` 的下一条语句继续执行；
3. 重复 1~2，若函数执行完成，触发 `StopIteration` 异常；

#### 2 yield使用场景

需求：生成随机数池，可以无限取值，范围 [1, 9999]；使用 yield 完成斐波那契数列。

#### 2.1 随机数池

```python
import random

def random_pool(min_val, max_val):
    while True:
        yield random.randint(min_val, max_val)

random_gen = random_pool(1, 9999)
next(random_gen)   # 范围内的随机整数
```

#### 2.2 斐波那契数列

数列：1, 1, 2, 3, 5, 8, 13, 21, ...

```python
def fibo(n):
    a, b = 0, 1
    i = 1
    while i < n:
        i += 1
        yield b
        a, b = b, a + b

gen_fibo = fibo(10)
for val in gen_fibo:
    print(val)
```

#### 3 send方法

生成器函数可以传参并接受参数：

1. 生成器对象调用 `send` 方法传参；
2. 生成器函数通过 `value = yield obj` 接受参数；

需求：定义生成器函数，将字符串数字转成整数，若传入值为 "q"，退出：

```python
def custom():
    value = yield ''
    while value != 'q':
        value = yield int(value) * 10
```

调用过程：

1. 使用 `next(gen)` 启动生成器，返回 ""，保存现场，等待下一次调用；
2. 调用 `gen.send(参数)`，参数被 `value` 接收，执行到 `yield` 返回并保存现场；
3. 重复 1~2，若传入 "q"，循环退出，抛出 `StopIteration`；

```python
gen = custom()
next(gen)        # ''
gen.send("20")   # 200
gen.send("120")  # 1200
gen.send("q")    # StopIteration
```

## 第四部分 文件与数据持久化
### 19. 文件详解

#### 2.1 快速实现文件读取

读取流程：打开文件 → `read()` 读取全部内容 → 关闭文件。

```python
# 文件路径
fpath = r"E:\vscode_dir\python_file\test.txt"
# 打开文件
f = open(fpath, encoding="utf-8")
# 使用 read 方法读取文件所有内容
text = f.read()
print(text)
# 关闭文件
f.close()
```

#### 2.2 快速实现文件写入

写入流程：只写方式打开（文件不存在则创建）→ `write()` 写入 → 关闭文件。

```python
# 文件路径
fpath = r"E:\vscode_dir\python_file\write_test.txt"
# 只写方式打开文件
f = open(fpath, "w")
# 写入文件
line = "人生苦短，我用 Python"
text = f.write(line)
f.close()
```

#### 3.1 open 方法

签名：`open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)`

| 参数 | 说明 |
|---|---|
| file | 文件路径名称 |
| mode | 打开方式 |
| buffering | 缓存机制：1 表示使用缓存机制；-1 表示使用系统默认；0 表示不使用缓存机制，只对 Binary 有效 |
| encoding | 编码格式 |
| newline | 换行符 |

#### 3.2 打开方式

| mode | 说明 |
|---|---|
| r | 只读模式，打开后不能执行写操作 |
| w | 只写模式，文件存在被清空，打开后不能执行读操作 |
| x | 创建新文件，以只写方式打开，若文件存在报错 |
| a | 追加模式 |
| + | 读写方式打开 |
| r+ | 读写方式打开 |
| w+ | 读写方式打开，文件存在被清空 |

二进制方式：`rb`、`wb`、`xb`、`rb+`、`wb+`，适用于图片、二进制文件等场景。

#### 3.3 文件读写操作

#### 3.3.1 基本读写

- 以 `w` 方式打开文件，会将当前的文件清空；
- 写文件换行，需要在行尾添加 `"\n"`。

```python
# 定义读取函数
def read_file(fpath):
    fr = open(fpath)
    content = fr.read()
    if content:
        print(content)
    else:
        print("文件内容为空")
    fr.close()


# 定义写入函数
def write_file(fpath, content=""):
    fw = open(fpath, "w")
    if content:
        text = fw.write(content)
    fw.close()


# 连续两次写入同一文件：w 模式先清空再写入，只保留最后一次内容
fpath = r"E:\vscode_dir\python_file\write_only.txt"
line = "人生苦短，我用 Python"
write_file(fpath, line)
write_file(fpath, line)
read_file(fpath)  # 输出：人生苦短，我用 Python
write_file(fpath)  # 不写入数据，文件被清空
read_file(fpath)  # 输出：文件内容为空
```

#### 3.3.2 读写方式打开

- 以 `w+` 方式打开，文件内容清空；
- 以 `r+` 方式打开，可读可写，不清空原内容。

```python
fpath = r"E:\vscode_dir\python_file\write_read.txt"
# 打开文件
f = open(fpath, "w+")
line = "人生苦短，我用 Python"
# 写入数据
f.write(line)
# 写入后位置在文件尾部，需重置读取位置
f.seek(0, 0)
# 读取写入内容
print(f.read())
f.close()
```

#### 3.3.3 实现重复读取

实现思路：
1. 文件读取完成后，关闭文件并重新打开；
2. 使用 `seek` 方法重置读取位置。

```python
fpath = r"E:\vscode_dir\python_file\write_read.txt"
# 打开文件
f = open(fpath, "r+")
# 读取文件内容
print(f.read())
line = "自律"
# 在文件尾部追加
f.write(line)
# 重置读取位置
f.seek(0, 0)
# 读取写入内容
print(f.read())
f.close()
```

`f.seek(cookie, whence=0, /)` 参数：
- `cookie`：偏移值；
- `whence`：偏移位置，0 表示文件起始位置，1 表示文件当前位置，2 表示文件尾部。

注意：
1. 文件不是以二进制方式打开时，whence 不为 0 时 cookie 设置为 0，偏移值与文件编码格式相关；
2. 文件以二进制方式打开时，cookie 可以设置为其他正确的值。

#### 4 文件编码问题

- Windows 下默认编码格式为 cp936（如 `open(fpath, "w")` 写入，文件对象的 `encoding` 为 `'cp936'`）；
- 只读打开文件，设置的编码格式要与其保存格式一致；
- 读取时遇到 `UnicodeDecodeError`，需要检查设置的编码格式。

```python
fpath = r"E:\vscode_dir\python_file\encode_test.txt"
# 未指定编码写入，Windows 默认使用 cp936
f = open(fpath, "w")
line = "床前明月光"
f.write(line)
print(f)  # <_io.TextIOWrapper name='...' mode='w' encoding='cp936'>
f.close()

# 用 utf-8 读取 cp936 保存的文件会报错
f = open(fpath, "r", encoding="utf-8")
f.read()  # UnicodeDecodeError: 'utf-8' codec can't decode byte ...
```

#### 5 文件读写方法

#### 5.1 文件读取方式

| 方法 | 说明 |
|---|---|
| f.read(size=-1, /) | 读取文件内容，默认读取完 |
| f.readline(size=-1, /) | 读取一行，读取到 EOF 或者新的一行结束 |
| f.readlines(hint=-1, /) | 读取多行 |
| for line in f: pass | 使用 for 循环逐行遍历文件 |

#### 5.2 文件写入方式

| 方法 | 说明 |
|---|---|
| f.write(text, /) | 写入数据 |
| f.writelines(lines, /) | 一次写入多行 |

---

### 20. CSV 文件详解
#### 1 csv 文件详解与应用
#### 1.1 csv 文件
csv 文件使用纯文本存储表格数据，以指定的分隔符进行分隔，第一行一般为列名。常见场景：天池、Kaggle 等平台提供的开源数据多为 csv 文件。

#### 2 csv 模块详解
#### 2.1 csv 快速上手
前提：导入 csv 模块。

csv_reader 主要参数：

| 参数 | 说明 |
|---|---|
| delimiter | 字段分隔符，默认为逗号 "," |
| lineterminator | 换行符，默认 "\r\n" |
| quotechar | 用于包含特殊字符的字段，默认双引号 |
| quoting | 写文件时控制引号行为 |

quoting 取值：

| 取值 | 说明 |
|---|---|
| csv.QUOTE_NONNUMERIC | 数字加引号 |
| csv.QUOTE_ALL | 所有字段加引号 |
| csv.QUOTE_MINIMAL | 特殊字段加引号 |
| csv.QUOTE_NONE | 都不加引号 |

#### 2.2 csv 读取两种方式
方式一：csv.reader 逐行读取，只有数据（每行为列表）。

```python
import csv
f = open(fpath, encoding="UTF-8-sig")
csv_reader = csv.reader(f)
for line in csv_reader:
    print(line)
f.close()
```

方式二：csv.DictReader 逐行读取，读取内容为列名 + 数据（每行为字典，键为第一行列名）。

```python
import csv
f = open(fpath, encoding="UTF-8-sig")
csv_reader = csv.DictReader(f)
for line in csv_reader:
    print(line)
f.close()
```

#### 2.3 writer 方式写入
主要方法与流程：

| 方法 | 说明 |
|---|---|
| csv.writer(iterable [, dialect='excel'], ...) | 创建 writer 对象 |
| writerow(row) | 写入一行 |
| writerows(rows) | 写入多行 |

注意：
1. 一般写入的第一行为字段；
2. 写入内容的顺序要与字段对应。

```python
import csv
fpath = r"E:\vscode_dir\python_file\csv_write_test.csv"
f = open(fpath, "w")
csv_write = csv.writer(f)
cols = ["姓名", "年龄", "身高"]
line = ["奇猫", 20, 175]
lines = [["小张", 21, 178], ["小李", 21, 172]]
csv_write.writerow(cols)      # 写入字段
csv_write.writerow(line)      # 写入第一行数据
csv_write.writerows(lines)    # 写入多行数据
f.close()
```

#### 2.4 csv 写入空白行问题
造成原因：写入两次换行。

解决方式：
- 方式 1：打开文件时 open 设置 newline 为空字符串：`f = open(fpath, "w", newline="")`
- 方式 2：创建 writer 对象时指定 lineterminator 为 "\r"：`csv_write = csv.writer(f, lineterminator="\r")`

#### 2.5 DictWriter 方式写入
主要方法与流程：

| 方法 | 说明 |
|---|---|
| csv.DictWriter(f, fieldnames, restval='', ...) | 创建 DictWriter 对象，fieldnames 为字段名称 |
| writeheader() | 写入字段名 |
| writerow(rowdict) | 写入一行，数据格式为字典 |
| writerows(rowdicts) | 写入多行 |

示例：

```python
import csv
fpath = r"E:\vscode_dir\python_file\csv_dictwrite_test.csv"
f = open(fpath, "w", newline="")
cols = ["姓名", "年龄", "身高"]
csv_write = csv.DictWriter(f, fieldnames=cols)
csv_write.writeheader()          # 写入列名
line = ["奇猫", 20, 175]
lines = [["小张", 21, 178], ["小李", 21, 172]]
item = dict(zip(cols, line))     # 写入一行（字典形式）
csv_write.writerow(item)
items = [dict(zip(cols, item)) for item in lines]
csv_write.writerows(items)       # 写入多行
f.close()
```

---

### 21. Excel 文件详解
#### 1 excel 文件  
- excel 相关模块需 pip 安装，课程主要介绍 openpyxl 模块。

#### 2 openpyxl  
安装：

```python
pip install openpyxl
```

官方文档：https://openpyxl.readthedocs.io/en/stable/

| 方法/项 | 说明 |
|---|---|
| `wb = load_workbook('xx.xlsx')` | 打开 excel 文件 |
| `wb.sheetnames` | 获取所有 sheet 名称 |
| `sheet = wb[sheetname]` | 根据名称获取 sheet |
| `wb.active` | 获取当前默认的 sheet |
| `wb.close()` | 关闭文件 |
| `wb.save(filename)` | 保存 workbook 到指定路径 |

#### 2.1 excel 操作过程  
1. 打开 excel 文件；2. 获取指定 sheet；3. 对行列单元格操作；4. 保存并关闭。

#### 2.2 打开关闭 excel 文件  
完整示例见 2.4（load_workbook → 遍历 sheetnames → wb.close()）。

#### 2.3 excel 内容读取  
| 方法/项 | 说明 |
|---|---|
| `sheet["A1"]`、`cell.value` | 获取单元格及单元格数据 |
| `sheet['A']`、`sheet['A':'B']` | 获取指定列的数据单元 |
| `sheet[n]`、`sheet[m:n]` | 获取指定行的数据单元 |
| `sheet["A1":"C5"]` | 获取指定行列范围的数据单元 |
| `ws.iter_cols(min_col, max_col, min_row, max_row)` | 范围数据单元迭代器，按列返回 |
| `ws.iter_rows(min_col, max_col, min_row, max_row)` | 范围数据单元迭代器，按行返回 |
| `sheet.max_row`、`sheet.max_column` | 最大行 / 最大列 |

#### 2.4 练习：计算总销售额与笔单价  
需求：计算总销售额与笔单价（每笔成交的平均金额）。

```python
from openpyxl import load_workbook

wb = load_workbook(r'E:\vscode_dir\python_file\online_order_small.xlsx')
ws = wb.active
pay_col = ws["D2":"D10"]
pay_ment_list = [cell[0].value for cell in pay_col[2:10]]
total = sum(pay_ment_list)
pay_average = round(total / len(pay_ment_list), 2)
print(f"销售额：{total}, 笔单价：{pay_average}")
```

#### 2.5 Excel 写入  
| 方法/项 | 说明 |
|---|---|
| `wb = Workbook()` | 创建 workbook 对象 |
| `sheet = wb.active` | 获取当前 sheet |
| `wb.create_sheet(title=None, index=None)` | 创建新 sheet，title 为名称 |
| `wb.remove(sheet)` | 删除 sheet |
| `sheet['A1'] = 42` | 设置单元格值 |
| `sheet.append([1, 2, 3])` | 插入一行数据 |
| `wb.save(fpath)` | 保存数据到 Excel |

#### 3 练习：按省份统计销售额、订单量  
需求：统计每个省份的销售额、订单量，并按省份拆分为新 sheet（以省份命名）。

数据处理要点：用列号取数，新增列需改代码；将字段与数据组成字典、按字段名取值，列名不变则代码无需修改。

统计代码（核心：列名与数值构成字典）：

```python
from collections import defaultdict
from openpyxl import load_workbook

def count_order(wb):
    ws = wb.active
    rows = ws.rows
    col_names = [cell.value for cell in next(rows)]  # 跳过字段行
    result = {}
    for row in rows:
        info = dict(zip(col_names, [cell.value for cell in row]))
        if info.get("省份") and info.get("订单状态") == "交易成功":
            p = result.setdefault(info["省份"], defaultdict(float))
            p["num"] += 1
            p["payment"] = round(p["payment"] + info.get("支付金额"), 3)
    return result

print(count_order(load_workbook(r"E:\vscode_dir\python_file\online_order.xlsx")))
```

#### 3.1 按照省份进行拆分  
流程：打开原文件并新建 workbook → 读取省份 → 添加省份 sheet → 写入对应数据。
写入方式：① 数据整理好后统一写入；② 读取一行即写对应 sheet，不存在则创建（本题采用）。

#### 4 excel 格式设置  
官方文档：https://openpyxl.readthedocs.io/en/stable/styles.html

| 属性 | 说明 |
|---|---|
| `cell.value` | 获取单元格内的值 |
| `cell.font` | 设置字体样式 |
| `cell.fill` | 设置填充颜色 |
| `cell.alignment` | 设置对齐方式 |
| `cell.border` | 设置边框样式 |

填充类型：通过 `dir(fills)` 查看，值为字符串，如 `fills.FILL_PATTERN_DARKGRAY` → `darkGray`。常见：`FILL_NONE`、`FILL_SOLID`、`FILL_PATTERN_DARKGRAY`、`FILL_PATTERN_MEDIUMGRAY` 等。

#### 4.1 练习：销售数据写入并高亮前 5  
产生随机销售数据（[50, 100]，10 人各 4 个季度成绩）写入 excel，销售总额前 5 的姓名设为红色（`Font(color="FF0000")`）。步骤：产生数据 → 统计 → 排序 → 写入并设置格式。

#### 5 excel 公式与图表应用  
#### 5.1 公式应用  
将公式以字符串形式赋给单元格（核心：插入公式），如 `ws["xx"] = "=AVERAGE(xm:xm)"`。

| 公式 | 说明 |
|---|---|
| `=AVERAGE(A1,A5)` | 求均值 |
| `=SUM(A1,A6)` | 求和 |

#### 6 excel 插入图表  
参考文档：https://openpyxl.readthedocs.io/en/stable/charts/introduction.html

需求：添加柱状图，对比每个学生各科课程成绩。

```python
from openpyxl import load_workbook
from openpyxl.chart import BarChart, Reference

wb = load_workbook(r'E:\vscode_dir\python_file\test.xlsx')
ws = wb['Sheet']
chart1 = BarChart()
chart1.type = "col"
chart1.title = "成绩对比图表"
data = Reference(ws, min_col=3, min_row=1, max_row=5, max_col=4)  # 数据区域
cats = Reference(ws, min_col=2, min_row=2, max_row=5)  # 类别区域
chart1.add_data(data, titles_from_data=True)
chart1.set_categories(cats)
ws.add_chart(chart1, "A10")
wb.save(r'E:\vscode_dir\python_file\chart_bar.xlsx')
```

---

### 22. JSON 与 Pickle

#### 1. 序列化与反序列化

- 序列化：将对象转成字节流，如将机器学习模型保存到文件
- 反序列化：将字节流转成对象，如读取文件还原机器学习模型

#### 2. json

#### 2.1 json 简介

json 是轻量级的数据交换格式，采用文本序列化，有一定可读性；用于网络数据传输与存储（前后端数据交换、MySQL 存储、爬虫数据保存到 redis 等）。

#### 2.2 json 模块及主要方法

模块导入：`import json`

| 方法 | 说明 |
|---|---|
| json.dumps(obj, ...) | 对象转 JSON 字符串 |
| json.loads(s, ...) | JSON 字符串转 Python 对象 |
| json.dump(obj, fp, ...) | 对象以 JSON 格式写入文件 |
| json.load(fp, ...) | 读取 JSON 文件转成 Python 对象 |

前提：obj 对象需支持该序列化方式。

#### 2.3 示例

```python
import json

info = {"华为": "鸿蒙", "Google": "android", "Apple": "IOS"}
json_data = json.dumps(info)   # 序列化
print(json.loads(json_data))   # 反序列化
```

#### 3. pickle 模块

pickle 是 Python 特有的二进制序列化与反序列化模块，序列化后不具有可读性。模块导入：`import pickle`

| 方法 | 说明 |
|---|---|
| pickle.dumps(obj, ...) | 将对象序列化为字节流 |
| pickle.loads(data, ...) | 将字节流反序列化为对象 |
| pickle.dump(obj, file, ...) | 以字节流方式保存到文件，file 以 "wb" 打开 |
| pickle.load(file, ...) | 从文件读取字节流反序列化，file 以 "rb" 打开 |

---

### 23. INI 配置文件处理

.ini 文件（Initialization File）即初始化文件，用于存放配置信息，例如 mysql 的配置文件。ini 文件由节、键、值组成，主要操作有：获取节下面的键及对应的值；添加、修改节或者下面的键、值。

#### 1 configparser 模块

处理 ini 文件使用 configparser 模块，导入方式：

```python
from configparser import ConfigParser
```

ini 文件格式为节（section）加键值对（name=value），示例（mysql 配置）：

```python
[mysqld_safe]
socket = /var/run/mysqld/mysqld.sock
nice = 0

[mysqld]
user = mysql
pid-file = /var/run/mysqld/mysqld.pid
socket = /var/run/mysqld/mysqld.sock
port = 3306
```

ConfigParser 常用方法：

| 方法/项 | 说明 |
|---|---|
| config = ConfigParser() | 创建 ConfigParser 对象 |
| config.read(fpath, encoding='utf-8') | 导入文件 |
| config.sections() | 获取所有 section 名称 |
| config.items() | 获取所有 section 名称及内容 |
| config.has_section(section) | 判断是否包含指定 section |
| config.has_option(section, option) | 判断 section 下是否包含 option |
| config.get(section, option, *, raw=False…) | 获取 section 下 key 对应的 value |
| config.add_section(section) | 添加 section |
| config.set(section, option, value=None) | 添加 key-value |
| config.write(fp, space_around_delimiters=True) | 写入文件 |

#### 2 读取操作

```python
from configparser import ConfigParser

fpath = r'E:\vscode_dir\python_file\netconfig.ini'
config = ConfigParser()
config.read(fpath, encoding='utf-8')

# 获取所有的节
sections = config.sections()
print(sections)

# 获取所有的 item
items = list(config.items())
print(items)
```

section 与 key 判断：

```python
res = config.has_section('baidu')
print(res)

res = config.has_option('baidu', 'addr')
print(res)
```

读取值：

```python
# 通过节、键找到对应的值
baidu_src = config.get('baidu', 'src')
print("src:", baidu_src)

# 获取节
baidu = config['baidu']
# 通过节找到键对应的值
baidu_addr = baidu.get('addr')
print("addr:", baidu_addr)
```

#### 3 写入操作

```python
from configparser import ConfigParser

fpath = r'E:\vscode_dir\python_file\new_config.ini'
config = ConfigParser()
# 可以在原来基础上添加信息
# config.read(fpath, encoding='utf-8')

config.add_section('tencent')
config.set('tencent', 'addr', ' 深圳 ')
config.set('tencent', 'src', 'https://www.tencent.com/')

fwpath = r'E:\vscode_dir\python_file\netconfig1.ini'
f = open(fwpath, 'w', encoding='utf-8')
config.write(f)
f.close()
```

---

### 24. OS 模块目录处理

#### 1 文件与目录处理

OS 模块提供操作系统相关功能的函数，比如：获取系统信息、文件与目录的操作、执行系统命令等。

官方文档：https://docs.python.org/zh-cn/3.7/library/os.html

主要模块：

```python
import os
import shutil
```

#### 2 目录操作

| 函数 | 说明 |
|---|---|
| os.getcwd() | 返回表示当前工作目录 |
| os.mkdir(name) / os.rmdir(name) | 创建目录 / 删除目录 |
| os.makedirs(name) / os.removedirs(name) | 创建目录树 / 删除目录 |
| os.listdir(path=None) | 获取指定目录下所有文件目录 |
| os.rename(src, dst, ...) | 文件目录重命名 |
| os.renames(old, new) | 递归方式重命名目录或者文件 |
| os.walk(top, topdown=True, ...) | 获取指定目录下所有文件目录，返回目录树迭代器 |

## 第五部分 正则表达式
### 25. 正则表达式
#### 2 re模块

正则表达式（Regular Expression）：描述一组字符串特征的模式，用来匹配特定字符串。应用场景：验证（如用户名、密码格式）、查找、替换、切分。Python 用 re 模块处理。

#### 2.1 re详解

主要方法：

| 方法 | 说明 |
|---|---|
| re.match(pattern, string, flags=0) | 从头匹配，返回 Match 或 None |
| re.search(pattern, string, flags=0) | 查找子串，返回 Match 或 None |
| re.findall(pattern, string, flags=0) | 查找所有匹配，返回列表 |
| re.split(pattern, string, maxsplit=0, flags=0) | 切分字符串，返回列表 |
| re.sub(pattern, repl, string, count=0, flags=0) | 替换，返回新字符串 |

flag 值：

| flag | 说明 |
|---|---|
| re.I | 忽略大小写 |
| re.L | 本地化匹配 |
| re.M | 多行匹配，改变 ^ 和 $ 的行为 |
| re.S | 点匹配任意字符（含 \n） |
| re.U | 按 Unicode 解析 |
| re.X | 忽略空白字符，可加注释 |

#### 2.2 第一个案例

匹配以数字开头的字符串：

```python
import re
print(re.match(r'\d', "001_sun"))  # \d 匹配任意数字，<re.Match object; span=(0, 1), match='0'>
print(re.match(r'\d', "qimao"))    # None
```

#### 2.3 Match对象

| Match对象方法 | 说明 |
|---|---|
| m.start() / m.end() | 匹配开始、结束索引 |
| m.span() | 匹配索引起止组成的元组 |
| m.group() | 匹配的字符串 |
| m.groups() | 所有子组的元组 |
| m.groupdict() | 所有命名子组的字典 |

#### 2.4 compile方法

re.compile 将正则字符串编译为 Pattern 对象，可调用其方法完成匹配查找；循环中重复操作时推荐先编译。

#### 3 正则表达式

#### 3.1 字符匹配

| 字符 | 说明 |
|---|---|
| . | 匹配任意字符（\n 除外） |
| \ | 转义符，匹配特殊字符 |
| [...] | 匹配字符集 |
| \d / \D | 匹配数字 / 匹配非数字 |
| \s / \S | 匹配空白字符 / 匹配非空白字符 |
| \w / \W | 匹配单词字符 [a-zA-Z0-9] / 匹配非单词字符 |

#### 3.2 匹配次数

| 字符 | 说明 |
|---|---|
| * | 匹配前一个内容 0 次或无限次 |
| + | 匹配前一个内容 1 次或无限次 |
| ? | 匹配前一个内容 1 次或 0 次 |
| {m} | 匹配前一个内容 m 次 |
| {m,n} | 匹配前一个内容 m 到 n 次 |
| *?、+?、{m,n}? | 贪婪变非贪婪，尽可能少匹配 |

```python
re.match(r'A+', "AAc")               # match='AA'
re.match(r'\d{3,5}', "123456abc")    # 贪婪，match='12345'
re.match(r'[1-9]?\d$', "10")         # 100 以内的有效数字（0-99）
```

#### 3.3 边界匹配

| 字符 | 说明 |
|---|---|
| ^ / $ | 匹配开头 / 匹配结尾 |
| \A / \Z | 仅匹配文本的开头 / 结尾 |
| \b | 匹配单词边界 |
| \B | 非单词边界 |

```python
# 邮箱：数字、字母、下划线组成，长度 6~15，后缀 @qq.com
re.match(r'[\da-zA-Z_]{6,15}@qq.com$', "testbcd@qq.com")
# <re.Match object; span=(0, 14), match='testbcd@qq.com'>
```

#### 3.4 分组匹配

| 字符 | 说明 |
|---|---|
| \| | 匹配左右任意一个表达式 |
| (...) | 分组 |
| (?P<name>...) | 分组起别名 |
| \num | 引用编号为 num 的分组 |
| (?P=name) | 引用别名为 name 的分组 |

```python
# 提取文本与数字
re.findall(r'([a-z]+):(\d+)', "apple:8, pear:20, banana:10")
# [('apple', '8'), ('pear', '20'), ('banana', '10')]
```

#### 4 split与sub方法

#### 4.1 split-切分

split：按照规则对文本切分，返回列表。

```python
re.split(r'[/\\]', "python/c\\C++/Java/Php/Nodejs")
# ['python', 'c', 'C++', 'Java', 'Php', 'Nodejs']
```

#### 4.2 sub-替换

函数原型：re.sub(pattern, repl, string, count=0, flags=0)
- pattern：匹配内容；repl：替换值（字符串或函数，函数则取其返回值）；string：被替换的字符串。

```python
# 将数字替换成 ****
re.sub(r'\d+', "****", "name:sun, pwd:123456, name:zhang,pwd:667788")
# 'name:sun, pwd:****, name:zhang,pwd:****'

# repl 为函数：>=6 替换为 "A"，否则 "B"
def replace_ab(ma):
    return "A" if int(ma.group()) >= 6 else "B"

re.sub(r'\d+', replace_ab, "sun:5, li:10, zhao:7, gao:8, wang:5")
# 'sun:B, li:A, zhao:A, gao:A, wang:B'
```

#### 5 练习

#### 5.1 匹配xml

xml 语法：`<tag>内容</tag>`

```python
s = '<li>tushu</li>'
re.match(r'<(.*?)>.+?</\1>', s)
# <re.Match object; span=(0, 14), match='<li>tushu</li>'>
```

#### 5.2 提取src链接地址

```python
html = '<img src="https://ss0.bdstatic.com/=0.jpg">'
re.findall(r'src="(http.*?)"', html)
# ['https://ss0.bdstatic.com/=0.jpg']
```

#### 5.7 匹配有效的163邮箱

规则：邮箱以字母开头，由下划线、数字、字母组成，长度 8~13，以 @163.com 结尾。

```python
re.match(r'[a-zA-Z][_\da-zA-Z]{7,12}@163\.com$', 'qimao1234@163.com')
```

#### 5.8 re.I

统计 th 开头单词，不区分大小写：`re.findall(r'th[a-zA-Z]*', 'This that the who', flags=re.I)` 返回 `['This', 'that', 'the']`。

#### 5.9 re.M

多行匹配，统计代码中函数数量：

```python
code = "def func1():\n    pass\nDef func2():\n    pass"
re.findall(r'^def ', code, flags=re.M)
```

## 第六部分 错误和异常
### 26. 错误和异常
#### 2 错误与异常
错误：
- 语法错误：Python 解释器会进行提示；
- 逻辑错误：程序运行结果与预期不一致，需要自己排查。

异常：程序运行出错时，解释器给出提示并定位代码位置；也可能是运行环境问题（内存不足、网络错误等）。

| 异常 | 说明 |
|---|---|
| BaseException | 所有异常的基类 |
| Exception | 常规错误的基类 |
| NameError | 变量没定义 |
| ValueError | 参数错误 |
| SyntaxError | 语法错误 |
| ImportError | 导入错误 |
| IndexError | 索引错误 |
| ZeroDivisionError | 除 0 错误 |

#### 3 异常处理
#### 3.1 try...except
捕获指定异常；捕获类型与触发异常不一致时不能捕获，单个异常用 `except Exception as e`。

```python
try:
    try_suite
except Exception1 as e:
    except_suite1
except Exception2 as e:
    except_suite2
```

#### 3.2 try...finally
无论是否捕获异常都会执行 finally 中的语句，常用于释放资源。

```python
try:
    try_suite
except Exception as e:
    except_suite
finally:
    pass
```

#### 4 raise 与 assert
用于主动产生异常，如参数检查、程序中的逻辑错误。

- raise：主动抛出异常，语法 `raise Exception(args)`。
- assert：表达式为假时抛出 AssertionError，语法 `assert expression [, args]`。

#### 5 自定义异常类
1. 必须继承 Exception 类；
2. 通过 raise 语句主动触发。

#### 6 with/as 语句
操作上下文管理器，自动分配并释放资源；语法 `with context as var:`，context 对象必须支持上下文协议。典型场景：打开文件忘记关闭。

```python
with open(fpath) as f:
    pass
print("f closed:", f.closed)
```

#### 6.2 上下文管理
自定义类实现 `__enter__`/`__exit__` 以支持上下文管理：

```python
class TestContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
```

## 第七部分 面向对象编程
### 27. 面向对象编程
#### 1 面向对象编程
面向对象编程（OOP）将数据和方法看做一个整体。

#### 1.1 面向对象编程特征
- 封装：隐藏实现，对外提供方法；
- 抽象：提取事物的数据与行为共性；
- 继承：子类继承父类的属性和方法；
- 多态：调用不同子类产生不同行为。

#### 1.2 面向对象基本概念
- 类：具有相同属性和方法的对象的集合；
- 对象：类的实例，包含数据成员和方法；
- 实例化：创建类的具体对象；
- 类属性：类中定义的变量，所有对象均可访问；
- 实例属性：具体实例对象相关的数据；
- 方法：类中定义的函数；
- 重载：子类中重新实现父类方法。

#### 1.3 快速理解面向对象
不用面向对象时用字典、列表管理员工；用面向对象时将员工抽象成类，用对象统计管理。

#### 2 类与实例
1. 类是抽象概念，对象是具体实例；
2. Python 中类也是对象；
3. 类与实例引入命名空间与作用域。

定义类的语法：
```python
class 类名:
    pass
```

#### 2.2 类属性与实例属性
```python
class Car:
    name = "汽车"

audi = Car()
print(audi.name)  # 汽车：继承类属性
audi.name = "A6"  # 仅新增实例属性
print(audi.name)  # A6
print(Car.name)   # 汽车：类属性未变
```

注意：实际工作中不推荐直接访问与修改属性，而是通过方法访问。

#### 2.3 私有属性
以 "__" 开头的属性不能直接通过类或实例访问，只能通过接口访问与修改（如 `Car.__price` 报 AttributeError）。

#### 3 方法
#### 3.1 封装
1. 不推荐直接访问属性，通过方法（接口）访问；
2. 将行为封装成方法，对外提供接口调用；
3. 方法中可以访问或修改属性值。

#### 3.2 实例方法
实例方法第一个参数为 self，self 即实例本身，id(self) 与 id(实例) 相同。

#### 3.3 理解 self
通过 self 可访问与修改实例属性。

#### 3.4 类定义过程
1. 定义类名；2. 找共同行为与数据并定义方法；3. 实现方法并调试。

#### 3.5 实例方法实现
实例方法定义：`def method(self, ...)`，通过 self 访问与修改实例属性。

#### 4 生命周期相关三个方法
#### 4.1 __new__方法
`__new__(cls, *args, **kwargs)` 创建对象并返回实例；不显式定义时默认调用父类的 __new__，一般很少用到。

#### 4.2 __init__方法
创建实例后第一个调用的方法，用于初始化实例属性；创建类时经常添加参数，在 __init__ 中处理（如 `self.name = name`、`self.__price = price`）。

#### 4.3 __del__方法
对象销毁时调用，用于回收资源，开发中较少用到。

#### 4.4 对象生命周期流程
创建实例：先 __new__ 创建对象，再 __init__ 初始化属性；销毁时调用 __del__。

#### 5 三种方法
#### 5.1 三种方法说明
实例方法、静态方法、类方法。

#### 5.2 三种方法使用场景
1. 实例方法：只有对象能使用，最常见；
2. 静态方法：与类及实例对象无关的代码；
3. 类方法：只涉及类属性的访问与修改。

#### 5.3 收银台结算案例
所有收银台共享打折信息（类方法）与提示语（静态方法），每台收款金额不同（实例方法）。
```python
class CheckOutCounter:
    discount = 1

    def __init__(self):
        self.amount = 0

    def pay(self):
        res = self.amount * self.discount
        self.amount = 0
        return res

    @classmethod
    def set_discount(cls, discount):
        cls.discount = discount

    @staticmethod
    def voice_tip():
        print("欢迎再来")

checkout = CheckOutCounter()
checkout.amount = 10
CheckOutCounter.set_discount(0.8)
print("支付金额：", checkout.pay())  # 支付金额： 8.0
CheckOutCounter.voice_tip()
```

#### 6 property 使用
#### 6.1 属性设置与访问
实际工作中需频繁修改与访问属性，一般通过方法实现；也可用 @property 将方法转为属性方式操作（实际操作仍走方法）。

#### 6.2 property 应用
@property 是修饰方法的装饰器，将方法转成属性：
```python
class Car:
    def __init__(self, price):
        self.__price = price

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price
```

#### 7 反射相关函数
#### 7.1 反射基本概念
反射：程序访问、检测和修改自身状态或行为的能力（自省）；面向对象中通过字符串形式操作对象的属性与方法。

| 函数 | 说明 |
|---|---|
| isinstance(obj, class_or_tuple) | 判断 obj 是否是指定类的实例 |
| dir(object) | 获取对象属性 |
| hasattr(obj, name) | 判断 obj 是否有 name 属性 |
| getattr(object, name[, default]) | 获取 obj 的 name 属性 |
| setattr(obj, name, value) | 设置 obj 的 name 属性与值 |
| delattr(obj, name) | 删除 obj 的 name 属性 |

#### 7.2 反射相关函数与应用
未知属性或方法不存在时动态添加：
```python
class Circle:
    pi = 3.14

c = Circle()
count_area = lambda self: self.pi * pow(self.r, 2)

for attr, value in {"r": 10, "count_area": count_area}.items():
    if not hasattr(c, attr):
        setattr(c, attr, value)

print("圆面积：", c.count_area(c))  # 圆面积： 314.0
```

#### 8 继承
继承：子类自动继承父类的属性与方法；Python 中自定义类继承于 object 类。
优点：提高代码复用与维护性；缺点：提升代码耦合性。

#### 8.1 基本语法
单继承：`class SubClass(Parent): pass`；多继承：`class SubClass(Parent1, Parent2): pass`。

#### 8.2 一个例子：学生类
```python
class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def work(self, *args, **kwargs):
        print("in Person.work")

class student(Person):  # 继承 Person，重载 work
    def work(self, subject):
        print("I'm studying %s now" % subject)

student('sun', 16).work("math")  # I'm studying math now
```

#### 8.3 super 关键字
子类重载父类方法后，可通过 `super()` 调用父类方法，如 `super().work()` 先执行父类 work。

#### 8.4 多重继承
多重继承：`class C(A, B)`；方法查找顺序 MRO 广度优先、左边优先，如 C → A → B → object。

#### 9 特殊方法
#### 9.1 __str__ 与 __repr__
| 方法 | 说明 |
|---|---|
| __str__ | 返回类的描述字符串，主要对用户展示 |
| __repr__ | 返回字符串，主要针对开发人员展示 |

#### 9.2 自定义输出
使用 print 输出自定义格式，需定义 __str__：
```python
class Rose:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return "name:%s price:%.2f" % (self.name, self.price)
```

#### 9.3 支持运算符
算术运算符：

| 方法 | 说明 |
|---|---|
| __add__(self, other) | 加法 |
| __sub__(self, other) | 减法 |
| __mul__(self, other) | 乘法 |
| __truediv__(self, other) | 除法 |
| __mod__(self, other) | 取模 |
| __pow__(self, other) | 幂运算 |

比较运算符：`__lt__ <`、`__le__ <=`、`__gt__ >`、`__ge__ >=`、`__eq__ ==`、`__ne__ !=`。

重载上述运算符可让类（如 Rose）根据价格进行比较。

#### 10 类组合与练习
类组合：A 类的对象作为 B 类的数据属性；一个类是另一个类的组件时推荐组合，例如团队与成员。

#### 10.1 学生管理系统
需求：班级管理系统，通过班级管理学生。
1. 班级中有多名同学；学生信息包括：学号、姓名、身高、出生年月；
2. 班级提供管理接口：插入、按条件删除、按条件查询学生；
3. 班级类提供友好的菜单操作。

#### 10.4 实现过程
1. 定义 Student 类并实现方法；2. 实现 Team 类并实现方法；3. 通过 Team 管理 Student；4. 调试。

#### 10.5 菜单操作
1. 友好的提示；2. q/Q：退出；a/A：创建并添加学生；d/D：按学号删除；f/F：按学号查找；s/S：显示所有学生；c/C：删除所有学生。

---

### 28. 面向对象基础（课上练习）
#### 1 类相关语法
#### 1.1 类与实例
用 `class` 定义类，类名加括号创建实例，`isinstance()` 判断对象是否为某类的实例：
```python
class Car:
    pass

car = Car()
isinstance(car, Car)  # True
```
#### 1.2 类属性与实例属性
#### 1.2.1 属性访问
类属性在类体中直接赋值，可通过类名或实例访问：
```python
class Car:
    name = "汽车"

audi = Car()
print(Car.name)    # 汽车
print(audi.name)   # 汽车
```
#### 1.2.2 理解类与对象的命名空间与作用域
- 给实例属性赋值只写入该实例的命名空间，不影响类属性；
- 通过类名修改类属性，会影响所有未自行覆盖该属性的实例。
```python
class Car:
    name = "汽车"

audi = Car()
audi.name = "A6"     # 仅修改实例
Car.name = "汽车类"   # 修改类属性

print(Car.name)   # 汽车类
print(audi.name)  # A6
```
#### 1.2.3 私有属性
以双下划线 `__` 开头的属性会被名字修饰（name mangling），类外直接访问会抛 `AttributeError`：
```python
class Car:
    name = "car"
    __price = "unkown"

print(Car.__price)
# AttributeError: type object 'Car' has no attribute '__price'
```
#### 2 方法
方法定义在类中，第一个参数约定为 `self`（表示实例本身），可接收任意参数：
```python
class ClassName:
    def func(self, *args, **kwargs):
        pass
```
#### 2.1 方法实现
方法通过 `self` 读写实例属性。通过类名调用方法时，第一个参数必须显式传入实例对象；通过实例调用时 `self` 自动传入，二者等价：
```python
class Car:
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

audi = Car()
audi.set_name("Audi")
audi.get_name()            # 'Audi'
Car.set_name(audi, "Car")  # 等价于 audi.set_name("Car")
```
#### 3 对象生命周期
#### 3.1 `__init__` 与 `__del__`
调用顺序：`__new__` → `__init__`（初始化属性）→ 删除对象时调用 `__del__`。`__init__` 缺少必填参数会抛 `TypeError`：
```python
class Car:
    def __new__(cls, *args, **kwargs):
        print("call __new__")
        return object.__new__(cls)

    def __init__(self, name, price, color):
        print("call __init__")
        self.name = name
        self.__price = price
        self.color = color

    def __del__(self):
        print("call __del__")

audi = Car("audi", 38, "red")
del audi
# 输出顺序：__new__ → __init__ → __del__
```
#### 3.2 计算面积通用类
`@classmethod` 的第一个参数是类 `cls`，可访问类属性；`@staticmethod` 与类和实例无关，不接收 self/cls：
```python
class CountArea:
    pi = 3.14

    @classmethod
    def circular_area(cls, r):
        return cls.pi * pow(r, 2)

    @staticmethod
    def square_area(side_length):
        return side_length ** 2

CountArea.circular_area(10)  # 314.0
CountArea.square_area(10)    # 100
```
#### 3.3 收银台案例
```python
class CheckOutCounter:
    discount = 1          # 默认折扣

    def __init__(self):
        self.amount = 0   # 默认结算金额

    def scan_good(self, value, *args):
        self.amount += value + sum(args)

    def pay(self):
        return self.amount * self.discount

    @classmethod
    def set_discount(cls, discount):
        cls.discount = discount

checkout_1 = CheckOutCounter()
checkout_1.scan_good(10)
CheckOutCounter.set_discount(0.8)
payment = checkout_1.pay()   # 8.0
```
#### 4 property
#### 4.1 property 应用
`@property` 把方法转为只读属性（getter），`@price.setter` 提供赋值（setter），调用时与普通属性无异：
```python
class Car_1:
    def __init__(self, price):
        self.__price = price

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

car = Car_1(10)
car.price = 8       # 以属性方式设置价格（走 setter）
print(car.price)    # 8，以属性方式访问价格（走 getter）
```
#### 5 反射
反射通过字符串名动态操作对象的属性与方法：
- `hasattr(obj, name)`：判断对象是否有该属性/方法；
- `setattr(obj, name, value)`：动态设置属性或绑定方法；
- `getattr(obj, name)`：动态获取属性或方法。
```python
class Circle:
    pi = 3.14

c = Circle()

def count_area_func(self):
    return self.pi * pow(self.r, 2)

hasattr(c, "pi")                                     # True
setattr(Circle, "count_area_func", count_area_func)  # 给类动态添加方法
hasattr(c, "count_area_func")                        # True
setattr(c, "r", 10)                                  # 给实例动态添加属性
c.count_area_func()                                  # 314.0
```

---

### 29. 继承与反射
#### 1 继承
#### 1.1 基本语法

```python
class Parent:
    pass

class SubClass(Parent):
    pass
```

`issubclass(SubClass, Parent)` 返回 `True`；所有类都继承自 `object`，所以 `issubclass(Parent, object)` 返回 `True`。

#### 1.2 继承示例

```python
class Person:
    def __init__(self, name, age):
        print("in Person call init")
        self.__name = name
        self.__age = age

    def get_name(self):
        return self.__name

    def set_age(self, age):
        self.__age = age

    def work(self, *args, **kwargs):
        print("in Person.work")

class Student(Person):
    def work(self, *args, **kwargs):
        super().work()
        print("in Student.work")

s = Student("xiaoming", 13)
s.work()
```

子类可重写父类方法：方法同名、参数列表不同即构成覆盖，如 `def work(self, subject):`。

#### 1.3 super 关键字

```python
class student(Person):
    def __new__(cls, *args, **kwargs):
        # 调用父类 __new__
        return super().__new__(cls)

    def work(self, subject):
        super().work()   # 调用父类 work
        print("I'm studying %s now" % subject)

s1 = student('sun', 16)
s1.work("math")
```

`super()` 在子类中显式调用父类方法。

#### 1.4 多重继承

```python
class A:
    def test(self):
        print("in A test")

class B:
    def test(self):
        print("in B test")

class C(A, B):
    pass

c = C()
c.test()   # in A test：按继承顺序取第一个
```

`C.mro()` 返回方法解析顺序 `[C, A, B, object]`，决定同名方法的查找顺序。

#### 2 特殊方法
#### 2.1 自定义输出 __str__ / __repr__

未定义时，`print(obj)` 与交互式显示都是默认的 `<__main__.Rose object at 0x...>` 内存地址形式。

```python
class Rose:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        # 供 print()/str() 调用
        return "name:%s price:%.2f" % (self.name, self.price)

    def __repr__(self):
        # 供交互式显示/repr() 调用
        return "name:%s price:%.2f object at 0x%016X" % (self.name, self.price, id(self))

rose = Rose("黑玫瑰", 20)
print(rose)   # name:黑玫瑰 price:20.00
```

定义 `__add__` 等特殊方法可为实例提供运算符支持，如 `__add__(self, other)` 返回 `self.price + other.price` 即支持 `+`。

#### 2.2 比较运算符支持

```python
class Rose:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __lt__(self, other):   # 支持 <
        return self.price < other.price

    def __gt__(self, other):   # 支持 >
        return self.price > other.price

rose_red = Rose("rose", 10)
rose_black = Rose("rose", 15)
```

定义 `__lt__`、`__gt__` 等特殊方法后，类的实例即可使用对应的比较运算符。

---

### 30. 班级练习（Jupyter）

```python
class Student:
    def __init__(self, name, num) -> None:
        self.__name = name
        self.__num = num
    def __str__(self):
        return f"name:{self.__name}, num:{self.__num}"
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name
    @property
    def num(self):
        return self.__num
    @num.setter
    def num(self, num):
        self.__num = num
    @staticmethod
    def create_student():
        name = input("学生名称:")
        num = int(input("学生学号:"))
        return Student(name, num)
```

```python
class Team:
    def __init__(self, team_name, team_id) -> None:
        self.student_list = []
        self.team_name = team_name
        self.team_id = team_id
    def add_student(self, student):
        print("add student:", student)
        self.student_list.append(student)
    def find_student_by_num(self, student_num):
        for student in self.student_list:
            if student.num == student_num:
                return student
    def delete_student_by_num(self, student_num):
        for index, student in enumerate(self.student_list):
            if student.num == student_num:
                print(f"del num:{student_num}", student)
                self.student_list.pop(index)
    def dump_all(self):
        for student in self.student_list:
            print(student)
    def clear_all(self):
        self.student_list.clear()
    def add_cmd(self):
        s = Student.create_student()
        self.student_list.append(s)
    def find_cmd(self):
        num = int(input("输入查找学号:"))
        s = self.find_student_by_num(num)
        print(s)
    def delete_cmd(self):
        num = int(input("输入删除学号:"))
        self.delete_student_by_num(num)
    def menu_main(self):
        help_info = '''
输入q/Q:退出；
输入a/A:创建并添加学生；
输入d/D:根据输入学号删除学生；
输入f/F:根据输入学号查找学生；
输入s/S:显示所有学生信息；
输入c/C:删除所有学生信息；
'''
        cmd_map = {'a': "add_cmd", 'f': 'find_cmd',
                   'd': 'delete_cmd', 'c': 'clear_all',
                   's': 'dump_all'}
        while True:
            print(help_info)
            cmd = input("输入命令:")
            cmd = cmd.lower()
            if cmd == 'q':
                break
            action = cmd_map.get(cmd)
            if action:
                getattr(self, action)()
```

## 第八部分 并发编程
### 31. 多进程详解与应用

#### 进程概念
进程：程序运行的实例（执行的过程），是系统调度与资源分配的基本单元。常见进程如手机应用、PC 应用（浏览器、游戏）等。

#### 2.1 进程相关知识点
- 进程 ID：程序运行的唯一标识。
- 进程相关模块：`multiprocessing`；`os.getpid()` 获取当前进程 ID，`os.getppid()` 获取父进程 ID。

Process 方法：

| 方法 | 说明 |
|---|---|
| p.start() | 创建进程，执行进程函数 |
| p.run() | 用当前进程执行进程函数 |
| p.join() | 等待进程执行完成 |
| p.is_alive() | 进程是否存活 |

#### 2.2 创建进程
构造：`multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)`

| 参数 | 说明 |
|---|---|
| target | 进程函数 |
| name | 进程名称 |
| args / kwargs | 位置参数 / 关键字参数 |
| daemon | 守护进程，须在 start() 前设置；为 True 时父进程退出后子进程也退出 |

#### 2.3 父子进程理解
子进程是父进程的拷贝，继承父进程的所有资源；但子进程对全局变量的修改不影响父进程（内存相互独立）：

```python
import multiprocessing, os
tmp = 10

def work():
    global tmp
    tmp = 100
    print('work pid:', os.getpid(), os.getppid())
    print("tmp in work:", tmp)

if __name__ == '__main__':
    p = multiprocessing.Process(target=work)
    p.start()
    p.join()
    print("tmp in main:", tmp)
```

#### 2.4 进程应用场景
使用场景：并行计算、函数执行过长、阻塞等。例：函数每次休眠 1 秒执行 6 次，多进程并行约 1 秒，单进程串行约 6 秒。

#### 2.5 进程间通信
常用方式：消息队列 `from multiprocessing import Queue`；共享内存 `from multiprocessing import Value, Array`。

Queue 方法：

| 方法 | 说明 |
|---|---|
| msgq = Queue(maxsize=0) | 创建消息队列 |
| msgq.put(obj, block=True, timeout=None) | 消息入队 |
| msgq.get(block=True, timeout=None) | 消息出队 |
| msgq.qsize() | 队列中消息数量 |

#### 2.6 练习：统计代码行数
思路：遍历目录找到 Python 文件并统计行数。多进程实现（任务队列 + 结果队列，收到 "q" 退出）：

```python
import multiprocessing, os, time
from multiprocessing import Queue

def countLine(queue_path, queue_result):
    linenum = 0
    while True:
        msg = queue_path.get()
        if msg.lower() == "q":
            break
        if msg.endswith(".py"):
            with open(msg, encoding="utf-8") as f:
                linenum += len(f.readlines())
    queue_result.put(linenum)

def scandir(path, queue_path):
    for root, _, flist in os.walk(path):
        for fname in flist:
            queue_path.put(os.path.join(root, fname))

if __name__ == '__main__':
    src_dir = r'E:\vscode_dir\part_7\process\django'
    queue_path, queue_result = Queue(), Queue()
    list_p = []
    start_time = time.time()
    for i in range(10):
        p = multiprocessing.Process(target=countLine, args=(queue_path, queue_result))
        list_p.append(p)
        p.start()
    scandir(src_dir, queue_path)
    for p in list_p:
        queue_path.put('q')
    for p in list_p:
        p.join()
    total = sum(queue_result.get() for _ in range(queue_result.qsize()))
    print("run time:%.2f, code total nums:%d" % (time.time() - start_time, total))
```

对比：文件较少时单进程占优（0.87s）；加大扫描次数后多进程占优（1.04s，总数 350570）。

#### 2.7 进程池
进程池：创建一定数量的进程供用户调用。

| 方法 | 说明 |
|---|---|
| Pool(processes=None, ...) | 创建进程池对象 |
| pools.apply(func, args=(), kwds={}) | 添加任务，阻塞模式 |
| pools.apply_async(func, args=(), kwds={}, callback=None, error_callback=None) | 添加任务，非阻塞；callback 处理返回值；返回 AsyncResult |
| pools.close() | 关闭进程池（停止添加任务） |
| pools.join() | 等待所有任务结束 |
| AsyncResult | 获取进程函数返回值 |

基本用法：

```python
from multiprocessing import Pool

pool = Pool(processes=3)          # 创建进程池
pool.apply_async(func, (msg, ))   # 添加任务
pool.close()                      # 停止添加任务
pool.join()                       # 等待任务结束
```

---

### 32. 多线程详解与应用
#### 1 多线程
#### 1.1 基本概念
- 线程：系统进行运算调度的最小单元，线程依赖于进程；多线程：在一个进程中，启动多线程并发执行任务，线程之间全局资源可以共享；
- 进程与线程区别：① 线程依赖于进程；② 线程之间资源共享；③ 线程调度开销小于进程开销。

#### 2.2 Python 中多线程限制
GIL（Global Interpreter Lock）：实现 CPython（Python 解释器）时引入的一个概念。

| 方法/项 | 说明 |
|---|---|
| GIL | 锁：实质是一个互斥锁（mutex） |
| GIL | 作用：防止多个线程同时去执行字节码，降低执行效率 |
| GIL | 问题：在多核 CPU 中，Python 的多线程无法发挥其作用，降低任务执行效率 |

#### 2 多线程相关模块与应用
#### 2.1 创建线程
threading 模块相关方法：

| 方法 | 说明 |
|---|---|
| threading.active_count() | 返回当前活动的线程数量 |
| threading.current_thread() | 获取当前的线程对象 |
| threading.get_ident() | 获取当前的线程 ID |
| threading.Thread(group=None, target=None, ...) | 创建线程对象 |

#### 2.2 线程相关方法
Thread 对象相关方法：

| 方法 | 说明 |
|---|---|
| t = Thread(group=None, target=None, name=None, args=(), kwargs=None, daemon=None) | 创建线程 |
| t.start() | 启动线程，运行线程函数 |
| t.run() | 运行线程函数 |
| t.setDaemon(daemonic) / t.daemon | 设置/获取 daemon 线程 |
| t.is_alive() | 线程是否存活 |
| t.join(timeout=None) | 等待线程退出 |
| t.getName() / t.ident | 获取线程名称 / 线程 ID |

注意：只有 Thread 对象调用 start 方法后，才能调用 join 方法等待。

#### 2.3 多线程应用
需求：定义线程函数，每个线程函数休眠 1 秒钟，查看执行过程；要点：① 线程之间执行是随机的；② 线程之间资源共享（g_value 的值发生变化）。

#### 2.4 全局变量操作问题
需求：主线程对变量加 1 执行 50W 次，子线程同时对变量减 1 执行 50W 次，最后查看该变量的值；结果：g_value 是一个随机值（如 239973），即两个线程同时操作同一变量产生线程安全问题；解决方式：引入锁机制。

#### 2.5 同步机制
引入锁机制：threading.Lock()。使用原理：对公共资源进行保护，只有获取锁之后，才能对公共资源进行修改访问；注意点：同一线程中，避免获取锁之后再次获取锁，这样会造成死锁。

| 方法 | 说明 |
|---|---|
| lock = threading.Lock() | 创建锁 |
| lock.acquire(blocking=True, timeout=-1) | 申请锁 |
| lock.release() | 释放锁 |

```python
from threading import Thread, Lock

g_value = 10000
nums = 500000
lock = Lock()

def sub_func():
    global g_value
    for i in range(nums):
        lock.acquire()
        g_value -= 1
        lock.release()

t = Thread(target=sub_func, name='test')
t.start()
for i in range(nums):
    lock.acquire()
    g_value += 1
    lock.release()
t.join()
print(f'g_value={g_value}')
```

#### 2.6 线程之间通信方式
消息队列：通过 from queue import Queue 导入。

| 方法 | 说明 |
|---|---|
| msgq = Queue(maxsize=0) | 创建消息队列 |
| msgq.put(item, block=True, timeout=None) | 存入消息 |
| msgq.get(block=True, timeout=None) | 获取消息 |
| msgq.empty() | 判断是否为空 |
| msgq.full() | 判断是否写满 |

## 第九部分 数据库
### 33. MySQL 数据库操作
#### 1 准备工作
1. 安装 MySQL 服务，熟悉常用 SQL 语句；
2. 安装 Python 操作模块：

```python
pip install pymysql
```

#### 2 pymysql 详解与应用
#### 2.1 操作流程
1. 连接数据库；
2. 创建游标；
3. 执行 SQL 语句（增删改查）；
4. 提交（commit）；
5. 关闭数据库。

#### 2.2 pymysql 常用方法
| 方法 | 说明 |
|---|---|
| `pymysql.connect(host, user, password, database)` | 连接数据库，参数为地址、用户名、密码、数据库名称 |
| `db.cursor(cursor=None)` | 创建游标 |
| `cursor.execute(query, args=None)` | 执行 SQL 语句：查询、删除、更新、插入等操作 |
| `cursor.executemany(query, args)` | 批量执行：一次插入多条数据 |
| `cursor.fetchall()` | 读取所有数据 |
| `cursor.fetchmany(size=None)` | 读取指定数量数据 |
| `cursor.fetchone()` | 获取一条数据 |
| `db.commit()` | 提交修改 |
| `db.close()` | 关闭数据库 |

#### 2.3 连接数据库
方式 1：

```python
import pymysql
db = pymysql.connect(host="localhost", user="root", password="abc123", database="TESTDB")
```

方式 2：

```python
config = {
    'user': 'root',         # 用户名
    'password': 'abc123',   # 密码
    'host': 'localhost',    # MySQL 服务地址
    'port': 3306,           # 端口，默认 3306
    'database': 'TESTDB',   # 数据库名
}
db = pymysql.connect(**config)
```

#### 2.4 获取游标
```python
cursor = db.cursor()
```

#### 2.5 执行 SQL 语句
```python
# 查看表名
cursor.execute("show tables;")
# 读取所有数据
data = cursor.fetchall()
for item in data:
    print(item)
```

#### 2.6 插入数据
```python
sql = 'insert into user_info (user_name, user_id, channel) values(%s,%s,%s)'
# 插入一条数据
cursor.execute(sql, ('何同学', "10001", "B站"))
# 批量插入多条数据
cursor.executemany(sql, [('张同学', "10002", "抖音"), ('奇猫', "10003", "抖音")])
db.commit()
```

#### 2.7 查询数据
```python
sql = 'select * from user_info'
cursor.execute(sql)
data = cursor.fetchall()
for item in data:
    print(item)
```

#### 2.8 关闭连接
```python
cursor.close()
db.close()
```

## 第十部分 数据分析
### 34. NumPy

#### numpy简介
numpy 是开源的 Python 科学计算模块，C 语言实现、计算快，支持矩阵与数组操作及均值、方差等运算，支持 excel、csv 数据导入。

#### numpy安装
pip install numpy；anaconda 自带 numpy；官方文档：https://numpy.org/doc/

#### ndarray
numpy 的基本数据结构：索引从 0 开始，元素同一种类型，与列表类似支持切片。

#### array 方法
array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0)

| 参数 | 说明 |
|---|---|
| object | 类似数组对象，如序列、range |
| dtype / order / ndmin | 元素类型 / 内存排列形式 / 指定维度 |

#### ndarray 轴与秩
- 轴（axis）：axis=0 为第一层数组，axis=1 为数组里的数组，依次类推；秩（rank）即维度

| 属性 | 说明 |
|---|---|
| .ndim | 秩 |
| .shape | 维度 |
| .size | 元素数量 |
| .dtype | 元素类型 |

#### 创建 ndarray 对象
| 方法 | 说明 |
|---|---|
| np.zeros / ones / empty(shape) | 值全为 0 / 1 / 随机 |
| np.full(shape, fill_value) | 值为 fill_value |
| np.arange([start,] stop[, step]) | 类似 range |
| np.linspace(start, stop, num=50) | 按起止与数量生成 |
| np.zeros_like / empty_like / ones_like(a) | 与 a 相同形状 |

#### np.random 相关方法
| 方法 | 说明 |
|---|---|
| np.random.rand(d0, d1, ...) | 按形状产生随机值 |
| np.random.randint(low, high=None, size=None) | 按范围产生整数 |

#### reshape 方法
array.reshape(shape, order='C')：调整形状，返回新 ndarray。order 为内存存储方式，以 a = [[1,2],[3,4]] 为例：C：a[0][0], a[0][1], a[1][0], a[1][1]；F：a[0][0], a[1][0], a[0][1], a[1][1]

#### numpy 数据类型
int8/16/32/64（简写 i1/i2/i4/i8，有符号）；uint8/16/32/64（u1/u2/u4/u8，无符号）。

#### ndarray 转其他数据结构
| 方法 | 说明 |
|---|---|
| a.tolist() | 转成列表 |
| a.tobytes() / a.tostring() | 转成 bytes |
| a.tofile(fid, sep="", format="%s") | 保存到文件 |

#### numpy 访问与修改
访问与列表类似，支持切片；一维轴为 0，二维为 0、1，三维为 0、1、2。

```python
a = np.arange(25).reshape(5, 5)
print(a[0])              # 取行
a[[1, 2, 4]]             # 多行
a[:, 1]                  # 列
a[[1, 3, 4], [2, 3, 4]]  # 多个元素
a[1:3, :3]               # 行列切片
a = np.arange(10)
a[0] = 10                # 改一个元素
a[:5] = 10               # 改多个元素
```

#### numpy 广播（broadcasting）
基本运算应用到所有元素，array 间为逐元素运算，如 a*10、a+b。

#### numpy 计算
求和、均值、方差等 numpy 模块与 array 对象均支持，用法类似：np.sum(a, axis=None, dtype=None, out=None)

| 方法 | 说明 |
|---|---|
| np.mean() / np.median() | 均值 / 中位数 |
| np.max() / np.min() / np.ptp() | 最大 / 最小 / 极差 |
| np.cumsum() | 累加和 |
| np.std() / np.var() / np.cov() | 标准差 / 方差 / 协方差 |
| np.sqrt() / np.log() / 三角函数 | 平方根 / 对数 / sin cos tan |

#### 多维 array 计算
指定 axis 得到不同效果：axis=1 按行计算，axis=0 按列计算。

```python
a = np.arange(10).reshape(2, 5)
print(np.sum(a, axis=1), np.sum(a, axis=0))  # 按行 / 按列
```

#### 数据拼接与分割
- np.concatenate((a1, a2, ...), axis=0)：拼接多个数组
- np.stack(arrays, axis=0)：沿 axis 堆叠（穿起来），非拼接
- np.hstack / np.vstack：水平 / 垂直拼接
- np.split(ary, indices_or_sections, axis=0)：按 axis 分割；np.vsplit / np.hsplit：垂直 / 水平切分

```python
np.concatenate((np.arange(1, 5).reshape(2, 2), np.arange(5, 9).reshape(2, 2)), axis=1)
```

#### nan 与缺省值处理
nan 标识缺失数据；None 是 Python 对象，不能与 nan 混淆。

```python
v1 = np.array([[90, 100], [np.nan, 100]])
np.isnan(v1)               # 判断是否为 nan
v1[np.isnan(v1)]           # 所有 nan 值
v1[np.isnan(v1) == False]  # 非 nan 值
```

#### np.all 与 np.any
np.all(a, axis=None, out=None)：所有元素非 0 才为 True；np.any(a, axis=None, out=None)：存在元素不为 0 即为 True

```python
a = np.arange(10).reshape(2, 5)
print(np.all(a, axis=0), np.all(a, axis=1))  # 垂直 / 水平轴
a = np.array([1, None])
print(np.any(a), np.all(a))  # None 注意
```

#### np.where
np.where(condition, [x, y])：给定 x, y 时满足条件输出 x，否则输出 y；未给定返回满足条件的索引。

```python
a = np.random.randint(30, 100, 10)
np.where(a >= 60, 'pass', 'failed')  # 是否及格
np.where(a >= 60)                    # 索引
```

---

### 35. Matplotlib

Matplotlib 是 Python 的绘图模块，与 Numpy、Pandas 配合使用，类似 MATLAB 的绘图工具；seaborn 等基于它实现；可在 Jupyter 中直接显示。官网：https://matplotlib.org/index.html

安装：`pip install matplotlib`（anaconda 环境已内置，无需安装）。

#### %matplotlib inline

`%matplotlib inline` 是 iPython 的魔法函数（Magic Function），将 matplotlib 绘制的图直接显示在页面中；不加则需调用 `plt.show()`。

#### 基本概念

- 画布（Figure）：图表大小，进行图表绘制；
- axes：坐标系，一个画布中可以指定多个坐标系；
- axis：坐标轴，每个坐标系都有一个坐标轴。

#### 基本使用

```python
plt.plot(*args, scalex=True, scaley=True, data=None, **kwargs)
```

- 只传一个数组时，x 取 0,1,2,…,N-1；
- data 参数：数据为字典时，x、y 为字典的 key（对 pandas 同样适用）。

```python
import matplotlib.pyplot as plt
xdata = range(5)
ydata = range(5)
plt.plot(xdata, ydata)
```

plot 常用参数：

| 参数 | 说明 |
|---|---|
| fmt | 字符串，线与点的属性（线型、点形状、颜色） |
| data | 数据 |
| kwargs | 关键字参数，如 linewidth、label 等 |

fmt 格式 `'-or'` 依次代表线型、点形状、颜色，顺序可以颠倒。

线型：

| 符号 | 说明 |
|---|---|
| '-' | solid line style |
| '--' | dashed line style |
| '-.' | dash-dot line style |
| ':' | dotted line style |

点形状：

| 符号 | 说明 |
|---|---|
| '.' | point marker |
| ',' | pixel marker |
| 'o' | circle marker |
| 'v' | triangle_down marker |
| '^' | triangle_up marker |
| '<' | triangle_left marker |
| '>' | triangle_right marker |

颜色：

| 符号 | 说明 |
|---|---|
| 'b' | blue |
| 'g' | green |
| 'r' | red |
| 'c' | cyan |
| 'm' | magenta |
| 'y' | yellow |
| 'k' | black |
| 'w' | white |

#### 坐标轴设置

| 方法 | 说明 |
|---|---|
| plt.xlabel(s, *args, **kwargs) | 设置 x 轴 label |
| plt.ylabel(s, *args, **kwargs) | 设置 y 轴 label |
| plt.xticks(*args, **kwargs) | 设置 x 轴 tick |
| plt.yticks(*args, **kwargs) | 设置 y 轴 tick |
| plt.xlim(*args, **kwargs) | 设置 x 轴范围 |
| plt.ylim(*args, **kwargs) | 设置 y 轴范围 |

```python
import matplotlib.pyplot as plt
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.plot(range(-10, 10), range(-10, 10), '-o')
plt.xlabel('x-value')
plt.ylabel('y-value')
# x 轴值与显示值一一对应：-10:a, -9:b ... 10:t
xticks = [chr(v) for v in range(ord('a'), ord('a') + 21)]
_ = plt.xticks(range(-10, 10), xticks)
```

#### 字体设置

字体设置包括大小、字体、颜色、旋转角度等。参考：https://matplotlib.org/api/text_api.html

| 参数 | 说明 |
|---|---|
| size | 大小，整数或 'xx-small','x-small','small','medium','large','x-large','xx-large' |
| rotation | 旋转角度 |
| fontfamily | 字体 |
| alpha | 透明度（0~1） |
| visible | 是否显示 |
| c | 颜色，例如 'r','b' |

```python
import matplotlib.pyplot as plt
plt.plot(range(5), '-o')
_ = plt.xticks(rotation=30, fontfamily='fantasy', size=20, alpha=0.7, visible=True, c='r')
```

#### title / 图例设置

- `plt.title(label, fontdict=None, loc='center', pad=None, **kwargs)`：设置标题；
- `plt.legend(*args, **kwargs)`：设置图例，绘制时用 label 指定名称再调用。

```python
import matplotlib.pyplot as plt
plt.plot(range(5), '-o', label="line1")
plt.plot(range(1, 6), '-o', label="line2")
plt.legend()
plt.title("case1")
```

#### 支持中文

```python
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号乱码
```

设置后 Jupyter 中全局有效，否则中文 title 显示为乱码。

#### 子图

`plt.subplot(nrows, ncols, index)`：返回 axes，简写可省略逗号，如 221 表示 2 行 2 列第 1 个。

```python
plt.subplot(1, 2, 1)  # 同 plt.subplot(121)
plt.subplot(1, 2, 2)  # 同 plt.subplot(122)
plt.subplot(2, 1, 1)  # 同 plt.subplot(211)
plt.subplot(2, 1, 2)  # 同 plt.subplot(212)
```

多行多列时返回的 axes 可单独设置，如 `axes = plt.subplot(221); axes.plot(range(4)); axes.set_facecolor('r')`。

#### 创建画布

`plt.figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=True, ...)`：num 为画布序号；figsize 为画布大小 (width, height)；facecolor 为画布颜色。可用 `plt.gca()` 获取当前坐标系。

#### 设置坐标轴位置

默认坐标系原点在左下角，可通过 spines 隐藏上、右边框并移动坐标轴：

```python
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(-4, 4, 200)
y = np.sin(x)
plt.figure()
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# 左轴移到 x=1，底轴移到 y=0
ax.spines['left'].set_position(('data', 1))
ax.spines['bottom'].set_position(('data', 0))
plt.plot(x, y)
```

#### 折线图

展示趋势变化关系，常与时间结合使用（如新增用户、股票数据等）。

```python
import matplotlib.pyplot as plt
import numpy as np
ydata = [100, 90, 120, 150, 200, 300, 210]
plt.plot(ydata)
plt.plot(np.cumsum(ydata))
plt.legend(['新增粉丝', '累计粉丝'])
plt.title("我的粉丝")
```

#### 散点图

显示若干数据系列中各数值之间的关系，一定程度反映数据分布，适用于维度较少的数据。方法：`plt.scatter(x, y, s=None, c=None, marker=None, ..., alpha=None, **kwargs)`。

```python
import matplotlib.pyplot as plt
import numpy as np
xValue = list(range(0, 101))
yValue = [x * np.random.rand() for x in xValue]
plt.scatter(xValue, yValue, s=20, marker='o')
```

#### 柱状图/条形图

显示一段时间内的数据变化或各项之间的比较情况。柱状图：`plt.bar(x, height, width=None, bottom=None, *, align='center', **kwargs)`；条形图：`plt.barh(*args, **kwargs)`。

```python
import matplotlib.pyplot as plt
import numpy as np
x = np.arange(4)
gdp_2019 = [10.7, 9.9, 7.1, 6.2]
tick_label = ['广东省', '江苏省', '山东省', '浙江省']
plt.bar(x, gdp_2019, 0.3, color='salmon', label='2019')
plt.legend()
_ = plt.xticks(x, tick_label)
```

#### 饼状图

展示总体数据中各项与总和的比例，用于各项数据对比。方法：`plt.pie(x, explode=None, labels=None, autopct=None, ...)`。

```python
import matplotlib.pyplot as plt
edu = [100, 200, 900, 600, 1000]
labels = ['中专', '大专', '本科', '硕士', '其他']
plt.pie(x=edu, labels=labels, autopct='%.1f%%')
plt.title('职工教育分布')
plt.show()
```

#### 直方图

展示数据分布情况。方法：`plt.hist(x, bins=None, range=None, ...)`，示例：`plt.hist(np.random.randn(10000))`。

#### 箱形图

直观描述数据的最大值、最小值、中位数、上四分位数、下四分位数及异常值。方法：`plt.boxplot(x, notch=None, sym=None, vert=None, whis=None)`。

```python
import matplotlib.pyplot as plt
import numpy as np
data = np.random.randn(10000)
plt.boxplot(data)
plt.show()
```

## 第十一部分 算法与数据结构
### 36. 逻辑强化（算法入门练习）

#### 有序列表中插入有序的元素
给定有序数字列表 nums 与数字 x，将 x 插入列表并保持有序。

实现思路：遍历 nums 取元素 val；若 x < val，将 x 插入 val 所在位置并 break；若 x 大于列表最大值，追加到末尾；列表为空时直接追加。

```python
def inser_x(nums, x):
    if nums:
        if nums[-1] <= x:
            nums.append(x)
        else:
            for index, val in enumerate(nums):
                if x < val:
                    nums.insert(index, x)
                    break
    else:
        nums.append(x)
```

#### 求交集
给定两个数组，计算交集；结果中每个元素唯一，不考虑输出顺序。

思路1：两个列表分别去重后合并，用 Counter 统计各元素出现次数，次数 > 1 的元素即为交集。

```python
from collections import Counter

def jiaoji(list1, list2):
    l1 = list(set(list1))
    l2 = list(set(list2))
    l1.extend(l2)
    r = Counter(l1)
    return [k for k in r if r[k] > 1]
```

思路2：遍历 list1，元素在 list2 中且未记录过则加入结果。

```python
def jiaoji(list1, list2):
    vals = []
    for val in list1:
        if val in list2 and val not in vals:
            vals.append(val)
    return vals
```

#### 旋转字符串
字符串左旋转：将前 k 个字符转移到字符串尾部。限制：1 <= k < len(s)。

```python
def reverse_left_words(s, k):
    if k > 0 and k < len(s):
        return s[k:] + s[:k]
```

#### 反转字符串
将字符列表原地反转（不使用 Python 默认方法）：start 指向开头、end 指向结尾，交换对应元素后 start 加 1、end 减 1，循环条件 start < end。

```python
def my_reverse(lists):
    start = 0
    end = len(lists) - 1
    while start < end:
        lists[start], lists[end] = lists[end], lists[start]
        start += 1
        end -= 1
```

#### 翻转字符串中单词
逐个翻转字符串中的单词：无空格字符构成一个单词；反转后去掉首尾多余空格，单词间只保留一个空格。用 s.split() 切分，过滤空白项，翻转单词列表，再用 ' '.join 拼接。

```python
def reverse_words(s):
    wds = [wd for wd in s.split() if wd.strip()]
    my_reverse(wds)
    return ' '.join(wds)
```

#### 合并两个有序列表
合并两个有序列表 l1、l2 为新的有序列表，不能使用 sort 方法：双索引逐对比较，较小值加入新列表；某个列表遍历完后，将另一列表剩余元素 extend 到新列表。

```python
def megre_list(list1, list2):
    index1 = 0
    index2 = 0
    lens1 = len(list1)
    lens2 = len(list2)
    new_list = []
    while index1 < lens1 and index2 < lens2:
        v1 = list1[index1]
        v2 = list2[index2]
        if v1 <= v2:
            new_list.append(v1)
            index1 += 1
        else:
            new_list.append(v2)
            index2 += 1
    if index1 < lens1:
        new_list.extend(list1[index1:])
    if index2 < lens2:
        new_list.extend(list2[index2:])
    return new_list
```

#### 解压缩编码列表
以行程长度编码压缩的整数列表 nums，格式为 [freq, val, freq, val, ...]，freq 与 val 成对出现（freq 为 val 的频次）。将 nums 解压为新列表：每两位取 freq、val，向新列表扩展 [val] * freq。

```python
def decompress_list(nums):
    lens = len(nums)
    i = 0
    new_list = []
    while i < lens:
        freq = nums[i]
        val = nums[i + 1]
        i += 2
        new_list.extend([val] * freq)
    return new_list
```

#### 数字列表加法操作
数字列表每位取值范围 0~9（如 189 表示为 [1,8,9]）。在 C/C++ 等语言中整型有位数上限，大数运算用列表逐位模拟，防止越界。

计算规则：从最低位开始逐位相加并处理进位；两个列表长度不同时，较长列表的剩余高位继续与进位相加；若最终仍有进位，插入结果最前面。

```python
def list_add(num1, num2):
    lens1 = len(num1)
    lens2 = len(num2)
    carry = 0
    res = []
    min_index = min(lens1, lens2) * -1
    i = -1
    while i >= min_index:
        v = num1[i] + num2[i] + carry
        if v >= 10:
            carry = 1
            res.insert(0, v - 10)
        else:
            carry = 0
            res.insert(0, v)
        i -= 1
    if lens1 != lens2:
        if lens1 > lens2:
            last_list = num1
            min_index = -lens1
        else:
            last_list = num2
            min_index = -lens2
        while i >= min_index:
            v = last_list[i] + carry
            if v >= 10:
                carry = 1
                res.insert(0, v - 10)
            else:
                carry = 0
                res.insert(0, v)
            i -= 1
    if carry:
        res.insert(0, carry)
    return res
```

#### 排队问题
n 名战士评分分别为 Si、Sj、Sk，选出下标 i < j < k 且满足 Si < Sj 且 Sj > Sk（中间值最大）的 3 人组成作战单位，求可组建数量。

三层遍历枚举所有三元组，判断 val > sub_val > last 或 val < sub_val < last：

```python
def count_teams(l):
    for index, val in enumerate(l):
        sub_list = l[index + 1:]
        for sub_index, sub_val in enumerate(sub_list):
            last_list = l[index + sub_index + 2:]
            if val > sub_val:
                for last in last_list:
                    if sub_val > last:
                        print(val, sub_val, last)
            else:
                for last in last_list:
                    if sub_val < last:
                        print(val, sub_val, last)
```

#### 计算和的最大乘积
将正整数 n 拆分为至少两个正整数的和，使乘积最大化。n <= 4 时不拆分（{1:1, 2:1, 3:2, 4:4}）；n > 4 时拆分为 3 的倍数最划算，n = 3k + x：

| n % 3 | k | 结果 |
|---|---|---|
| 1 | (n-4)//3 | pow(3, k) * 4 |
| 2 | n//3 | pow(3, k) * (n % 3) |
| 0 | n//3 | pow(3, k) |

```python
def integer_break(n):
    n_map = {1: 1, 2: 1, 3: 2, 4: 4}
    val = n_map.get(n, 0)
    k = 0
    if not val:
        tmp = n % 3
        if tmp == 1:
            k = (n - 4) // 3
            tmp = 4
        elif tmp == 2:
            k = n // 3
        else:
            k = n // 3
            tmp = 1
        val = pow(3, k) * tmp
    return val
```

#### n 的第 K 个因子
正整数 i 满足 n % i == 0 即 n 的因子。将 n 的所有因子升序排列，若因子数量 >= k 返回第 k 个因子，否则返回 -1。

思路1：遍历 1 到 n 收集所有因子。

```python
def kthFactor(n, k):
    list_fac = []
    for i in range(1, n + 1):
        if n % i == 0:
            list_fac.append(i)
    if len(list_fac) >= k:
        return list_fac[k - 1]
```

思路2：因子成对出现，min_fac 与 max_fac = n // min_fac 配对，从两端向中间收集，只需检查到平方根级别。

```python
def kthFactor(n, k):
    list_fac = []
    min_val, max_val = 1, n
    i = 0
    if n > 1:
        while min_val < max_val:
            if n % min_val == 0:
                t = n // min_val
                max_val = t
                if max_val != min_val:
                    list_fac.insert(-1 * i, t)
                list_fac.insert(i, min_val)
                i += 1
            min_val += 1
    else:
        list_fac.append(n)
    if len(list_fac) >= k:
        return list_fac[k - 1]
    else:
        return -1
```

#### 合并区间
合并所有重叠区间。前提：区间按左端点有序（s1.left <= s2.left）；若 s1.right < s2.left 则两区间不重叠，直接加入；若 s1.right >= s2.left 则重叠，将 s1.right 更新为两者中较大值。

```python
def merge_list(intervals):
    if len(intervals) <= 1:
        return intervals
    res = []
    start = 0
    end = -1
    intervals = sorted(intervals, key=lambda item: item[start])
    res.append(intervals[0])
    for i in range(1, len(intervals)):
        if res[-1][end] < intervals[i][start]:
            res.append(intervals[i])
        elif intervals[i][end] > res[-1][end]:
            res[-1][end] = intervals[i][end]
    return res
```

---

### 37. 递归问题

#### 递归函数
递归函数：函数自身调用自身，且必须有一个明确的结束条件；递归函数有层数限制。

Python 中递归最大深度：
```python
import sys
sys.getrecursionlimit()
```

#### N 的阶乘
N! = N × (N-1) × (N-2) × ... × 2 × 1

实现思路1：正向循环
```python
def factorial(n):
    total = 1
    while n >= 1:
        total *= n
        n -= 1
    return total
```

实现思路2：使用递归
```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)
```

#### 斐波那契（Fibonacci）数列
求斐波那契数列的第 n 项，定义：F(0) = 0，F(1) = 1，F(N) = F(N-1) + F(N-2)（N > 1）。

思路1：递归实现（结束条件：n <= 1）
```python
def fib_func(n):
    if n <= 1:
        return n
    return fib_func(n - 1) + fib_func(n - 2)
```

思路2：递推（初始 a = 1, b = 1；每轮 a, b = b, a + b，a 为最终值）
```python
def fib_func(n):
    a, b = 1, 1
    if n == 0:
        return 0
    while n > 1:
        a, b = b, a + b
        n -= 1
    return a
```

#### 计算和
求 1+2+3+...+n，不能使用乘除法、for、while、if、else 语句。

思路：递归 + 逻辑运算符
```python
def mysum(val):
    tmp = val
    tmp += val > 0 and mysum(tmp - 1)
    return tmp
```

#### 遍历多维列表
给定多维数字列表，找出其中大于 x 的所有数字。

思路：遍历列表；用 isinstance 判断元素是否为列表，是则递归，否则比较大小并收集。

```python
nums = [0, [1, 2, 3], [4], [2, 3, 4], [[4, 5, 6], [7, [8, [9], [10]]], [1, 2, 3]]]

def find_x(nums, x, res):
    for item in nums:
        if isinstance(item, list):
            find_x(item, x, res)
        else:
            if item > x:
                res.append(item)

result = []
find_x(nums, 5, result)
```

#### 实现列表全排列
[1, 2, 3] 的全排列共 6 种：(1,2,3) (1,3,2) (2,1,3) (2,3,1) (3,1,2) (3,2,1)。

实现方式1：itertools.permutations
```python
from itertools import permutations
for item in permutations([1, 2, 3]):
    print(item)
```

实现方式2：递归实现
基本思路：依次取一个元素，与剩余元素的全排列组合；截止条件：列表中只有一个元素时直接返回。

```python
def permutation(array):
    output = []
    if len(array) == 1:
        return [array]
    for i in range(len(array)):
        sub_array = list(array)
        val = sub_array.pop(i)
        for item in permutation(sub_array):
            output.append([val] + item)
    return output

permutation([1, 2, 3])
```

---

### 38. 回溯算法

#### 回溯法概述
回溯法（探索与回溯法，又称试探法）是一种选优搜索法，用递归或递推实现，用于找出解集或满足约束条件的最佳解。可读性强但耗时较长，能用递推公式迭代求解的问题应避免使用。

#### 三个概念
- **约束函数**：根据题意定义，描述合法解的一般特征，用于去除不合法解。
- **状态空间树**：对所有解的图形描述，树上每个子节点只有一部分与父节点不同。

| 节点类型 | 含义 |
|---|---|
| 扩展节点 | 当前正在求出其子节点的节点（DFS 中只允许一个） |
| 活结点 | 节点本身及其父节点均满足约束函数 |
| 死结点 | 不必再求其子节点 |

#### DFS 与 BFS
- **DFS**（Depth First Search）：沿每个分支路径深入到不能再深入，每个节点只能访问一次。
- **BFS**（Breadth First Search）：盲目搜寻法，系统展开并检查图中所有节点以寻找结果。

#### 实现步骤
按选优条件向前搜索；发现当前选择不优或达不到目标时退回一步重新选择。这种"走不通就退回"的技术即回溯法，满足回溯条件的点称为"回溯点"。

#### 组合总和
给定无重复元素的数组 `nums` 与目标数 `target`，找出所有和为 `target` 的组合（数字可无限制重复选取）。对 `nums` 排序后从最小值开始探索；组合和大于 `target` 或索引越界即截止，等于 `target` 则记录。

函数接口 `backtrack(nums, i, tmp, target, res)`：

| 参数 | 说明 |
|---|---|
| nums | 数字列表 |
| i | 起始索引 |
| tmp | 当前数字组合 |
| target | 目标值 |
| res | 结果列表 |

```python
def backtrack(nums, i, tmp, target, res):
    n = len(nums)
    tmp_sum = sum(tmp)
    if tmp_sum > target or i == n:
        return
    if tmp_sum == target:
        res.append(tmp)
        return
    for j in range(i, n):
        if tmp_sum + nums[j] > target:
            break
        backtrack(nums, j, tmp + [nums[j]], target, res)
```

#### 括号生成
给定数字 `n`，生成 n 对括号的所有有效组合。任意前缀中左括号数 ≥ 右括号数，左括号数最大为 n；左右括号都用完（`left == 0 and right == 0`）时记录结果。

```python
def backtrack(res, tmp, left, right):
    if left == 0 and right == 0:
        res.append(tmp)
        return
    if left > 0:
        backtrack(res, tmp + '(', left - 1, right)
    if right > left:
        backtrack(res, tmp + ')', left, right - 1)
```

#### 全排列
给定无重复数字的序列，返回所有可能的全排列。遍历索引 `i`，弹出副本中 `i` 处元素 `val`，递归排列剩余元素；`nums` 为空时记录结果。

```python
def permute(nums, res, tmp):
    lens = len(nums)
    if lens == 0:
        res.append(tmp)
        return
    for i in range(lens):
        tmp_list = list(nums)
        val = tmp_list.pop(i)
        permute(tmp_list, res, tmp + [val])
```

#### 复原 IP 地址
给定只含数字的字符串，复原所有可能的 IP 地址格式。有效 IP 由四个整数组成（0~255，无前导 0），用 `.` 分隔。每部分长度 1~3 位，取前 1/2/3 位递归找下一字段；截止条件：字符串为空且已有 4 段。

```python
def restore_ip_addresses(s, res, tmp):
    if len(s) == 0 and len(tmp) == 4:
        res.append('.'.join(tmp))
        return
    for i in range(min(3, len(s))):
        p = s[:i + 1]  # 取前 i 位
        if p and 0 <= int(p) <= 255 and str(int(p)) == p:
            restore_ip_addresses(s[i + 1:], res, tmp + [p])
```

#### 分割回文串
将字符串 `s` 分割成若干回文子串，返回所有分割方案。切成 A、B 两部分，A 为回文则继续切分 B；已切总长度等于原串长度（`cur_lens == max_lens`）时记录。

```python
def split_s(s, tmp, cur_lens, res, max_lens):
    if cur_lens == max_lens:
        res.append(tmp)
        return
    for i in range(1, len(s) + 1):
        head = s[:i]
        if head != head[::-1]:
            continue
        split_s(s[i:], tmp + [head], cur_lens + i, res, max_lens)
```

#### 将数组拆分成斐波那契序列
将数字字符串 `S` 拆成斐波那契式序列，满足 `F[i] + F[i+1] = F[i+2]`。先确定前两个数（`i`、`j` 为结束位置），后续数必须等于前两数之和且与剩余串前缀匹配，否则该组合无效；`s` 为空且已选数大于 2 时记录。

```python
def split_fibonacci(s, tmp, res):
    if len(s) == 0 and len(tmp) > 2:
        res.append(tmp)
        return
    tmp_lens = len(tmp)
    if tmp_lens >= 2:
        next_num = tmp[-1] + tmp[-2]
        next_str = str(next_num)
        if s.startswith(next_str):
            split_fibonacci(s[len(next_str):], tmp + [next_num], res)
    elif tmp_lens == 0:
        lens = len(s)
        for i in range(1, lens):
            suba = s[:i]
            if i > 1 and suba[0] == '0':
                break
            subb = s[i:]
            lenb = len(subb)
            for j in range(1, lenb + 1):
                tmpb = subb[:j]
                if j > 1 and tmpb[0] == '0':
                    break
                numb = int(tmpb)
                split_fibonacci(subb[j:], tmp + [int(suba), numb], res)
```

---

### 39. 动态规划

#### 基本思想

进入某状态后，后续从该状态开始的最优解必然是整体最优解（最优原理）：后续选择只与当前状态有关。

#### 特点

每个子问题只求解一次并保存结果，需要时直接查表，以空间换时间。

#### 特性

| 特性 | 说明 |
|---|---|
| 最优化原理（最优子结构） | 问题最优解所包含的子问题的解也是最优的 |
| 无后效性 | 状态一旦确定，后续过程只与当前状态有关 |
| 有重叠子问题 | 子问题不独立，可能被多次使用 |

#### 要素

| 要素 | 说明 |
|---|---|
| 阶段 | 按一定次序求解的若干相互联系的阶段 |
| 状态 | 每个阶段开始时所处的自然状况或客观条件 |
| 决策 | 从前一阶段转化到后一阶段的递推关系（状态转移方程） |

#### 步骤

| 步骤 | 内容 |
|---|---|
| 1. 设计状态变量 | 一维 `dp[i]` 或二维 `dp[i][0]`、`dp[i][1]` |
| 2. 确定状态转移方程 | 描述前后状态的递推关系 |
| 3. 初始化变量 | 设置 dp 初值 |
| 4. 考虑输出 | 确定最终返回的状态 |

#### 最大子序和

找到 nums 中具有最大和的连续子数组并返回最大和。暴力法：以每个元素为起点，求其后所有连续子数组的和并记录最大值。示例：`[-2,1,-3,4,-1,2,1,-5,4]` → 6。

```python
def max_sub_array(array):
    max_val = array[0]
    for i in range(len(array)):
        for j in range(i + 1, len(array) + 1):
            max_val = max(max_val, sum(array[i:j]))
    return max_val
```

#### 最长回文子串

找到 s 中最长的回文子串（回文串倒序后与自身相同）。`dp[i][j]=1` 表示 `s[i...j]` 是回文串；状态方程：`s[i]==s[j]` 且（长度 ≤2 或 `dp[i+1][j-1]=1`）时 `dp[i][j]=1`。示例：`"babad"` → `"bab"`。

```python
def longest_palindrome(s):
    lens = len(s)
    matrix = [[0] * lens for _ in range(lens)]
    max_lens, max_str = 0, ''
    for i in range(lens):
        for j in range(i + 1):
            if s[i] == s[j] and (i - j <= 1 or matrix[j + 1][i - 1]):
                matrix[j][i] = 1
                if i - j + 1 > max_lens:
                    max_lens, max_str = i - j + 1, s[j:i + 1]
    return max_lens, max_str
```

#### 等差数列划分

统计数组中为等差数列的子数组个数。等差条件：`nums[i]-nums[i-1] == nums[i-1]-nums[i-2]`；满足时 `dp[i] = dp[i-1]+1`；结果 `sum(dp)`。

```python
def count_slices(nums):
    if len(nums) < 3:
        return 0
    dp = [0] * len(nums)
    for i in range(2, len(nums)):
        if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]:
            dp[i] = dp[i - 1] + 1
    return sum(dp)
```

#### 三角形最小路径和

自顶向下求最小路径和，每步移到下一行下标相同或 +1 的结点。用一维 `dp` 从右往左更新，结果 `min(dp)`。

```python
def minimum_total(triangle):
    dp = [0] * len(triangle)
    dp[0] = triangle[0][0]
    for i in range(1, len(triangle)):
        for j in range(i, -1, -1):
            if j == 0:
                dp[j] += triangle[i][j]
            elif j == i:
                dp[j] = dp[j - 1] + triangle[i][j]
            else:
                dp[j] = triangle[i][j] + min(dp[j - 1], dp[j])
    return min(dp)
```

#### 最大正方形

在 '0'/'1' 矩阵中找只含 '1' 的最大正方形。状态方程：`dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1`；第一行/列遇 '1' 时 `dp[i][j]=1`；结果 `max(dp)**2`。

```python
def max_square(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, columns = len(matrix), len(matrix[0])
    max_size = 0
    dp = [[0] * columns for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == '1':
                dp[i][j] = 1 if i == 0 or j == 0 else min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                max_size = max(max_size, dp[i][j])
    return max_size * max_size
```

#### 丑数

丑数是质因数只含 2、3、5 的正整数（1 是丑数），求第 n 个丑数。每个丑数由 2、3、5 相乘产生：`dp=[1]`，每次插入三者乘积的最小值，对应索引 +1。

```python
def ugly_n(n):
    nums, i2, i3, i5 = [1], 0, 0, 0
    for _ in range(1, n):
        ugly = min(nums[i2] * 2, nums[i3] * 3, nums[i5] * 5)
        nums.append(ugly)
        if ugly == nums[i2] * 2:
            i2 += 1
        if ugly == nums[i3] * 3:
            i3 += 1
        if ugly == nums[i5] * 5:
            i5 += 1
    return nums[-1]
```

#### 买卖股票的最大利润

prices[i] 为第 i 天价格，最多完成一笔交易（不能先卖后买）求最大利润。例：`[7,1,5,3,6,4]` → 5。遍历记录当前索引前的最小值 `min_val`；状态方程：`dp[i] = max(dp[i-1], nums[i]-min_val)`（`nums[i] <= min_val` 时更新 `min_val`）。

```python
def max_perfit(nums):
    min_val = nums[0]
    dp = [0] * len(nums)
    for i, val in enumerate(nums):
        if val <= min_val:
            min_val = val
        dp[i] = max(dp[i - 1], val - min_val)
    return dp[-1]
```

#### 买卖股票最佳时机2

最多完成两笔交易（不能同时参与多笔交易）求最大利润。状态设计：`dp[i][j]`，i 为第 i 天，j 为最大交易次数。状态方程：`min_cost = prices[i] - dp[i-1][j-1]`；`dp[i][j] = max(dp[i-1][j], prices[i] - min_cost)`。

#### 0-1背包问题

n 种物品和容量 C 的背包，物品 i 重量 $w_i$、价值 $v_i$，选择物品使总价值最大。$dp[i][W]$ 表示前 i 件物品在容量 W 下的最大价值；状态方程：`dp[i][W] = max(dp[i-1][W], dp[i-1][W-w_i]+v_i)`（`w_i > W` 时取 `dp[i-1][W]`；`i==0` 或 `W==0` 时为 0）。

```python
def bag(n, c, w, v):
    dp = [[0] * (c + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, c + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= w[i - 1]:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w[i - 1]] + v[i - 1])
    return dp
```

---

### 40. 贪心算法

#### 基本概念
贪心算法：每一步都采取当前状态下最优的选择，希望得到全局最优。

关键点：
- 需**最优子结构**：局部最优解决定全局最优解；
- 须具**无后效性**：结果只与当前状态有关；
- 不能对所有问题得整体最优解；典型应用：最小生成树、哈夫曼编码等。

#### 贪心算法与动态规划异同
| 对比项 | 贪心算法 | 动态规划 |
|---|---|---|
| 推导 | 由上一步最优推下一步，不保留历史 | 记录所有局部最优解 |
| 方向 | 自顶向下 | 自底向上 |
| 结果 | 不保证全局最优，复杂度低 | 穷举得最优解，复杂度高 |

相同点：都需最优子结构，可分解为子问题。

#### 跳跃游戏
非负整数数组，每元素为该位置可跳最大长度，求到末位最少跳跃次数。示例：`[2,3,1,1,4]`→`2`。

思路（O(n)）：维护 `end`（本次最远边界）与 `max_post`（区间内最远可达）；`i == end` 时步数 +1，重置 `end = max_post`。

```python
def can_jump(nums):
    step = end = max_post = 0
    for i in range(len(nums) - 1):
        max_post = max(max_post, i + nums[i])
        if i == end:
            step += 1
            end = max_post
    return step
```

#### 找零钱问题
面值 `[20, 10, 5, 1]`，求给定 `x` 的最少钱币数。

思路：尽量用大面值，每面值 `m` 取 `x//m` 张，余 `x%=m`。示例：`x=25`→`2`（20+5）。

```python
def give_money(x):
    nums = []
    for m in [20, 10, 5, 1]:
        nums.append(x // m)
        x %= m
    return sum(nums), nums
```

#### 过河问题
N 人过河，船每次坐两人，耗时取较慢者，且需一人划回，求最短总时间。

思路：按时间升序；N<4 时取 `a[0]`、`a[1]`、`a[0]+a[1]+a[2]`；N>=4 时每次送走最慢两人，比较两方案（最快往返接送 / 最快二人先行）取小耗时，`n -= 2` 循环。

```python
def cross_river(a):
    a.sort()
    n, t = len(a), 0
    while n >= 4:
        t += min(2 * a[0] + a[n - 1] + a[n - 2], a[0] + 2 * a[1] + a[n - 1])
        n -= 2
    return t + (a[0] + a[1] + a[2] if n == 3 else a[n - 1])
```

---

### 41. 分治算法

#### 分治法定义

把复杂的一个问题分成两个或多个相同或相似的子问题，再把子问题分成更小的子问题，直到最后子问题可以简单地直接求解；原问题的解即子问题解的合并。

#### 基本思想

将一个难以直接解决的大问题，分割成一些规模较小的相同问题，以便各个击破、分而治之。

#### 分治策略

- 对规模为 n 的问题：若规模小可直接解决，否则分解为 k 个规模较小的子问题；
- k 个子问题互相独立且与原问题形式相同，可递归或递推地解决；
- 将各个子问题的解合并得到原问题的解；
- 若不满足上述条件，考虑使用贪心算法或动态规划。

#### 基本步骤

| 步骤 | 说明 |
|---|---|
| 分解 | 将原问题分解为若干个规模较小、相互独立、与原问题形式相同的子问题 |
| 解决 | 子问题规模较小则直接求解，否则递归地解各个子问题 |
| 合并 | 将各个子问题的解合并为原问题的解 |

#### 常见应用

二分搜索、大整数乘法、合并排序、快速排序、线性时间选择、最接近点对问题、循环赛日程等。

#### 漂亮的数组

若由 1~n 组成的数组 A 满足：对每个 i<j，都不存在 k（i<k<j）使 A[k]*2 = A[i]+A[j]，则 A 是漂亮数组。给定 N，返回任意漂亮数组。

基本思路：

- 漂亮数组 + 漂亮数组 = 漂亮数组；
- 按奇偶位置取值将数组拆成两份，递归拆分，子数组数量 ≤2 时合并。

例如对 [1,2,3,4,5,6,7]：奇数位 [1,3,5,7] -> [1,5]+[3,7] -> [1,5,3,7]；偶数位 [2,4,6] -> [2,6]+[4] -> [2,6,4]；合并得 [1,5,3,7,2,6,4]。

```python
def split_list(nums):
    if len(nums) <= 2:
        return nums
    left = split_list(nums[::2])
    right = split_list(nums[1::2])
    return left + right

split_list(list(range(1, 11)))
# 输出: [1, 9, 5, 3, 7, 2, 10, 6, 4, 8]
```

#### 为运算表达式设计优先级

给定含有数字和运算符（+、-、*）的字符串，通过添加括号改变运算优先级，返回所有可能的结果。

示例：

- "2-1-1" -> [0, 2]：((2-1)-1)=0，(2-(1-1))=2；
- "2*3-4*5" -> [-34, -14, -10, -10, 10]。

分治法实现：

- 分解：按运算符将表达式分成左右两部分，分别求解；
- 解决：递归调用，直到只剩下数字，再按运算符计算子问题的解；
- 合并：根据运算符合并左右两部分的解，得出最终解。

```python
def diff_ways_compute(s):
    # 只有数字时直接返回
    if s.isdigit():
        return [int(s)]
    res = []
    for i, char in enumerate(s):
        if char in ['+', '-', '*']:
            # 1. 遇到运算符，分解字符串，递归求解左右两侧的结果集
            left = diff_ways_compute(s[:i])
            right = diff_ways_compute(s[i + 1:])
            # 2. 合并结果：根据左右计算结果与运算符合并子问题结果
            for l in left:
                for r in right:
                    if char == '+':
                        res.append(l + r)
                    elif char == '-':
                        res.append(l - r)
                    else:
                        res.append(l * r)
    return res

diff_ways_compute("2*3-4*5")
```

