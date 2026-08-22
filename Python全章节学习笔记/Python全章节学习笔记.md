# Python 全章节学习笔记

> 本笔记由 Python 目录下全部课件自动提取整理而成，共 43 个章节文件，涵盖基础语法、函数、文件与数据、面向对象、并发、数据库、数据分析与算法等主题。
> 代码块来自 Jupyter 笔记（算法章节），其余章节为 PPT/PDF 课件文本。

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
- **附录 合并版 PDF（与正文章节内容有重复）**
  - [42. 附录 A：PDF合并PY1（Python 入门综合）](#42-附录-apdf合并py1python-入门综合)
  - [43. 附录 B：PDF合并2-3章（列表等章节合并）](#43-附录-bpdf合并2-3章列表等章节合并)

---

## 第一部分 基础语法与数据结构
### 1. 数字
#### 1 数据结构

主要内容：

目标：

1. 熟练应用数据结构解决当前问题；
2. 锻炼思维，提升编程能力；
3. 掌握当下，用在未来；

#### 2 数字部分内容

如图：

#### 3 数字类型

主要类型：

| 方法/项 | 说明 |
|---|---|
| 类型 | 说明 样例 |
| int | 整数 1,2,3,100... |
| float | 浮点 3.14, 2.1.... |
| complex | 复数 complex(1, 2) |
| bool | 布尔值 只有：True与False |
定义数字变量：

1. 定义pi
2. 定义半径
3. 定义布尔值

```python
pi = 3.14
```
```python
r = 5
```

```python
b = False
```
```python
pi
```
3.14

#### 4 数字计算与类型转换

#### 4.1 数字相关运算符

1. 支持比较运算符
2. 支持算数运算符
3. 支持逻辑运算符

```python
#直播带货，帽子销量100，T-shirt销量120，对比销售量大小；
hat_total = 100
tshirt_total = 120
```
```python
hat_total > tshirt_total
```
False

```python
#计算销售额
hat_price = 40
tshirt_price = 30
hat_sales = hat_price * hat_total
tshirt_sales = tshirt_price * tshirt_total
```

```python
hat_sales
```
4000

```python
tshirt_sales
```
3600

#### 4.2 不同数字类型进行计算，结果如何?

1. Python中，整数与浮点数处理结果？
2. Python中，浮点数与布尔值处理结果？

```python
pi = 3.14
r = 5
```
```python
2 * pi * r
```
31.400000000000002

```python
1 + True
```
2

```python
1 == True
```
True

```python
1.0 == True
```
True

#### 4.3 默认转换规则

默认转换顺序：

complex > float > int > bool

#### 4.4 数字类型强制转换

数据类型强制转换：

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 示例 |
| int([x]) | 将x转成整数 int(3.14)->3 |
| int(x, base=10) | 将数字字符串转整数 int('3')->3 |
float(x=0)将数字或者字符串转浮点 float('3')->3.0

bool(x) 将任意对象转成bool bool(1)->True

```python
#圆面积只保留整数
r = 5
pi = 3.14
```

```python
tmp = pi * (r ** 2)
```
```python
int(tmp)
```
78

```python
int(pi)
```
3

```python
bool(pi)
```
True

```python
bool(0.0)
```
False

```python
int("10", base= 16)
```
16

#### 5 数字相关函数

#### 5.1 基本函数

函数 说明

round(number, ndigits=None)指定小数后位数

pow(x, y, z=None, /)x**y或者x**y%z

abs(x, /) x的绝对值

```python
#对每个计算结果保留2位
#求绝对值
```

```python
pi = 3.14
r = 5
```
```python
tmp = 2*pi* r
tmp
```
31.400000000000002

```python
round(tmp, 1)
```
31.4

```python
pow(2,3)
```
8

```python
a = - 1
```

```python
abs(a)
```
1

#### 5.2 math模块

math模块相关数学函数
使用方式：

import math

#### 5.3 数学常数

函数, math. 说明

pi 表示圆周率，3.141592653589793

e 自然对数的底， 2.718281828459045

#### 5.4 三角函数

函数, math. 说明

sin(x)/cos(x) 返回的x弧度的正/余弦值

asin(x)acos(x)返回x的反正/反余弦弧度值

tan(x) 返回x弧度的正切值

atan(x) 返回x的反正切弧度值

#### 5.5 指数函数等

函数, math. 说明

factorial(x) 计算阶乘，返回x！

sqrt(x) 返回x的平方根

floor(x)取最接近x的整数，返回整数<x

| 方法/项 | 说明 |
|---|---|
| log(x[, base]) | 以 Base 为底的 x 的对数 |
| log10(x) | 以10为底的x的对数 |
| log2(x) | 以2为底的x的对数 |
```python
import math
```

```python
math.sin(0.3)
```
0.29552020666133955

#### 6 强化练习

#### 6.1 给定数字，计算其对应的阶乘

需求：

1）给定数字n，
2）n! = n*(n-1)*(n-2)....*1；
例如：5! = 5*4*3*2*1

思路：

```python
def func(n):
ret = 1
for i in range(1, n+ 1):
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

示例：

1）给定数字：23456，输出:65432
2）给定数字：230，输出：032
3）给定数字：1，输出数字1

```python
def reverse_digit(num):
if num < 10:
print(num)
else :
while num > 0:
print("num:", num)
tmp = num % 10
print(tmp, end= "")
num //= 10
```
```python
reverse_digit(23456)
```
num: 23456
6num: 2345
5num: 234
4num: 23
3num: 2
2
### 2. 字符串详解
#### 1 主要内容

定义字符串
字符串类型
字符串编码格式
生成字符串
字符串相关函数
字符串相关方法

#### 2 定义字符串

字符串：单引号(')，双引号(")，三引号(''', """)开头结尾； 例如：

s1 = "Python"
s2 = 'hat'
s3 = """project"""

常见的错误定义方式：

```python
#引号前后不一致
s = "qimao'
```
File "<ipython-input-1-3a96f76982fa>" , line 2
s = "qimao'
^
SyntaxError : EOL while scanning string literal

```python
#引号中间包含相同引号
s = 'it's me'
```
File "<ipython-input-2-6593473f4b33>" , line 2
s = 'it's me'
^
SyntaxError : invalid syntax

```python
s = "it's me"
```

```python
s = 'it\'s me'
```

```python
s
```
"it's me"

#### 3 字符串类型

>1. 普通字符串:引号开头结尾，例如："this", 'python';
>2. 原字符串：r开头，例如：r'c\c++\Python';
>3. Byte类型：b开头，例如：b'test';

注意点：

1. 原字符串不会对转义符进行转义；
2. Byte类型一般处理编码数据，媒体数据(图片，音乐等)；

```python
s = r'c\c++\Python'
```
```python
s = "it\'s me"
s
```
"it's me"

```python
s1 = r"it\'s me"
s1
```
"it\\'s me"

#### 4 编码格式

基本概念：

是计算机科学领域里的一项业界标准，包括字符集、编码方案等。Unicode是为了解决传统的字符编码方案的局限而产生的，它为每种语言中的每个字符设定了统一并且唯一的二进制编码，以满足跨语言、跨平台进行文
本转换、处理的要求。

编码格式：gbk, utf-6, utf-16, gb2312等；
Unicode是Python3默认编码格式,编码格式转换关系：

编码格式操作；

```python
s = "香蕉"
#编码方式：utf-8
s1 = s.encode('utf-8')
print(type(s1), s1)
#解码方式必须为utf-8
print(s1.decode('utf-8'))
#错误操作：
#print(s1.decode('gb2312'))
```
<class 'bytes'> b'\xe9\xa6\x99\xe8\x95\x89'
香蕉

```python
s = "香蕉"
#编码方式：utf-8
s1 = s.encode('utf-8')
s1
```
b'\xe9\xa6\x99\xe8\x95\x89'

```python
print(type(s1), s1)
```
<class 'bytes'> b'\xe9\xa6\x99\xe8\x95\x89'

```python
s1.decode("utf8")
```
'香蕉'

```python
s1.decode("gb2312")
```
---------------------------------------------------------------------------
UnicodeDecodeError Traceback (most recent call last)
<ipython-input-22-28804593a97d> in <module>
----> 1 s1.decode( "gb2312" )

UnicodeDecodeError : 'gb2312' codec can't decode byte 0x99 in position 2: illegal multibyte sequence

#### 5 创建字符串

#### 5.1 使用%格式化

使用%号，构建字符串，常见例子：

user_name = "name=%s"%("sun")
user_info = "name=%s, age=%d"%("sun", 14)

%s, %d被称为占位符，主要的占位符包括：

| 方法/项 | 说明 |
|---|---|
| 符号 | 说明 |
| %s | 对象str方法的返回值(一般选择这种方式) |
| %r | 对象的repr方法的返回值 |
| %d、%i | 数字格式化 |
| %f | 浮点数格式化 |
| %.nf | 浮点数保留n位小数 |
| %x，%X | 数字格式化为16进制(x,X大小写) |
| %c | 格式化字符及其 ASCII 码 |
| %e | 科学计数法表示的浮点数(e小写) |
```python
s = '%.2f'%(1/3)
s
```
'0.33'

#### 5.2 f字符串

f字符串是python3.6版本中新增语法，语法格式如下：

f'{var1} {var1}'

f字符串特点:

1. 字符串以f或者F开头，f'{a}',a变量必须定义
2. f字符串优点：使用更加方便

练习： 给定英雄与类型：

hero_names = ["程咬金", "马超","蔡文姬", "王昭君", "曹操"]
hero_types = ["坦克", "刺客","游走", "法师", "战士"]

输出结果：

程咬金:坦克
马超:刺客
蔡文姬:游走
王昭君:法师
曹操:战士

```python
hero_names = ["程咬金", "马超","蔡文姬", "王昭君", "曹操"]
hero_types = ["坦克", "刺客","游走", "法师", "战士"]
```
```python
for name, t in zip(hero_names, hero_types):
line = f"{name}:{t}"
print(line)
```
程咬金:坦克
马超:刺客
蔡文姬:游走
王昭君:法师
曹操:战士

```python
for item in zip(hero_names, hero_types):
print(item)
```
('程咬金', '坦克')
('马超', '刺客')
('蔡文姬', '游走')
('王昭君', '法师')
('曹操', '战士')

#### 6 字符串相关函数

#### 6.1 字符串相关函数

函数 说明

str(object='') 将对象转成字符串对象

sorted(iterable,key=None, reverse=False)对迭代对象排序，返回列表

| 方法/项 | 说明 |
|---|---|
| ord(c) | 将字符转成ASCII码 |
| chr(i) | 将ASCII码转成字符 |
| int(str) | 将字符串转成数字 |
| float(str) | 将字符串转成浮点数 |
```python
str(10)
```
'10'

```python
l = [1,2,3]
```
```python
str(l)
```
'[1, 2, 3]'

ASSIC码表

#### 6.2 练习1

输出下面内容：
给定字符列表，输除其对应的ASCII码，例如：

listchr = ['a', 'z', 'c']
输出结果：

```python
listchr = ['a', 'z', 'c']
for char in listchr:
print(char, ord(char))
```
a 97
z 122
c 99

#### 6.3 练习2

给定两个字符，输出两个字符之间所有的字符 例如：

1. 给定[a,d],输出：abcd；
2. 给定[d,z],输出：defg...z;

```python
def func(start, end):
s = ""
for val in range(ord(start), ord(end)+ 1):
s += chr(val)
print(s)
return s
```
```python
func("d", "z")
```
d
de
def
defg
defgh
defghi
defghij
defghijk
defghijkl
defghijklm
defghijklmn
defghijklmno
defghijklmnop
defghijklmnopq
defghijklmnopqr
defghijklmnopqrs
defghijklmnopqrst
defghijklmnopqrstu
defghijklmnopqrstuv
defghijklmnopqrstuvw
defghijklmnopqrstuvwx
defghijklmnopqrstuvwxy
defghijklmnopqrstuvwxyz

'defghijklmnopqrstuvwxyz'

#### 7 字符串相关方法

#### 7.1 查找

查找：查找子串位置

方法 说明 参数

S.find(sub[, start[, end]])从前向后查找，返回sub在S第一次出现位置，不存在返回-1 start与stop限定查找范围

| 方法/项 | 说明 |
|---|---|
| S.rfind(sub[, start[, end]]) | 从后向前查找，功能同上， 同上 |
| S.index(sub[, start[, end]]) | 功能同S.find, 不同：子串不存在报异常 同上 |
| S.count(sub[, start[, end]]) | 返回子串在S中出现次数 同上 |
练习：

给定字符串：phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'，
需求:解析小米11的价格

```python
phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'
```
```python
start = phoneprice.find("小米11:")
end = phoneprice.find(",", 13)
```
```python
phoneprice[start+ len("小米11:"):end]
```
'3599'

```python
phoneprice.find("9")
```
11

```python
phoneprice.rfind("9")
```
33

#### 7.2 替换

替换：将指定子串替换成新的字符串

方法 说明

S.replace(old, new[, count])将old使用new替换，返回新的字符串

| 方法/项 | 说明 |
|---|---|
| 参数：old | 被替换字符串 |
| 参数：new | 替换后内容 |
| 参数：count | 替换数量，默认替换所有 |
练习：

给定：s="li:level1, sun:level2, liu:level2"
替换：s = "li:A+， sun:A, liu:A"

```python
s = "age:9899"
new_s = s.replace("9", "*", 1)
```

```python
new_s
```
'age:*899'

```python
s= "li:level1, sun:new_s, liu:level2"
new_s = s.replace("level1", "A+")
```

```python
levels = ["level1", "level2", "level3"]
new_level = ["A+", "A", "B+"]
new_str = "li:level1, sun:level2, liu1:level2, liu2:level3"
for old, new_s in zip(levels, new_level):
new_str = new_str.replace(old, new_s)
print(new_str)
```
li:A+, sun:A, liu1:A, liu2:B+

```python
new_s = new_s.replace("level2", "A")
```
```python
new_s
```
'li:A+, sun:A, liu:A'

#### 7.3 字符串切分

切分：将字符串按照指定分隔符进行分割，得到字符串列表

方法 说明

S.split(sep=None, maxsplit=-1)从前向后通过sep对S切分，返回切分子串组成的列表

| 方法/项 | 说明 |
|---|---|
| S.rsplit(sep=None, maxsplit=-1) | 从后向前切分，功能同上 |
| 参数：sep | 分隔符，默认所有空字符， |
| 参数：maxsplit | 指定切分数量，默认所有的都要切分 |
练习：

1. 程序员A技能："python C++ C Java Mysql Hive",问：A掌握几门技能？
2. 图片地址："http://i1.umei.cc/uploads/tu/201711/9999/6e312a86a7.jpg" (http://i1.umei.cc/uploads/tu/201711/9999/6e312a86a7.jpg"), 问：如何获取图片名称及图片类型？
3. 给定字符串：phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'，解析字符串中所有手机类型及对应的价格

```python
skills = "python C++ C Java Mysql Hive"
```
```python
len(skills.split())
```
6

```python
url = "http://i1.umei.cc/uploads/tu/201711/9999/6e312a86a7.jpg"
```

```python
pic_name = url.rsplit("/", 1)[- 1]
pic_name.split(".")[- 1]
```
'jpg'

```python
pic_name
```
'6e312a86a7.jpg'

```python
phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'
```
```python
items = phoneprice.split(",")
```
```python
for item in items:
name, price = item.split(":")
print(f"{name}的售价：{price}")
```
荣耀50Pro的售价：3689
小米11的售价：3599
vivoX60的售价：4498

```python
s = "1\n2\n3"
```
```python
s.split()
```
['1', '2', '3']

#### 7.4 字符串拼接

拼接：使用指定分隔符将可迭代字符串组成新的字符串

方法 说明

S.join(iterable)使用S将迭代对象中的元素(字符串类型)拼接成新的字符串

S 指定的连接符

iterable 字符串迭代对象

练习： skills = ['c++', 'Python', 'Java']，将技能列表进行拼接，结果：'c++/Python/Java'

```python
skills = ['c++', 'Python', 'Java']
```

```python
"/".join(skills)
```
'c++/Python/Java'

```python
";".join(skills)
```
'c++;Python;Java'

#### 7.5 strip方法：

strip方法：用于对字符串头尾进行处理，示意图如下：

方法 说明

S.strip(chars=None)从S头尾处理，删除在chars中的元素，如果元素不在chars中，停止删除

| 方法/项 | 说明 |
|---|---|
| S.lstrip(chars=None) | 从S的开始位置开始处理，功能同上 |
| 方法 | 说明 |
| s.rstrip(chars=None | 从S的结尾位置开始处理，功能同上 |
| 参数：chars | 为指定字符集，默认为空白字符 |
```python
s = " \n msg "
```

```python
s
```
' \n msg '

```python
s.strip()
```
'msg'

```python
s = "#-msg#-"
```

```python
s.strip("-#")
```
'msg'

```python
s.lstrip("#-")
```
'msg#-'

```python
s.rstrip("#-")
```
'#-msg'

#### 7.6 字符串开头结尾判断

字符串判断开头或结尾：

方法 说明

S.startswith(prefix[, start[, end]])S以指定子串开头返回True，否则返回False

S.endswith(suffix[, start[, end]])S以指定子串结尾返回True, 否则返回False

| 方法/项 | 说明 |
|---|---|
| 参数：prefix | 子串 |
| 参数：start | 起始索引 |
| 参数：end | 结束索引 |
练习：过滤出所有的小米手机

mi = 'xiaomi'
listphone = ['xiaomi11', 'huaweimeta20', 'xiaomi11Pro', 'xiaomi10']

输出结果：

xiaomi11
xiaomi11Pro
xiaomi10

```python
s = "hello"
sub_s = "he"
```
```python
s.endswith("e")
```
False

```python
mi = 'xiaomi'
listphone = ['xiaomi11', 'huaweimeta20', 'xiaomi11Pro', 'xiaomi10']
```

```python
for phone in listphone:
if phone.startswith(mi):
print(phone)
```
xiaomi11
xiaomi11Pro
xiaomi10

#### 7.7 字符串大小写转换

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 返回值 |
| S.lower() | 将字符串中所有大写字符为小写 返回新字符串 |
| S.upper() | 将字符串中的小写字母转为大写字母 同上 |
| S.title()字符串标题化，将每个单词首字母大写，其他小写 | 同上 |
| S.capitalize() | 将字符串中的首字母大写，其他小写 同上 |
| S.swapcase() | 将字符串中的大小写交换 同上 |
练习：

```python
s = 'Python CookBook'
print('原字符串：',s)
print('字符全部小写：',s.lower())
print('字符全部大写：',s.upper())
print('单词首字母大写：',s.title())
print('首字母大写：',s.capitalize())
print('大小写转换：',s.swapcase())
```
原字符串： Python CookBook
字符全部小写： python cookbook
字符全部大写： PYTHON COOKBOOK
单词首字母大写： Python Cookbook
首字母大写： Python cookbook
大小写转换： pYTHON cOOKbOOK

#### 7.8 format方法

format：

1. 可以使用{}用来代替%，且参数位置与个数不受限制：
2. 指定位置{n}对应第n个参数;
3. 指定参数{name}；

练习：

```python
f = '{} age is {}'
print(f.format('sun', 18))
print(f.format('li', 19))
f = '{1} age is {0}'
#{1}对应zhang, {0}对应20
print(f.format(20, 'zhang'))
#指定参数
f = '{name} age is {age}'
print(f.format(name = 'zhao', age = 20))
```

```python
f = '{} age is {}'
print(f.format('sun', 18))
print(f.format('li', 19))
```
sun age is 18
li age is 19

```python
f = '{1} age is {0}'
#{1}对应zhang, {0}对应20
print(f.format(20, 'zhang'))
```
zhang age is 20

```python
#指定参数
f = '{name} age is {age}'
print(f.format(name = 'zhao', age = 20))
```
zhao age is 20

#### 7.9 字符串判断相关方法

主要内用于大小写，字符类型判断：

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| S.isalpha() | 判断字符串中所有字符为字母 |
| S.isdigit() | 判断字符串中所有字符为数字 |
| S.islower/isupper() | 判断字符串中所有字符为小/大写字母 |
| S.isspace() | 判断字符串中所有字符为空格 |
S.istitle()判断字符串中所有的单词拼写首字母是否为大写，且其他为小写

```python
s = "12345"
s.isdigit()
```
True

```python
s = "abcd1"
s.isalpha()
```
False
### 3. 列表
#### 1 主要内容

主要内容：

如何创建列表
可变数据结构
列表相关函数
列表相关方法

#### 2 列表基础

1. 列表定义方式：[value1, value2, ....]
2. 列表理解：理解为容器，可以存放任意对象；
3. 列表支持：修改，插入，删除；

```python
l = [1, "1", "123", None ]
```

```python
l
```
[1, '1', '123', None]

#### 2.1 列表创建方式

1. 直接定义列表：list1 = [1,'1','2',3']
2. 多维列表：list2 = [1,2,3,['a','b', 'c']]
3. 使用list函数：list(iterable=(), /)

```python
s = "qimao"
```

```python
tmp = list(s)
tmp
```
['q', 'i', 'm', 'a', 'o']

```python
"".join(tmp)
```
'qimao'

#### 2.2 列表遍历

1. 使用while+索引；
2. 使用for循环进行遍历；
3. 多维列表访问：list2[3][0]

练习：遍历二维列表

scores = ["class_1", ["sun",80, 60], ["zhao", 70, 90]]

```python
scores = ["class_1", ["sun",80, 60], ["zhao", 70, 90]]
```
```python
type(scores)
```
list

```python
isinstance(scores, list)
```
True

```python
isinstance(scores, str)
```
False

```python
for item in scores:
if isinstance(item, list):
for val in item:
print(val)
else :
print(item)
```
class_1
sun
80
60
zhao
70
90

```python
scores
```
['class_1', ['sun', 80, 60], ['zhao', 70, 90]]

```python
scores[0:2]
```
['class_1', ['sun', 80, 60]]

#### 2.3 列表修改

列表是一种可变的数据结构，修改列表中的某个元素，列表不变；

listv = [60, 90, 59]
listv[1] = 62

练习：给定一个成绩列表，如果成绩为-1，将其修改为0；
例如：a = [96, 80, -1, 66]

例如：a [96, 80, 1, 66]

```python
listv = [60, 90, 59]
listv[1] = 62
print(listv)
```

```python
a = [96, 80, - 1, 66]
for index, val in enumerate(a):
if val == -1:
a[index] = 0
```

#### 3 列表相关函数

方法 说明

list(iterable=(), /) 将迭代对象转成列表

max/min(iterable, [key=func]) 获取最大最小值

len(obj) 获取长度

sum(iterable, start=0, /)迭代对象求和，迭代对象元素必须为数字；

练习：给定字符串列表，找出对应的数字的最大元素，
例如：listnum = ['200', '798','1000'],返回值：'1000'

```python
listnum = ['200', '798','1000']
```

```python
max(listnum, key= int)
```
'1000'

```python
l = [100, 200, 400, 599]
```
```python
sum(l)
```
1299

#### 4 列表相关方法

#### 4.1 列表中添加元素

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| l.append(obj) | 在列表尾部添加元素 |
| l.insert(index, obj) | 指定索引插入元素 |
L.extend(iterable)在尾部扩展列表，将可迭代对象元素添加到列表尾部

```python
l = [1,2,3]
#尾部添加4
l.append(4)
print(l)
#在起始位置插入-1
l.insert(0,- 1)
print(l)
#extend添加可迭代对象
s = '567'
l.extend(s)
print(l)
```
```python
l = [1,2,3]
#尾部添加4
l.append(4)
```

```python
l
```
[1, 2, 3, 4]

```python
#在起始位置插入-1
l.insert(0,- 1)
print(l)
```
[-1, 1, 2, 3, 4]

```python
s = '567'
l.extend(s)
print(l)
```
[-1, 1, 2, 3, 4, '5', '6', '7']

#### 4.2 列表统计与查找

方法 说明

L.count(value) 统计value在L中出现次数

L.index(value, [start, [stop]])返回value第一次出现位置，不存在报异常

示例：

```python
l = [1,2,3,4,3,5,3]
print('3出现次数：',l.count(3))
print('3第一次出现位置:',l.index(3))
#注意返回值，认为该元素在列表中实际的位置
print('3在索引为3之后，第一次出现位置:',l.index(3,3))
```
```python
l = [1,2,3,4,3,5,3]
print('3出现次数：',l.count(3))
```
3出现次数： 3

```python
print('3第一次出现位置:',l.index(3))
```
3第一次出现位置: 2

```python
print('3在索引为3之后，第一次出现位置:',l.index(3,3))
```
3在索引为3之后，第一次出现位置: 4

#### 4.3 列表删除

方法 说明

l.pop(index=-1, /) 删除并返回index对应的value,默认值为-1

l.remove(value, /)删除第一次出现value的值，如果不存在产生异常

l.clear() 清空列表

示例：

```python
l = [1,4,2,4,3,4]
#删除最后一个元素
l.pop()
print(l)
#删除第一个元素
l.pop(0)
print(l)
#删除第一个4
l.remove(4)
print(l)
#清空列表
l.clear()
print(l)
```
```python
l = [1,4,2,4,3,4]
#删除最后一个元素
l.pop()
print(l)
```
[1, 4, 2, 4, 3]

```python
l.pop(0)
print(l)
```
[4, 2, 4, 3]

```python
l.remove(4)
print(l)
```
[2, 4, 3]

```python
l.clear()
print(l)
```
[]

#### 4.4 列表陷阱

动态删除列中，可能造成某些问题，达不到想要的效果，例如：删除列表中重复元素；

```python
vals = [1,2,3,4,4,5,4,5,6]
for val in vals:
if vals.count(val) > 1:
vals.remove(val)
print(vals)
print(vals)
```
[1, 2, 3, 4, 4, 5, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 4, 5, 6]
[1, 2, 3, 4, 5, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 6]

```python
vals = [1,2,1,2,3,4,4,5,4,5,6]
while True :
for item in vals:
if vals.count(item) > 1:
vals.remove(item)
break
else :
break
print(vals)
```
[1, 2, 3, 4, 5, 6]

#### 5 元组

元组与列表类似，但是元组不可变；

#### 5.1 创建元组:

1. 方式1：t1 = (1,2,3)
2. 方式2：t2 = tuple("123")

```python
t1 = (1,2,3)
t1
```
(1, 2, 3)

```python
1,2,3
```
(1, 2, 3)

```python
tuple("1234")
```
('1', '2', '3', '4')

```python
tuple([1,2,3,4])
```
(1, 2, 3, 4)

```python
a, b,c = (1,2,3)
```

#### 5.2 元组常用的方法

方法 说明

T.count(value) 统计value在L中出现次数

T.index(value, [start, [stop]])返回value第一次出现位置，不存在产生异常

#### 5.3 问题：元组和列表类似，为什么还要使用元组？

元组不可变，在某些场景下，我们希望数据不变化的时候，就可以使用元组;

```python
t1 = (1,2,3)
```
```python
t1[0] = -1
```
---------------------------------------------------------------------------
TypeError Traceback (most recent call last)
<ipython-input-64-dfabc5d41138> in <module>
----> 1 t1[0] = -1

TypeError : 'tuple' object does not support item assignment

#### 6 列表强化练习

#### 6.1 练习1：

在有序列表中插入元素，需求：

1. 给定有序的数字列表，
2. 从键盘读取输入数字，将输入值插入到列表中，使其有序，
3. 输入值为：q,退出循环
例如：
v = [1,2,3]
输入：2
结果：[1,2,2,3]
输入：5
结果：[1,2,2,3,5]

基本思路如图：

```python
def insert_value(listnum):
while True :
val = input("输入数字:")
if val == "q":
break
val = int(val)
for index, item in enumerate(listnum):
if val <= item:
listnum.insert(index, val)
break
else :
listnum.append(val)
print(listnum)
listn = [1,2,3]
insert_value(listn)
```
输入数字:1
[1, 1, 2, 3]
输入数字:0
[0, 1, 1, 2, 3]
输入数字:1000
[0, 1, 1, 2, 3, 1000]
输入数字:20
[0, 1, 1, 2, 3, 20, 1000]
输入数字:q

#### 6.2 练习2：

数字转成数字列表，例如：

输入：320,输出：[3,2,0]
输入：9527,输出：[9,5,2,7]

```python
def num_to_list(num):
result = []
snum = str(num)
for value in snum:
result.append(int(value))
return result
```

```python
num_to_list(320)
```
[3, 2, 0]

```python
num_to_list(9527)
```
[9, 5, 2, 7]

#### 6.3 练习3：

需求：将两个有序列数字列表进行合并，并使其有序，例如：

v1 = [1,2,3,4]
v2 = [2,5,8]
结果：
v = [1,2,2,3,4,5,8]

要求：不要使用默认排序算法；

```python
def megre_list(n1, n2):
result = []
l1 = len(n1)
l2 = len(n2)
index1, index2 = 0, 0
while index1 < l1 and index2 < l2:
print(f"index1:{index1}, index2:{index2}")
if n1[index1] <= n2[index2]:
result.append(n1[index1])
index1 += 1
else :
result.append(n2[index2])
index2 += 1
if index1 < l1:
tail = n1[index1:]
else :
tail = n2[index2:]
result.extend(tail)
print(result)
return result
```
```python
v1 = [1,2,3,4, 10]
v2 = [0,1,2,5,8]
megre_list(v1, v2)
```
index1:0, index2:0
index1:0, index2:1
index1:1, index2:1
index1:1, index2:2
index1:2, index2:2
index1:2, index2:3
index1:3, index2:3
index1:4, index2:3
index1:4, index2:4
[0, 1, 1, 2, 2, 3, 4, 5, 8, 10]

[0, 1, 1, 2, 2, 3, 4, 5, 8, 10]
### 4. 列表解析
#### 1 主要内容

列表解析语法
列表解析应用

#### 2 列表解析详解

基本概念：列表解析：在一个序列中应用表达式，并将结果保存到列表中；

#### 2.1 列表解析基本使用方式

基本语法：

[expr for iter in iterable]

主要参数：

参数 说明

iterable 迭代对象

iteriterable中的元素

expr 表达式

执行流程：

#### 2.2 列表解析基本练习

1. 生成列表：[1,2,3,4,5]
2. 生成列表：["0", "1", "2", "3", "4", "5"]
3. 将520转成：[5,2,0]

```python
[val for val in range(1, 6)]
```
[1, 2, 3, 4, 5]

```python
[val ** 2 for val in range(1, 6)]
```
[1, 4, 9, 16, 25]

```python
[pow(val, 2) for val in range(1, 6)]
```
[1, 4, 9, 16, 25]

```python
[str(val) for val in range(0, 6)]
```
['0', '1', '2', '3', '4', '5']

```python
[int(val) for val in str(520)]
```
[5, 2, 0]

```python
import random
```
```python
[random.randint(1, 100) for i in range(10)]
```
[18, 53, 68, 53, 72, 18, 33, 49, 84, 37]

#### 2.3 列表解析与判断条件

基本语法：

[expr(value) for value in iter if cond_expr(value)]

执行过程：

#### 2.4 列表解析条件判断练习

1. 生成1~100之间偶数列表；
2. 给定成绩：[59, 100, 20, 30, 80]，过滤出成绩大于等于60的成绩；
3. 给定一段英文歌曲，统计每个单词长度与总长；

英文歌曲部分歌词：

When I was young I'd listen to the radio
Waiting for my favorite songs
When they played I'd sing along,

It made me smile.

```python
res = [val for val in range(1, 101) if val% 2==0]
print(res)
```
[2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100]

```python
scores = [59, 100, 20, 30, 80]
[score for score in scores if score >= 60]
```
[100, 80]

```python
scores = [59, 100, 20, 30, 80]
[score >= 60 for score in scores]
```
[False, True, False, False, True]

```python
words = """
When I was young I'd listen to the radio
Waiting for my favorite songs
When they played I'd sing along,
It made me smile.
"""
```

```python
word_len = [len(word) for word in words.split()]
```
```python
word_len
```
[4, 1, 3, 5, 3, 6, 2, 3, 5, 7, 3, 2, 8, 5, 4, 4, 6, 3, 4, 6, 2, 4, 2, 6]

```python
sum(word_len)
```
98

#### 2.5 多重循环列表解析

基本语法：

[expr(v1,v2) for v1 in iters1 for v2 in iters2]

执行过程：

1：取v1,
2：顺序去v2,
3：执行expr(v1,v2),
4：重复1~3步骤，

```python
[(v1, v2) for v1 in range(1,4) for v2 in range(1,4)]
```
[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

#### 2.6 多重循环列表解析练习

1. 给定两个数字列表，计算两两的乘积；
2. 使用列表解析完成1~9乘法口诀； 输出结果：

['1*1=1', '1*2=2', '2*2=4', '1*3=3', '2*3=6', '3*3=9', '1*4=4', '2*4=8', '3*4=12', '4*4=16', '1*5=5', '2*5=10', '3*5=15', '4*5=20', '5*5=25', '1*6=6', '2*6=12', '3*6=18', '4*6=24', '5*6=30',
'6*6=36', '1*7=7', '2*7=14', '3*7=21', '4*7=28', '5*7=35', '6*7=42', '7*7=49', '1*8=8', '2*8=16', '3*8=24', '4*8=32', '5*8=40', '6*8=48', '7*8=56', '8*8=64', '1*9=9', '2*9=18', '3*9=27', '4*
9=36', '5*9=45', '6*9=54', '7*9=63', '8*9=72', '9*9=81']

```python
[v1 * v2 for v1 in range(1,4) for v2 in range(1,4)]
```
[1, 2, 3, 2, 4, 6, 3, 6, 9]

```python
res = [f"{j}*{i}={i* j}" for i in range(1, 10) for j in range(1, 10) if i >= j]
print(res)
```
['1*1=1', '1*2=2', '2*2=4', '1*3=3', '2*3=6', '3*3=9', '1*4=4', '2*4=8', '3*4=12', '4*4=16', '1*5=5', '2*5=10', '3*5=15', '4*5=20', '5*5=25', '1*6=6', '2*6=12', '3*6=18', '4*6=24', '5*6=30', '6*6=3
6', '1*7=7', '2*7=14', '3*7=21', '4*7=28', '5*7=35', '6*7=42', '7*7=49', '1*8=8', '2*8=16', '3*8=24', '4*8=32', '5*8=40', '6*8=48', '7*8=56', '8*8=64', '1*9=9', '2*9=18', '3*9=27', '4*9=36', '5*9=4
5', '6*9=54', '7*9=63', '8*9=72', '9*9=81']

```python
l = [f"{j}*{i}={i* j}" for i in range(1, 10) for j in range(1, 10) if i>= j]
```
### 5. 序列
#### 1 主要内容

如图

重点：

1. 掌握序列的通用方法
2. 重点掌握字符串列表使用；
3. 学习编程思路，提升代码编写与调试能力

#### 2 序列

#### 2.1 主要对象

如图：

#### 2.2 序列结构

问题：如何去理解序列？

注意：

1. 索引起始值为：0
2. 索引最大值：(序列长度)-1
3. 负向索引，最后一个元素为索引为：-1

#### 2.3 序列访问方式

如图：

```python
s = "123"
```
```python
s[0],s[-1]
```
('1', '3')

```python
s[100]
```
---------------------------------------------------------------------------
IndexError Traceback (most recent call last)
<ipython-input-28-2a138df92e52> in <module>
----> 1 s[ 100]

IndexError : string index out of range

基本语法：

s = "helloCoCo"
#第一个元素
s[0]
#最后一个元素
s[-1]
#切片操作
s[:2]
s[2:]

注意：

1. 序列访问不能越界
2. 重点理解切片操作，灵活使用索引

#### 2.4 序列访问示意图

如图：

#### 2.5 序列遍历

序列遍历方式：

1. 使用for循环
2. 使用while循环

```python
s
```
'helloCoCo'

```python
for val in s:
print(val)
```
h
e
l
l
o
C
o
C
o

#### 2.6 序列运算符

如图：

常见操作：

1. 比较运算符
2. not操作
3. 加法操作
4. 乘法操作

#### 2.7 序列相关函数

序列支持通用函数：

| 方法/项 | 说明 |
|---|---|
| 函数 | 说明 |
| len(obj) | 获取可迭代对象长度 |
| max(iterable, *[, default=obj, key=func]) | 获取迭代对象中最大值，func为元素处理函数 |
| min(iterable, *[, default=obj, key=func]) | 获取迭代对象中最小值，func为元素处理函数 |
val in seq val在seq中返回True, 否则返回False

val not in seq val不在seq中返回True, 否则返回False

all(iterable, /)如果iter中每个对象x, 其bool(x)都为真，返回真，否则返回False

any(iterable, /)如果iter中每个对象x, 其bool(x)有一个为真，返回真，否则返回False

zip(*iterables) 将多个可迭代队形进行合并，返回zip对象

sorted(iterable, /, *, key=None, reverse=False) 对迭代对象进行排序，默认从小到大,返回列表

#### 2.8 理解max，min中的key

给定一个数字列表：

vals = [1, -10, 3, -11, 8, -3]

需求：

1. 获取列表中最大的元素
2. 获取列表中绝对值最大的元素

```python
vals = [1, -10, 3, -11, 8, -3]
max(vals, key=abs), max(vals)
```

对key的理解

1. 设置key函数,
2. 每个元素使用key函数进行处理,
3. max,min函数根据处理后结果选择最大或者最小值；
4. 返回最大最小值对应的元素；

处理过程如图：
### 6. 字典
#### 1 主要内容

理解字典
字典创建方式
字典相关函数
字典相关方法

#### 2 字典介绍

#### 2.1 基本概念

字典是Python中唯一映射性数据结构；

1. 字典定义：{key1:value, key2:value}，key在字典中是唯一的；
2. 字典是一种可变的容器模型，可以存储任意类型对象；
3. 字典在python3.6版本中是有序的数据结构；

使用场景：对应关系

1. 姓名：张飞
2. ID:9527

需求：定义一个用户信息，包括：姓名，性别，年龄

```python
user_info = {"name":"张", "sex":"male", "age":"28"}
```
```python
user_info
```
{'name': '张', 'sex': 'male', 'age': '28'}

```python
user_info["name"]
```
'张'

#### 2.2 字典定义

基本形式：

#### 2.3 字典key要求

字典中的key是唯一的，并且可以hash
判断下填埋你字典的值：

```python
info = {"id":"8001", "port":80, "port":8001}
dvalue = {1:'one', 1.0:"1"}
```

```python
info
```
{'id': '8001', 'port': 8001}

```python
dvalue = {1:'one', 1.0:"1"}
```
```python
dvalue
```
{1: '1'}

```python
hash(1), hash(1.0)
```
(1, 1)

```python
d = {[]:1}
```
---------------------------------------------------------------------------
TypeError Traceback (most recent call last)
<ipython-input-11-d3a40b24cabb> in <module>
----> 1 d = {[ ]:1}

TypeError : unhashable type: 'list'

#### 2.4 字典访问

两种形式：

1. 访问单个元素：d[key]
2. 遍历字典；for循环进行遍历

```python
info
```
{'id': '8001', 'port': 8001}

```python
info["id"]
```
'8001'

```python
info["sex"]
```
---------------------------------------------------------------------------
KeyError Traceback (most recent call last)
<ipython-input-14-0809afa984f2> in <module>
----> 1 info[ "sex" ]

KeyError : 'sex'

```python
for key in info:
print(key, info[key])
```
id 8001
port 8001

#### 2.5 字典修改

基本语法：d[key] = value

```python
info
```
{'id': '8001', 'port': 8001}

```python
info["id"] = 800
```
```python
info
```
{'id': 800, 'port': 8001}

#### 3 字典相关函数

#### 3.1 创建字典

dict函数：

1. dict()：创建空字典
2. dict(mapping)：创建字典

```python
d = {}
```
```python
d['id'] = 9527
```
```python
d
```
{'id': 9527}

```python
#二维列表，每个字列表元素必须是两个
d1 = dict([['name','sun'],['score',90]])
#列表与元组组合，元组每个元素必须是两个
d3 = dict([(1,2),(3,4)])
#列表与字符串，字符串长度必须是两个
d2 = dict(['12','34'])
```

```python
d1 = dict([['name','sun'],['score',90]])
d1
```
{'name': 'sun', 'score': 90}

```python
d3 = dict([(1,2),(3,4)])
d3
```
{1: 2, 3: 4}

```python
d2 = dict(['12','34'])
d2
```
{'1': '2', '3': '4'}

```python
l1 = ["name","age"]
l2 = ["li", 18]
```
```python
dict(zip(l1, l2))
```
{'name': 'li', 'age': 18}

#### 3.2 其他函数

| 方法/项 | 说明 |
|---|---|
| 函数 | 说明 |
| len(obj) | 返回字典长度 |
| sum(iterable) | 对字典所有key求和 |
max/min(iterable, key=func)获取字典中key中的最大值

key in dict 判断key是否在字典中

```python
d = dict([(1,2),(3,4)])
print('len(d):',len(d))
print('sum(d):', sum(d))
print('max(d):', max(d))
```
len(d): 2
sum(d): 4
max(d): 3

```python
d
```
{1: 2, 3: 4}

```python
1 in d
```
True

```python
5 in d
```
False

```python
5 not in d
```
True

#### 4 字典相关方法

#### 4.1 fromkeys

dict.fromkeys(iterable, value=None, /)：根据可迭代对象创建字典；
主要参数：

1. iterable：迭代对象，每个元素可以hash
2. value：设置每个key的默认值，默认为None

需求：

1.生成字典：d1 = {1:0,2:0,3:0,....9:0},
2.生成字典：d2 = {"a":1,"b":1,"c":1},

```python
d = {}
for key in range(1, 10):
d[key] = 0
d
```
{1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

```python
dict.fromkeys(range(1, 10), 0)
```
{1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

```python
s = "abc"
d2 = dict.fromkeys(s, 1)
```
```python
d2
```
{'a': 1, 'b': 1, 'c': 1}

#### 4.2 获取字典的k和v

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| D.keys() | 获取字典所有keys, |
| D.values() | 获取字典所有values, |
| D.items() | 获取字典没对键值组成的item对象； |
需求：
给定下面数据：

user_info = dict([('name','sun'), ('age',18)])
user_kpi = {"Q1":90, "Q2":80, "Q3":89,"Q4":85}

1. 遍历d1的所有key与value
2. 计算用户KPI均值

```python
user_info = dict([('name','sun'), ('age',18)])
```
```python
user_info
```
{'name': 'sun', 'age': 18}

```python
tmp = user_info.keys()
```

```python
list(user_info.keys())
```
['name', 'age']

```python
user_info.values()
```
dict_values(['sun', 18])

```python
for k, v in user_info.items():
print(k, v)
```
name sun
age 18

```python
user_kpi = {"Q1":90, "Q2":80, "Q3":89,"Q4":85}
```
```python
sum(user_kpi.values())/ len(user_kpi)
```
86.0

#### 4.3 get方法

dict.get(key, default=None)：获取key对应值，若不存在返回default； 需求：

user_kpi = {"Q1":90, "Q2":80, "Q3":89}

1. 获取用户Q1与Q4的KPI
2. 若KPI不存在返回-1

```python
user_kpi = {"Q1":90, "Q2":80, "Q3":89}
```

```python
user_kpi.get("Q1")
```
90

```python
user_kpi.get("Q4", - 1)
```

-1

```python
user_kpi["Q4"]
```
---------------------------------------------------------------------------
KeyError Traceback (most recent call last)
<ipython-input-23-ad7a4d3c8731> in <module>
----> 1 user_kpi[ "Q4" ]

KeyError : 'Q4'

#### 4.4 setdefault方法

dict.setdefault(self, key, default=None)：添加元素；

1. 如果key存在，返回key对应的值，不添加元素；
2. 如果key在字典中不存在，在字典中添加元素：{key:defatult}

需求:设置KPI:

user_kpi = {"Q1":90, "Q2":80, "Q3":89}
Q1设置为80
Q4设置为96

1. 如果当前KPI存在，不修改；
2. 如果当前KPI不存在，设置给定值；

```python
user_kpi = {"Q1":90, "Q2":80, "Q3":89}
```

```python
user_kpi.setdefault("Q1", 80)
```
90

```python
user_kpi
```
{'Q1': 90, 'Q2': 80, 'Q3': 89}

```python
user_kpi.setdefault("Q4", 96)
```
96

```python
user_kpi
```
{'Q1': 90, 'Q2': 80, 'Q3': 89, 'Q4': 96}

#### 4.5 字典删除

方法 说明

D.pop(k[,d])返回并删除k对应的元素，若k在D中不存在且设置d，返回d,否则异常

D.popitem() 返回并删除一组元素k-v

D.clear() 清空字典

需求：删除order_info中的price信息；

```python
order_info = {"id":8566,"product_name":"pc", "channel":"douyin", "price":999}
```

```python
order_info.pop("price")
```
999

```python
order_info
```
{'id': 8566, 'product_name': 'pc', 'channel': 'douyin'}

```python
order_info.pop("price", - 1)
```
-1

#### 4.6 字典更新

方法：update

D.update([E, ]\*\*F)：更新或者添加多个元素， E为字典，F为可迭代对象(k,v)

如图

更新过程：

1. 更新：D[k] = E[k]；
2. 添加：D[k] = E[k]

```python
user_kpi = {"Q1":90, "Q2":80, "Q3":89}
new_kpi = {"Q1":80, "Q4":90}
```

```python
user_kpi.update(new_kpi)
```
```python
user_kpi
```
{'Q1': 80, 'Q2': 80, 'Q3': 89, 'Q4': 90}

#### 5 练习

#### 5.1 练习1：统计字符出现数量

需求：给定一个字符串，统计每个字符出现次数，例如：

s = 'aabb'
结果：{a:2, b:2}

```python
def count_char(s):
cinfo = {}
for c in s:
if cinfo.get(c, 0):
cinfo[c] += 1
else :
cinfo[c] = 1
return cinfo
```
```python
s = "aabbccccddddeeee"
count_char(s)
```
{'a': 2, 'b': 2, 'c': 4, 'd': 4, 'e': 4}

```python
def count_char2(s):
char_keys = [chr(val) for val in range(ord("a"), ord("z")+ 1)]
cinfo = dict.fromkeys(char_keys, 0)
for c in s:
cinfo[c] += 1
[cinfo.pop(key) for key in char_keys if cinfo[key] == 0]
return cinfo
```
```python
count_char2(s)
```
{'a': 2, 'b': 2, 'c': 4, 'd': 4, 'e': 4}

#### 5.2 练习2：删除字典中指定数据

给定员工信息，删除KPI评分小于6的所有用户信息

kpi_info = {
1001:{"score":8.9, "name":"sun"},
1002:{"score":8, "name":"zhang"},
1003:{"score":5.9, "name":"zhao"},
1004:{"score":4.2, "name":"li"},
1005:{"score":7, "name":"hao"},
}

```python
kpi_info = {
1001:{"score":8.9, "name":"sun"},
1002:{"score":8, "name":"zhang"},
1003:{"score":5.9, "name":"zhao"},
1004:{"score":4.2, "name":"li"},
1005:{"score":7, "name":"hao"},
}
```

```python
kpi_keys = list(kpi_info.keys())
for k in kpi_keys:
v = kpi_info[k]
if v["score"] < 6:
print(k, v["score"])
kpi_info.pop(k)
```
#### 1003 5.9
#### 1004 4.2

```python
kpi_info
```
{1001: {'score': 8.9, 'name': 'sun'},
1002: {'score': 8, 'name': 'zhang'},
1005: {'score': 7, 'name': 'hao'}}

```python
[kpi_info.pop(key) for key in list(kpi_info.keys()) if kpi_info[key]["score"] < 6]
```
[{'score': 5.9, 'name': 'zhao'}, {'score': 4.2, 'name': 'li'}]

```python
kpi_info
```
{1001: {'score': 8.9, 'name': 'sun'},
1002: {'score': 8, 'name': 'zhang'},
1005: {'score': 7, 'name': 'hao'}}

#### 5.3 练习3：用户登录

模拟用户注册登录：

实现过程：

```python
def login():
print("call login")
def reg():
print("call reg")
```
```python
user_info = {}
def menu():
tips = "1:登录\n2:注册\n3:退出\n"
while True :
select = input(tips)
if select == "1":
login()
elif select == "2":
reg()
elif select == "3":
print("退出")
break
else :
print("input error")
```

```python
def login():
name = input("用户名：")
pwd = input("密码:")
if name not in user_info:
print("用户名不存在")
elif pwd != user_info[name]:
print("密码错误")
else :
print("登录成功")
```
```python
def reg():
name = input("用户名：")
pwd = input("密码:")
if name in user_info:
print("用户名已存在")
elif pwd == "":
print("密码不能为空")
else :
user_info[name] = pwd
print("注册成功")
```

```python
menu()
```
### 7. 集合
#### 1 主要内容

集合介绍
集合常用方法

#### 2 集合

#### 2.1 定义集合

集合是一个无序的不重复元素序列；
定义方式：

s1 = {val1, val2, val3,...}
s2 = set(iter)

集合要点：

1. 集合元素不重复；
2. 集合不支持索引与切片操作 ；

#### 2.2 集合基本操作

```python
s = {'apple', 'banana', 'pear'}
#集合长度
print(len(s))
#判断是否存在
print('banana' in s)
#遍历集合
for val in enumerate(s):
print(val)
```
3
True
(0, 'banana')
(1, 'apple')
(2, 'pear')

```python
for val in s:
print(val)
```
banana
apple
pear

```python
vlist = [1,1,2,3,5,5]
```

```python
list(set(vlist))
```
[1, 2, 3, 5]

#### 3 集合相关方法

操作S. 说明

| 方法/项 | 说明 |
|---|---|
| add(x)) | 在集合中添加元素 |
| discard(x) | 删除S中元素x |
| pop() | 随机删除一个元素 |
| remove(x) | 删除集合中指定元素，x必须存在于S中 |
| clear()) | 清空集合 |
| copy() | 拷贝集合 |
difference(S1, S2,...)) 返回S与其他集合的差

| 方法/项 | 说明 |
|---|---|
| difference_update(S1,S2...) | 更新S为S与S1,S2...的差 |
| intersection(S1,S2,...) | 返回S与其他集合共同交集 |
| intersection_update(S1,S2,...) | 更新S为S与其他集合的交集 |
isdisjoint(S1)两个集合有交集返回False， 否则返回True

| 方法/项 | 说明 |
|---|---|
| issubset(S1) | 判断当前集合是否是S1的子集 |
| issuperset(S1) | 判断S1是否是当前集合的子集 |
| symmetric_difference(S1) | 返回S与S1中不重复元素 |
| symmetric_difference_update(S1) | 更新S为S与S1中不重复元素 |
| union(S1,S2...) | 返回S与S1,S2...并集 |
| update(S1,S2...) | 更新集合S |
### 8. 拷贝问题（深浅拷贝）
#### 1 Copy问题
1. 浅拷贝：拷贝父对象，不会拷贝对象的内部的子对象
2. 深拷贝：完全拷贝了父对象及其子对象
#### 1.1 浅拷贝
#### 1.2 浅拷贝问题
#### 2 copy模块
例子1：
v1 = [1,2,3]
v2 = list(v1)
v3 = v2
v1, v2, v3是什么关系？
```python
v1 = [1,2,3]
v2 = list(v1)
v3 = v2
```
```python
id(v1), id(v2), id(v3)
```
(2166892587656, 2166892595848, 2166892595848)
```python
v1[1] = 10
```
```python
v1, v2, v3
```
([1, 10, 3], [1, 2, 3], [1, 2, 3])
例子2：
v4 = [1,"test", [2,3,4]]
v5 = list(v4)
问题：
v4[0] = -1
v5[0] = ?
v4[2][0] = 10
v5[2][0] = ?
```python
v4 = [1,"test", [2,3,4]]
v5 = list(v4)
```
```python
id(v4), id(v5)
```
(2166891702600, 2166892619144)
```python
v4[0] = -1
```
```python
v5
```
[1, 'test', [2, 3, 4]]
```python
v4[2][0] = 10
```
```python
v4, v5
```
([-1, 'test', [10, 3, 4]], [1, 'test', [10, 3, 4]])
拷贝过程：
```python
copy模块
```
拷贝模块
import copy
浅拷贝：copy.copy(x)
深拷贝：copy.deepcopy(x, memo=None, _nil=[])
tmp1 = [1,[2,3]]
tmp2 = copy.deepcopy(tmp1)
tmp1[1][0] = -1
tmp2[1][0] = ?
```python
import copy
```
```python
tmp1 = [1,[2,3]]
tmp2 = copy.deepcopy(tmp1)
```

```python
id(tmp1[1]), id(tmp2[1])
```
(2166891745096, 2166892619528)
```python
tmp1, tmp2
```
([1, [2, 3]], [1, [2, 3]])
```python
tmp1[1][0] = -10
```
```python
tmp1, tmp2
```
([1, [-10, 3]], [1, [2, 3]])
```python
id(tmp1[1]), id(tmp2[1])
```
(2166891744904, 2166892660296)
## 第二部分 Python 常用模块
### 9. 模块与导入
#### 1 内容与目标  
主要内容与目标： 
#### 2 模块与导入  
模块：每个 python 文件都是一个独立的模块 
模块作用：实际工作中，整个项目代码比较多，可以将相同功能代码放到一个文件中，不同功能代码放 
到不同文件中，使代码易于维护； 
模块：引入命名空间与作用域 
#### 2.1 导入方式  
语法如下： 
例如： 
| 方法/项 | 说明 |
|---|---|
| # | 导入整个模块 |
| import | 模块 |
| # | 导如指定的属性 |
| from | 模块 import xxx |
| # | 导入多个属性 |
| from | 模块 import xxx, xxx |
| # | 导入后起别名 |
| import | 模块 as 别名 |
| from | 模块 import xxx as 别名 1 ， xxx as 别名 2 |
import os
from functools import reduce
import time as tm
from random import randint, randrange
from os.path import join as os_join

#### 2.2 导入过程  
模块导入要点： 
1. 模块导入中会被加载，加载过程中会被执行； 
2. 模块可以被导入多次，但是只会加载 1 次； 
实例： 
准备工作：在 vscode 一个文件中，创建两个文件： my_add.py, main_test.py ，在 mian_test.py 中导入 
my_add ，观察现象？ 
结果： my_add.py 运行一次。 
问题：实际工作中，每当编写一个模块，一般会有测试代码，如何使测试代码在导入中不执行？ 
#### 2.3 导入搜索路径  
查找过程： 
1. 在当前目录下搜索该模块 
2. 在环境变量  PYTHONPATH 中指定的路径列表中依次搜索 
3. 在  Python 安装路径的  lib 库中搜索 
具体可以查看 sys.path 的值： 
程序运行时，需要导入指定模块，可以将路径添加到 sys.path 中； 

#### 2.4 __name__变量  
__name__说明： 
1. 文件被执行： __name__值为 __main__
2. 文件被导入： __name__值为模块名 
需求：当文件被执行时，执行测试代码，当文件作为模块被导入，不执行测试代码： 

import sys
sys.path
def func_add(x, y):
return x + y
# 通过 __name__ 的值，判断是否导入
if __name__ == "__main__":
print("test func_add(1, 2)=%d"%func_add(1,2))
func_add(1, 2)

#### 3 包  
主要内容： 
1. 包的概念 
2. 相对导入与绝对导入 
#### 3.1 包的概念  
包：是一个包含 __init__.py 文件的文件夹， 
作用：更好的管理源码； 
#### 3.2 相对导入与绝对导入  
绝对导入 :
相对导入：在包内部进行导入，基本语法： 
注意点： 




import 模块
from 模块  import 属性
from . 模块  import xxx
from .. 模块  import xxx
import . 模块
# 注意：
#. 代表当前目录
#.. 代表上一级目录
#... 代表上上级目录，依次类推
绝对导入：一个模块只能导入自身的子模块或和它的顶层模块同级别的模块及其子模块；
相对导入：一个模块必须有包结构且只能导入它的顶层模块内部的模块；
### 10. collections 模块
主要内容
熟悉 collections
掌握新的数据结构
c o l l e c t i o n s 模块
| 方法/项 | 说明 |
|---|---|
| collections | 模块是对 dict 、 list 、 set 、 tuple 的扩展，在某些场景下可以替代这些数据类型； |
| collections | 主要包括： |
| 数据类型 | 说明 |
| Counter | 字典的子类，提供了可哈希对象的计数功能 |
defaultdict字典的子类，提供了工厂函数，为字典查询提供了默认值
OrderedDict字典的子类，保证被添加的顺序
namedtuple创建命名元组子类的工厂函数
deque 类似列表容器，实现了在两端快速添加 (append) 和弹出 (pop)
ChainMap 类似字典的容器类，将多个映射集合到一个视图里面
这里我们主要介绍： Counter ，  defaultdict ， OrderedDict ， namedtuple
C o u n t e r 
主要方法：
方法 说明
c = Counter(*args, **kwds)创建 Counter 对象
c.elements() 返回所有元素组成的迭代器，根据出现次数排序
c.most_common(n=None)获取出现次数最多的前 N 个元素
c.subtract(*args, **kwds)从迭代对象中减去元素
c.update(*args, **kwds)从迭代对象中增加元素
示例：

from collections import Counter
s = "this is test"
#创建Counter
c = Counter(s)
print(c)
#查看数量
print("c.elements():", list(c.elements()))
#元素对应数量增加
c.update(s)
print('update(s):', c)
#元素对应数量减少
c.subtract(s)
print('subtract(s):', c)

Counter({'t': 3, 's': 3, 'i': 2, ' ': 2, 'h': 1, 'e': 1})
c.elements(): ['t', 't', 't', 'h', 'i', 'i', 's', 's', 's', ' ', ' ', 'e']
update(s): Counter({'t': 6, 's': 6, 'i': 4, ' ': 4, 'h': 2, 'e': 2})
subtract(s): Counter({'t': 3, 's': 3, 'i': 2, ' ': 2, 'h': 1, 'e': 1})
d e f a u l t d i c t 
collections.defaultdict(default_factory) ：为字典 key 提供一个默认的值；直接看例子：
O r d e r e d D i c t 
Python 中字典是无序的，很多时候我们希望字典保留其添加顺序；
OrderedDict ：保留字典添加顺序，其操作与 dict 类似；
相关操作：
OrderedDict([('key1', 'value1'), ('key2', 'value2'), ('key3', 'value3')])
n a m e d t u p l e 
namedtuple ：使用属性的方式去访问元素；  直接看案例：

from collections import defaultdict
#默认值为int,0
d = defaultdict(int)
print(d)
#d['A'], 增加Key:A 对应的值为0
print(d['A'])
#d['B'], d['B']的默认值为0，
d['B'] += 1
print(d.items())



from collections import OrderedDict
d = OrderedDict()
d['key1'] = 'value1'
d['key2'] = 'value2'
d['key3'] = 'value3'
print(d)



from collections import namedtuple
#三种定义方式
Person = namedtuple('Person', ['name', 'age'])
Man = namedtuple('Man', 'name,age')
Woman = namedtuple('Woman', 'name age')
p = Person('sun', 15)
m = Man('li', 15)
w = Woman('zhao', 14)
print('Person:', p.name, p.age)
print('Man:', m.name, m.age)
print('Woman:', w.name, w.age)
### 11. 随机数模块
#### 1 random模块

#### 1.1 模块导入

主要方式：

#导入模块
import xxx
#在模块中导入某个属性
from xxxx import xx
#导入之后起别名
import xxxx as xx

例如：

import random
import random as rd
from random import randint

```python
import random
```
```python
from random import randint
```
```python
randint(0, 4)
```
1

#### 1.2 random模块主要方法

random模块数字相关方法：

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| random() | 产生[0,1]之间随机浮点数 |
| uniform(a,b) | 产生(min(a,b), max(a,b))之间随机浮点数 |
| randint(a,b) | 产生[a,b] 之间随机整数 |
| seed(a=None, version=2) | 设置随机数生成器的种子 |
randrange([start], stop, [,step])指定范围内，按step递增的集合中取一个随机数，step缺省值为1

练习：

1. 生成0~1之间随机数
2. 生成0~10之间随机数
3. 生成0~10之间随机偶数

```python
random.random()
```
0.8148861899801072

```python
random.uniform(10, 1)
```
3.255903623455204

```python
random.seed(0)
random.randint(0,10)
```
6

```python
random.randrange(0, 11, 2)
```
6

#### 2 猜数字小游戏

需求：

1.游戏开始每次产生随机数字，
2.读取用户输入，如果猜中，提示中奖,
3.如果猜错，进行合理的提示,

过程如下图：

```python
def guess_num():
x = randint(1, 100)
while True :
tmp = input("输入数字：")
tmp = int(tmp)
if tmp == x:
print("猜中了")
break
elif tmp > x:
print("输入过大")
else :
print("输入过小")
```

```python
guess_num()
```
输入数字：5
输入过小
输入数字：8
猜中了

```python
tmp = int(tmp)
```
```python
x == tmp
```
True

```python
type(tmp)
```
int

```python
type(x)
```
int

#### 3 生成4随机数字验证码

1. 生成4个随机数字
2. 将4个数字生成图片

#### 3.1 生成4个数字组成的字符串

#### 3.2 使用PIL模块生成随机码图片

安装PIL模块:

pip install pillow

导入模块：

from PIL import Image,ImageDraw,ImageFont

```python
def getRandomColor():
'''获取一个随机颜色(r,g,b)格式的'''
c1 = random.randint(0,255)
c2 = random.randint(0,255)
c3 = random.randint(0,255)
return (c1,c2,c3)
def createRandomImage(s):
# 获取一个Image对象，参数:RGB模式,宽,高，随机颜色
image = Image.new('RGB',(100,30),getRandomColor())
# 创建一个Draw对象
draw = ImageDraw.Draw(image)
# 创建字体，字体与字体大小
font= ImageFont.truetype(r"C:\Windows\Fonts\Arial\arial.ttf",size= 32)
# 在图片上写东西,参数是：定位，字符串，颜色，字体
draw.text((15,0),s,getRandomColor(),font= font)
return image
#image.save(open('test.png','wb'),'png')
createRandomImage("1235")
```
### 12. 时间处理
| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| time.time() | 返回当前时间戳，类型：浮点数 |
| time.time_ns() | 返回纳秒，类型：整数 |
1. 时间处理  
#### 1.1 主要内容  


#### 1.2 时间应用场景  
应用场景： 

常见操作： 
#### 1.3 时间转化关系  
#### 2 time 模块  
导入方式： 
#### 2.1 时间戳 (timestamp)  
相关方法： 
示例： 
1. 根据时间筛选数据，例如： 1 个月数据， 1 年数据，某天数据；
2. 与时间相关指标统计：日活，月活，留存等；
1. 获取当前时间与时间戳；
2. 时间转换，例如：时间字符串转成时间对象；
3. 时间差计算，例如：最近三天，最近 7 天，两个时间差；
import time

结果： 
#### 2.2 struct_time  
struct_time 形式 
字段说明： 
方法 说明 
time.localtime([secs])将时间戳转成 struct_time 类型，如果 secs 为空，获取当前时间 
time.gmtime([secs])将时间戳转换为 UTC 时区 (0 时区 ) 的 struct_time ，如果 secs 为空， 
获取当前时间 
struct_time 相关方法 
示例： 
结果： 
time.time()
time.time_ns()
1642755589.5800028
1642755596121648200
time.struct_time(
tm_year=2022, tm_mon=1, tm_mday=1, 
tm_hour=1, tm_min=26, tm_sec=57, 
tm_wday=4, tm_yday=21, tm_isdst=0)
tm_year ：年
tm_mon ：月 
tm_mday ：日 
tm_hour ：时 
tm_min ：分 
tm_sec ：秒 
tm_wday ：星期 (0-6 ，周日为 0)
tm_yday ：今年第几天
tm_isdst ：是否夏令时
st_beijing = time.localtime()
st_utc0 = time.gmtime()
print(st_beijing)
print(st_utc0)
# 注意：北京时间与 utc0 时区相差 8 小时
time.struct_time(tm_year=2022, tm_mon=1, tm_mday=21, tm_hour=17, tm_min=13, 
tm_sec=54, tm_wday=4, tm_yday=21, tm_isdst=0)
time.struct_time(tm_year=2022, tm_mon=1, tm_mday=21, tm_hour=9, tm_min=13, 
tm_sec=54, tm_wday=4, tm_yday=21, tm_isdst=0)

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| time.localtime(ts) | 将时间戳转成 struct_time |
| time.mktime(tuple) | 将 struct_time 转成时间戳 |
| 方法 | 说明 |
time.strptime(string,
format) 将字符串按照对应的格式转成 struct_time 对象 
time.strftime(format[,
tuple]) 将 strcut_time 对象按照指定格式转成字符串时间 
time.asctime([tuple]) 将 strct_time 对象转成可读的时间字符串，例如： 'Fri Jan 21
18:06:51 2022'
time.ctime(seconds) 将时间戳转成可读的时间字符串，例如： 'Fri Jan 21 18:06:51 2022'
#### 2.3 时间戳与 struct_time 转化  
方法 
示例： 
结果： 
#### 2.4 字符串时间与 struct_time 转化  
方法： 
format 格式： 
ts1 = time.time()
print(ts1)
st = time.localtime(ts)
print(st)
ts2 = time.mktime(st)
print(ts2)
1642758472.6243522
time.struct_time(tm_year=2022, tm_mon=1, tm_mday=21, tm_hour=17, tm_min=24, 
tm_sec=45, tm_wday=4, tm_yday=21, tm_isdst=0)
1642757085.0

| 方法/项 | 说明 |
|---|---|
| 格式 | 说明 |
| %Y | 年份 [xxxx] |
| %y | 年份 [xx] |
| %m | 月份 [01 ， 12] |
| %d | 日期 [01 ， 31] |
| %H | 小时 [00 ， 23] |
| %I | 小时 [00 ， 12] |
| %S | 秒数 [00 ， 59] |
%p AM 或 PM
| 方法/项 | 说明 |
|---|---|
| %x | 日期（月 / 日 / 不带世纪的年份） |
| %X | 时间（时 : 分 : 秒） |
| %A | 本地完整星期名称 |
| %a | 本地简化星期名称 |
| %B | 本地完整的月份名称 |
| %b | 本地简化的月份名称 |
| %w | 星期（ 0-6 ）， 0 ：周日， 1 ：周 1 ，以此类推 |
| 类 | 说明 |
| datetime.date | 表示日期，常用的属性有： year, month 和 day |
| datetime.time | 表示时间，常用属性有： hour, minute, second, microsecond |
datetime.datetime表示日期时间 
datetime.timedelta表示两个 date 、 time 、 datetime 实例之间的时间间隔，分辨率（最小单 
位）可达到微秒 
datetime.timezone时区相关类 
练习： 
1. 获取当前时间戳，并将转成 strct_time ； 
2. 获取当前的 struct_time, 并转成时间戳 ;
3. 将时间戳转成时间字符串，格式： “yyyy-mm-dd hh:mm:ss” ； 
4. 将时间字符串转成时间戳； 

#### 3 datetime 模块  
相关操作：

结果： 

#### 4 calendar 模块  
calendar ，是与日历相关的模块，主要使用： 
from datetime import date, time, datetime
# 创建 date 对象
date_obj = date(2022, 1, 10)
# 创建 time 对象
time_obj = time(12, 30,1)
# 获取当前的时间
dt_now = datetime.now()
print(dt_now)
# 获取当前时间戳
print(dt_now.timestamp())
# 获取当前时间的 date
print(dt_now.date())
# 获取当前的 time
print(dt_now.time())
# 计算时间差
dt_delta = dt_now - datetime(2022, 1,23)
print(dt_delta)
# 转成时间字符串
s = dt_now.strftime("%Y-%m-%d %H:%M:%S")
print(s)
# 将时间字符串转 datetime 对象
print(datetime.strptime(s, "%Y-%m-%d %H:%M:%S"))
2022-01-25 09:43:09.224662
1643074989.224662
2022-01-25
09:43:09.224662
#### 2 days, 9:43:09.224662
2022-01-25 09:43:09
2022-01-25 09:43:09
import calendar
# 获取某一年日历，第一行为年份，第二行月份，第三行为星期
import calendar
print(calendar.calendar(2022))
# 判断是否是闰年
calendar.isleap(2018) 
# 获取指定年月的日历
print(calendar.month(2022,1))
# 计算指定年月日是星期几
calendar.weekday(2022,1,1)

#### 5 案例  
用户订单数据，格式如下： 
#### 5.1 理解需求  
#### 1 ）按照年月统计订单量； 
#### 2 ）给定日期 ( 时间字符串 ) ，统计其前后三天的的订单量； 
注意点： 
#### 1 ）需求 1 ：读取文件时间，将其转成 struct_time 时间或者标准字符串时间； 
#### 2 ）需求 2 ：时间字符串转成合理的时间类型，读取文件时间，统计前后三天时间； 
#### 3 ）注意点：如果文件以 utf-8 方式打开，出现： \ufeff ，编码格式修改为： UTF-8-sig
#### 5.2 需求 1 ：按年月统计  
分析： 
1. 当前时间格式及问题，转化的目标格式，先完成时间处理； 
2. 理解并实现按月统计订单量； 
3. 函数封装； 

#### 5.2.1 时间处理  
目标格式： "yyyy-mm"
代码实现： 
import csv
user_pay_order_path = r"E:\vscode_dir\python_file\user_pay_order.csv"
# 读取数据
f = open(user_pay_order_path, encoding=" UTF-8-sig")
csv_reader = csv.DictReader(f)
# 读取一行数据
line = next(csv_reader)
print(line)
# 获取支付时间
ts = line.get("order_paytime")
print(ts)

结果： 
#### 5.2.2 功能实现  
结果： 
#### 5.3 需求 2 ：统计 7 天内数据  
理解需求：给定日期，获取前三天，当前，后三天数据， 
过滤条件： 
# 将支付时间转成 struct_time
st = time.strptime(ts, "%Y/%m/%d %H:%M")
# 将 struct_time 转成年月格式
pay_date = time.strftime("%Y-%m", st)
print(pay_date)
OrderedDict([('id', '115'), ('order_status', '2'), ('order_paytype', 'iPhone 6 
Plus'), ('order_describe', 'requestPayment:fail cancel'), ('order_paytime', 
'2019/3/28 8:32')])
2019/3/28 8:32
2019-03
from collections import Counter
def count_order_by_month(fpath):
# 使用 Counter 统计数量
counter = Counter()
f = open(user_pay_order_path, encoding=" UTF-8-sig")
csv_reader = csv.DictReader(f)
for line in csv_reader:
ts = line.get("order_paytime")
# 将支付时间转成 struct_time
st = time.strptime(ts, "%Y/%m/%d %H:%M")
# 将 struct_time 转成年月格式
pay_date = time.strftime("%Y-%m", st)
# 统计数量
counter[pay_date] += 1
f.close()
return counter
user_pay_order_path = r"E:\vscode_dir\python_file\user_pay_order.csv"
res = count_order_by_month(user_pay_order_path)
for month, total in res.items():
print(month, total)
2019-03 54
2019-04 629
...
2021-04 7
2021-05 2
方式 1 ： | 给定时间日期 - 订单时间日期 | <=3, 以日期为准
方式 2 ： | 给定时间的时间戳 - 订单时间戳 | <=3*24*60*60 ，以时间戳为准，更精准

#### 5.3.1 时间处理  
结果： 
#### 5.3.2 计算时间差  
1. 考虑函数接口与返回值； 
2. 考虑使用不同方式进行比较； 

代码实现： 
from datetime import datetime, date
import time
def sdate_to_date(s, format = "%Y/%m/%d %H:%M"):
# 将时间转 date
t_datetime = datetime.strptime(s, format)
t_date = t_datetime.date()
return t_date
def sdate_to_ts(s, format = "%Y/%m/%d %H:%M"):
# 将时间转成时间戳
st = time.strptime(s, format)
ts = time.mktime(st) 
return ts
sdate = "2019/3/21 00:00"
print(sdate_to_date(sdate))
print(sdate_to_ts(sdate))
2019-03-21
1553097600.0
def is_seven_interval_days(sdate, order_time, cmp_type = "DAY"):
# 默认比较方式：按天
if cmp_type == "DAY":
set_date = sdate_to_date(sdate)
order_date = sdate_to_date(order_time)
interval = set_date - order_date
print("DAY:", set_date, order_date)
return abs(interval.days) <= 3
else:
set_ts = sdate_to_ts(sdate)
ts = sdate_to_ts(order_time)
print("TS:", set_ts, ts)
interval = set_ts - ts
return abs(interval) <= 3*24*60*60

sdate = "2019/3/21 00:00"
order_date = "2019/3/24 23:59"
is_seven_interval_days(sdate, order_date, "TS")

结果： 
#### 5.3.3 代码实现  
给定一个日期，遍历订单，统计 7 天内的订单量； 
结果： 



TS: 1553097600.0 1553443140.0
False
import csv
def count_order_by_setdate(date, fpath):
f = open(user_pay_order_path, encoding=" UTF-8-sig")
csv_reader = csv.DictReader(f)
order_num = 0
for line in csv_reader:
ts = line.get("order_paytime")
if is_seven_interval_days(date, ts):
order_num += 1
f.close()
return order_num
user_pay_order_path = r"E:\vscode_dir\python_file\user_pay_order.csv"
sdate = "2019/3/27 00:00"
order_num = count_order_by_setdate(sdate, user_pay_order_path)
print(f" 在 {sdate} 7 天内的订单量： {order_num}")
在 2019/3/27 00:00 7 天内的订单量： 40
## 第三部分 函数与函数式编程
### 13. 函数基础详解
#### 1 主要内容与目标  
主要内容： 

目标： 
1. 根据需求合理的定义函数，理解函数参数，理解第三方模块中函数调用方法； 
2. 理解 LEGB 作用域，面试必备； 
3. 掌握装饰器，在使用第三方框架，能够使用其提供的装饰器； 
4. 掌握 yield 关键字与递归函数； 

#### 2 函数基础  
#### 2.1 函数三要素与作用  
函数三要素： 
1. 函数名； 
2. 函数参数； 
3. 函数返回值，默认返回值 None ； 
示例：

函数实现过程： 
实际工作中，我们会经常使用第三方模块提供的函数，或者自己编写函数供其他人调用； 

函数添加说明： 
定义函数式，在函数下添加字符串，例如： 

函数使用要点： 

函数作用 

#### 2.2. 函数定义与使用常见问题  
def funcname(args):
pass
def my_add(x, y):
"""
功能： xy 两个变量相加
返回值：返回两个对象相加的和

"""
return x + y
help(my_add)
#### 1 ）理解函数作用；
#### 2 ）函数调用需要参数；
#### 3 ）接收函数返回值；
1. 封装，接口；
2. 模块化，代码复用；

#### 2.3 函数名  
函数名定义： 
例如： 
#### 2.4 函数参数  
函数参数类型：无参，有参，带默认值参数，可变长参数； 
#### 2.4.1 无参函数  
定义函数，没有参数，例如： 
#### 2.4.2 形参函数  
函数定义： 
#### 2.4.3 带默认值参数  
函数定义中，参数可以带默认值，当调用时，带默认值参数可以不写； 
常见的默认值函数： open 等 
#### 1 ）遵循规则：小写字母与下划线组成；
#### 2 ）通过函数名能够理解函数作用，增加代码可读性；
# 不推荐方式
def func(x):
pass
# 推荐方式
def is_odd(x):
pass
import time
def get_timestamp():
return time.time()
get_timestamp()
#1 个参数函数
def str_to_int(s):
if s.strip():
return int(s.strip())
return 0
#2 个参数函数
def my_add(x, y):
return x+y
num = str_to_int("10")
res = my_add(10, 20)
print(num, res)

#### 2.4.5 位置参数与关键字参数  
函数调用，通过下面两种方式传递参数： 
例如： 
#### 2.4.4 可变长非关键字参数  
使用场景：函数非关键字参数数量不确定，例如： 
基本语法： 
示例： 
结果： 
# 默认十进制
def str_to_int(s, base = 10):
value = int(s, base)
return value
# 十进制，逢十进一
base_10 =  str_to_int("10")
# 二进制，逢二进一
base_2 = str_to_int("10",base = 2)
print(base_10, base_2)
#### 1 ）调用函数时，根据函数定义的参数位置来传递参数；
#### 2 ）调用函数是，通过 “ 键 - 值 ” ，使函数更加清晰、容易使用，避免参数顺序问题；
# 定义求余函数
def calculate_remainder(m, n):
return m%n
# 位置参数
print(calculate_remainder(10,3))
# 关键字参数
print(calculate_remainder(n = 3, m = 10))
print(min(1,2,3,5))
print(min(5,6,7))
#*args 用来将参数打包成 tuple 给函数调用
def func(*args):
pass
def func(*args):
print("*args value:", args)
print("*args type :", type(args))
print("*args 拆包后 :", *args)
func(1,2,3)

问题： *args 在使用中，需要在再次使用，如何处理？ 
例如：定义一个函数，分别求给定数据的最大值与最小值 
调用过程分析： 

#### 2.4.5 可变长关键字参数  
使用场景：关键字参数数量不确定； 
语法： **kwargs 打包关键字参数成 dict 给函数体调用 
使用方式： 
问题：如果 **kwargs 在使用中，需要再次使用，如何处理？ 
*args value: (1, 2, 3)
*args type : <class 'tuple'>
*args 拆包后 : 1 2 3
def count_max_min(x, y, *args):
max_val = max(x, y, *args)
min_val = min(x, y, *args)
print(max_val, min_val)
listv = list(range(10))
# 调用时拆包；
# 调用时打包为元组；
count_max_min(1,2,*listv)
# 定义方式：
def func(**kwargs):
print("**kwargs value:", kwargs)
print("**kwargs type :", type(kwargs))
print("*kwargs:", *kwargs)
# 调用方式
func(name="sun", age=10)

#### 2.4.6 参数顺序  
定义函数时，函数参数顺序与调用顺序： 
例如： 
结果，第二次调用出现问题： 
#### 2.4.6 函数参数陷阱  
一个例子： 
def func(**kwargs):
print("**kwargs value:", kwargs)
print("**kwargs type :", type(kwargs))
print("*kwargs:", *kwargs)
def test(**kwargs):
func(**kwargs)
dinfo = {"name":"sun", "age":10}
# 调用 test 时候进行拆包为关键字参数
# 执行中 test 将其打包成字典
test(**dinfo)
位置参数，可变长非关键字参数，带默认值参数，可变长关键字参数
# 定义函数
def func(x, y, *args, z = 10,  **kwargs):
pass
# 调用顺序
func(10, 20, 20,30, z = 20, a = 10)
# 错误调用
func(10,20, z = 20, 20, 30, a = 10)
File "<ipython-input-19-fad3376ebbf5>", line 8
func(10,20, z = 20, 20, 30, a = 10)
^
SyntaxError: positional argument follows keyword argument
#listv 默认值列表
def test_func(value, listv = []):
print(id(listv))
listv.append(value)
return listv
glist = []
v1 = test_func(1, glist)
v2 = test_func(2)
v3 = test_func(3)
print(v1, id(v1))
print(v2, id(v2))

结果： 
分析： 
#### 2.5 函数返回值  
函数返回值： 
#### 2.5.1 默认返回值  
函数默认返回值为 None
结果： 
#### 2.5.2 return 返回单个结果  
定义函数，根据需求返回合理的结果 
print(v3, id(v3))
2577490518536
2577480524488
2577480524488
[1] 2577490518536
[2, 3] 2577480524488
[2, 3] 2577480524488
函数 test_func 默认参数 listv = [], 只创建一次，如果使用默认参数，实质是使用函数中的 listv ，所以
造成该结果；
def func():
pass
res = func()
print(res, type(res))
None <class 'NoneType'>
def foo(x, y):
return x+y
res = foo(10, 20)
print(res)

LEGB   说明 
L Local ( 函数内部 ) 局部作用域 
E Enclosed ( 嵌套函数的外层函数内部 ) 嵌套作用域（闭包） 
G Global ( 模块全局 ) 全局作用域 
B Buildin ( 内建 ) 内建作用域 
结果： 30
#### 2.5.3 返回多个对象  
返回多个值，实际返回的是一个元组； 
结果： 
#### 2.6 函数作用域  
作用域：变量在程序中的可应用范围； 
引入作用域操作：定义函数，类； 
#### 2.6.1 一个例子  
程序输出结果： 
#### 2.6.2 LEGB 原则  
LEGB 说明： 
Python 查找变量的规则： LEGB ； 
def count_max_min(x,y,*args):
max_val = max(x, y, *args)
min_val = min(x, y, *args)
return max_val, min_val
res = count_max_min(10, 20, 2,3,4,5)
print(res)
max_value, min_value = count_max_min(10, 20, 2,3,4,5)
print(max_value, min_value)
(20, 2)
#### 20 2
x = 10
def func():
x = 1
print("in  func x:", x)
func()
print("out func x:", x)
Local-->Enclosed-->Global-->Builtin

命名空间类别 记录值 
局部命名空间（函数 :local namespace ） 函数参数与局部变量 
模块命名空间（全局 :global namespace ） 全局变量，函数，导入模块等 
内置命名空间（内置 :build-in ） 内置函数及异常信息 
如果在函数内重新定义相同的名称的变量，则其作用域变量可以认为被屏蔽； 
#### 2.6.3 命名空间  
命名空间 (Namespace) ：实质名称到对象的映射，便于变量的查找； 
命名空间说明： 
局部与全局命名空间查看： 
例如： 
#### 2.6.4 作用域陷阱  
代码如下： 
locals() ：局部命名空间
globals() ：全局命名空间
x = 10
def func():
x = 1
print("in  func x:", x)
print("locals:", locals())
func()
print("out func x:", x)
print("globals:", globals())
x = 10
def func():
print(x)
x = 20
func()

结果： 
原因： python 解释器认为 func 中的 x 是局部变量，但是局部变量 x 没有初始化，所以报错； 
#### 2.6.5 global 关键字  
问题：如何在局部变量中使用全局变量？ 
示例： 
结果： x=20,y=10



1 x = 10
#### 2 def func():
----> 3     print(x)
4     x = 20
#### 5 func()
UnboundLocalError: local variable 'x' referenced before assignment
#global 关键字，声明变量为全局 :
# 例如：在函数内部声明 x 为全局变量
global x
#nonlocal 关键字，声明变量为嵌套作用域，注意该关键字只能用在嵌套中；
nonlocal x
x = 10
y = 10
def g_test():
global x
x = 20
y = 30
g_test()
print("x=%d,y=%d"%(x, y))
### 14. 匿名函数与函数式编程
#### 1 主要内容：

1. 匿名函数；
2. 函数式编程中三个重要函数；

目标：

1. 掌握匿名函数定义方式与应用；
2. 灵活应用函数式编程

#### 2 匿名函数

#### 2.1 一个需求

需求：判断一个数字是否是奇数，如果是奇数返回True，否则返回False

```python
def is_odd(x):
return x%2 == 1
x = 10
print(f"{x} is odd:{is_odd(x)}")
x = 11
print(f"{x} is odd:{is_odd(x)}")
```
#### 10 is odd:False
#### 11 is odd:True

问题：这种简单的函数，能不能通过一条与实现？

#### 2.2 lambda

lambda：表示定义匿名函数，基本语法：

#定义语法
func = lambda:pass
#调用方法
func()

说明：

1. lambda为关键字，在其他语言，例如：java中，也存在这种语法；
2. 匿名函数没有名称，返回值为函数对象；
3. 匿名函数中的表达式只能由一条语句；
4. 匿名函数调用后返回值为表达式结果；
5. 匿名函数不要太复杂，要考虑后期维护；

#### 2.3 无参匿名函数：

需求：定义一个函匿名函数，功能：返回当前的时间戳

```python
import time
get_ts = lambda :time.time()
```

```python
get_ts()
```
1645484812.6514194

```python
import time
get_ts = lambda :time.time()
get_ts()
```
1643264332.6779656

```python
import time
def get_ts():
return time.time()
```

#### 2.4 带参数的匿名函数

1. 计算两个数的和；
2. 给定一个成绩，判断是否及格(判断标准：大于等于60)；

```python
x = 60
y = 50
my_add = lambda m, n: m + n
print(f"{x}+{y}={x+y}")
is_pass = lambda value:True if value >= 60 else False
print(f"{x} is pass:{is_pass(x)}")
print(f"{y} is pass:{is_pass(y)}")
```
60+50=110
#### 60 is pass:True
#### 50 is pass:False

#### 2.5 可变长参数匿名函数

需求：给定一系列数字，求和

```python
my_sum = lambda x, y, *args: x + y + sum(args)
res = my_sum(1,2,3,4,5,6)
print(res)
```
21

#### 3 匿名函数应用

#### 3.1 列表排序

需求：给定数字列表,按照规则排序：每个元素与5的差的绝对值，从小到大排序；

```python
nums = [- 3, 2, 1,9,10]
nums.sort(key = lambda value:abs(5- value), reverse= False )
print(nums)
```
[2, 1, 9, 10, -3]

#### 3.2 字典列表排序

给定一组用户信息，数据格式如下：

user_info = [{'name':'sun', 'age':10},{'name':'li', 'age':13},{'name':'zhao', 'age':12}]

需求：按照用户年龄从小到大排序

```python
user_info = [{'name':'sun', 'age':15},{'name':'li', 'age':12},{'name':'zhao', 'age':13}]
user_info.sort(key= lambda item:item.get('age'))
user_info
```
[{'name': 'li', 'age': 12},
{'name': 'zhao', 'age': 13},
{'name': 'sun', 'age': 15}]

#### 4 函数式编程

#### 4.1 map函数

map(func, *iterables)：对迭代对象每个元素处理，返回map对象,处理过程如下：

需求：

1. 将字符串列表：['1', '2', '3']转成：[1,2,3]
2. 给定三个学生语文与数学成绩，且一一对应：[90,80,40]，[88, 92, 77,88],计算每个学生的总成绩；
3. 某次消费记录：bill = ['Apple 20', 'Pear 5', 'Banana 10'] ,计算消费金额，结果为：35；

```python
l = ['1', '2', '3']
[int(val) for val in l]
r = map(int, l)
list(r)
```

```python
math = [90,80,40]
chinese = [88, 92, 77,88]
```

```python
res = map(lambda x, y, * args:x+ y+sum(args), math, chinese, math)
```

```python
list(res)
```
[268, 252, 157]

```python
math = [90,80,40]
chinese = [88, 92, 77,88]
res = map(lambda x,y:x+ y, math, chinese)
list(res)
```

```python
bill = ['Apple 20', 'Pear 5', 'Banana 10']
```

```python
res = sum(map(lambda val:int(val.split()[- 1]), bill))
```

```python
res
```
35

```python
bill = ['Apple 20', 'Pear 5', 'Banana 10']
r = map(lambda val:val.split()[- 1], bill)
sum(map(int, r))
```

思考问题： 当调用map函数计算成绩时，是否发生了计算？

```python
def my_sum(x, y):
print(f"{x}+{y}={x+ y}")
return x + y
math = [90,80,40]
chinese = [88, 92, 77,88]
```

```python
#查看执行map结果
res = map(my_sum, math, chinese)
```

```python
next(res)
```
---------------------------------------------------------------------------
StopIteration Traceback (most recent call last)
<ipython-input-44-99bd7a0c47e0> in <module>
----> 1 next(res)

StopIteration :

#### 4.2 reduce函数

reduce函数：

from functools import reduce
reduce(function, sequence[, initial])

基本原理：

说明：

1. function函数参数为2个；
2. reduce调用过程：依次从sequence中取一个元素，和上一次function的结果做参数，再次调用function；
3. 第一次调用function时，如果设置initial，function参数为：sequence的第一个元素和initial；
4. 第一次调用function时，没有设置initial, function参数为：sequence中的前两个元素；

需求：

1. 计算1~10的累加和；
2. 计算1~10阶乘；

```python
from functools import reduce
res = reduce( lambda x, y: x+y, range(1, 11) )
print(f"sum res:", res)
res = reduce( lambda x, y: x*y, range(1, 11) )
print(f"factorial res:", res)
```
sum res: 55
factorial res: 3628800

给定一组消费数据，计算累积销售额；

```python
order_list = [{"数量":2, "单价":15},
{"数量":1, "单价":10},
{"数量":7, "单价":12},
{"数量":4, "单价":13},
]
```

```python
def count_amount(value, order):
amount = order.get("数量") * order.get("单价")
return value + amount
reduce(count_amount, order_list, 0)
```
176

#### 4.3 filter函数

filter函数用于根据条件过滤数据；

filter(function or None, iterable)

1. filter作用：使用function对iterable每个元素进行处理, 将返回值为真的保留，返回filter迭代器；
2. function为指定函数：处理iterable每个元素；
3. function为None：根据iterable中的元素进行判断；

需求：

1. l = [1,2,3,4,5,6],过滤列表中的偶数；
2. report = [[90,80],[55,70],[50,45]],过滤成绩，平均分及格；

```python
report = [[90,80],[55,70],[50,45]]
res = filter(lambda item:sum(item)/ len(item) >= 60, report)
```

```python
l = [1,2,3,4,5,6]
res = filter(lambda val:val% 2== 0, l)
```

```python
list(res)
```
[2, 4, 6]
### 15. 递归函数
#### 1 递归基本原理

递归函数：函数在内部调用自身；

递归函数特性：

1. 函数内部，自己调用自己；
2. 有一个明确的结束条件；
3. 每次进入更深一层递归时，问题规模相比上次递归都应有所减少;
4. python中使用递归考虑栈溢出

递归优缺点：

1. 优点：逻辑简单清晰,
2. 缺点：过深的调用会导致栈溢出；

```python
deep = 1
def func():
global deep
deep += 1
print("call func")
func()
```

```python
deep
```
1

#### 2 阶乘实现

需求：计算N以内阶乘，1*2*3*....n

#### 2.1 使用while循环

```python
v = 1
i = 1
while i <= 5:
v *= i
i+=1
print(v)
```
120

#### 2.2 递归实现

基本思路：

关键点：

1. 定义函数；
2. 自己调用自己；
3. 找到截止条件；

```python
def recursion(num):
print("num :", num)
if num == 1:
return num
return num * recursion(num - 1)
```

```python
recursion(5)
```
num : 5
num : 4
num : 3
num : 2
num : 1

120

```python
def recursion(num):
#截止条件
if num == 1:
return 1
return num * recursion(num-1)
recursion(5)
```
120

#### 3 斐波那契数列

斐波那契数列：即著名的兔子数列：1、1、2、3、5、8、13、21、34、……

1. 初始值：1,1
2. 第三个数开始，为前两个和；

需求：输入n,计算对应的斐波那契数；

```python
def fibo(n):
if n <= 2:
return 1
else :
return fibo(n- 1) + fibo(n- 2)
```

```python
fibo(5)
```
5

```python
for n in range(1, 10):
print(fibo(n), end= " ")
```
#### 1 1 2 3 5 8 13 21 34

#### 4 遍历多维列表

需求：遍历多维列表中的每个元素，注意：列表中子元素为：列表，单个字符，数字； 问题：

```python
data = [1,2,3,['a', 'b', 'c',['d','e','f']],[4,5,6,[7,8,9]]]
```

```python
def sort_list(items):
for item in items:
if isinstance(item, list):
sort_list(item)
else :
print(item, end= " ")
sort_list(data)
```
#### 1 2 3 a b c d e f 4 5 6 7 8 9

```python
data = [1,2,3,['a', 'b', 'c',['d','e','f']],[4,5,6,[7,8,9]]]
def sort_list(items):
for value in items:
if isinstance(value, list):
sort_list(value)
else :
print(value, end= ' ')
sort_list(data)
```
### 16. 闭包
#### 1 闭包

#### 1.1 基本概念

内部函数中，对在外部作用域（但不是在全局作用域）的变量进行引用，那么内部函数就被认为是闭包(closure)

例如：

#foo为外部函数
def foo():
#m相对于bar，是外部变量
m = 10
#bar为内部函数
def bar(n):
return n * m
#foo函数返回值：内部函数
return bar

```python
def out_func(x):
m = 10
def inner_func(n):
return n * m * x
return inner_func
```

```python
def foo():
m = 10
def bar(n):
return m * n
return bar
```

#### 1.2 闭包理解

1. 函数内部定义函数；
2. 内部函数引用外部变量；
3. 函数返回值为函数；

#### 1.3 带着问题去理解

如下代码：

```python
def foo():
m = 10
def bar(n):
return n * m
print("id(bar):", id(bar))
return bar
```

```python
res = foo()
```
id(bar): 1525577370504

```python
id(res)
```
1525577370504

```python
res
```
<function __main__.foo.<locals>.bar(n)>

```python
res(2)
```
20

```python
func = foo()
func(2)
```
id(bar): 1525577368344

20

1. foo函数的返回值？
2. res = foo(),res是?
3. 添加合理的打印信息，查看函数调用过程？

#### 2 闭包应用场景

#### 2.1 n次幂计算

需求：定义一组函数，计算指定数值N次幂

```python
def make_pow2(n):
return pow(n, 2)
def make_pow10(n):
return pow(n, 10)
```

```python
print("make_pow2(2)=",make_pow2(2))
print("make_pow10(2)=",make_pow10(2))
```
make_pow2(2)= 4
make_pow10(2)= 1024

#### 2.2 新需求

传入参数可以为数字字符串,如何处理？

```python
def make_pow2(n):
return pow(int(n), 2)
def make_pow10(n):
return pow(int(n), 10)
```

问题：如果需要对参数继续转换，且有多个类似函数，如何处理？

#### 2.3 引入闭包

代码实现：

```python
def make_pow(m):
def inner(n):
return pow(int(n), m)
return inner
```

```python
make_new_pow2 = make_pow(2)
make_new_pow10 = make_pow(10)
print("make_new_pow2(2)=",make_new_pow2(2))
print("make_new_pow10(2)=",make_new_pow10(2))
```
make_new_pow2(2)= 4
make_new_pow10(2)= 1024

#### 2.4 闭包应用场景

1. 封装，代码复用；
2. 装饰器；

#### 2.5 可变长参数

```python
def logfunc(level= 'info'):
def logmsg(msg, * args, ** kwargs):
print(f'{level}--> : {msg}, {args},{kwargs}')
return logmsg
```

```python
debug_func = logfunc('debug')
info_func = logfunc('info')
error_func = logfunc('error')
```

```python
debug_func("test", 1,2,3, y= 10)
info_func("info")
error_func("error")
```
debug--> : test, (1, 2, 3),{'y': 10}
info--> : info, (),{}
error--> : error, (),{}

#### 2.6 __closure__属性

闭包函数： __closure__属性实质为元组，用于记录外部变量；

```python
def logfunc(level= 'info'):
def logmsg(msg, * args, ** kwargs):
print(f'{level}--> : {msg}')
return logmsg
info_func = logfunc('info')
```

```python
print("info地址 ：0x%016X"% id("info"))
```
info地址 ：0x000001632F78E070

```python
info_func.__closure__
```
(<cell at 0x00000163337F2AC8: str object at 0x000001632F78E070>,)

```python
attr = info_func.__closure__
print("info地址 ：0x%016X"% id("info"))
print("闭包closure：",type(attr), attr)
print("外部变量值 ：",attr[0].cell_contents)
```
info地址 ：0x000001632F78E070
闭包closure： <class 'tuple'> (<cell at 0x00000163337F2AC8: str object at 0x000001632F78E070>,)
外部变量值 ： info
### 17. 装饰器
主要内容

装饰器：对函数进行处理，并返回新的函数

#### 1 再看闭包

```python
def deco_func(level = 'info'):
def foo(msg):
print(f'{level}:{msg}')
return foo
f = deco_func()
f('test')
```
info:test

#### 2 一个需求

需求：定义一系列函数,对函数进行检验，前两个参数必须为整数；

```python
def make_pow(x, y):
print("call make_pow")
if isinstance(x, int) and isinstance(y, int):
return x ** y
def make_sum(x, y):
print("call make_sum")
if isinstance(x, int) and isinstance(y, int):
return x + y
def make_mul(x, y):
print("call make_mul")
if isinstance(x, int) and isinstance(y, int):
return x * y
```

问题：三个函数中检查参数重复，如果还要对其他参数进行检验，如何操作？

```python
def deco_func(f):
print("call deco_func")
def inner(x, y, * args):
print("call here inner")
if isinstance(x, int) and isinstance(y, int):
return f(x, y, * args)
return inner
```

```python
def make_pow(x, y, * args):
print("call make_pow")
return x ** y
make_pow = deco_func(make_pow)
```
call deco_func

```python
make_pow(2,3,3)
```
call here inner
call make_pow

8

#### 3 使用装饰器

装饰器基本语法：

def deco_func(f):
def inner():
return f()
return inner
@deco_func
def foo():
pass

注意：

1. deco_func为装饰器函数，
2. foo被装饰函数,
3. 当运行此代码，deco_func被调用，过程：foo = deco_func(foo)，
4. 结果：foo函数成为inner函数外部变量，foo指向inner函数

一个案例：

```python
#装饰器函数
def deco_func(f):
print("call deco_func")
def inner(x, y, * args):
print("call here inner")
if isinstance(x, int) and isinstance(y, int):
return f(x, y, * args)
return inner
```

```python
#被装饰函数
#@deco_func为装饰器语法糖
@deco_func
def make_pow(x, y, * args):
print("call make_pow")
return x ** y
```
call deco_func

```python
make_pow(2,3)
```
call here inner
call make_pow

8

#### 4 装饰器带参数

需求：定义一组log输出函数，log的等级分为：info, debug, error;

```python
def deco_func(f):
def inner(msg):
msg = "msg:"+ msg
f(msg)
return inner
```

```python
@deco_func
def log_info(msg):
print(msg)
```

```python
log_info("test")
```
msg:test

问题：如何在输出信息中添加：info, debug, error；

解决方式：将deco_func修改为内部变量，在外添加level_func

```python
def level_func(level):
def deco_func(f):
def inner(msg):
'''
inner level
'''
msg = level + " msg:"+ msg
f(msg)
return inner
return deco_func
```

```python
#调用过程
#1:调用level_func，返回deco_func，
#2:@deco_func对log_info进行装饰，返回inner
@level_func("info")
def log_info(msg):
'''
info level
'''
print(msg)
@level_func("error")
def log_error(msg):
'''
error level
'''
print(msg)
```

```python
log_info("this is test")
log_error("this is test")
```
info msg:this is test
error msg:this is test

```python
log_error?
```

#### 5 wraps

装饰器使用问题：某些场景下，我们希望使用装饰器，但是，不希望改变函数名及说明，例如：

```python
from functools import wraps
def deco_func(f):
#使用wraps装饰f
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

```python
test?
```
### 18. 生成器函数
#### 1 主要内容

1. yield；
2. 生成器函数应用；
3. 基于yield实现生产者与消费者；

#### 1.1 带yeild关键字函数

```python
def func():
print("--> step 1")
yield "hello"
print("--> step 2")
yield "world"
print("--> step 3")
```

```python
gen = func()
```

```python
gen
```
<generator object func at 0x000002115C597148>

```python
next(gen)
```
--> step 1

'hello'

```python
next(gen)
```
--> step 2

'world'

```python
next(gen)
```
--> step 3

---------------------------------------------------------------------------
StopIteration Traceback (most recent call last)
<ipython-input-6-6e72e47198db> in <module>
----> 1 next(gen)

StopIteration :

```python
gen = func()
```

调用说明：

1. func被调用，并不会执行；
2. func被调用后返回生成器；
3. 可以使用next函数或者for对生成器操作；

#### 1.2 理解yield调用过程

理解：

1. 第一次调用next(gen)执行后，遇到yield关键字，返回其对应的对象，并保存现场；
2. 再次调用next(gen)，从yield的下一条语句继续执行；
3. 重复1~2，如果执行完成，触发StopIteration异常；

#### 2 yield使用场景

需求：

1. 生成随机数池，可以无限取值,范围：[1, 9999]；
2. 使用yield完成斐波那契数列；

#### 2.1 随机数池

```python
import random
def random_pool(min_val, max_val):
while True :
yield random.randint(min_val, max_val)
random_gen = random_pool(1, 9999)
```

```python
next(random_gen)
```
7717

#### 2.2 斐波那契数列

数列：1,1,2,3,5,8,13,21，....

```python
def fibo(n):
a,b = 0, 1
i = 1
while i < n:
i += 1
yield b
a, b = b, a+ b
```

```python
gen_fibo = fibo(10)
```

```python
for val in gen_fibo:
print(val)
```

#### 3 send方法

生成器函数可以传参并接受参数

1. 生成器对象调用send方法传参；
2. 生成器函数 value = yield obj接受参数；

需求：定义生成器函数，将字符串数字转成整数，若转化值为"q"，退出；

```python
def custom():
value = yield ''
while value != 'q':
value = yield int(value)* 10
```

```python
gen = custom()
next(gen)
```
''

```python
gen.send("20")
```
200

```python
gen.send("120")
```
1200

```python
gen.send("q")
```
---------------------------------------------------------------------------
StopIteration Traceback (most recent call last)
<ipython-input-17-95b59e229c68> in <module>
----> 1 gen.send("q" )

StopIteration :

调用过程：

1. 使用next方法，启动生成器，生成器返回"",保留现场，等待下一次调用；
2. 调用生成器send方法，传入参数，value接受参数，执行到yield返回并保存现场；
3. 重复1~2过程，如果遇到"q"，退出；
## 第四部分 文件与数据持久化
### 19. 文件详解
1. 文件主要内容  
文件目的： 
1. 可以对大量文件进行处理； 
2. 了解常见文件的格式，掌握对应模块，在实际工作与学习中，能够灵活应对； 
3. 通过文件学习，锻炼编程思维，强化编程能力； 

2. 快速入门文件操作  
主要内容：

读与写过程： 

#### 2.1 快速实现文件读取  
准备工作：在本地准备文本文件 
读取操作： 
结果： 

#### 2.2 快速实现文件写入  
准备工作：准备写入文件路径，建议写新文件 
写入操作： 

# 文件路径
fpath = r"E:\vscode_dir\python_file\test.txt"
# 打开文件
f = open(fpath, encoding="utf-8")
# 使用 read 方法读取文件所有了内容
text = f.read()
print(text)
# 关闭文件
f.close()
职场人要坚持锻炼身体，时刻关注自己的健康，
尤其 30 岁以后，注意健康饮食，配合适量运动，
保持内心的平和，懂的给自己减压，保持良好的睡眠
# 文件路径
fpath = r"E:\vscode_dir\python_file\write_test.txt"
# 只写方式打开文件
f = open(fpath, "w")
# 写入文件
line = " 人生苦短 , 我用 Python"
text = f.write(line)
f.close()

| 方法/项 | 说明 |
|---|---|
| 参数 | 说明 |
| file | 文件路径名称 |
| mode | 打开方式 |
| buffering | 缓存机制，  1, 表示使用缓存机制， -1 表示使用系统默认  0 ，表示不适用缓存机制，只 |
对 Binary 有效 
| 方法/项 | 说明 |
|---|---|
| encoding | 编码格式 |
| newline | 换行符 |
| 参数 | 说明 |
| r | 只读模式，打开后不能执行写操作 |
| w | 只写模式，文件存在被清空，打开后不能执行读操作 |
| x | 创建新文件，以只写方式打开，若文件存在报错 |
| a | 追加模式， |
| + | 读写方式打开 |
| r+ | 读写方式打开 |
| w+ | 读写方式打开，文件存在被清空 |
二进制方式 rb, wb, xb, rb+, wb+ ，场景：图片，二进制文件等 
#### 3 文件打开方式详解  
#### 3.1 open 方法  
文件打开方法： 
主要参数： 
#### 3.2 打开方式  
文件打开模式： 
#### 3.3 文件读写操作  
#### 3.3.1 基本读写  
1. 以 “w“ 方式打开文件，会将当前的文件清空； 
2. 写文件换行，需要在行尾添加 “\n” ； 
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, 
closefd=True, opener=None) 
# 定义读取函数
def read_file(fpath):
fr = open(fpath)
content = fr.read()

结果： 
#### 3.3.2 读写方式打开  
文件以 r+ 或者 w+ 方式打开 
以 w+ 方式打开，文件内容清空 
以 r+ 方式打开： 
if content:
print(content)
else:
print(" 文件内容为空 ")
f.close()

# 定义写入函数
def write_file(fpath, content = ""):
fw = open(fpath, "w")
if content:
text = fw.write(content)
fw.close()
# 文件路径
fpath = r"E:\vscode_dir\python_file\write_only.txt"
# 写入内容
line = " 人生苦短 , 我用 Python"
# 打开文件并写入一行
write_file(fpath, line)
# 写入第二行
write_file(fpath, line)
# 读取文件内容
read_file(fpath)
# 只打开文件，不写入数据
write_file(fpath)
# 读取文件内容
read_file(fpath)
人生苦短 , 我用 Python
文件内容为空
fpath = r"E:\vscode_dir\python_file\write_read.txt"
# 打开文件
f = open(fpath, "w+")
line = " 人生苦短 , 我用 Python"
# 写入数据
text = f.write(line)
# 重置读取位置
f.seek(0, 0)
# 读取写入内容
print(f.read())
f.close()

#### 3.3.3 实现重复读取  
实现思路： 
1. 文件读取完成后，关闭文件并重新打开； 
2. 使用 seek 方法，重置读取位置； 
1. 重复打开实现方式： 
2. 使用 seek 重置位置 
重复读取文件 
fpath = r"E:\vscode_dir\python_file\write_read.txt"
# 打开文件
f = open(fpath, "r+")
# 读取文件内容
print(f.read())
line = " 自律 "
# 在文件尾部追加
f.write(line)
# 重置读取位置
f.seek(0, 0)
# 读取写入内容
print(f.read())
f.close()
fpath = r"E:\vscode_dir\python_file\test.txt"
# 第一次读取
f = open(fpath, encoding="utf-8")
text = f.read()
print(text)
f.close()
# 第二次读取
f = open(fpath, encoding="utf-8")
text = f.read()
print(text)
f.close()
f.seek(cookie, whence=0, /)
主要参数：
cookie ：偏移值；
whence ：偏移位置， 0 ：文件起始位置， 1 ：文件当前位置， 2 ：文件尾部
注意：
1）当文件不是以二进制方式打开，当 whence 不为 0 时， cookie 设置为 0 ；偏移值与文件编码格式相关；
2）当文件以二进制方式打开， cookie 可以设置其他正确的值；重复读取文件：

结果： 
#### 4 文件编码问题  
文件写入与读取： 

window 下默认编码格式： cp936 ，测试方法： 
结果： 
fpath = r"E:\vscode_dir\python_file\test.txt"
# 打开文件
f = open(fpath, encoding="utf-8")
# 设置读取次数
for i in range(3):
# 第一次读取
text = f.read()
print(text)
# 读取完成后，重置读取位置
f.seek(0, 0)
职场人要坚持锻炼身体，时刻关注自己的健康，
......
保持内心的平和，懂的给自己减压，保持良好的睡眠
fpath = r"E:\vscode_dir\python_file\encode_test.txt"
f = open(fpath, 'w')
line = " 床前明月光 "
f.write(line)
print(f)
f.close()
<_io.TextIOWrapper name='E:\\vscode_dir\\python_file\\write_only.txt' mode='w' 
encoding='cp936'>

| 方法/项 | 说明 |
|---|---|
| 读取方法 | 说明 |
| f.read(size=-1, /) | 读取文件内容，默认读取完 |
| f.readline(size=-1, /) | 读取一行，读取到 EOF 或者新的一行结束 |
| f.readlines(hint=-1, /) | 读取多行 |
for line in f: pass 使用 for 循环逐行遍历文件 
| 方法/项 | 说明 |
|---|---|
| 写入方法 | 说明 |
| f.write(text, /) | 写入数据 |
| f.writelines(lines, /) | 一次写入多行 |
编码引发的问题： 
结果： 
注意： 
1. 只读打开文件，设置编码格式要与其保存格式一致 
2. 一般看到打开文件，读取时遇到 "UnicodeDecodeError" 问题，需要检查设置的编码格式 

#### 5 文件读写方法  
#### 5.1 文件读取方式  
主要方法： 
#### 5.2 文件写入方式  
主要方法： 

fpath = r"E:\vscode_dir\python_file\encode_test.txt"
f = open(fpath, 'r', encoding="utf-8")
f.read()
#### 320 # decode input (taking the buffer into account)
321         data = self.buffer + input
--> 322         (result, consumed) = self._buffer_decode(data, self.errors, 
final)
#### 323 # keep undecoded input until the next call
324         self.buffer = data[consumed:]
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb4 in position 0: invalid 
start byte

6. 文件练习  
#### 6.1 产生销售数据  
需求：给定三个指定商品 (pr001, pr002, pr003) ，渠道 (channel1, channel2, channel3) ，销售额 (1~40
之间随机数 ) ，产生 30 条销售数据； 
示例： 
实现思路： 
1. 分析文件格式 ,
2. 分析使用知识点 ,
3. 代码实现与调试 ,
4. 封装成函数 ,
代码实现： 
pr001 channel1 38.2
pr002 channel2 36.5
pr003 channel2 37.1
pr002 channel3 18.6
import random
def gen_sales_report(fpath, nums = 30):
# 只写方式打开文件
fw = open(fpath, "w")
# 定义商品 ID
goodids = ["pr001", "pr002", "pr003"]
# 定义渠道
channels = ["channel1", "channel2", "channel3"]
max_value, min_value = 40, 10
for i in range(30):
# 商品 ID
goodid = random.choice(goodids)
# 渠道 ID
chid = random.choice(channels)
# 销售额
value = random.randint(min_value, max_value)
# 拼接一行数据
line = f"{goodid} {chid} {value}\n"
#print(line)
# 写入数据
fw.write(line)
fw.close()

fpath =  r"E:\vscode_dir\python_file\sales_report.txt"     
gen_sales_report(fpath)

#### 6.2 根据条件过滤数据  
需求：按照条件进行过滤，并数据保存到新文件中 
例如：获取商品： pr001 的所有数据，并保存到 pr001.txt 中 
实现思路： 
1. 读取数据 
2. 根据条件筛选数据，并记录符合条件数据 
3. 将数据写入对应的文件 
代码实现： 
#### 6.3 数据统计  
统计每个渠道，每个商品，总销售额； 
注意：假设渠道，商品数量未知； 
1. 统计每个渠道销售额，统计每个商品销售额； 
2. 数据结构设计， 
3. 统计思路及代码实现 
代码实现： 
# 销售数据
fpath =  r"E:\vscode_dir\python_file\sales_report.txt" 
# 过滤结果
pr001_report =  r"E:\vscode_dir\python_file\pr001_sales_report.txt" 
def filer_report_by_product(in_fpath, out_fpath, product):
# 打开销售数据
f = open(in_fpath)
# 创建新文件，保存过滤数据
fw = open(out_fpath, "w")
for line in f:
if line.startswith(product):
print(line, end="")
fw.write(line)
f.close()
fw.close()

# 过滤 pr001 的数据
filer_report_by_product(fpath, pr001_report, "pr001")  
from collections import Counter
def read_report(in_fpath):
# 打开销售数据
f = open(in_fpath)
# 切分数据
items = [line.strip().split() for line in f if line.strip()]
f.close()
return items

结果： 
#### 6.4 课后练习  
1. 按商品统计订单量， 
2. 按渠道统计订单量， 
3. 按商品统计每单成交的平均价格， 
4. 按渠道统计每单成交的平均价格， 
def analyse_data_by_product(items):
# 使用 Counter 进行统计
counter = Counter()
# 遍历数据
for product, _, price in items:
# 按商品统计销售额
counter[product] += float(price)
return counter
def analyse_data_by_channel(items):
# 使用 Counter 进行统计
counter = Counter()
# 遍历数据
for product, ch, price in items:
# 按商品统计销售额
counter[ch] += float(price)
return counter

fpath =  r"E:\vscode_dir\python_file\sales_report.txt" 
# 解析数据
data = read_report(fpath)
# 商品及销售额
product_result = analyse_data_by_product(data)
print(" 商品统计数据： ")
for item in product_result.items():
print(item)
# 渠道及销售额
print(" 渠道销售数据 ")
channel_result = analyse_data_by_channel(data)
for item in channel_result.items():
print(item)
商品统计数据：
('pr001', 212.0)
('pr003', 313.0)
('pr002', 266.0)
渠道销售数据
('channel3', 258.0)
('channel1', 302.0)
('channel2', 231.0)
### 20. CSV 文件详解
#### 1 csv 文件详解与应用  
#### 1.1 csv 文件  
csv 文件：使用纯文本来存储表格数据，并以指定的分隔符进行分隔， csv 的第一行一般为列名； 
常见场景：天池， Kaagle 等平台，提供开源数据多为 csv 文件； 
数据格式如下： 
#### 1.2 csv 部分主要内容  
主要内容： 
#### 1.3 学习目的  
1. 掌握 csv 文件格式； 
2. 掌握 csv 模块，能够熟练对 csv 文件进行读写操作； 
3. 锻炼思维与编程能力，提升对数据结构掌握与实用，提升解决问题的能力； 
#### 1.4 准备工作  
准备数据集： 
1. 某年中国人口统计数据集 (china_stastic.csv);
2. 俄罗斯人口统计数据集 (russian_demography.csv);
下载地址： 
链接： https://pan.baidu.com/s/1ZGastVBF2jXc3U9Q_DkPDg?pwd=qmqm  
提取码： qmqm

| 方法/项 | 说明 |
|---|---|
| 参数 | 说明 |
| delimiter | 字段分隔符，  默认为逗号： “,” |
| lineterminator | 换行符，默认： “\r\n” |
| quotechar | 用于包含有特殊字符字段，默认双引号 |
| quoting | 写文件控制引号行为 |
| quoting | 参数 说明 |
| csv.QUOTE_NONNUMERIC | 数字加引号 |
| csv.QUOTE_ALL | 所有字典加引号 |
| csv.QUOTE_MINIMAL | 特殊字典加引号 |
| csv.QUOTE_NONE | 都不加引号 |
2. csv 模块详解  
主要内容： 
| 方法/项 | 说明 |
|---|---|
| 1.csv | 模块及对应方法； |
| 2.csv | 文件读取； |
| 3.csv | 文件写入； |
#### 2.1 csv 快速上手  
前提：导入 csv 模块； 
csv_reader 主要参数： 
quoting 主要字段： 
#### 2.2 csv 读取两种方式  
python 中， csv 模块提供两种方法对文件进行读取； 
方式 1 ：逐行读取，只有数据， csv_reader = csv.reader(iterable [, dialect='excel'],…)
# 导入模块
import csv
# 打开文件
f = open(fpath)
# 创建 reader 对象
csv_reader = csv.reader(f)
# 逐行读取文件
for row in csv_reader:
print(line)
# 关闭文件
f.close()

结果： 

方式 2 ：逐行读取，读取内容：  列名 + 内容， csv_reader = csv. DictReader (iterable [, 
dialect='excel'],…)
结果： 
fpath = r"E:\vscode_dir\python_file\china_stastic.csv"
import csv
# 打开文件
f = open(fpath, encoding="UTF-8-sig")
# 创建 csvreader 对象
csv_reader = csv.reader(f)
# 逐行读取
for line in csv_reader:
print(line)
# 关闭文件
f.close()
['area', 'count', '2020 比重 ', '2010 比重 ']
| 方法/项 | 说明 |
|---|---|
| [' | 全国 [5]', '1411778724', '100', '100'] |
| [' | 北京 ', '21893095', '1.55', '1.46'] |
| [' | 天津 ', '13866009', '0.98', '0.97'] |
| [' | 河北 ', '74610235', '5.28', '5.36'] |
...
fpath = r"E:\vscode_dir\python_file\china_stastic.csv"
import csv
f = open(fpath, encoding="UTF-8-sig")
# 创建 DictReader 对象
csv_reader = csv.DictReader(f)
for line in csv_reader:
print(line)
# 关闭文件
f.close()
OrderedDict([('area', ' 全国 [5]'), ('count', '1411778724'), ('2020 比重 ', 
'100'), ('2010 比重 ', '100')])
OrderedDict([('area', ' 北京 '), ('count', '21893095'), ('2020 比重 ', '1.55'), 
('2010 比重 ', '1.46')])
OrderedDict([('area', ' 天津 '), ('count', '13866009'), ('2020 比重 ', '0.98'), 
('2010 比重 ', '0.97')])
OrderedDict([('area', ' 河北 '), ('count', '74610235'), ('2020 比重 ', '5.28'), 
('2010 比重 ', '5.36')])
OrderedDict([('area', ' 山西 '), ('count', '34915616'), ('2020 比重 ', '2.47'), 
('2010 比重 ', '2.67')])
OrderedDict([('area', ' 内蒙古 '), ('count', '24049155'), ('2020 比重 ', '1.7'), 
('2010 比重 ', '1.84')])
OrderedDict([('area', ' 辽宁 '), ('count', '42591407'), ('2020 比重 ', '3.02'), 
('2010 比重 ', '3.27')])

#### 2.3 writer 方式写入  
主要方法与流程： 
注意： 
1. 一般写入第一行为字段 
2. 写入内容的顺序要与字段对应 
具体实现： 
结果： 
#### 2.4 csv 写入空白行问题  
造成原因：写入两次换行 
解决方式： 
方式 1. 打开文件， open 设置 newline 为空字符串： f = open(fpath, "w",newline="")
# 创建 writer 对象
csvw = csv. writer(iterable [, dialect='excel'],…)
# 写入一行
csv.writerow(row) 
# 写入多行
csv.writerows(rows)
import csv
fpath = r"E:\vscode_dir\python_file\csv_write_test.csv"
# 打开文件
f = open(fpath, "w")
# 创建 writer 对象
csv_write = csv.writer(f)
cols = [" 姓名 ", " 年龄 ", " 身高 "]
line = [" 奇猫 ", 20, 175]
lines = [[" 小张 ", 21, 178],[" 小李 ", 21, 172]]
# 写入字段
csv_write.writerow(cols)
# 写入第一行数据
csv_write.writerow(line)
# 写入多行数据
csv_write.writerows(lines)
# 关闭文件
f.close()

方式 2. 创建 write 对象，指定 lineterminator 为 "\r" ： csv_write = csv.writer(f, lineterminator="\r")
#### 2.5 DictWriter 方式写入  
写入流程： 
示例： 
3. csv 文件练习  
准备工作：下载 russian_demography.csv 数据集，数据集内容与字段： 
数据集内容： 
# 创建 DictWriter 对象， fieldnames ：字段名称 
csvw = csv.DictWriter(f, fieldnames, restval='',...)
# 写入字段
wrcsv.writeheader()
# 写入一行数据，数据格式为字典
wrcsv.writerow(rowdict)
# 写入多行数据
wrcsv.writerow(rowdicts)
import csv
fpath = r"E:\vscode_dir\python_file\csv_dictwrite_test.csv"
# 打开文件
f = open(fpath, "w",newline="")
cols = [" 姓名 ", " 年龄 ", " 身高 "]
# 创建 writer 对象
csv_write = csv.DictWriter(f, fieldnames=cols)
# 写入列名
csv_write.writeheader()
# 写入数据，将数据整理成字典形式；
line = [" 奇猫 ", 20, 175]
lines = [[" 小张 ", 21, 178],[" 小李 ", 21, 172]]
# 写入第一行数据
item = dict(zip(cols, line))
csv_write.writerow(item)
# 写入多行数据
items = [dict(zip(cols, item)) for item in lines]
csv_write.writerows(items)
# 关闭文件
f.close()

| 方法/项 | 说明 |
|---|---|
| 字段 | 说明 |
| year | 年份 |
| region | 地区 |
| npg | 增长率 |
birth_rate 1000 人口出生率 
death_rate 1000 人口死亡率 
gdw 人口比重 
urbanization 城市化率 
字段说明： 
需求： 
1. 基本数据统计，数据量，年份值及数量，地区及数量； 
2. 按照年份统计整体的出生率，死亡率，并分别降序； 
3. 将指定年份将数据保存到指定文件中； 
目标： 
1. 使用 Python 处理数据； 
2.csv 文件读写强化练习； 
3. 数据结构灵活使用； 
4. 提升编程思维与动手能力； 
#### 3.1 基本信息统计  
问题： 
1. 数据读取？ 
2. 选择哪种数据结构记录？

数据结构： 
代码实现： 
#### 3.2 按照年份统计出生率与死亡率  
问题： 
1. 数据结构定义？  
2. 实现过程与思路？ 
数据结构： 
基本数据统计完成之后，分别计算每个年份对应的出生率，死亡率 
代码实现： 
result = {lens:0, years:[], regions:[]}
# 或者
result = {lens:0, years:set(), regions:set()}
import csv
def count_base_info(fpath):

result = {"lens":0, "years":[], "regions":[]}
f = open(fpath)
csv_reader = csv.DictReader(f)
for item in csv_reader:
result["lens"] += 1
year = item.get("year")
region = item.get("region")
key_map = {"years":"year", "regions":"region"}
for k1, k2 in key_map.items():
value = item.get(k2)
if value and value not in result[k1]:
result[k1].append(value)

return result

fpath = r"E:\vscode_dir\python_file\russian_demography.csv"
res = count_base_info(fpath)
| 方法/项 | 说明 |
|---|---|
| # | 统计总数量 |
| print(" | 数据量： ", res["lens"]) |
| # | 输出年份数量及数值 |
| print(" | 年份数量： ", len(res["years"])) |
| print(" | 所有年份 ",' '.join(res["years"])) |
| # | 输出区域数量及名称 |
| print(" | 区域数量： ",len(res["regions"])) |
| print(" | 区域名称： ",",".join(res["regions"])) |
| # | 记录每年的累积出生率，死亡率，数量，最后统计计算平均出生率，死亡率； |
{
年份:{year:年份,birth_rate:累加值， death_rate:累加值， counts ：出现次数},
年份:{year:年份,birth_rate:累加值， death_rate:累加值， counts ：出现次数},
...
}

import csv
def str_to_float(value):
# 将字符串装成浮点数
if value.strip():
return float(value.strip())
else:
return 0
def count_rate(fpath):
# 数据基本统计
result = {}    
f = open(fpath)
csv_reader = csv.DictReader(f)

for item in csv_reader:
# 获取年份，出生率，死亡率
year = item.get("year")
birth_rate = str_to_float(item.get("birth_rate"))
death_rate = str_to_float(item.get("death_rate"))
# 根据年份统计数据
if year in result:
tmp = result[year]
tmp["birth_rate"] += birth_rate
tmp["birth_rate"] = round(tmp["birth_rate"],2)
tmp["death_rate"] += death_rate
tmp["death_rate"] = round(tmp["death_rate"],2)
tmp["nums"] += 1

else:
tmp = {"year":year,"birth_rate":birth_rate,"death_rate":death_rate, 
"nums":1}
result[year]= tmp
# 统计每个年份的平均出生率与死亡率
res = []
for key in result:
values = result[key]
tmp = {"year":key}
tmp["average_birth_rate"] = round(values["birth_rate"]/values["nums"],2)
tmp["average_death_rate"] = round(values["death_rate"]/values["nums"],2)
res.append(tmp)

return res
def dump(items):
for item in items:
print(item)
# 获取出生率
def sort_by_birth_rate(item):
return item.get("average_birth_rate")
# 获取死亡率
def sort_by_death_rate(item):
return item.get("average_death_rate")
fpath = r"E:\vscode_dir\python_file\russian_demography.csv"

#### 3.3 将指定年份保存  
思路与流程： 
1. 打开 csv 文件遍历数据 
2. 过滤指定年份数据 
3. 保存数据到指定的 csv 文件 
代码实现： 




res = count_rate(fpath)   
res.sort(key=sort_by_birth_rate, reverse=True)
dump(res)
res.sort(key=sort_by_death_rate, reverse=True)
dump(res)
def filer_data(infpath, outfpath, year):

result = {}
rows = []
fr = open(infpath)

csv_reader = csv.DictReader(fr)
for item in csv_reader:
# 按年份过滤
if year == item.get("year"):
rows.append(item)
fr.close()

# 打开文件
fw = open(outfpath, "w",newline="")
# 获取列名
cols = item.keys()
# 创建 DictWriter 对象
csv_writer = csv.DictWriter(fw, fieldnames=cols)
# 写入字段
csv_writer.writeheader()
# 写入数据
csv_writer.writerows(rows)
# 关闭文件
fw.close()
year = "2007"
infpath = r"E:\vscode_dir\python_file\russian_demography.csv"
outfpath = r"E:\vscode_dir\python_file\2017_data.csv"
filer_data(infpath, outfpath, year)
### 21. Excel 文件详解
#### 1 excel 文件  
主要内容： 

注意点： 
1.excel 相关模块需要使用 pip 进行安装； 
2. 学习此类模块，通过官网或者网络找案例，对要使用的功能进行验证； 
3. 课程中主要介绍： openpyxl 模块； 
#### 2 openpyxl  
openpyxl 安装： 
官方文档： 

pip install openpyxl
https://openpyxl.readthedocs.io/en/stable/

方法 说明 
wb = load_workbook(‘xx.xlsx') 打开 excel 文件 
wb.sheetnames 获取所有 sheet 名称 
sheet = wb[sheetname] 根据名称获取 sheet
| 方法/项 | 说明 |
|---|---|
| wb.active | 获取当前默认的 sheet |
| wb.close() | 关闭文件 |
| wb.save(filename) | 将当前的 workbook 保存到指定的路径 |
#### 2.1 excel 操作过程  
1. 打开 excel 文件； 
2. 获取指定的 sheet;
3. 对 sheet 中的行列单元格进行操作； 
4. 保存并关闭文件； 
#### 2.2 打开关闭 excel 文件  
目标： 
1. 打开 excel;
2. 获取所有的 sheet;
3. 根据名称获取 sheet;
相关操作： 
#### 2.3 excel 内容读取  
目标： 
1. 获取指定单元格及内容 
2. 获取指定行及内容 
# 导入模块
from openpyxl import load_workbook
order_path = r'E:\vscode_dir\python_file\online_order.xlsx'
# 打开 excel 文件
wb = load_workbook(order_path)
# 获取 sheet 的名称
sheetnames = wb.sheetnames
for sheetname in sheetnames:
print("sheet name:", sheetname)
current_sheet = wb[sheetname]
print(current_sheet)
wb.close()

方法 说明 
cell = sheet["A1"] 获取一个单元格 
| 方法/项 | 说明 |
|---|---|
| cell.value | 获取单元格数据 |
| sheet['A'] | 获取第 A 列数据单元 |
| sheet['A':'B'] | 获取第 A 到 B 列数据单元 |
| sheet[n] | 获取第 n 行数据单元 |
| sheet[m:n] | 获取 m 到 n 行数据单元 |
| sheet["A1":"C5"] | 获取指定行列范围的数据单元 |
ws.iter_cols(min_col, max_col, min_row ， 
max_row ） 
返回指定范围数据单元迭代器，数据格式按 
列返回 
ws.iter_rows(min_col, max_col, min_row ， 
max_row ） 
返回指定范围数据单元迭代器，数据格式按 
行返回 
sheet.max_row 获取当前 sheet 中最大行 
sheet.max_column 获取当前 sheet 中最大列 
3. 获取指定列及内容 
4. 获取指定范围及内容 
相关方法： 
#### 2.4 iter_cols 与 iter_rows 说明

#### 2.5 练习  
需求： 
1. 计算当前总销售额；  
2. 计算笔单价 ( 每笔成交的平均金额 ) ； 
基本思路： 
1. 打开 excel 文件，获取 sheet ； 
2. 找到 " 支付金额 " ，获取数值； 
3. 计算销售额与客单价； 
具体实现： 
#### 2.6 Excel 写入  
相关方法 
from openpyxl import load_workbook
order_path = r'E:\vscode_dir\python_file\online_order_small.xlsx'
# 打开文件
wb = load_workbook(order_path)
# 获取当前 sheet
ws = wb.active
# 获取表格
pay_col = ws["D2":"D10"]
# 获取支付金额
pay_ment_list = [cell[0].value for cell in pay_col[2:10]]
# 计算总销售额
total = sum(pay_ment_list)
# 计算笔单价
pay_average = round(total/len(pay_ment_list), 2)
| 方法/项 | 说明 |
|---|---|
| # | 输出结果 |
| print(f" | 销售额： {total}, 笔单价： {pay_average}") |
| 方法 | 说明 |
wb = Workbook() 创建 workbook 对象 
sheet = wb.active 获取当前 sheet
wb.create_sheet(title=None, index=None) 创建新的 sheet ， title 为 sheet 名称 
wb.remove(sheet) 根据名称删除 sheet
sheet['A1'] = 42 设置单元格值 
sheet.append([1, 2, 3]) 插入一行数据 
wb.save(fpath) 保存数据到 Excel
基本操作： 
#### 3 练习  

需求： 
1. 统计每个省份的销售额，订单量； 
2. 按照省份将数据拆分，保存到新的 excel 的 sheet 中， sheet 以省份命名； 
#### 3.1 按照省份统计  
基本流程： 
1. 理解需求， 
2. 理解数据， 
3. 数据结构选择， 
4. 订单状态处理， 
5. 指标计算， 
数据结构格式： 
from openpyxl import Workbook
f_path = r'E:\vscode_dir\python_file\write_test.xlsx'
# 创建 Workbook 对象
test_wb = Workbook()
# 创建 sheet1
ws = test_wb.create_sheet('sheet1', 0)
# 添加一行数据
ws.append([1,2,3,4])
# 添加一行数据
ws.append([4,5,6,7])
# 设置指定的单元格
ws['A3'] = 10
# 保存文件
test_wb.save(f_path)

数据处理 
代码实现： 
{
| 方法/项 | 说明 |
|---|---|
| ' | 江苏省 ': defaultdict(float, {'num': 4463.0, 'payment': 358718.3}), |
| ' | 广东省 ': defaultdict(float, {'num': 5828.0, 'payment': 449990.8}), |
| ' | 辽宁省 ': defaultdict(float, {'num': 1076.0, 'payment': 77805.4}), |
| ' | 广西壮族自治区 ': defaultdict(float, {'num': 564.0, 'payment': 42123.1}), |
}
>1. 使用列号 ( 数字 ) 获取每列数值，问题：如果新增列，需要修改列值；
>2. 将字段与数据处理成字典，根据字段名获取数据值 , 好处：只要列名不变，代码不需要修改；
def count_order(wb):
ws = wb.active
#rows 为迭代器
rows =  ws.rows
# 第一行字段不要
row = next(rows)
col_names = [cell.value for cell in row]
result = {}
status_success = " 交易成功 "
# 获取数据
for row in rows:
# 获取每行数据
values = [cell.value for cell in row]
# 列名与数值构成字典
order_info = dict(zip(col_names, values))
# 获取省份，订单状态，支付金额
province = order_info.get(" 省份 ")
order_status = order_info.get(" 订单状态 ")
order_pay = order_info.get(" 支付金额 ")


if province and order_status == status_success and province in 
result:
# 当前数据有效，且该省份在当前的结果中
info = result.get(province)
info["num"] += 1
info["payment"] += order_pay
info["payment"] = round(info["payment"], 3)

elif province and order_status == status_success:
# 当前数据有效，且当前省份没有在当前结果中

info = defaultdict(float)
result[province] = info
info["num"] += 1
info["payment"] += order_pay
info["payment"] = round(info["payment"], 3)

return result
# 导入模块
from openpyxl import Workbook

结果： 

#### 3.2 按照省份进行拆分  
基本流程 
1. 打开原文件，新建 workbook ， 
2. 读取源文件，获取省份， 
3. 在新 workbook 中添加对应的省份的 sheet ， 
4. 将省份对应的数据添加到 sheet 中 
写入方式 
代码实现 
from collections import defaultdict
# 目录
fpath = r"E:\vscode_dir\python_file\online_order.xlsx"
# 打开 Excel
wb = load_workbook(fpath)
# 数据统计
res = count_order(wb)
print(res)
# 关闭 excel
wb.close()
{' 江苏省 ': defaultdict(float, {'num': 4463.0, 'payment': 358718.3}),
' 广东省 ': defaultdict(float, {'num': 5828.0, 'payment': 449990.8}),
...
}
方式 1 ：将省份对应的数据整理好之后，统一写入；
方式 2 ：读取一行，写入到对应的 sheet 中，如果 sheet 不存在则在新的 workbook 中创建对应的
sheet ，然后写入；
本题目，使用第二种方式实现；
def split_order_by_field(src_path, des_path, field):

sheet_map = {}
# 打开源文件
src_wb = load_workbook(src_path)
# 创建写对象
dest_wb = Workbook()

# 获取当前数据的字段
src_sheet = src_wb.active
rows = src_sheet.rows
row = next(rows)
# 获取字段值

column_names = [cell.value for cell in row]
for row in rows:

#### 4 excel 格式设置  
官方文档： 
主要格式设置： 
# 获取一行数据
values = [cell.value for cell in row]
# 转成字典
order_info = dict(zip(column_names, values))
# 根据字段进行拆分
field_value = order_info.get(field)
# 根据字段对应值，找到 sheet
if field_value and field_value in sheet_map:
sheet = sheet_map.get(field_value)
sheet.append(values)
else:
# 如果没有对应的 sheet, 创建新的 sheet
sheet = dest_wb.create_sheet(field_value)
sheet.append(column_names)
sheet.append(values)
sheet_map[field_value] = sheet

src_wb.close()
dest_wb.save(des_path)


from openpyxl import load_workbook
from openpyxl import Workbook
src_path = r"E:\vscode_dir\python_file\online_order.xlsx"
dest_path = r"E:\vscode_dir\python_file\online_order_split.xlsx"
split_order_by_field(src_path, dest_path, " 省份 ")
https://openpyxl.readthedocs.io/en/stable/styles.html

| 方法/项 | 说明 |
|---|---|
| 属性 | 说明 |
| cell.value | 获取单元格内的值 |
| cell.font | 设置单元格内的字体样式 |
| cell.fill | 设置单元格内的填充颜色 |
| cell.alignment | 设置单元格内的对齐方式 |
| cell.border | 设置单元格内的边框样式 |
单元格设置： 

#### 4.1 字体设置  
默认设置： 

#### 4.2 单元格设置  
默认设置 
填充类型选择： 

from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, 
Font
# 字体设置
font = Font(name='Calibri', size=11, bold=False, italic=False, vertAlign=None, 
underline='none', strike=False, color='FF000000')
# 填充设置
fill = PatternFill(fill_type=None, start_color='FFFFFFFF',end_color='FF000000')
# 边框设置
border = Border(left=Side(border_style=None, color='FF000000'),...)
# 对齐设置
alignment=Alignment(horizontal='general', vertical='bottom', text_rotation=0, 
wrap_text=False, shrink_to_fit=False, indent=0)
通过 dir(fills)查看，主要填充类型，对应值为字符串，
例如： fills.FILL_PATTERN_DARKGRAY ，结果： darkGray ：
'FILL_NONE', 'FILL_PATTERN_DARKDOWN','FILL_PATTERN_DARKGRAY', 
'FILL_PATTERN_DARKGRID', 'FILL_PATTERN_DARKHORIZONTAL', 
'FILL_PATTERN_DARKTRELLIS', 'FILL_PATTERN_DARKUP',
'FILL_PATTERN_DARKVERTICAL','FILL_PATTERN_GRAY0625','FILL_PATTERN_GRAY125','FILL
_PATTERN_LIGHTDOWN',
'FILL_PATTERN_LIGHTGRAY','FILL_PATTERN_LIGHTGRID','FILL_PATTERN_LIGHTHORIZONTAL'
,'FILL_PATTERN_LIGHTTRELLIS','FILL_PATTERN_LIGHTUP','FILL_PATTERN_LIGHTVERTICAL'
,'FILL_PATTERN_MEDIUMGRAY','FILL_SOLID',

姓名 Q1 Q1 Q3 Q4 
id01 90 100 88 77
id02 77 95 90 80
#### 4.3 格式设置练习  

#### 4.4 销售数据练习  
产生随机销售数据，数值范围： [50:100] ，数据格式： 
将数据写入 excel, 并将销售总额排名前 5 ，姓名设置为红色； 
步骤： 
1. 产生数据 
2. 统计数据 
3. 排序 
4. 写入数据，并设置格式 
具体实现： 
产生数据 
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
from openpyxl.styles import PatternFill
from openpyxl import Workbook
fpath = r'E:\vscode_dir\python_file\excel_font_test.xlsx'
wb = Workbook()
ws = wb.active
#A1 设置颜色
ft1 = Font(color="FF0000")
a1_cell = ws["A1"]
a1_cell.font = ft1
a1_cell.value = " 兰陵王 "
#A2 设置颜色，大小，字体
ft2 = Font(name=' 微软雅黑 ', size=14, color="00808000")
a2_cell = ws["A2"]
a2_cell.font = ft2
a2_cell.value = " 孙悟空 "
#A2 设置颜色，大小，字体，  下划线
ft3 = Font(name=' 隶书 ', size=14, color="00FF00FF", underline="single")
a3_cell = ws["A3"]
a3_cell.font = ft3
# 设置填充色
fill = PatternFill(fill_type="solid",start_color='0000DD',end_color='FF000000')
a3_cell.fill = fill
a3_cell.value = " 亚瑟 "
wb.save(fpath)

数据格式： 
代码实现： 

按照销售额统计数据 

写入数据 
数据格式：
```
data = {
"id01":[90, 100, 88, 77],
"id02":{90, 77, 67, 97},
....
....
"id10":{88, 98, 54, 77},
}
```
import random
def gen_item():
start = 50
end = 101
vals = []
for i in range(4):
vals.append(random.randint(start, end))
return vals
def gen_data(num):
uid = ["id%02d"%i for i in range(1, num+1)]
values = [gen_item() for i in range(1, num+1)]
data = dict(zip(uid, values))
return data
data = gen_data(10)
data
# 求和函数
def sum_func(item):
return sum(item[1])
# 排序获取排名前 5 的数据
max_five = sorted(data.items(),key=sum_func, reverse=True)[:5]
max_five_key = [item[0] for item in max_five]
max_five_key
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
from openpyxl import Workbook
def save_data_to_excel(fpath, data, max_five):
# 第一行为字段
fields = [" 姓名 ", "Q1", "Q2", "Q3", "Q4"]

公式 说明 
求均值 =AVERAGE(A1,A5)
求和 =SUM(A1, A6)
#### 5 excel 公式与图表应用  
#### 5.1 公式应用  
准备工作，熟悉 excel 常用的公式，例如： 
excel 中使用公式方式如下，核心点：插入公式；： 
练习，如下数据，计算每个科目的平均分，并将 excel 另存； 
# 设置单元格字体颜色
ft = Font(color="FF0000")
# 打开 excel
wb = Workbook()
ws = wb.active
# 添加字段
ws.append(fields)
i = 1
# 获取数据
for key,v in data.items():
i += 1
row = list(v)
row.insert(0, key)
ws.append(row)
# 若该员工排名前 5 ，设置其字体格式
if key in max_five:
cell_name = "A%d"%i
cell = ws[cell_name]
cell.font = ft
# 保存文件
wb.save(fpath)

fpath = r'E:\vscode_dir\python_file\sales_count.xlsx'
save_data_to_excel(fpath, data, max_five_key)
ws["xx"] = "=AVERAGE(xm:xm)"

代码实现： 
#### 6 excel 插入图表  
建议参考文档： 
需求：在上面 excel 中添加柱状图，对比每个学生各科课程 
代码实现： 
from openpyxl import load_workbook
path = r'E:\vscode_dir\python_file\test.xlsx'
spath = r'E:\vscode_dir\python_file\t_2.xlsx'
wb = load_workbook(path)
ws = wb['Sheet']
# 获取
max_row = ws.max_row
# 插入行为最大行 +1
insert_row = max_row+1
# 插入计算值： =AVERAGE(A1:A4)
formula = '=AVERAGE(%s1:%s%d)'
# 插入位置分别为： CD ；
ws['C%d'%insert_row] = formula%('C','C', max_row)
ws['D%d'%insert_row] = formula%('D','D', max_row)
# 保存
wb.save(spath)
https://openpyxl.readthedocs.io/en/stable/charts/introduction.html
from openpyxl import load_workbook
from openpyxl.chart import BarChart, Reference
path = r'E:\vscode_dir\python_file\test.xlsx'
spath = r'E:\vscode_dir\python_file\chart_bar.xlsx'
wb = load_workbook(path)
ws = wb['Sheet']
chart1 = BarChart()
chart1.type = "col"
chart1.style = 10
chart1.title = " 成绩对比图表 "
chart1.y_axis.title = ' 成绩 '
chart1.x_axis.title = ' 姓名 '
# 选择数据区域
data = Reference(ws, min_col=3, min_row=1, max_row=5, max_col=4)
# 选择 cats 区域
cats = Reference(ws, min_col=2, min_row=2, max_row=5)
# 添加数据
chart1.add_data(data, titles_from_data=True)
# 添加类别
chart1.set_categories(cats)
chart1.shape = 4
# 图表位置
ws.add_chart(chart1, "A10")
# 保存添加图表
wb.save(spath)
### 22. JSON 与 Pickle
方法 说明 
json. dumps(obj,…) 将对象转 Json 字符串，前提： obj 对象支持该序列化方式 
json. loads(s,…) 将 Json 字符串转 Python 对象 
json. dump(obj,  fp ， ... ） 将对象以 json 格式写入文件  , 前提： obj 对象支持该序列化方式 
json. load(fp,…) 将 json 文件数据转成 Python 对象 
1. 主要内容  
序列化：将对象转成字节流，例如：机器学习模型转成字节流，保存到文件； 
反序列化：将字节流转成对象，例如：读取文件，将字节流转成机器学习模型； 
2. json  
#### 2.1 json 简介  
json ：一种轻量级的数据交换格式，文本序列化，具有一定的可读性； 
主要作用：网络数据传输，数据存储，交换等 
使用场景： 
1. 前端与后台请求数据格式； 
2.mysql 中数据存储； 
3. 分布式爬虫中，将数据保存到 redis 等； 
#### 2.2 json 模块及主要方法  
模块导入： 
主要方法： 
#### 2.3 json 练习  
Json 序列化与反序列化 
import json

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| pickle.dumps(obj ， ...) | 将 python 对象序列化为字节流 |
| pickle.loads(data,...) | 将字节流反序列化为 Python 对象 |
pickle.dump(obj, file,
...) 将对象存以字节流方式保存到文件， file 为文件对象，以 “wb” 方式打开 
pickle.load(file ， ... ） 将文件字节流反序列化为 Python 对象， file 为文件对象，以 "rb" 方式打 
开 
Json 文件存储与读取 
#### 3 pickle 模块  
pickle 是 Python 中特有的，用于二进制序列化与反序列模块，序列化后不具有可读性； 
#### 3.1 picke 模块及主要方法  
模块导入： 

主要方法： 
import json
info = {" 华为 ":" 鸿蒙 ", "Google":"android", "Apple":"IOS"}
# 将 python 对象对转成 json 数据
json_data = json.dumps(info)
print(json_data)
# 将 Json 数据转成 python 对象
data = json.loads(json_data)
print(data)
import json
fpath = r"E:\vscode_dir\python_file\test_obj.json"
info = {" 华为 ":" 鸿蒙 ", "Google":"android", "Apple":"IOS"}
# 将 python 对象对象转成 json 数据
fw = open(fpath, "w")
json.dump(info, fw)
print("save info to file")
fw.close()
fr = open(fpath)
# # 将 Json 数据转成 python 对象
data = json.load(fr)
print(data)
import pickle

#### 3.2 pickle 练习  
序列化与反序列化 
pickle 文件存储与读取 







import pickle
info = {" 华为 ":" 鸿蒙 ", "Google":"android", "Apple":"IOS"}
pickle_data = pickle.dumps(info)
print(pickle_data)
data = pickle.loads(pickle_data)
print(data)
import pickle
fpath = r"E:\vscode_dir\python_file\test_obj.pickle"
info = {" 华为 ":" 鸿蒙 ", "Google":"android", "Apple":"IOS"}
# 将 python 对象对象转成 json 数据
fw = open(fpath, "wb")
pickle.dump(info, fw)
print("save info to file")
fw.close()
fr = open(fpath, "rb")
# # 将 pcikle 转成 python 对象
data = pickle.load(fr)
print(data)
### 23. INI 配置文件处理
主要内容  
1. ini 文件格式  
.ini 文件是 Initialization File 的缩写，即初始化文件，被用于配置文件，例如： mysql 等的配置文件； 
ini 文件由：节，键，值组成 ;
文件格式： 
mysql 配置文件： 
ini 文件主要操作： 
1. 获取节下面的键及对应的值； 
2. 添加，修改节或者下面的键或者值； 
#### 2 configparser 模块  
模块导入： 
节
[section]
参数
（键=值）
name=value
[mysqld_safe]
socket          = /var/run/mysqld/mysqld.sock
nice            = 0
[mysqld]
user            = mysql
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
port            = 3306
from configparser import ConfigParser

方法 说明 
config = ConfigParser() 创建 ConfigParser 对象 
| 方法/项 | 说明 |
|---|---|
| config.read(fpath, encoding='utf-8') | 导入文件 |
| config.sections()/items() | 获取所有的 section 名称 / 名称与 section |
| config.values() | 返回每个 section |
| config.keys()/config.values() | 获取所有的 sections 的 key/section |
| config.has_section(section) | 是否包含 section |
config.has_option(section, option) section 下是否包含 option
config.get(section, option, *, raw=False…) 获取 section 下 key 对应 value
#### 3.1 读取相关方法  
#### 3.2 读取操作  
#### 3.2.1 打开文件  
#### 3.2.2 读取 session  
结果： 
#### 3.2.3 section 与 key 判断  
结果： 
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
['baidu', 'jingdong']
[('DEFAULT', <Section: DEFAULT>), ('baidu', <Section: baidu>), ('jingdong', 
<Section: jingdong>)]
res = config.has_section('baidu')
print(res)
config.has_option('baidu', 'addr')
print(res)
True
True

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| config.add_section(section) | 添加 session |
| config.set(section, option, value=None) | 添加 key-value |
| config.write(fp, space_around_delimiters=True) | 写入文件 |
#### 3.2.4 读取值  
结果： 
#### 2.3 ini 文件写入方法  
#### 2.4 ini 文件写入  
#### 2.4.1 创建 ConfigParser 对象  
#### 2.4.2 添加 sesction  
#### 2.4.3 添加 key_value  
#### 2.4.4 保存到文件  

# 通过节，键找到对应的值
baidu_src = config.get('baidu', 'src')
print("src:", baidu_src)
# 获取节
baidu = config['baidu']
# 通过节找到键对应的值
baidu_addr = baidu.get('addr')
print("addr:", baidu_addr)
src: www.baidu.com
addr: 北京
from configparser import ConfigParser
fpath = r'E:\vscode_dir\python_file\new_config.ini'
config = ConfigParser()
# 可以在原来基础上添加信息
#config.read(fpath, encoding='utf-8')
config.add_section('tencent')
config.set('tencent', 'addr', ' 深圳 ')
config.set('tencent', 'src', 'https://www.tencent.com/')
fwpath = r'E:\vscode_dir\python_file\netconfig1.ini'
f = open(fwpath, 'w', encoding='utf-8')
config.write(f)
f.close()
### 24. OS 模块目录处理
| 方法/项 | 说明 |
|---|---|
| 函数 | 说明 |
| os.getcwd() | 返回表示当前工作目录 |
| os.mkdir(name)/os.rmdir(name) | 创建目录 / 删除目录 |
os.makedirs(name)/os.removedirs(name)创建目录树 / 删除目录 
os.listdir(path=None) 获取指定目录下所有文件目录 
os.rename(src , dst**,.. ） 文件目录重命名 
os.renames(old , new ) 递归方式重命名目录或者文件 
os.walk(top, topdown=True,…) 获取指定目录下所有文件目录，返回目录树迭代器 
#### 1 文件与目录处理  
OS 模块模块提供了操作系统相关功能的函数，比如：获取系统信息，文件与目录的操作，执行系统命令 
等； 
官方文档： https://docs.python.org/zh-cn/3.7/library/os.html
主要内容： 
主要模块： 
#### 2 目录操作  
import os
import shutil

#### OCR 补充（图片幻灯片识别，可能有少量误差）

1文件与目录处理
OS模块模块提供了操作系统相关功能的函数，比如：获取系统信息，文件与目录的操作，执行系统命令
等；
主要内容：
官方文档：https://docs.python.org/zh-cn/3.7/library/os.html
目录操作。
遍历目录。
文件与目录
其他操作
创建目录
删除/复制/移动目录
获取目录下所有文件
获取目录及子目录下所有文件
是否是文件/目录
文件目录是否存在
路径拼接
主要模块：
import os
import shutil
2目录操作
函数
os.getcwdO
os.mkdir（name）/os.rmdir（name）
os.makedirs（name）/os.removedirs（name）
os.listdir（path=None）
os.rename（Src, dst**..）
os.renames（old, new）
os.walk（top, topdown=True....）
说明
返回表示当前工作目录
创建目录/删除目录
创建目录树/删除目录
获取指定目录下所有文件目录
文件目录重命名
递归方式重命名目录或者文件
获取指定目录下所有文件目录，返回目录树迭代器
## 第五部分 正则表达式
### 25. 正则表达式
#### 1 主要内容

如图：

#### 2 re模块

正则表达式（Regular Expression）：是用于描述一组字符串特征的模式，用来匹配特定的字符串。

应用场景：

1.验证，例如：对字符串按照设置规则进行检验，比如：用户名，密码格式；
2.查找，例如：在文本中查找指定规则字符串；
3.替换，例如：将指定的文本替换为新文本；
4.切分，例如：按照指定的分隔符对文本进行切分；

#### 2.1 re详解

Python中使用re模块处理正则表达式，主要功能：匹配，查找，切分，替换；

使用过程：

#导入re模块
import re

主要方法：

方法 说明

re.match(pattern, string, flags=0) 从头匹配，匹配成功返回Match对象，否则返回None

re.search(pattern, string, flags=0)在指定的字符串按照规则查找子串，匹配成功返回Match对象，否则返回None

| 方法/项 | 说明 |
|---|---|
| re.findall(pattern, string, flags=0) | 查找所有匹配，返回匹配列表 |
| re.split(pattern, string, maxsplit=0, flags=0) | 切分字符串，返回切分后的列表 |
| re.sub(pattern, repl, string, count=0,flags=0) | 字符串替换，返回替换后的字符串 |
flag值：

| 方法/项 | 说明 |
|---|---|
| flag | 描述 |
| re.I | 匹配对大小写不敏感 |
| re.L | 做本地化识别匹配 |
| re.M | 多行匹配，改变'^'和'$'的行为 |
| re.S | 点任意匹配模式，改变'.'的行为 |
| re.U | 根据Unicode字符集解析字符 |
re.X正则表达式可以是多行， 忽略空白字符，并可以加入注释

#### 2.2 第一个案例

需求：匹配以数字开头的字符串

例如：以match方法进行匹配

```python
import re
s1 = "001_sun"
s2 = "qimao"
```

```python
ma = re.match(r'\d', s1)
```

```python
ma
```
<re.Match object; span=(0, 1), match='0'>

```python
ma = re.match(r'\d', s2)
```

```python
type(ma)
```
NoneType

```python
import re
s1 = "001_sun"
s2 = "qimao"
#\d表示匹配任意数字
ma1 = re.match('\d', s1)
print(ma1)
ma2 = re.match('\d', s2)
print(ma2)
```

#### 2.3 Match对象

| 方法/项 | 说明 |
|---|---|
| Match对象方法 | 说明 |
| m.start()/m.end() | 匹配开始和结束时的索引 |
| m.span() | 匹配索引开始结束组成元组 |
| m.group() | 匹配的字符串 |
| m.groups() | 包含所有子组的元组 |
m. groupdict()返回匹配的所有命名子组的字典

```python
import re
s1 = "001_sun"
#\d表示匹配任意数字
ma = re.match(r'\d', s1)
print("ma.group:", ma.group())
print("ma.span:", ma.span())
print("ma.start:%d, ma.end:%d"% (ma.start(), ma.end()))
```

#### 2.4 compile方法

re.compile用于将字符串形式的正则表达式编译为Pattern对象，可以使用Pattern对象种方法完成匹配查找等操作；

应用场景：如果在循环中进行重复的操作，推荐先将正则表达式转成Pattern对象；

```python
re_cmp = re.compile(r'\d')
```

```python
re_cmp.match('0123')
```
<re.Match object; span=(0, 1), match='0'>

```python
re_cmp = re.compile(r'\d')
ma = re_cmp.match("0123")
print(ma)
```

#### 3 正则表达式

#### 3.1 字符匹配

字符 说明

. 匹配任意字符(\n除外)

| 方法/项 | 说明 |
|---|---|
| \转义符 | 特殊字符匹配 |
| […] | 匹配字符集 |
| \d/\D | 匹配数字/匹配非数字 |
| \s/\S | 匹配空白字符/匹配非空白字符 |
| \w/\W | 匹配单词字符[a-zA-Z0-9]/匹配非单词字符 |
说明：

[0-9]:匹配数字
[a-z]:匹配小写字母
[A-Z]:匹配大写字母

需求：

1. 字符串以大写字母开头；
2. 字符串以数字开头；
3. 字符串以数字或者小写字母开头；
4. 字符串第一个字符位数字，第二个字符为小写字符；
5. 字符串以ABCDE中某个字符开头；

```python
import re
s1 = "Python"
s2 = "15011345578"
s3 = "AB_test"
s4 = "test"
```

```python
re.match(r'[A-Z]', s1)
```
<re.Match object; span=(0, 1), match='P'>

```python
re.match(r'\d', s2)
```
<re.Match object; span=(0, 1), match='1'>

```python
re.match(r'[0-9a-z]', s1)
```

```python
re.match(r'[0-9a-z]', s4)
```
<re.Match object; span=(0, 1), match='t'>

```python
s5 = "1aabc"
```

```python
re.match('\d[a-z]', s5)
```
<re.Match object; span=(0, 2), match='1a'>

```python
re.match(r'[ABCDE]', s3)
```
<re.Match object; span=(0, 1), match='A'>

#### 3.2 匹配次数

| 方法/项 | 说明 |
|---|---|
| 字符 | 说明 |
| * | 匹配前一个内容0次或者无限次 |
| + | 匹配前一个内容一次或者无限次 |
| ？ | 匹配前一个内容一次或者0次 |
| {m} | 匹配前一个内容m次 |
| {m,n} | 匹配前一个内容m到n次 |
| *？，+？，{m,n}？ | 将贪婪匹配变成非贪婪匹配，尽可能少匹配 |
需求：

1. 字符串开头以小写字符+数字或数字开头；
2. 判断100以内的有效数字字符串；
3. 有效的QQ号，长度6到15位；

```python
s1 = "c"
re.match(r'A*', s1)
```
<re.Match object; span=(0, 0), match=''>

```python
s2 = "AAc"
re.match(r'A+', s2)
```
<re.Match object; span=(0, 2), match='AA'>

```python
s3 = 'ab'
re.match(r'\d?', s3)
```
<re.Match object; span=(0, 0), match=''>

```python
s4 = "AAC"
re.match(r'A*?', s4)
```
<re.Match object; span=(0, 0), match=''>

```python
s4 = "AAC"
re.match(r'A+?', s4)
```
<re.Match object; span=(0, 1), match='A'>

```python
s5 = "123456abc"
re.match(r'\d{3,5}', s5)
```
<re.Match object; span=(0, 5), match='12345'>

```python
s6 = "my age is 10cm"
ma = re.search(r'\d+', s6)
```

```python
ma.group()
```
'10'

```python
#字符串开头以小写字符+数字
#或数字开头
s7 = 'a1abc'
re.match(r'[a-z]?\d', s7)
```
<re.Match object; span=(0, 2), match='a1'>

```python
#判断100以内的有效数字字符串；0-99
s8 = '10'
re.match(r'[1-9]?\d$', s8)
```

```python
s9 = '123458888888'
re.match(r'\d{5,9}', s9)
```

#### 3.3 边界匹配

| 方法/项 | 说明 |
|---|---|
| 字符 | 说明 |
| ^ | 匹配开头 |
| $ | 匹配结尾 |
| \A | 仅匹配文本的开头 |
| \Z | 仅匹配文本的结尾 |
| \b | 匹配单词边界([a-zA-Z]之间) |
| \B | 非单词匹配([^\b]之间) |
需求：

1. 匹配有效的邮箱，邮箱格式：邮箱名：由数字，字母，下划线组成,长度6~15，后缀：@xxx.com；
2. 找到以t结尾的单词；
3. 找到以t开头的单词；

```python
mail = 'testbcd@qq.com'
re.match(r'[\da-zA-Z_]{6,15}@qq.com$', mail)
```
<re.Match object; span=(0, 14), match='testbcd@qq.com'>

```python
s = "where what hat the this that thtot"
```

```python
re.findall(r'\w+?t\b',s)
```
['what', 'hat', 'that', 'thtot']

```python
re.findall(r't\w+?\b',s)
```
['the', 'this', 'that', 'thtot']

```python
s1 = 'AAAAAA'
re.match(r'A+$', s1)
```
<re.Match object; span=(0, 6), match='AAAAAA'>

```python
s1 = 'AAAAAA'
re.search(r'^A+$', s1)
```
<re.Match object; span=(0, 6), match='AAAAAA'>

```python
s = "where what hat the this that"
re.findall(r'\w*?t\b', s)
```

#### 3.4 分组匹配

| 方法/项 | 说明 |
|---|---|
| 字符 | 说明 |
| | | 匹配左右任意一个表达式 |
| 字符 | 说明 |
| （…） | 分组 |
(?P<name> ) 分组起一个别名

\num 引用编号为num的分组

(?P=name) 引用别名为name的分组

需求：

1. 匹配100内的有效数字字符串(0~99)；
2. 给定字符串："apple:8, pear:20, banana:10"，提取文本与数字;
3. 提取html文本中所有的url;
4. 文本开头与结尾为相同的数字；

```python
snum = '100'
re.match(r'\d$|[1-9]\d$', snum)
```

```python
items = ["01", "100", "10", "9", "99"]
re_cmp = re.compile(r"^\d$|[1-9]\d$")
item = "99"
for item in items:
ma = re_cmp.match(item)
print(ma)
```
None
None
<re.Match object; span=(0, 2), match='10'>
<re.Match object; span=(0, 1), match='9'>
<re.Match object; span=(0, 2), match='99'>

```python
s = "apple:8, pear:20, banana:10"
```

```python
re.findall(r'([a-z]+):(\d+)', s)
```
[('apple', '8'), ('pear', '20'), ('banana', '10')]

```python
html = """<a href="https://movie.douban.com/subject/6786002/"><img width="100" alt="触不可及" src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p1454261925.webp" class=""></a>""
```

```python
re.findall(r'"(https:.*?)"', html)
```
['https://movie.douban.com/subject/6786002/',
'https://img9.doubanio.com/view/photo/s_ratio_poster/public/p1454261925.webp']

```python
html = """<a href="https://movie.douban.com/subject/6786002/"><img width="100" alt="触不可及" src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p1454261925.webp" class=""></a>""
re.findall(r'"(https:.*?)"', html)
```

```python
text = '1021'
re.match(r'(\d).*?(\1)$', text)
```
<re.Match object; span=(0, 4), match='1021'>

```python
#使用分组索引
texts = ['101', "2223", '1omyhat', '5abc6']
text = '101'
re.match(r'(\d).*?(\1)', text)
```

```python
#使用别名
text = "1234541"
ma = re.match(r'(?P<start>.*).*?(?P=start)', text)
ma.groupdict()
```
{'start': '1'}

```python
ma.groups()
```
('1',)

#### 4 split与sub方法

#### 4.1 split-切分

split:按照规则对文本切分，返回列表；
需求：

1. 给定英文句子，统计单词的数量；
2. 给定文本，将"python/c\C++/Java/Php/Nodejs",切分成编程语言列表；

```python
import re
s = "When someone walk out your life, let them. They are just making more room for someone else better to walk in."
```

```python
words = re.split(r'\W', s)
words = [word for word in words if word.strip()]
```

```python
len(words)
```
21

```python
s = "python/c\C++/Java/Php/Nodejs"
```

```python
re.split(r'[/\\]', s)
```
['python', 'c', 'C++', 'Java', 'Php', 'Nodejs']

```python
import re
s = "When someone walk out your life, let them. They are just making more room for someone else better to walk in."
words = re.split(r'\W', s)
words = [wd for wd in words if wd.strip()]
len(words)
```

```python
s = "python/c\C++/Java/Php/Nodejs"
re.split(r"[/\\]", s)
```

#### 4.2 sub-替换

函数原型：

re.sub(pattern, repl, string, count=0, flags=0)

主要参数：

pattern：匹配内容；
repl：替换值，字符串或者函数，若为函数，替换为函数的返回字符串；
string：替换字符串；

需求：

1. 将所有的数字替换成4个*;
2. 给定绩效文本，大于等于6，替换为"A", 否则替换为"B";
3. 给定多个运动员三次运动成绩，只保留最大值；

```python
s1 = "name:sun, pwd:123456, name:zhang,pwd:667788"
re.sub(r'\d+', "****", s1)
```
'name:sun, pwd:****, name:zhang,pwd:****'

```python
def replace_ab(ma):
value = ma.group()
value = int(value)
if value >= 6:
return "A"
return "B"
s2 = "sun:5, li:10, zhao:7, gao:8, wang:5"
re.sub(r'\d+', replace_ab, s2)
```
'sun:B, li:A, zhao:A, gao:A, wang:B'

```python
def replace_max(ma):
value = ma.group()
values = value.split(',')
values = [float(value) for value in values if value.strip()]
max_val = max(values)
return str(max_val)
s3 = "谷爱凌:9.8,9.7,9.6,高梨沙罗:9.88,9.6,9.7"
re.sub(r'[\d,\.]+', replace_max, s3)
```
'谷爱凌:9.8高梨沙罗:9.88'

#### 5 练习

#### 5.1 匹配xml

xml语法：

<tag>内容</tag>

```python
s = '<li>tushu</li>'
```

```python
re.match(r'<(.*?)>.+?</\1>', s)
```
<re.Match object; span=(0, 14), match='<li>tushu</li>'>

```python
ma = re.match(r'<(?P<tag>.*?)>.+?</(?P=tag)>', s)
```

```python
ma.groups()
```
('li',)

```python
ma.groupdict()
```
{'tag': 'li'}

```python
s = '<li>xxx</li>'
re.match(r'<([\w]+)>.+</\1>', s)
```

```python
s = '<li>xxx</div>'
re.match(r'<(?P<tag>[\w]+)>.+</(?P=tag)>', s)
```

#### 5.2 提取src链接地址

```python
html = '<img class="main_img" data-imgurl="https://ss0.bdstatic.com/0.jpg" src="https://ss0.bdstatic.com/=0.jpg" style="background-color: rgb(182, 173, 173); width: 263px; height: 164.495px;"
```

```python
re.findall(r'src="(http.*?)"', html)
```
['https://ss0.bdstatic.com/=0.jpg']

```python
html = '<img class="main_img" data-imgurl="https://ss0.bdstatic.com/0.jpg" src="https://ss0.bdstatic.com/=0.jpg" style="background-color: rgb(182, 173, 173); width: 263px; height: 164.495px;"
ma = re.search(r'src="(.+?)"', html)
ma.groups()
```

#### 5.3 统计th开头单词个数

```python
s = 'that this,theme father/this teeth'
```

```python
re.findall(r'\bth[a-zA-Z]*?\b', s)
```
['that', 'this', 'theme', 'this']

#### 5.4 提取所有数字

```python
info = 'apple:21, banana:8, pear:7'
```

```python
result = re.findall(r'\d+', info)
```

#### 5.5 统计单词数量

```python
info = 'This is the tenth volume of the History of the Reformation of the Sixteenth Century, and the fifth of the Second Series. The first series described the history of that great epoch fro
```

```python
len(re.split(r'[\W]+', info))
```
35

#### 5.6 不及格成绩替换为xx

```python
scores = '90,100,66,77,33,80,27'
```

```python
def replace_faild(ma):
values = ma.group()
v = int(values)
if v < 60:
return 'xx'
return values
```

```python
re.sub(r'\d+', replace_faild, scores)
```
'90,100,66,77,xx,80,xx'

#### 5.7 匹配有效的163邮箱

规则：邮箱以字母开头，由下划线，数字，字母组成，长度8~13，并以@163.com结尾；

```python
mail = 'qimao1234@163.com'
```

```python
re.match(r'[a-zA-Z][_\da-zA-Z]{7,12}@163\.com$', mail)
```

#### 5.8 re.I

统计th开头单词，不区分大小写

```python
s = 'This that the who'
```

```python
re.findall(r'th[a-zA-Z]*', s, flags= re.I)
```
['This', 'that', 'the']

```python
re.findall(r'th[a-zA-Z]*', s)
```
['that', 'the']

#### 5.9 re.M

多行匹配，统计代码中函数数量

```python
code = '''
def func1():
pass
Def func2():
pass
class t:
def func():
pass
'''
```

```python
re.findall(r'^def ', code, flags= re.M)
```
['def ', 'Def ']
## 第六部分 错误和异常
### 26. 错误和异常
#### 1 主要内容  
目标： 
1. 理解错误与异常，掌握常见的异常，能够根据异常定位问题； 
2. 掌握异常处理方式，使程序更加健壮； 
2. 错误与异常  
错误： 
1. 语法错误， Python 解释器会进行提示； 
2. 逻辑错误，程序运行结果与预期不一致，需要自己排查； 
异常： 
常见异常： 
1. 程序运行出错， Python 解释器进行提示，定位代码位置进行修改；
2. 运行环境问题，例如：内存不足，网络错误等；

| 方法/项 | 说明 |
|---|---|
| 异常 | 说明 |
| Exception | 常规错误的基类 |
| BaseException | 所有异常的基类 |
| NameError | 变量没定义 |
| ValueError | 参数错误 |
| SyntaxError | 语法错误 |
| ImportError | 导入错误 |
| IndexError | 索引错误 |
| ZeroDivisionError | 除 0 错误 |
#### 3 异常处理  
#### 3.1 try...except  
作用：捕获指定的异常； 
基本语法： 
Exception ：指定捕获的异常类型，如果设置捕获异常与触发异常不一致，不能捕获； 
捕获多种异常： 
#### 3.2 try...finally  
作用：不管是否捕获异常，程序都会执行 finally 中的语句； 
使用场景：释放资源等； 
基本语法： 
try:
try_suite
except Exception as e:
except_suite
try:
try_suite
except Exception1 as e:
except_suite1
except Exception2 as e:
except_suite2
try: 
try_suite
except Exception as e: 
except_suite 
finally:
pass

#### 4 raise 与 assert 语句  
raise 与 assert 语句，用于主动产生异常； 
例如： 
1. 参数检查； 
2. 程序执行中逻辑错误，主动抛出异常； 

#### 4.1 raise 语句  
raise 语句：检查程序异常，主动抛出异常； 
基本语法： 
#### 4.2 assert 语句  
assert 语句：判断表达式结果是否为真，如果不为真，抛出 AssertError 异常； 
基本语法： 
示例： 
结果： 
#### 5 自定义异常类  
异常类关系： 
raise Exception(args)
raise NameError(‘value not define’)
assert expression [,args]
def my_add(x,y):
assert isinstance(x, int),"x must be int"
assert isinstance(y, int),"y must be int"
return x + y

my_add(1,2)
my_add(1, "2")
<ipython-input-3-6601aa1270b6> in my_add(x, y)
#### 1 def my_add(x,y):
#### 2 assert isinstance(x, int),"x must be int"
----> 3     assert isinstance(y, int),"y must be int"
#### 4 return x + y
5 
AssertionError: y must be int

自定义异常类注意点： 
1. 必须继承 Exception 类 
2. 通过 raise 语句主动触发 
例如： 
结果： 
#### 6 with/as 语句  
with/as ：操作上下文管理器（ context manager ），达到自动分配且释放资源目标； 
#### 6.1 with/as 应用  
基本语法： 
注意点： context 对象必须支持上下文协议 
使用场景：打开文件，忘记关闭； 
文件操作： 
class Net404Error(Exception):
def __init__(self):
args = (" 访问连接不存在 ", "404")
super().__init__(*args)
net_error_404 = Net404Error()
raise net_error_404
Net404Error                               Traceback (most recent call last)
<ipython-input-28-42cab2dc5bcb> in <module>
#### 4 super().__init__(*args)
5 net_error_404 = Net404Error()
----> 6 raise net_error_404
Net404Error: (' 访问连接不存在 ', '404')
with context as var:
with_suite

#### 6.2 上下文管理  
上下文管理理解： 
自定义类支持上下文管理： 
结果： 

fpath = r'E:\vscode_dir\database\co2_data.csv'
with open(fpath) as f:
pass
print("f closed:", f.closed)
class TestContext:
def __enter__(self):
print("call __enter__")
return self

def __exit__(self, exc_type, exc_val, exc_tb):
print("call __exit__")

with TestContext() as tc:
print(tc)
call __enter__
<__main__.TestContext object at 0x0000021855C3EDD8>
call __exit__
## 第七部分 面向对象编程
### 27. 面向对象编程
#### 1 面向对象编程  
面向对象编程 (object-oriented programming,OOP) 是相对于面向过程的一种编程方式，面向对象将数 
据和方法看做一个整体。 
#### 1.1 面向对象编程特征  
封装 :   将具体实现隐藏，提供方法，供外部调用； 
抽象： 将一类事物的数据与行为进行提取，提取事物的共性； 
继承： 类与类之间有一种父与子的关系，子类继承父类的属性和方法； 
多态： 调用不同的子类将会产生不同的行为； 
#### 1.2 面向对象基本概念  
类 (Class):  用来描述具有相同的属性和方法的对象的集合，定义类对象公共的属性和方法； 
对象： ，通过类定义的数据结构实例。对象包括两个数据成员和方法。 
实例化： 创建一个类的实例，类的具体对象。 
类属性： 类中定义变量，属于公共属性，所有对象均可访问； 
实例属性： 具体实例对象的相关的数据； 
方法： 类中定义的函数。 
继承： 即一个派生类（ derived class ）继承基类（ base class ）的字段和方法。 
子类： B 继承 A ，则称 B 为 A 的子类； 
重载： 子类中重新实现父类方法； 
#### 1.3 快速理解面向对象  
一个例子：公司有 N 名员工，每个员工有不同的行为与属性，如何对其进行管理？ 
不用面向对象：使用字典，列表等数据结构对员工信息进行管理； 
使用面向对象：将员工按照部门，职位抽象成不同类，使用对象进行统计管理； 
#### 2 类与实例  
#### 2.1 类与实例  
类与对象概念： 
1. 类是抽象概念，对象具体存在的实例； 
2.Python 中类也是对象； 
3. 类与实例引入命名空间与作用域； 
python 中定义类语法： 
例如：定义汽车类 
class 类名：
pass
class Car:
pass

创建类对象 
#### 2.2. 类属性与实例属性  
目标： 
1. 属性与方法使用 
2. 类与实例引入作用域 
实例与类的属性与方法的使用： 
例如： 
结果： 

类与实例有自己命名空间与作用域，如下代码： 
结果： 
car = Car()
实例 . 属性
实例 . 方法
类名 . 属性
类名 . 方法
class Car:
name = " 汽车 "
audi = Car()
print("Car.name:", Car.name)
print("audi.name:", audi.name)
Car.name: 汽车
audi.name: 汽车
class Car:
name = " 汽车 "
audi = Car()
audi.name = "A6"
bwm = Car()
Car.name = " 汽车类 "
print("Car.name:", Car.name)
print("audi.name:", audi.name)
print("bwm.name:", bwm.name)
Car.name: 汽车类
audi.name: A6
bwm.name: 汽车类

类属性与实例属性理解 
1.audi.name = "A6" 作用：为 audi 对象增加 “name” 属性，并没有修改类 Car 的 “name” 属性； 
2.bwm 对象继承 Car 类 name 属性，当访问 “name” 属性时，获取 Car 类中的 name 属性； 
注意：实际工作中，不推荐直接访问与修改属性，而是通过方法进行访问； 
#### 2.3 私有属性  
在某些场景下，不希望直接通过类或者实例直接访问属性，例如：员工薪资，明星年龄，收入等； 
解决方式：属性以双下划线开头 "__" ，该属性只能通过接口进行访问与修改 ;
例如： 
结果： 
#### 3 方法  
主要内容： 
1. 实例方法； 
2. 理解 self;
3. 类的定义与实现； 
#### 3.1 封装  
面向对象编程中，封装基本理解： 
1. 不推荐直接去访问实例或者类属性，而是通过方法 ( 接口 ) 去访问； 
2. 将行为封装成方法，对外提供接口调用； 
3. 在方法中，可以访问或者修改属性值； 

class Car:
name = "car"
__price = "unkown"
print(Car.__price)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
AttributeError: type object 'Car' has no attribute '__price'

#### 3.2 实例方法  
基本语法： 
需求： 
1. 为 Car 类添加方法，获取与设置 name 属性； 
2. 为 Car 类添加启动，停止方法； 
代码实现： 
#### 3.3 理解 self  
实例方法的第一参数为 self, self 即实例本身，例如： 
结果： 
#### 3.4 类定义过程  
基本思路： 
1. 定义类名； 
2. 找到共同行为与数据； 
3. 定义方法； 
4. 实现每一个方法； 
class ClassName:
def func(self, *args, **kwargs):
pass
class Car:
name = "Car"
def set_name(self, name):
pass
def get_name(self, name):
pass
def start(self):
pass
def stop(self):
pass
class Car:
name = "Car"
def stop(self):
print("id(self):", id(self))

audi = Car()
print("audi:", id(audi))
audi.stop()
audi: 2510193013576
id(self): 2510193013576

5. 调试； 
汽车类定义，共同行为： 
#### 3.5 实例方法实现  
实现 set_name 与 get_name 方法： 
结果： 
#### 4 生命周期相关三个方法  
实例的生命周期： 
class Car:
name = "car"

def set_name(self, name):
print("set name:", name)
self.name = name

def get_name(self):
return self.name

audi = Car()
audi.set_name("audi")
car_name = audi.get_name()
print("car_name:", car_name)
set name: audi
car_name: audi

#### 4.1 __new__方法  
基本语法： 
主要参数： 
1.cls: 类本身； 
2.*args, **kwargs ：参数； 
3.object.__new__(cls) ：调用父类创建对象； 
注意： 
1. 在自定义类中，不显示定义 new 方法，默认调用父类中 new 方法，并返回实例； 
2. 一般来说，很少用到该方法； 

#### 4.2 __init__方法  
__init__方法：创建实例后调用的第一个方法，用于初始化实例属性； 
在创建类中，会经常加一些参数，这些参数在 init 方法中处理，例如： 
需求： 
1. 为 Car 类添加 init 方法， 
2. 并在创建实例时，指定名称与价格： 
class ClassName:
def __new__(cls, *args, **kwargs):
return object.__new__(cls)
from collections import defaultdict
obj = defaultdict(int)
obj["level1"] += 1
class Car:
def __new__(cls, *args, **kwargs):
print("call new:", args)
return object.__new__(cls)

def __init__(self, name, price):

结果： 
#### 4.3 __del__方法  
__del__: 对象销毁调用，主要用于回收清理占用的资源；对于开发人员来说，用到场景较少； 
#### 4.4 对象生命周期流程  
结果： 
#### 5 三种方法  
#### 5.1 三种方法说明  
python 中类中方法类型：实例方法，静态方法，类方法，如下图： 
''' 属性初始化 '''
print(f"name={name}, price={price}")
self.name = name
self.speed = 0
self.__price = price

audi = Car("audi_A6", 36.5)
bmw = Car("BMW_X1", 24.2)
call new: ('audi_A6', 36.5)
name=audi_A6, price=36.5
call new: ('BMW_X1', 24.2)
name=BMW_X1, price=24.2
class Car:
def __new__(cls, *args, **kwargs):
print("call new:")
return object.__new__(cls)

def __init__(self, name, price):
''' 属性初始化 '''
print("call init")
pass
def __del__(self):
print("call del")

audi = Car("audi_A6", 36.5)
del audi
call new:
call init
call del

#### 5.2 三种方法使用场景  
1. 实例方法：只有类的对象才能使用，最常见； 
2. 静态方法：一般用于和类对象以及实例对象无关的代码； 
3. 类方法：方法中只涉及对类属性访问与修改，可以使用类方法； 
#### 5.3 收银台结算案例  
场景描述： 
场景理解： 
1. 所有收银台的打折信息相同，可以通过接口进行设置； 
2. 每个收银台收款不同； 
4. 每个收银台都有一样的提示语； 
收银台行为： 
1. 设置打折信息； 
2. 扫码添加商品，记录每位顾客商品金额； 
3. 根据商品金额与打折信息计算支付金额；

4. 支付完成后，记录金额清空，并进行提示； 
实现思路： 
1. 理解需求，找出公共属性与行为； 
2. 定义类及相关方法； 
3. 实现每个方法； 
4. 调试测试每个接口； 
5. 代码优化整理； 

类定义： 
类实现： 
class CheckOutCounter:
# 折扣默认为 1
discount = 1

def __init__(self):
# 默认结算金额 0
self.amount = 0

def scan_good(self, value, *args):
# 扫码添加商品
pass

def pay(self):
# 计算支付金额
pass

@classmethod
def set_discount(cls, discount):
# 设置折扣
pass

@classmethod
def get_discount(cls):
# 设置折扣
pass

@staticmethod
def voice_tip():
# 支付完提示
pass
class CheckOutCounter:
# 折扣默认为 1
discount = 1

def __init__(self):
# 默认结算金额 0
self.amount = 0

调用过程： 
结果： 
#### 6 property 使用  
#### 6.1 属性设置与访问  
实际工作中，需要对属性进行频繁的修改与访问，一般实现方式： 
def scan_good(self, value, *args):
# 扫码添加商品
self.amount += value
self.amount += sum(args)

def pay(self):
res = self.amount * self.discount
self.amount = 0
return res

@classmethod
def set_discount(cls, discount):
# 设置折扣
cls.discount = discount

@classmethod
def get_discount(cls):
# 设置折扣
return cls.discount

@staticmethod
def voice_tip():
| 方法/项 | 说明 |
|---|---|
| # | 支付完提示 |
| print(" | 欢迎再来，购物愉快 ") |
| # | 创建收银台对象 |
checkout_1 = CheckOutCounter()
# 扫码添加商品
checkout_1.scan_good(10)
# 设置折扣
CheckOutCounter.set_discount(0.8)
# 支付
payment = checkout_1.pay()
print(" 支付金额： ", payment)
# 提示下次再来
CheckOutCounter.voice_tip()
支付金额：  8.0
欢迎再来，购物愉快
class Car:
def __init__(self, price):
self.__price = price

def set_price(self, price):

问题：如果属性过多，有没有一种方式： 
1. 使用属性方式进行操作； 
2. 实际操作使用方法； 
#### 6.2 property 应用  
@property ：是用来修饰方法的装饰器，主要作用：将方法转成属性，例如： 
结果：当前汽车价格：  8
#### 7 反射相关函数  
#### 7.1 反射基本概念  
反射基本概念：程序可以访问、检测和修改它本身状态或行为的一种能力（自省） 
python 面向对象中的反射：通过字符串的形式操作对象相关的属性与方法； 
场景：要访问对象的属性或者使用其方法，判断是否存在； 
self.__price = price

def get_price(self):
return self.__price

car = Car(10)
car.set_price(9)
cur_price = car.get_price()
print(" 当前汽车价格： ", cur_price)
class Car_1:
def __init__(self, price):
self.__price = price

# 使用 @property 将获取 price 方法转为属性
@property
def price(self):
return self.__price

# 将 price.setter 将设置价格方法转为属性
@price.setter
def price(self, price):
self.__price = price

car = Car_1(10)
# 以属性方式设置价格
car.price = 8
# 以属性方式访问价格
price = car.price
| 方法/项 | 说明 |
|---|---|
| print(" | 当前汽车价格： ",car.price) |
| 函数 | 说明 |
| isinstance(obj, class_or_tuple) | 判断 obj 对象是否是指定类的实例 |
| dir(object) | 获取对象属性 |
hasattr(obj, name ） obj 对象是否有 name 属性 
| 方法/项 | 说明 |
|---|---|
| getattr(object, name[, default]) | 获取 obj 对象 name 属性 |
| setattr(obj, name, value) | 设置 obj 对象的 name 属性与值 |
| delattr(obj, name) | 删除 obj 对象的 name 属性 |
#### 7.2 反射相关函数与应用  
相关函数： 
定义 circle 类： 
问题： 
1. 不知道当前是否设置半径 r
2. 不知道是否有计算面积方法 
3. 如果不存在需要动态添加 
实现： 
结果：圆面积：  314.0
class Circle:
pi = 3.14
class Circle:
pi = 3.14

c = Circle()
# 定义面积计算函数
def count_area_func(self):
return self.pi * pow(self.r, 2)
r_name = "r"
r_value = 10
key_map = {"r":10, "count_area":count_area_func}
for attr, value in key_map.items():
# 若 cirle 中不存在 attr 值，设置 attr=value
if not hasattr(c, attr):
setattr(c, attr, value)

# 动态获取 c 中的 count_area 方法
count_area = getattr(c, "count_area")
# 计算 Circle 对象的面积
area = count_area(c)
print(" 圆面积： ",area)

#### 8 继承  
继承：子类自动继承父类的属性与方法，在 Python 中，自定义类继承于 object 类； 
继承优缺点： 
优点：提高代码复用与维护性，例如： Django ， Scrapy ， PyQt 等框架都需要使用继承； 
缺点：提升代码的耦合性 
#### 8.1 基本语法  
语法： 
例如： 
#### 8.2 一个例子：学生类  
需求：定义 Preson 与 Student 类，关系如下： 
代码实现： 
class SubClass(Parent1, Parent2,.....):
pass
class Parent:
pass
class SubClass(Parent):
pass
# 定义 Person 类
class Person:
def __init__(self, name, age):
print("in Person call init")
self.__name = name
self.__age = age

def get_name(self):
return self.__name

结果： 
#### 8.3 super 关键字  
子类中重载父类方法，子类中调用父类方法： 
例如： 
结果： 

def set_age(self, age):
self.__age = age

def work(self, *args, **kwargs):
print("in Person.work")

# 学生类继承 Person 类
class student(Person):
# 重载 work 方法
def work(self, subject):
print("I'm studying %s now"%subject)

s1 = student('sun', 16)
print("s1 name:", s1.get_name())
s1.work("math")
in Person call init
s1 name: sun
I'm studying math now
super().func()
# 学生类继承 Person 类
class student(Person):
#student 中重新实现 __new__ 方法，需要调用父类 __new__ 方法
def __new__(cls, *args, **kwargs):
# 调用父类 __new__ 方法
return super().__new__(cls)

def work(self, subject):
# 调用父类 work 方法
super().work()
print("I'm studying %s now"%subject)

s1 = student('sun', 16)
print("s1 name:", s1.get_name())
s1.work("math")
in Person call init
s1 name: sun
in Peron.work
I'm studying math now

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| __str__ | 返回字符串，内容为类的描述，主要对用户进行展示 |
| __repr__ | 返回字符串，主要针对开发人员展示 |
#### 8.4 多重继承  
Python 中，支持多重继承，一个子类继承多个父类，例如： 
输出结果： in A test
问题：子类如何查找父类方法？ 
MRO(Method Resolution Order) ：方法解析顺序 
python 中查找规则：广度优先，左边优先；将超找顺序记录到 mro 中； 
结果： 
分析：当执行 c.test() ，查找顺序： C ， A ， B ， object;

#### 9 特殊方法  
目标： 
1. 自定义 print 内容 
2. 自定义类支持运算符； 
#### 9.1 __str__与 __repr__  
对比：使用 print 输出自定义类与 list 类对象，比较不同； 
问题：如何输出自定义格式？ 
需要在类中添加下面两个方法： 
例如，在 jupyer 中 , 定义玫瑰类，主要属性：玫瑰名称与价格， 
输出结果如下： 
class A:
def test(self):
print("in A test")
class B:
def test(self):
print("in B test")
class C(A, B):
pass
c = C()
c.test()
C.mro()
[__main__.C, __main__.A, __main__.B, object]

#### 9.2 自定义输出  
需求：使用 print 打印，输出名称与价格； 
实现： 
结果： name: 黑玫瑰  price:20.00
#### 9.3 支持运算符  
算数运算符： 
class Rose:
def __init__(self, name, price):
self.name = name
self.price = price

def __str__(self):
# 自定义 __str__ 方法
return "name:%s price:%.2f"%(self.name, self.price)


def __repr__(self):
return "name:%s price:%.2f object at 0x%016X"%(self.name, self.price, 
id(self))

rose = Rose(" 黑玫瑰 ", 20)
print(rose)

方法 说明 
__add__（ self, other ） 加法 
__sub __（ self, other ） 减法 
__mul __（ self, other ） 乘法 
__truediv __（ self, other ） 除法 
__mode __（ self, other ） 取模 
__pow __（ self, other ） 幂运算 
方法 说明 
__lt__ <
__le__ <=
__gt__ >
__ge__ >=
__eq__ ==
__ne__ !=
比较运算符： 
需求： Rose 类支持根据价格进行比较 


#### 10 类组合与练习  
类组合： A 类的对象作为 B 类数据属性； 
适用场景：类之间有显著不同，一个类是另一个类的组件，推荐使用组合； 
例如：团队与成员，

#### 10.1 学生管理系统  
需求：班级管理系统，通过班级管理学生 
1. 班级中有多名同学； 
2. 学生信息包括：学号，姓名，身高，出生年月 
3. 班级对外提供管理接口：插入学生，根据条件删除学生，根据条件查询学生信息； 
4. 班级类提供友好的菜单进行操作； 
#### 10.2 学生类与班级类  

#### 10.4 实现过程  
1. 定义 Student 类，并实现相关方法； 
2. 实现 Team 类，并实现相关方法； 
3. 通过 Team 类管理 Student 类； 
4. 代码调试； 

#### 10.5 菜单操作  







#### 1 ：友好的提示；
#### 2 ：输入 q/Q: 退出；
#### 3 ：输入 a/A: 创建并添加学生；
#### 4 ：输入 d/D: 根据输入学号删除学生；
#### 5 ：输入 f/F: 根据输入学号查找学生；
#### 6 ：输入 s/S: 显示所有学生信息；
#### 7 ：输入 c/C: 删除所有学生信息；
### 28. 面向对象基础（课上练习）
#### 1 类相关语法

#### 1.1 类与实例

```python
class Car:
pass
car = Car()
isinstance(car, Car)
```
True

#### 1.2 类属性与实例属性

#### 1.2.1 属性访问

```python
class Car:
name = "汽车"
audi = Car()
print("Car.name:", Car.name)
print("audi.name:", audi.name)
```
Car.name: 汽车
audi.name: 汽车

#### 1.2.2 理解类与对象命名空间与作用域

```python
class Car:
name = "汽车"
```

```python
audi = Car()
audi.name = "A6"
```

```python
audi.name
```
'A6'

```python
Car.name
```
'汽车'

```python
bwm = Car()
Car.name = "汽车类"
```

```python
bwm.name
```
'汽车类'

```python
Car.name
```
'汽车类'

```python
class Car:
name = "汽车"
audi = Car()
audi.name = "A6"
bwm = Car()
Car.name = "汽车类"
print("Car.name:", Car.name)
print("audi.name:", audi.name)
print("bwm.name:", bwm.name)
```
Car.name: 汽车类
audi.name: A6
bwm.name: 汽车类

#### 1.2.3 私有属性

```python
class Car:
name = "car"
__price = "unkown"
print(Car.__price)
```
---------------------------------------------------------------------------
AttributeError Traceback (most recent call last)
<ipython-input-11-5e2a166cab7c> in <module>
3 __price = "unkown"
4
----> 5 print( Car. __price)

AttributeError : type object 'Car' has no attribute '__price'

#### 2 方法

```python
class ClassName:
def func(self, * args, ** kwargs):
pass
```

#### 2.1 添加方法

```python
class Car:
name = "car"
def set_name(self, name):
pass
def get_name(self):
pass
def start(self):
pass
def stop(self):
pass
```

```python
class Car:
name = "Car"
def set_name(self, name):
pass
def get_name(self, name):
pass
def start(self):
pass
def stop(self):
pass
```

#### 2.2 理解self

```python
class Car:
name = "Car"
def stop(self):
print("id(self):", id(self))
audi = Car()
print("audi:", id(audi))
audi.stop()
```
audi: 2659570209992
id(self): 2659570209992

#### 2.3 类定义

```python
class Car:
name = "car"
def set_name(self, name):
pass
def get_name(self):
pass
def up_speed(self, value):
pass
def down_speed(self):
pass
def stop(self):
pass
```

#### 2.4 方法实现

```python
class Car:
name = "Car"
def set_name(self, name):
self.name = name
def get_name(self):
return self.name
```

```python
audi = Car()
```

```python
audi.get_name()
```
'Car'

```python
audi.set_name("Audi")
```

```python
audi.get_name()
```
'Audi'

```python
class Car:
name = "car"
def set_name(self, name):
print("set name:", name)
self.name = name
def get_name(self):
return self.name
```

```python
Car.set_name(audi, "Car")
```
set name: Car

```python
1:Car他是一个类，并没有和实例绑定，当调用set_name方法时候，第一个参数，必须给定Car的一个对象，否则报错
2:audi调用set_name的时候，只需要传一个参数，因为audid对象，第一个参数self,就是自己，所以只需要一个参数即可
```
File "<ipython-input-24-47b98828df2c>" , line 1
1:Car他是一个类，并没有和实例绑定，当调用set_name方法时候，第一个参数，必须给定Car的一个对象，否则报错
^
SyntaxError : invalid character in identifier

```python
class Car:
name = "car"
def set_name(self, name):
print("set name:", name)
self.name = name
def get_name(self):
return self.name
audi = Car()
audi.set_name("audi")
car_name = audi.get_name()
print("car_name:", car_name)
```
set name: audi
car_name: audi

#### 3 对象声明周期

#### 3.1 __new__方法

```python
class ClassName:
def __new__(cls, * args, ** kwargs):
return object.__new__(cls)
```

#### 3.2 __init__方法

```python
from collections import defaultdict
obj = defaultdict(int)
obj["level1"] += 1
```

```python
class Car:
def __new__(cls, * args, ** kwargs):
print("call __new__")
return object.__new__(cls)
def __init__(self, name, price, color):
print("call __init__")
self.name = name
self.__price = price
self.color = color
def get_car_info(self):
return f"car name={self.name}, price={self.__price}w, color={self.color}"
def __del__(self):
print("call __del__")
```

```python
audi = Car("audi", 38, "red")
```
call __new__
call __init__

```python
del audi
```
call __del__

```python
audi.get_car_info()
```
---------------------------------------------------------------------------
NameError Traceback (most recent call last)
<ipython-input-31-e0411b1696ec> in <module>
----> 1 audi. get_car_info( )

NameError : name 'audi' is not defined

```python
audi = Car("audi", 48)
```
call __new__
call __del__

---------------------------------------------------------------------------
TypeError Traceback (most recent call last)
<ipython-input-32-cf36d4a0eb62> in <module>
----> 1 audi = Car( "audi" , 48 )

TypeError : __init__() missing 1 required positional argument: 'color'

```python
class Car:
def __new__(cls, * args, ** kwargs):
print("call new:", args)
return object.__new__(cls)
def __init__(self, name, price):
'''属性初始化'''
print(f"name={name}, price={price}")
self.name = name
self.speed = 0
self.__price = price
audi = Car("audi_A6", 36.5)
bmw = Car("BMW_X1", 24.2)
```
call new: ('audi_A6', 36.5)
name=audi_A6, price=36.5
call new: ('BMW_X1', 24.2)
name=BMW_X1, price=24.2

#### 3.3 完整周期

```python
class Car:
def __new__(cls, * args, ** kwargs):
print("call new:")
return object.__new__(cls)
def __init__(self, name, price):
'''属性初始化'''
print("call init")
pass
def __del__(self):
print("call del")
audi = Car("audi_A6", 36.5)
del audi
```
call new:
call init
call del

#### 3.4 计算面积通用类

1. 圆面积
2. 正方形面积

```python
class CountArea:
pi = 3.14
@classmethod
def circular_area(cls, r):
return cls.pi * pow(r, 2)
@staticmethod
def square_area(side_length):
return side_length** 2
```

```python
CountArea.circular_area(10)
```
314.0

```python
CountArea.square_area(10)
```
100

#### 3.5 收银台案例

```python
class CheckOutCounter:
#折扣默认为1
discount = 1
def __init__(self):
#默认结算金额0
self.amount = 0
def scan_good(self, value, * args):
#扫码添加商品
pass
def pay(self):
#计算支付金额
pass
@classmethod
def set_discount(cls, discount):
#设置折扣
pass
@classmethod
def get_discount(cls):
#设置折扣
pass
@staticmethod
def voice_tip():
#支付完提示
pass
```

```python
class CheckOutCounter:
#折扣默认为1
discount = 1
def __init__(self):
#默认结算金额0
self.amount = 0
def scan_good(self, value, * args):
#扫码添加商品
self.amount += value
self.amount += sum(args)
def reset(self):
self.amount = 0
def pay(self):
res = self.amount * self.discount
return res
@classmethod
def set_discount(cls, discount):
#设置折扣
cls.discount = discount
@classmethod
def get_discount(cls):
#设置折扣
return cls.discount
@staticmethod
def voice_tip():
#支付完提示
print("欢迎再来，购物愉快")
```

```python
#创建收银台对象
checkout_1 = CheckOutCounter()
#扫码添加商品
checkout_1.scan_good(10)
#设置折扣
CheckOutCounter.set_discount(0.8)
#支付
payment = checkout_1.pay()
#复位
checkout_1.reset()
print("支付金额：", payment)
#提示下次再来
CheckOutCounter.voice_tip()
```
支付金额： 8.0
欢迎再来，购物愉快

#### 4 property

#### 4.1 一个例子

```python
class Car:
def __init__(self, price):
self.__price = price
def set_price(self, price):
self.__price = price
def get_price(self):
return self.__price
car = Car(10)
car.set_price(9)
cur_price = car.get_price()
print("当前汽车价格：", cur_price)
```
当前汽车价格： 9

#### 4.2 property应用

```python
class Car_1:
def __init__(self, price):
self.__price = price
#使用@property将获取price方法转为属性
@property
def price(self):
return self.__price
#将price.setter将设置价格方法转为属性
@price.setter
def price(self, price):
self.__price = price
car = Car_1(10)
#以属性方式设置价格
car.price = 8
#以属性方式访问价格
price = car.price
print("当前汽车价格：",car.price)
```
当前汽车价格： 8

#### 5 反射

```python
class Circle:
pi = 3.14
```

```python
c = Circle()
```

```python
hasattr(c, "pi")
```
True

```python
hasattr(c, "count_area_func")
```
False

```python
#定义面积计算函数
def count_area_func(self):
return self.pi * pow(self.r, 2)
```

```python
setattr(Circle,"count_area_func", count_area_func)
```

```python
hasattr(c, "count_area_func")
```
True

```python
hasattr(c, 'r')
```
False

```python
setattr(c, 'r', 10)
```

```python
c.count_area_func()
```
314.0

```python
class Circle:
pi = 3.14
c = Circle()
#定义面积计算函数
def count_area_func(self):
return self.pi * pow(self.r, 2)
r_name = "r"
r_value = 10
key_map = {"r":10, "count_area":count_area_func}
for attr, value in key_map.items():
#若cirle中不存在attr值，设置attr=value
if not hasattr(c, attr):
setattr(c, attr, value)
#动态获取c中的count_area方法
count_area = getattr(c, "count_area")
#计算Circle对象的面积
area = count_area(c)
print("圆面积：",area)
```
圆面积： 314.0

```python
class A:
def set_name(self, name):
print("call a set_name", name)
class B:
def setName(self, name):
print("call b setName", name)
```

```python
a = A()
b = B()
```

```python
def set_the_name(obj, name):
func_list = ["set_name", "setName"]
for func_name in func_list:
if hasattr(obj, func_name):
func = getattr(obj, func_name)
func(name)
break
```

```python
set_the_name(a, "testa")
```
call a set_name testa

```python
set_the_name(b, "testb")
```
call b setName testb
### 29. 继承与反射
#### 1 继承

#### 1.1 基本语法

```python
class Parent:
pass
class SubClass(Parent):
pass
```

```python
issubclass(SubClass, Parent)
```
True

```python
issubclass(Parent, object)
```
True

#### 1.2 一个例子

```python
#定义Person类
class Person:
def __init__(self, name, age):
print("in Person call init")
self.__name = name
self.__age = age
def get_name(self):
return self.__name
def set_age(self, age):
self.__age = age
def work(self, * args, ** kwargs):
print("in Person.work")
```

```python
class Student(Person):
def work(self, * args, ** kwargs):
super().work()
print("in Student.work")
```

```python
s = Student("xiaoming", 13)
```
in Person call init

```python
s.work()
```
in Person.work
in Student.work

```python
#定义Person类
class Person:
def __init__(self, name, age):
print("in Person call init")
self.__name = name
self.__age = age
def get_name(self):
return self.__name
def set_age(self, age):
self.__age = age
def work(self, * args, ** kwargs):
print("in Person.work")
#学生类继承Person类
class student(Person):
#重载work方法
def work(self, subject):
print("I'm studying %s now"% subject)
s1 = student('sun', 16)
print("s1 name:", s1.get_name())
s1.work("math")
```
in Person call init
s1 name: sun
I'm studying math now

#### 1.3 super关键字

```python
#学生类继承Person类
class student(Person):
def __new__(cls, * args, ** kwargs):
#调用父类__new__方法
return super().__new__(cls)
#重载work方法
def work(self, subject):
#调用父类work方法
super().work()
print("I'm studying %s now"% subject)
s1 = student('sun', 16)
print("s1 name:", s1.get_name())
s1.work("math")
```
in Person call init
s1 name: sun
in Person.work
I'm studying math now

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
c.test()
```
in A test

```python
C.mro()
```
[__main__.C, __main__.A, __main__.B, object]

#### 2 特殊方法

#### 2.1 自定义输出

```python
class Rose:
def __init__(self, name, price):
self.name = name
self.price = price
rose = Rose("黑玫瑰", 20)
```

```python
rose
```
<__main__.Rose at 0x1ca0909b5c8>

```python
print(rose)
```
<__main__.Rose object at 0x000001CA0909B5C8>

```python
l = [1,2,3]
```

```python
l
```
[1, 2, 3]

```python
print(l)
```
[1, 2, 3]

```python
class Rose:
def __init__(self, name, price):
self.name = name
self.price = price
def __str__(self):
print("call rose __str__")
return f"Rose name:{self.name}, price:{self.price}"
def __repr__(self):
print("call rose repr")
return f"Rose name:{self.name}, price:{self.price}"
def __add__(self, other):
return self.price + other.price
def __lt__(self, other):
print("call lt")
return self.price < other.price
rose1 = Rose("黑玫瑰", 20)
rose2 = Rose("红玫瑰", 15)
```

```python
rose2 < rose1
```
call lt

True

```python
print(rose)
```
<__main__.Rose object at 0x000001CA0909B5C8>

```python
rose
```
<__main__.Rose at 0x1ca0909b5c8>

```python
class Rose:
def __init__(self, name, price):
self.name = name
self.price = price
def __str__(self):
#自定义__str__方法
return "name:%s price:%.2f"% (self.name, self.price)
def __repr__(self):
return "name:%s price:%.2f object at 0x%016X"% (self.name, self.price, id(self))
rose = Rose("黑玫瑰", 20)
print(rose)
```
name:黑玫瑰 price:20.00

#### 2.2 比较运算符支持

```python
class Rose:
def __init__(self, name, price):
self.name = name
self.price = price
def __lt__(self, other):
#支持小于
return self.price < other.price
def __gt__(self, other):
#支持大于
return self.price > other.price
rose_red = Rose("rose", 10)
rose_black = Rose("rose", 15)
```
### 30. 班级练习（Jupyter）
```python
class Student:
def __init__(self, name, num) -> None :
self.__name = name
self.__num = num
def dump_info(self):
print(f"name:{self.__name}, num:{self.__num}")
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
def __init__(self, team_name, team_id) -> None :
self.student_list = []
self.team_name = team_name
self.team_id = team_id
def add_student(self, student):
print("add student:", student)
self.student_list.append(student)
def find_student_by_num(self, student_num):
for student in self.student_list:
if student.num == student_num:
#print(f"find num:{student_num}", student)
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
cmd_map = {'a':"add_cmd", 'f':'find_cmd',
'd':'delete_cmd', 'c':'clear_all',
's':'dump_all'}
while True :
print(help_info)
cmd = input("输入命令:")
cmd = cmd.lower()
if cmd == 'q':
break
action = cmd_map.get(cmd)
if action:
func = getattr(self, action)
func()
# elif cmd == "a":
# self.add_cmd()
# elif cmd == "f":
# self.find_cmd()
# elif cmd == 'd':
# self.delete_cmd()
# elif cmd == 'c':
# self.clear_all()
# elif cmd == 's':
# self.dump_all()
```

```python
t1 = Team("001", 1)
```

```python
t1.menu_main()
```

输入q/Q:退出；
输入a/A:创建并添加学生；
输入d/D:根据输入学号删除学生；
输入f/F:根据输入学号查找学生；
输入s/S:显示所有学生信息；
输入c/C:删除所有学生信息；

输入命令:a
学生名称:1
学生学号:2

输入q/Q:退出；
输入a/A:创建并添加学生；
输入d/D:根据输入学号删除学生；
输入f/F:根据输入学号查找学生；
输入s/S:显示所有学生信息；
输入c/C:删除所有学生信息；

输入命令:q

```python
s2 = Student(3,3)
```

```python
t1.add_student(s2)
```
add student: name:3, num:3

```python
tmp = t1.find_student_by_num(2)
```

```python
print(tmp)
```
name:1, num:2

```python
t1.delete_student_by_num(2)
```
del num:2 name:1, num:2

```python
t1.dump_all()
```
name:3, num:3

```python
t1.clear_all()
```
## 第八部分 并发编程
### 31. 多进程详解与应用
1. 主要内容  
进程内容： 
#### 2 进程详解与应用  
进程：程序运行的实例，执行的过程，它是系统调度与资源分配基本单元； 
场景： 
1. 一个手机应用：微信，抖音，浏览器，淘宝，游戏等； 
2. 一个 PC 应用：浏览器，办公软件，游戏等； 
基本理解： 
#### 2.1 进程相关知识点  
进程的 ID ：程序运行的唯一标识； 
Python 中获取进程 ID 方式： 
Python 中进程相关模块： multiprocessing
os.getpid(): 获取当前进程 ID
os.getppid() ：获取当前父进程 ID

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| p.start() | 创建进程，执行进程函数 |
| p.run() | 使用当前继承执行进程函数 |
| p.join() | 等待进程执行完成 |
| p.is_alive() | 进程是否存活 |
#### 2.2 创建进程  
相关方法： 
Process 对象相关方法： 
#### 2.3 父子进程理解  
子进程是父进程的拷贝，子进程继承父进程的所有资源； 
# 导入模块
import multiprocessing
import os
# 定义子进程函数：
def func(*args, **kwargs):
print("subProcess pid:%d ppid:%d"%(os.getpid(), os.getppid()))
if __name__ == "__main__":
# 创建进程对象
p = multiprocessing.Process(target=func)
# 创建进程，并执行进程函数
p.start()
# 等待子进程结束
p.join()
print("main process pid:%d"%os.getpid())
multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={}, 
*, daemon=None,)
# 主要参数：
target ：进行函数
name ：进程名称
args ：参数
kwargs: 参数
daemon ：守护进程，在调用 start 之前设置，如果 daemon 设为 True ，则父进程退出后，子进程也退出
import multiprocessing
import os
import time
tmp = 10
def work():
global tmp
tmp = 100
print('work pid:', os.getpid(), os.getppid())
print("tmp in work:", tmp)

问题：最后一句代码， tmp 的输出值？ 
#### 2.4 进程应用场景  
使用场景：并行计算，某个函数执行时间过长，阻塞等； 
一个例子：某函数，执行过程中休眠 1 秒，执行 6 次，使用单进程与多进程调用，对比耗时； 

#### 2.5 进程间通信  
常用方式： 
1. 消息队列： from multiprocessing import Queue
2. 共享内存： from multiprocessing import Value,Array

消息队列方法： 
if __name__ == '__main__':
# 创建进程
p = multiprocessing.Process(target=work)
# 运行进程
p.start()
print("call main process pid:", os.getpid())
# 等待程序结束
p.join()
#tmp 的输出值
print("tmp in main:", tmp)
import multiprocessing
import os
import time
tmp = 10
def work():
print("call work")
time.sleep(1)

if __name__ == '__main__':
n = 6
plist = []
ts = time.time()
for i in range(n):
p = multiprocessing.Process(target=work)
p.start()
plist.append(p)
for i in range(n):
p.join()
print("run time:%.2f"%(time.time() - ts))

方法 说明 
msgq = Queue(maxsize=0) 创建消息队列 
| 方法/项 | 说明 |
|---|---|
| msgq.put(obj, block=True, timeout=None) | 消息入队 |
| msgq.get(block=True, timeout=None) | 消息出队 |
| msgq.qsize() | 获取消息队列中数量 |
练习：主进程中创建多个子进程，子进程收到消息 ”Q“ 退出； 
代码实现： 
#### 2.6 练习：统计代码行数  
#### 2.6.1 单进程实现  
基本实现思路： 
1. 遍历目录，找到 Python 文件； 
2. 打开文件，并统计文件行数； 
3. 统计行数； 
代码实现： 
import multiprocessing
import os
import time
from multiprocessing import Queue
def work(msgq):
while True:
msg = msgq.get()
if msg == "Q":
break
else:
print("recv msg:", msg)
if __name__ == '__main__':
msgq = Queue()
list_p = []
for i in range(1, 10):
p = multiprocessing.Process(target=work, args=(msgq,))
list_p.append(p)
p.start()
# 发送不同的消息
for i in range(1, 10):
msgq.put("Test%d"%i)
# 发出退出命令
for p in list_p:
msgq.put("Q")
# 等待进程退出
for p in list_p:
p.join()

结果： run time:0.87, code lens:350570
#### 2.6.2 多进程实现  
实现思路： 
import os
import time
from numpy import result_type
def countLine(fpath):
if fpath.endswith('.py'):
with open(fpath, encoding='utf-8') as f:
lens = len(f.readlines())
return lens
return 0
def scandir(fpath):
lens = 0
# 遍历目录
for root, subdir, flist in os.walk(fpath):
if flist:
for fname in flist:
fpath = os.path.join(root, fname)
lens += countLine(fpath)
return lens
if __name__ == '__main__':
src_dir = r'E:\vscode_dir\part_7\process\django'
total = 0
nums = 1
start_time = time.time()
for i in range(nums):
total += scandir(src_dir)
end_time = time.time()
print("run time:%.2f, code total nums:%d"%(end_time-start_time, total))

执行思路： 

代码实现： 
import multiprocessing
import os
import time
from multiprocessing import Queue

# 统计文件行数
def countLine(queue_path, queue_result):
linenum = 0
while True:
# 接受文件路径
msg = queue_path.get()
# 消息为 q 退出
if msg.lower() == "q":
break
# 消息为 Python 文件，开始统计
if msg.endswith(".py"):
try:
with open(msg, encoding="utf-8") as f:
# 统计文件行数，并进行累加
linenum += len(f.readlines())
except Exception as e:
print(msg, e)
# 退出后，将统计结果发送到消息队列
queue_result.put(linenum)

# 扫描目录
def scandir(path, queue_path):
for root, _, flist in os.walk(path):
if flist:
for fname in flist:
# 将目录添加到消息队列
fpath = os.path.join(root, fname)
queue_path.put(fpath)
if __name__ == '__main__':
src_dir = r'E:\vscode_dir\part_7\process\django'
start_time = time.time()
queue_path = Queue()
queue_result = Queue()
list_p = []
n = 10
nums = 1
start_time = time.time()
# 创建进程
for i in range(n):
p = multiprocessing.Process(target=countLine, args=(queue_path, 
queue_result))
list_p.append(p)
p.start()
# 主进程，扫描目录
for i in range(nums):
scandir(src_dir, queue_path)
# 扫描完成发送退出消息
for p in list_p:
queue_path.put('q')
# 等待子进程结束
for p in list_p:
p.join()

方法 说明 
pools = Pool(processes=None,…) 创建进程池对象 
pools.apply(func, args=(), kwds={}) 添加任务，阻塞模式 
pools.apply_async(func, args=(), kwds={}, callback=None,
error_callback=None)
非阻塞模式，  
Callback 处理 func 的返回值  
返回 AsyncResult 对象 
| 方法/项 | 说明 |
|---|---|
| pools.close() | 关闭进程池 |
| pools.join() | 等待所有任务结束 |
| AsyncResult | 通过 AsyncResult 获进程函数 |
的返回值 
结果： run time:1.04, code total nums:350570
对比：因为文件数量较少，所以单进程占优； 
修改扫描次数：将程序中的 nums 修改为 20 ，发现多进程占优； 
#### 2.7 进程池  
进程池：创建一定数量的进程，供用户调用； 
进程池类： 
主要方法： 
基本实现过程： 
使用进程池统计文件数量： 
total = 0
# 统计文件行数
for i in range(queue_result.qsize()):
total += queue_result.get()
end_time = time.time()
# 输出打印结果
print("run time:%.2f, code total nums:%d"%(end_time-start_time, total))
from multiprocessing import Pool
from multiprocessing import Pool
# 创建进程池对象，指定进程数量 3
pool = Pool(processes = 3) 
# 添加任务与参数
pool.apply_async(func, (msg, ))
| 方法/项 | 说明 |
|---|---|
| # | 停止添加 |
| pool.close()# | 停止添加 |
| # | 等待所有任务结束 |
pool.join()
from multiprocessing import Pool

import os
import time
from unittest import result
# 统计文件行数
def countLine(fpath):
linenum = 0
if fpath.endswith('.py'):
with open(fpath, encoding="utf-8") as f:
linenum = len(f.readlines())
return linenum
def sacndir(fpath, pools):
result = []
# 获取指定目录下所有文件
for root, sundir, flist in os.walk(fpath):
if flist:
for fname in flist:
# 判断是否为 .py
if fname.endswith('.py'):
# 拼接目录
path = os.path.join(root, fname)
# 进程池添加任务
r = pools.apply_async(countLine, args=(path,))
# 将结果保存到 result 中
result.append(r)
# 计算统计结果
total= sum([r.get() for r in result])
return total
if __name__ == "__main__":

total = 0
nums = 20
src_dir = r'E:\vscode_dir\part_7\process\django'
start_time = time.time()
pools = Pool(processes=10)
for i in range(nums):
total += sacndir(src_dir, pools)

# 停止添加任务
pools.close()
# 等待程序结束
pools.join()
end_time = time.time()
# 输出统计结果
print("run time:%.2f, code total nums:%d"%(end_time-start_time, total))
### 32. 多线程详解与应用
#### 1 多线程  
#### 1.1 基本概念  
线程：系统进行运算调度的最小单元，线程依赖与进程； 
多线程：在一个进程中，启动多线程并发执行任务，线程之间全局资源可以共享； 
进程与线程区别： 
1. 线程依赖于进程； 
2. 线程之间资源共享； 
3. 线程调度开销小于进程开销； 
#### 2.2 Python 中多线程限制  
GIL （ Global Interpreter Lock ）：实现 CPython （ Python 解释器）时引入的一个概念， 
| 方法/项 | 说明 |
|---|---|
| GIL | 锁：实质是一个互斥锁 (mutex); |
| GIL | 作用：防止多个线程同时去执行字节码，降低执行效率； |
| GIL | 问题：在多核 CPU 中， Python 的多线程无法发挥其作用，降低任务执行效率； |
执行过程对比如下图： 
#### 2 多线程相关模块与应用  
#### 2.1 创建线程  
python 中创建线程过程： 
import threading
# 线程函数
def thread_func(*args, **kwargs):
print("in thread func")
def main():
# 创建线程对象
t = threading.Thread(target=thread_func, args=())
# 创建线程，启动线程函数
t.start()
print("in main func")

| 方法/项 | 说明 |
|---|---|
| threading | 相关方法 说明 |
| threading.active_count() | 返回当前活动的线程数量 |
| threading.current_thread() | 获取当前的线程对象 |
threading.get_ident( ） 获取当前的线程 ID
threading.Thread(group=None, target=None ， ...... ） 创建线程对象 
方法 说明 
t=Thread( group=None, target=None, name=None, args=(),
kwargs=None, daemon=None) 创建线程 
t.start() 创建进程运行线 
程函数 
t.run() 运行线程函数 
t. setDaemon( daemonic) 设置 daemon 线 
程 
t. is_alive() 线程是否 alive
t. join( timeout=None) 等待线程退出 
t.daemon 是否是 daemon
线程 
t. getName() 获取线程名称 
t.ident 获取线程 ID
#### 2.2 线程相关方法  
导入模块 
threading 模块相关方法： 
Thread 对象相关方法 
注意：只有 Thread 对象调用 start 方法后，才能调用 join 方法等待； 
# 等待线程结束
t.join()
if __name__ == "__main__":
main()
import threading

#### 2.3 多线程应用  
需求：定义线程函数，每个线程函数休眠 1 秒钟，查看执行过程； 
结果： 
从输出结果中可以看到： 
1. 线程之间执行是随机的； 
2. 线程之间资源共享 (g_value 的值发生变化 ) ； 
import threading
import time
g_value = 1
# 线程函数
def thread_func(*args, **kwargs):
global g_value
g_value += 1
# 休眠 1 秒
time.sleep(1)
# 获取线程 ID
ident = threading.get_ident()
# 获取当前线程
t = threading.current_thread()
# 获取线程名称与 ident
print("name:%s ident:%d"%(t.getName(), t.ident))
def main():
thread_num = 5
thread_list = []
# 创建线程对象
for i in range(thread_num):
name = "thread_%d"%i
t = threading.Thread(name=name, target=thread_func, args=())
thread_list.append(t)
t.start()
# 等待线程结束
for t in thread_list:
t.join()
if __name__ == "__main__":
main()
print("g_value:", g_value)
name:thread_1 ident:71056
name:thread_4 ident:69808
name:thread_0 ident:69940
name:thread_3 ident:38832
name:thread_2 ident:71100
g_value: 6

方法 说明 
lock = threading.Lock() 创建锁 
lock.acquire(blocking=True, timeout=-1) 申请锁 
lock.release() 释放锁 
#### 2.4 全局变量操作问题  
需求： 
1. 定义变量 a=10000 ， 
2. 主线程对变量进行加 1 操作，执行 50W 次； 
3. 创建子线程，同时对变量进行减 1 操作，执行 50W 次； 
4. 最后查看该变量的值 
代码实现： 
结果： g_value=239973 ，说明： g_value 是一个随机值； 
问题分析： AB 两个线程同时对一个变量进行操作，产生线程安全问题； 
解决方式：引入锁机制 
#### 2.5 同步机制  
引入锁机制： threading.Lock()  
from threading import Thread
g_value = 10000
nums = 500000
def sub_func():
# 减 1 操作
global g_value
for i in range(nums):
g_value -= 1
def add_func():
# 加 1 操作
global g_value
for i in range(nums):
g_value += 1
if __name__ == "__main__":
# 创建线程对象
t = Thread(target=sub_func, name='test')
# 创建线程运行程序
t.start()
add_func()
# 等待线程执行完成
t.join()
print(f'g_value={g_value}')

使用原理：对于公共资源进行保护，只有获取锁之后，才能对公共资源进行修改访问； 
修改后代码： 
注意点：同一线程中，避免获取锁之后，再次获取所，这样造成死锁； 
#### 2.6 线程之间通信方式  
消息队列： 
使用方式： 
from threading import Thread
from threading import Lock
g_value = 10000
nums = 500000
lock = Lock()
def sub_func():
# 减 1 操作
global g_value
for i in range(nums):
# 修改 g_value 前，需要获取锁
lock.acquire()
g_value -= 1
# 修改完成后释放锁
lock.release()
def add_func():
# 加 1 操作
global g_value
for i in range(nums):
# 修改 g_value 前，需要获取锁
lock.acquire()
g_value += 1
# 修改完成后释放锁
lock.release()
if __name__ == "__main__":
# 创建线程对象
t = Thread(target=sub_func, name='test')
# 创建线程运行程序
t.start()
add_func()
# 等待线程执行完成
t.join()
print(f'g_value={g_value}')
from queue import Queue

方法 说明 
msgq = Queue(maxsize=0) 创建消息队列 
| 方法/项 | 说明 |
|---|---|
| msgq.put(item, block=True, timeout=None) | 存入消息 |
| msgq.get(block=True, timeout=None) | 获取消息 |
| msgq.empty() | 判断消息队列是否为空 |
| msgq.full() | 判断消息队列是写满 |
## 第九部分 数据库
### 33. MySQL 数据库操作
#### 1 准备工作

#### 1.1 Mysql准备：

1. 安装mysql服务；
2. 熟悉常用的sql语句；

#### 1.2 mysql相关模块

推荐pymysql 安装方式：

pip install pymysql

#### 2 pymysql模详解与应用

#### 2.1 操作流程：

1. 连接数据库；
2. 创建游标；
3. 执行sql语句：增删改查；
4. 提交；
5. 关闭数据库；

#### 2.2 pymysql相关方法：

方法 说明

db=pymysql.connect(args, *kwargs)连接数据库，参数:地址，用户名，密码，数据库名称

cursor = db.cursor(cursor=None) 创建游标

| 方法/项 | 说明 |
|---|---|
| cursor.execute(query, args=None) | 执行sql语句：查询，删除，更新，插入等操作 |
| cursor.executemany(query, args) | 批量执行：一次插入多条数据 |
| cursor.fetchall() | 读取所有数据 |
| cursor.fetchmany(size=None) | 读取指定数量数据 |
| cursor.fetchone() | 获取一条数据 |
| db.commit() | 提交修改 |
| db.close() | 关闭数据库 |
#### 2.3 连接数据库

方式1：

```python
import pymysql
#链a接数据库
db = pymysql.connect(host = "localhost",user= "root",password = "abc123",database= "TESTDB")
```

方式2：

```python
config = {
'user':'root', #用户名
'password':'abc123', #密码
'host':'localhost', #mysql服务地址
'port':3306, #端口,默认3306
'database':'TESTDB' #数据库名字，testdb
}
db = pymysql.connect(** config)
```

#### 2.4 获取游标

```python
#获取cursor
cursor = db.cursor()
```

#### 2.5 执行sql语句

```python
#查看表名
f = cursor.execute("show tables;")
```

```python
#读取所有数据
data = cursor.fetchall()
#输出数据
for item in data:
print(item)
```
('u1',)
('user_info',)

#### 2.6 插入数据

```python
#执行sql语句,插入一条数据
sql = 'insert into user_info (user_name, user_id, channel) values(%s,%s,%s)'
#插入一条数据
cursor.execute(sql, ('何同学', "10001", "B站"))
#插入多条数据
cursor.executemany(sql, [('张同学', "10002", "抖音"),('奇猫', "10003", "抖音")])
db.commit()
```

#### 2.7 查询数据

```python
sql = 'select * from user_info'
cursor.execute(sql)
#读取所有数据
data = cursor.fetchall()
#打印数据
for item in data:
print(item)
```

#### 2.8 关闭连接

```python
cursor.close()
#关闭连接
db.close()
```

#### 3 练习

将csv中数据数据按照条件导入到数据库中，并统计不同渠道用户数量；
## 第十部分 数据分析
### 34. NumPy
#### 1 numpy简介
numpy:开源的python科学计算模块，用于数据快速处理；
numpy支持矩阵与数组操作，计算速度快，是Python中科学计算的基础库；
numpy优点：
1：底层使用C语言实现，计算速度快
#### 3.2 创建ndarray对象
2：numpy支持均值，累积和，方差等运算，可以直接使用；
3：numpy处理数据方式灵活，支持excel, csv等多种方式数据导入；
#### 3.2.3 ndarray相关属性
#### 3.2.4 创建ndarray对象
#### 3.2.5 np.radom相关方法
#### 2 numpy安装
#### 3.2.7 ndarray对象转其他数据结构
方式1：pip install numpy
方式2：anaconda环境：自带numpy,不用安装
numpy官方文档：https://numpy.org/doc/ (https://numpy.org/doc/)
numpy源码：https://github.com/numpy/numpy (https://github.com/numpy/numpy)
#### 3.4.3 二维array
#### 3.4.4 三维array
#### 3.4.5 多维数据取值
#### 3 numpy使用
#### 3.5 numpy计算
第一次使用
#### 3.5.2 array之间计算
#### 3.5.3 多维array之间计算
```python
import numpy as np
values = np.array([1,2,3,4,5])
print(values)
print(type(values))
[1 2 3 4 5]
<class 'numpy.ndarray'>
```
#### 3.6.3 np.hstack与np.vstack
#### 3.6.4 numpy分割
#### 3.1 ndarray
#### 3.7 numpy其他操作
1.numpy中基本数据结构；
2.ndarray对象索引从0开始
3.所有元素是同一种类型；
4.与列表类似，支持切片等操作；
#### 3.7.5 np.where
#### 3.2.1 array方法
array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
主要参数;
说明
objec 类似数组对象，例如：序列，range对象等
元素类型
order 数据内存排列形式
指定维度
理解：objec,dtype,ndmin
```python
#一维ndarray
print(np.array([1,2,3]))
#二维ndarray,元素类型为float32
print(np.array([1,2,3], dtype= 'f' ,ndmin=2))
[1 2 3]
[[1. 2. 3.]]
```
#### 3.2.2 ndarray轴与秩
轴（axis）：每一个线性的数组称为是一个轴；
第一个轴（axis=0）：第一层数组，
第二个轴（axis=1）：数组里的数组
依次类推；
秩（rank）：维度
示意图：
| 方法/项 | 说明 |
|---|---|
| 属性 | 说明 |
| .ndim | 秩 |
| .shape | 维度 |
| .size | 元素数量 |
| .dtype | 元素类型 |
示例：

```python
nd = np.array([1,2,3], ndmin= 2)
print(f'ndim:{nd.ndim}')
print(f'shape:{nd.shape}')
print(f'size:{nd.size}')
print(f'dtype:{nd.dtype}')
numpy简介
ndim:2
shape:(1, 3)
size:3
dtype:int32
```
说明
np.zeros(shape, dtype=float, order='C')
根据指定shape创建默认值为0的ndarray对象
np.empty(shape, dtype=float, order='C') 根据指定shape创建默认值为随机数的ndarray对象
np.ones(shape, dtype=float, order='C')
根据指定shape创建默认值为1的ndarray对象
np.full(shape, fill_value, dtype=None, order='C')根据指定shape创建默认值为fill_value的ndarray对象
np.arange([start,] stop[, step,], dtype=None)
类似于range,返回ndarray对象
np.linspace(start,stop,num=50,endpoint=True,retstep=False,dtype=None,axis=0,) 根据给定起始值与数量，返回ndarray对象
np.zeros_like/empty_like/ones_like(a, dtype=None, order='K', subok=True)
根据给定array返回相同形状的ndarray对象
示例：
```python
#一维
a = np.zeros(10)
print('zeros:\n',a)
#二维
a = np.ones((2,10))
print('ones:\n',a)
#根据指定数据形状
b = np.empty_like(a)
print('empty_like:\n',b)
#arange:
a = np.arange(0,20, 2)
print('arange:\n',a)
```
#### 3.7.2 nan判断
zeros:
[0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
ones:
[[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]]
empty_like:
[[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]]
arange:
[ 0 2 4 6 8 10 12 14 16 18]
方法 说明
np.random.rand(d0, d1, ..., dn))根据给定形状产生随机值
np.random.randint(low, high=None, size=None, dtype='l')根据指定值范围产生整数
示例：
```python
#根据指定形状产生随机值
print("random.rand:\n", np.random.rand(2,3))
#根据指定形状产生指定范围随机值
print('random.randint:\n', np.random.randint(10, 20, size= (2,10)))
random.rand:
[[0.65119326 0.58517776 0.35584462]
[0.6864957 0.50112408 0.85771027]]
random.randint:
[[19 13 18 17 17 10 19 19 14 17]
[10 13 17 16 10 13 19 17 12 10]]
```
#### 3.2.6 reshape方法
array.reshape(shape, order='C')
作用：调整array的新装，返回新的ndarray对象
示例：
```python
a = np.arange(10)
b = a.reshape(2,5)
print('a.reshape(2,5):\n',b)
print('b.reshape(10):\n', b.reshape(10))
a.reshape(2,5):
[[0 1 2 3 4]
[5 6 7 8 9]]
b.reshape(10):
[0 1 2 3 4 5 6 7 8 9]
```
理解下order中的C与F：
二维array对象：
a = [[1,2],[3,4]]
C代表在C语言中数据在内存存储方式；
a[0][0],a[0][1],a[1][0],a[1][1]
F代表在Fortran语言中数据在内存存储方式；
a[0][0],a[1][0],a[0][1],a[1][1]
示例：

```python
a = np.arange(10)
b = a.reshape(2,5)
print('b:\n', b)
c = b.reshape(10, order= 'C')
d = b.reshape(10, order= 'F')
print('c:\n',c)
print('d:\n',d)
b:
[[0 1 2 3 4]
[5 6 7 8 9]]
c:
[0 1 2 3 4 5 6 7 8 9]
d:
[0 5 1 6 2 7 3 8 4 9]
```
#### 3.3 numpy的数据类型
a = np.arange(10)
#### 3.4.1 一维array
说明
a.tolist() 转成列表
a.tostring(order='C') 转成bytes
a.tobytes(order='C') 转成bytes
a.tofile(fid, sep="", format="%s")保存到文件，fid：打开文件或者路径
示例：
#### 3.5.4 基本计算
```python
a = np.arange(10)
print(a.tolist())
print(a.tobytes())
```
#### 3.6.1 多个array拼接
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
b'\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00\x06\x00\x
00\x00\x07\x00\x00\x00\x08\x00\x00\x00\t\x00\x00\x00'
#### 3.6.5 vsplit与hsplit
常用数据类型：
#### 3.7.4 np.all与any
说明
int8/16/32/64 i1/i2/i4/i8 有符号8/16/32/64位整数
uint8/16/32/64 u1/u2/u4/u8 无有符号8/16/32/64位整数
#### 3.4 numpy访问与修改
numpy访问与列表类似，支取切片操作
```python
import numpy as np
a = np.arange(25)
#索引0对应值：
v = a[0]
print(v)
#索引为10值：
v = a[10]
print(v)
#切片操作：
v = a[10:20]
print(v)
v = a[20:]
print(v)
v = a[10:20:2]
print(v)
v = a[20:10:- 2]
print(v)
[10 11 12 13 14 15 16 17 18 19]
[20 21 22 23 24]
[10 12 14 16 18]
[20 18 16 14 12]
```
#### 3.4.2 理解numpy中的轴
一维array，轴：0
二维array，轴：0,1
三维array，轴：0,1,2

```python
import numpy as np
a = np.arange(25)
#2x2矩阵
a = a.reshape(5,5)
print(a)
#取a[0]
print('->a[0]:\t\t',a[0])
#取a[0][0]
print('->a[0][0]:\t',a[0][0])
[[ 0 1 2 3 4]
[ 5 6 7 8 9]
[10 11 12 13 14]
[15 16 17 18 19]
[20 21 22 23 24]]
[0 1 2 3 4]
```
```python
import numpy as np
a = np.arange(27)
#2x2矩阵
a = a.reshape(3,3,3)
#取a[0]
print(a[0])
#取a[0][0]
print('->a[0][0]:\t',a[0][0])
print('->a[0][0][0]:\t',a[0][0][0])
[[0 1 2]
[3 4 5]
[6 7 8]]
[0 1 2]
```
#### 3.6.2 多个数组的堆叠
```python
import numpy as np
a = np.arange(25)
#2x2矩阵
a = a.reshape(5,5)
print(a)
3.7.5 np.where
[[ 0 1 2 3 4]
[ 5 6 7 8 9]
[10 11 12 13 14]
[15 16 17 18 19]
[20 21 22 23 24]]
```
```python
#取行
print(a[0])
#取某个元素
print(a[0][1])
print(a[0,1])
[0 1 2 3 4]
```
```python
#取指定多行：
a[[1,2,4]]
```
array([[ 5, 6, 7, 8, 9],
[10, 11, 12, 13, 14],
[20, 21, 22, 23, 24]])
```python
#切片取行：
a[:5:2]
```
array([[ 0, 1, 2, 3, 4],
[10, 11, 12, 13, 14],
[20, 21, 22, 23, 24]])
```python
#取第一列：
a[:,1]
```
array([ 1, 6, 11, 16, 21])
```python
#取指定多列
a[:,[1,3]]
```
array([[ 1, 3],
[ 6, 8],
[11, 13],
[16, 18],
[21, 23]])
```python
#切片取指定多列
a[:,::2]
```
array([[ 0, 2, 4],
[ 5, 7, 9],
[10, 12, 14],
[15, 17, 19],
[20, 22, 24]])
```python
#取指定多个元素
a[[1,3,4],[2,3,4]]
```
array([ 7, 18, 24])
```python
#取指定行列
a[1:3,:3]
```
array([[ 5, 6, 7],
[10, 11, 12]])
#### 3.4.6 array修改：

```python
a = np.arange(10)
print(a)
#修改一个元素
a[0] = 10
print(a)
#修改多个元素
a[:5] = 10
print(a)
3.1 ndarray
[0 1 2 3 4 5 6 7 8 9]
[10 1 2 3 4 5 6 7 8 9]
[10 10 10 10 10 5 6 7 8 9]
```
#### 3.5.1 numpy广播： boardcasting
基本运算被应用到array所有的元素中
```python
a = np.arange(10)
print(a)
print(a* 10)
print(a+ 1)
print(a/ 2)
```
[0 1 2 3 4 5 6 7 8 9]
[ 0 10 20 30 40 50 60 70 80 90]
[ 1 2 3 4 5 6 7 8 9 10]
[0. 0.5 1. 1.5 2. 2.5 3. 3.5 4. 4.5]
#### 3.5.6 numpy其他计算相关方法
#### 3.6.3 np.hstack与np.vstack In [104]: 1 a = np.arange(5)
2 b = np.array([1,2,3,4,5])
#### 3 print(a)
#### 4 print(b)
#### 5 print(a+ b)
#### 6 print(a* b)
[0 1 2 3 4]
[1 2 3 4 5]
[1 3 5 7 9]
[ 0 2 6 12 20]
```python
t = np.arange(10).reshape(2,5)
a = np.ones_like(t)
b = np.full_like(t, 10)
print(a)
print(b)
print(a+ b)
[[1 1 1 1 1]
[1 1 1 1 1]]
[[10 10 10 10 10]
[10 10 10 10 10]]
[[11 11 11 11 11]
[11 11 11 11 11]]
```
主要包括：求和，均值，方差，累积和等；
numpy模块与array对象都支持这些方法，使用方式也类似，我们来看一种即可；
这些方法参数类似，我们以sum为例：
np.sum(a,axis=None,dtype=None,out=None,keepdims=,initial=)
a.sum(axis=None, dtype=None, out=None, keepdims=False)
numpy中常用计算相关方法：
| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| np.mean() | 计算均值 |
| np.max() | 最大值 |
| np.min() | 最小值 |
| np.cumsum() | 计算累加和 |
| np.std() | 计算标准差 |
| np.var() | 计算方差 |
| np.cov() | 计算协方差 |
| np.average() | 计算平均值 |
| np.media() | 计算中位数 |
| np.ptp() | 计算极值(最大值与最小值差) |
相应操作如下：
```python
import numpy as np
a = np.arange(10)
print(a)
#求和，最大，最小，极差
print(np.sum(a), np.max(a), np.min(a), np.ptp(a))
#方差，中位数，
print(np.var(a), np.median(a))
#累加和:[a[0], a[0]+a[1], a[0]+a[1]+a[2], ...]
print(np.cumsum(a))
[0 1 2 3 4 5 6 7 8 9]
9 0 9
8.25 4.5
[ 0 1 3 6 10 15 21 28 36 45]
```
#### 3.5.5 多维array计算
多维array指定axis，可以得到不同效果，在计算常用指标，发挥奇效。

```python
import numpy as np
a = np.arange(10)
a = a.reshape(2,5)
a
```
array([[0, 1, 2, 3, 4],
[5, 6, 7, 8, 9]])
```python
#指定axis为1,按行进行计算
print(np.sum(a, axis= 1))
#指定axis为0：按列进行计算
print(np.sum(a, axis= 0))
```
[10 35]
[ 5 7 9 11 13]
方法 说明
np.sqrt()计算平方根
np.log() 计算对数
np.min() 最小值
np.cos/sin/tan/ 三角函数
np.std()计算标准差
#### 3.6 numpy数据拼接分割
多个数组拼接：concatenate((a1, a2, ...), axis=0, out=None)
```python
a = np.arange(1,5).reshape(2,2)
b = np.arange(5,9).reshape(2,2)
print(f'{a}\n---\n{b}')
```
[[1 2]
[3 4]]
---
[[5 6]
[7 8]]
```python
#轴为1进行拼接
'''
[[1,2],[3,4]]
[[5,6],[7,8]]
结果
[1,2,]+[5,6]
[3,4]+[7,8]
'''
np.concatenate((a,b), axis= 1)
```
array([[1, 2, 5, 6],
[3, 4, 7, 8]])
```python
#轴为0进行拼接
np.concatenate((a,b), axis= 0)
```
array([[1, 2],
[3, 4],
[5, 6],
[7, 8]])
np.stack(arrays, axis=0, out=None) 基本理解：arrays，沿着axis进行堆叠，类似穿起来，而不是拼接 例如：
```python
a = np.arange(0,2)
b = np.arange(2,4)
c = np.arange(4,6)
'''
[0, 1]
[2, 3]
[4, 5] ->
沿着axis=0拼接：
[[0, 1],
[2, 3],
[4, 5],]
'''
np.stack((a,b,c), axis= 0)
```
array([[0, 1],
[2, 3],
[4, 5]])
```python
a = np.arange(0,2)
b = np.arange(2,4)
c = np.arange(4,6)
'''
[0, 1]
[2, 3]
[4, 5] ->
沿着axis=1拼接：
[[0,2,4],
[1,3,5]]
'''
np.stack((a,b,c), axis= 1)
```
array([[0, 2, 4],
[1, 3, 5]])
分别为水平拼接与垂直拼接

```python
a = np.arange(0,2)
b = np.arange(2,4)
c = np.arange(4,6)
print(np.hstack((a,b,c)))
print(np.vstack((a,b,c)))
numpy简介
[0 1 2 3 4 5]
[[0 1]
[2 3]
[4 5]]
```
split方法：将制定的array按照aixs分割成制定值
np.split(ary, indices_or_sections, axis=0)
#### 3.2.7 ndarray对象转其他数据结构 In [93]: 1 np.split(np.arange(4),2, axis= 0)
[array([0, 1]), array([2, 3])]
```python
a = np.arange(8).reshape(2,4)
print(a)
```
[[0 1 2 3]
[4 5 6 7]]
```python
#按照axis=0进行切分，分成2份
np.split(a, 2, axis= 0)
```
[array([[0, 1, 2, 3]]), array([[4, 5, 6, 7]])]
```python
#按照axis=1进行切分，分成2份
np.split(a, 2, axis= 1)
```
#### 3.6.3 np.hstack与np.vstack Out[98]: [array([[0, 1],
[4, 5]]), array([[2, 3],
[6, 7]])]
#### 3.7.1 nan与缺省值处理
#### 3.7.3 boolean索引
vsplit沿着垂直轴切分
hsplit沿着水平轴切分
```python
a = np.arange(10)
np.hsplit(a, 5)
```
[array([0, 1]), array([2, 3]), array([4, 5]), array([6, 7]), array([8, 9])]
```python
a = np.arange(10).reshape(2,5)
np.vsplit(a, 2)
```
[array([[0, 1, 2, 3, 4]]), array([[5, 6, 7, 8, 9]])]
Nan是nunpy和pandas中用于标识缺失数据
None:Python 中对象，不能与Nan混淆一起
一个例子：某同学两次考试，有一次因为某些情况没有参加，数据格式如下：
```python
v1 = np.array([[90, 100],[np.nan, 100]])
v1
```
array([[ 90., 100.],
[ nan, 100.]])
```python
np.isnan(v1)
```
array([[False, False],
[ True, False]])
array的值都为True或者False；
例如：array([[False, False],[ True, False]]) 获取所有nan值：
```python
v1[np.isnan(v1)]
```
array([nan])
获取非nan值
```python
v1[np.isnan(v1) == False ]
```
array([ 90., 100., 100.])
np.all(a, axis=None, out=None, ):沿着给定的axis判断是否有元素为0，为0返回False,不设置axis，判断所有元素
np.any(a, axis=None, out=None, )：沿着给定的axis判断是否有元素不为0，为0返回False，不设置axis，判断所有元素
例如：
```python
a = np.arange(10)
print(a)
print(np.all(a))
[0 1 2 3 4 5 6 7 8 9]
False
```

```python
a = np.arange(10).reshape(2,5)
#沿着axis=0，简单理解垂直轴
print(np.all(a, axis= 0))
#沿着axis=1，简单理解水平轴
print(np.all(a, axis= 1))
numpy简介
[False True True True True]
[False True]
3.1 ndarray
```
```python
b = np.zeros_like(a)
print(b)
print(np.all(b))
print(np.any(b))
```
[[0 0 0 0 0]
[0 0 0 0 0]]
False
False
注意None
```python
a = np.array([1, None ])
print(a)
print(np.any(a))
print(np.all(a))
[1 None]
None
```
where(condition, [x, y]):
如果给定x,y,满足条件condition，输出x，不满足输出y；
如果没有x,y,返回满足条件对应的值的索引；
示例：随机生成成绩单，判断是否及格
```python
a = np.random.randint(30,100, 10)
print(a)
np.where(a>= 60, 'pass', 'failed')
3.7.5 np.where
[62 59 95 38 39 64 78 65 73 94]
```
array(['pass', 'failed', 'pass', 'failed', 'failed', 'pass', 'pass',
'pass', 'pass', 'pass'], dtype='<U6')
获取满足条件的索引：
```python
np.where(a>= 60)
```
(array([0, 2, 5, 6, 7, 8, 9], dtype=int64),)
获取满足条件值：
```python
a[np.where(a>= 60)]
```
array([62, 95, 64, 78, 65, 73, 94])
### 35. Matplotlib
Matplotlib是Python的绘图模块，他与Numpy，Pandas等配合使用，类似于MATLAB 的绘图工具;
Matplotlib是一个基础工具，后面所介绍的seanborn等都是基于这个模块实现;
Matplotlib可以在Jupyter中直接显示，是Python进行数据分析的必备模块之一;
官网：https://matplotlib.org/index.html (https://matplotlib.org/index.html)
案例：https://matplotlib.org/gallery/index.html (https://matplotlib.org/gallery/index.html)
#### 1.2 anaconda环境
#### 1.3 matplotlib第一个图表
#### 1.4 %matplotlib inline 1 matplotlib安装与基本介绍
#### 1.5 认识matplotlib图表：
#### 1.1 只有python环境
#### 2.1 第一个图表
pip install matplotlib
#### 2.3 图表配置及文档查看
#### 2.4 通过fmt设置颜色
#### 2.6 字体设置
不需要安装，直接可以使用
#### 2.8 支持中文
#### 2.9 子图
#### 2.11 设置坐标轴(1)
#### 2.12 设置坐标轴(2) In [2]: ▾ 1 #导入matplotlib
#### 2 import matplotlib.pyplot as plt
#### 3 import numpy as np
#### 4 #创建图表
#### 5 plt.plot(np.arange(5), np.arange(5))
#### 6 #显示
#### 7 plt.show()
#### 3.6 箱形图
#### 1.4 %matplotlib inline
%matplotlib inline作用：iPython 中定义的魔法函数（Magic Function）,将matplotlib绘制的图显示在页面里中；
如果不加这句话需要调用：plt.show()
```python
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
plt.plot(np.arange(5), np.arange(5))
#plt.show()
```
[<matplotlib.lines.Line2D at 0x158adaf2240>]
认识画布，axis,axes 画布：图表大小，进行图表绘制
axes：坐标系，一个画布中可以指定多个坐标系
axis：坐标轴,每个坐标系都有一个坐标轴
#### 2 matplotlib基本使用
主要内容：
1：绘制基本本表；
2：图表格式设置；
3：多图与子图；
绘制折线图：
plt.plot(*args, scalex=True, scaley=True, data=None, **kwargs)
更多参数可以查看说明文档；

```python
% matplotlib inline
import matplotlib.pyplot as plt
xdata = range(5)
ydata = range(5)
#xdata:x轴数据，ydata:y轴数据
plt.plot(xdata,ydata)
```
[<matplotlib.lines.Line2D at 0x18e27a50388>]
#### 2.2 折线图常用方式：
#### 2.5 设置x与y轴
#### 2.7 title/图例设置
#### 2.10 创建画布
#### 2.12 设置坐标轴(2)
#### 3 matplotlib常用的图表
#### 3.1 折线图
#### 3.2 散点图
#### 3.3 柱状图/条形图
#### 3.5 直方图
```python
y = range(1,4)
#x值为0,1,2,N-1
plt.plot(y)
```
[<matplotlib.lines.Line2D at 0x18e293518c8>]
```python
#数据为字典，x,y为字典key,这种方式对于后面pandas同样试用
plt.plot('x','y', data= {'x':[1,2,3], 'y':[4,5,6]})
d:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:2: RuntimeWarning: Second argument 'y' is ambiguous: could be a color spec but is in data; using as da
data or use three arguments to plot.
```
[<matplotlib.lines.Line2D at 0x18e28fbc088>]
文档查看，方式1： pyplot 子模块文档地址：https://matplotlib.org/api/pyplot_summary.html (https://matplotlib.org/api/pyplot_summary.html)
在页面中找到plot方法，点击进入plot方法的介绍
文档查看，方式2：直接查看
| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| fmt | 字符串，线与点的属性 |
| data | 数据 |
| kwargs | 关键字参数 |
fmt格式：'-or',分别代表：线型，点形状，颜色，顺序可以颠倒
设置线型
符号 说明
'-' solid line style
'--' dashed line style
'-.'+dash-dot line style
':' dotted line style
点设置
符号 说明
'.' point marker
',' pixel marker
'o' circle marker
'v' triangle_down marker
'^' triangle_up marker
'<' triangle_left marker
'>' riangle_right marker
颜色设置

符号 说明
'b' lue
'g' green
'r' red
'c' cyan
'm' magenta
'y' yellow
'k' black
'w' white
更多新详细说明参考：https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html (https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html)
一个例子：
```python
#fmt:--:虚线，o:点形状为圆，r:红色,, linewidth：设置线宽度
plt.plot(range(4), '--or', linewidth= 2)
#fmt:-.：虚线，<：点形状为三角，r:蓝色
plt.plot(range(1,5), '-.<b')
```
[<matplotlib.lines.Line2D at 0x1f47f2eff28>]
#### 3.4 饼状图
坐标轴设置包括：
坐标轴值，坐标轴显示值，坐标轴标签
说明
设置x轴lable plt.xlabel(s, *args, **kwargs)
设置y轴lable plt.ylabel(s, *args, **kwargs)
设置x轴tick plt.xticks(*args, **kwargs)
设置y轴tick plt.yticks(*args, **kwargs)
设置x轴范围 plt.xlim(*args, **kwargs)
设置y轴范围 plt.ylim(*args, **kwargs)
一个例子：
```python
#设置xy轴范围(-10, 10)
import matplotlib.pyplot as plt
plt.xlim(- 10,10)
plt.ylim(- 10,10)
#折线图
plt.plot(range(- 10,10),range(- 10,10), '-o')
#设置x-ylabel
plt.xlabel('x-value')
plt.ylabel('y-value')
#设置x轴显示坐标值(x轴值与显示值要对应，例如：-10:a, -9:b...10:t)
xticks = [chr(v) for v in range(ord('a'), ord('a')+ 21)]
_ = plt.xticks(range(- 10,10),xticks)
```
字体设置包括大小，字体，颜色，旋转角度等
参考链接：https://matplotlib.org/api/text_api.html (https://matplotlib.org/api/text_api.html)
常用的设置：
说明
角度
字体
size 大小，整数或者 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
透明度(0~1)
是否显示
颜色，例如'r','b'
具体例子：

```python
#设置xy轴范围(-10, 10)
import matplotlib.pyplot as plt
#折线图
plt.plot(range(5), '-o')
#设置x-ylabel
_ = plt.xlabel('x-value')
_ = plt.ylabel('y-value')
_ = plt.xticks(rotation= 30, fontfamily = 'fantasy', size= 20,alpha= 0.7,visible= True ,c= 'r')
```
plt.title(label, fontdict=None, loc='center', pad=None, **kwargs):设置标题；
plt.legend(*args, **kwargs)：设置图例，例如一个图表中可以绘制多个折现，每个折现代表说明可以使用legend标识；
详细参数可以查看说明与帮助文档；
方式1：
```python
import matplotlib.pyplot as plt
#折线图
plt.plot(range(5), '-o', label= "line1")
plt.plot(range(1,6), '-o', label= "line2")
#设置x-ylabel
plt.legend()
plt.title("case1")
```
Text(0.5, 1.0, 'case1')
方式2
```python
import matplotlib.pyplot as plt
#折线图
line1 = plt.plot(range(5), '-o')
line2 = plt.plot(range(1,6), '-o')
#设置x-ylabel
plt.legend(('l1', 'l2'))
plt.title("case1")
```
Text(0.5, 1.0, 'case1')
若支持中文需要进行如下设置：
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
一个例子：将title设置为中文，结果显示乱码

```python
import matplotlib.pyplot as plt
#折线图
line1 = plt.plot(range(5), '-o')
line2 = plt.plot(range(1,6), '-o')
#设置x-ylabel
plt.legend(('l1', 'l2'))
plt.title("案例1")
```
#### 1.2 anaconda环境 Out[38]: Text(0.5, 1.0, '案例1')
设置支持中文
设置之后，jupyter中全局有效
```python
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
import matplotlib.pyplot as plt
#折线图
line1 = plt.plot(range(5), '-o')
line2 = plt.plot(range(1,6), '-o')
#设置x-ylabel
plt.legend(('l1', 'l2'))
plt.title("案例1")
```
Text(0.5, 1.0, '案例1')
添加多个图表方式可以使用子图及多图
plt.subplot(*args, **kwargs):返回axes
方式1：一行多列
```python
plt.subplot(1,2,1) #同：plt.subplot(121)
plt.subplot(1,2,2) #同：plt.subplot(122)
```
<matplotlib.axes._subplots.AxesSubplot at 0x1e2ec000ec8>
方式2：一列多行
```python
plt.subplot(2,1,1)# 同plt.subplot(211)
plt.subplot(2,1,2)# 同plt.subplot(212)
```
<matplotlib.axes._subplots.AxesSubplot at 0x1e2f0225288>
方式3：

方式3：多行多列,并进行不同设置
```python
#axes1
axes1 = plt.subplot(221)
axes1.plot(range(4))
axes1.set_facecolor('r')
#axes2
axes2 = plt.subplot(222)
axes2.plot(range(1,5))
axes2.set_facecolor('y')
#axes3
axes3 = plt.subplot(223)
axes3.plot(range(2,6))
axes3.set_facecolor('b')
#axes4
axes4 = plt.subplot(224)
axes4.plot(range(3,7))
axes4.set_facecolor('c')
```
理解子图：axes对应每个坐标系，
plt.figure(num=None,figsize=None,dpi=None,facecolor=None,edgecolor=None,frameon=True,...clear=False,**kwargs)
说明
画布序号
figsize画布大小，格式：(width, heigh)，例如：(100, 20)
画布颜色
示例：
```python
#创建画布1
plt.figure(1,figsize= (6, 3))
plt.plot([1,2,3])
#创建画布2
plt.figure(2,figsize= (5, 5), facecolor= 'y')
plt.plot([4,5,6])
#获取当前坐标系
ax = plt.gca()
#设置颜色为ax
ax.set_facecolor('r')
```
默认坐标系为00，有时候我们希望坐标轴中心点在其他位置，且只希望显示x,y两个轴，实现如下

```python
import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np
#支持中文
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
#结局负数乱码
plt.rcParams['axes.unicode_minus']= False
x = np.linspace(- 4, 4, 200)
y = np.sin(x)
plt.figure()
#获取当前axes
ax = plt.gca()
#坐标系中right,top不显示
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
#设置ticks显示位置
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
#移动坐标轴位置：中心位置为(1,0)
ax.spines['left'].set_position(('data', 1))
ax.spines['bottom'].set_position(('data', 0))
plt.plot(x, y)
```
[<matplotlib.lines.Line2D at 0x1b9196ff438>]
import mpl_toolkits.axisartist as axisartist
```python
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist
fig = plt.figure('Sine Wave', (6,4))
#创建axisartist对象
ax = axisartist.Subplot(fig, 1,1,1)
#增加坐标系
fig.add_axes(ax)
#坐标设置不显示
ax.axis[:].set_visible(False )
#指定坐标系位置
ax.axis["x"] = ax.new_floating_axis(0, 0)
ax.axis["y"] = ax.new_floating_axis(1, 0)
ax.axis["x"].set_axis_direction('top')
ax.axis["y"].set_axis_direction('left')
#设置坐标轴格式
ax.axis["x"].set_axisline_style("->", size = 2.0)
ax.axis["y"].set_axisline_style("->", size = 2.0)
t = np.linspace(0, 1* np.pi)
y = 2* np.sin(2* t)
ax.plot(t, y, color = 'red', linewidth = 2)
plt.title('y = 2sin(2t)',fontsize = 14)
#设置x轴刻度
ax.set_xticks(np.linspace(0.25,1.25,5)* np.pi)
ax.set_xticklabels(['$\\frac{\pi}{4}$','$\\frac{\pi}{2}$', '$\\frac{3\pi}{4}$', '$\pi$', '$\\frac{5\pi}{4}$', '$\\frac{3\pi}{2}$'])
ax.set_yticks([0, 1, 2])
#设置xy周范围
ax.set_xlim(- 0.5* np.pi,1.5* np.pi)
ax.set_ylim(- 2.2, 2.2)
```
(-2.2, 2.2)
折线图：趋势变化关系，场合时间等结合起来使用；
例如：新增用户，累计用户，股票数据等;
案例：近一周某用户粉丝每天增长量与累积粉丝数：
```python
import matplotlib.pyplot as plt
import numpy as np
ydata = [100, 90, 120, 150, 200, 300, 210]
sumydata = np.cumsum(ydata)
```

```python
plt.plot(ydata)
plt.plot(sumydata)
plt.legend(['新增粉丝', '累计粉丝'])
plt.title("我的粉丝")
```
#### 1 matplotlib安装与基本介绍 Out[25]: Text(0.5,1,'我的粉丝')
显示若干数据系列中各数值之间的关系,一定程度反映数据分布关系；
适用于维度较少数据
方法：plt.scatter(x, y, s=None, c=None,marker=None,...,alpha=None,**kwargs)
```python
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
%matplotlib inline
xValue = list(range(0, 101))
yValue = [x * np.random.rand() for x in xValue]
plt.title(u'散点图')
plt.xlabel('x-data')
plt.ylabel('y-data')
plt.legend()
plt.scatter(xValue, yValue, s= 20, marker= 'o')
```
<matplotlib.collections.PathCollection at 0x1b91b6be438>
显示一段时间内的数据变化或显示各项之间的比较情况
例如：数据对比
相关方法：
柱状图
bar(x, height, *, align='center', **kwargs)
bar(x, height, width, *, align='center', **kwargs)
bar(x, height, width, bottom, *, align='center', **kwargs)
条形图：
plt.barh(*args, **kwargs)
```python
import matplotlib.pyplot as plt43v发v
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
import numpy as np
plt.figure(figsize= (8,4))
x=np.arange(4)
gdp_2019 = [10.7, 9.9,7.1,6.2]
#设置柱状图的宽度
bar_width= 0.3
tick_label= ['广东省','江苏省','山东省','浙江省']
#绘制并列柱状图
plt.bar(x,gdp_2019,bar_width,color= 'salmon',label= '2019')
plt.title('GDP(万亿)')
plt.legend()
_ = plt.xticks(x,tick_label)
```

```python
import matplotlib.pyplot as plt
dic = {'a': 22, 'b': 10, 'c': 6, 'd': 4, 'e': 2, 'f': 10, 'g': 24, 'h': 16, 'i': 1, 'j': 12}
s = sorted(dic.items(), key= lambda x: x[1], reverse= False ) # 对dict 按照value排序 True表示翻转 ,转为了列表形式
x_x = []
y_y = []
for i in s:
x_x.append(i[0])
y_y.append(i[1])
x = x_x
y = y_y
fig, ax = plt.subplots()
ax.barh(x, y)
labels = ax.get_xticklabels()
plt.setp(labels, rotation= 0, horizontalalignment= 'right')
for a, b in zip(x, y):
plt.text(b+ 1, a, b, ha= 'center', va= 'center')
plt.ylabel('name')
plt.xlabel('数量')
plt.title("分布")
```
Text(0.5,1,'分布')
总体数据中，各项与总和的比例；
各个数据对比，例如：不同地区销售额占比；
plt.pie(x, explode=None, labels=None...)
```python
import matplotlib.pyplot as plt
# 构造数据
edu = [100,200,900, 600, 1000]
labels = ['中专','大专','本科','硕士','其他']
plt.pie(x = edu, labels= labels, autopct= '%.1f%%')
plt.title('职工教育分布')
plt.show()
```
数据分布情况
plt.hist(x, bins=None, range=None,...)
```python
import matplotlib.pyplot as plt
import numpy as np
# 构造数据
data = np.random.randn(10000)
plt.hist(data)
plt.show()
```
箱形图可以很直观的描述数据的最大值、最小值、中位数、上四分位数、下四分位数、异常值，
plt.boxplot(x, notch=None, sym=None, vert=None, whis=None)

```python
import matplotlib.pyplot as plt
import numpy as np
# 构造数据
data = np.random.randn(10000)
plt.boxplot(data)
plt.show()
```
```python
plt.boxplot?
```
## 第十一部分 算法与数据结构
### 36. 逻辑强化（算法入门练习）
有序列表中插入有序的元素
需求：给定有序数字列表与数字，将数字插入列表中，并使列表有序；
例如：

nums = [1,2,4,4] x = 3, 插入后结果：[1,2,3,4,4]
nums = [1,2,4,4] x = 5, 插入后结果：[1,2,4,4,5]

实现思路：

遍历列表nums，取元素val

如果插入值x小于val, 将x插入到val位置；

如果x大于num中最大值，将x插入到nums最后位置；

代码实现：

```python
def inser_x(nums, x):
    #列表不为空
    if nums:
        #x大于nums中的最大值
        if nums[-1] <= x:
            nums.append(x)
        else:
            for index, val in enumerate(nums):
                if x < val:
                    nums.insert(index, val)
                    #插入之后必须调用break
                    break
    else:
        #列表为空，直接插入x
        nums.append(x)
nums = [1,2,4,4]
inser_x(nums, 3)
nums
```

```
[1, 2, 4, 4, 4]
```

求交集
给定两个数组，编写一个函数来计算它们的交集。

要求：

输出结果中的每个元素一定是唯一的。

不考虑输出结果的顺序。

例如：

list1 = [4,9,5], list2 = [9,4,9,8,4]
输出：[9,4]

实现思路1：

list1与list2分别去重；

并合并数据集；

统计每个字符出现数量；

字符数量如果大于1，则说明有重复元素

```python
from collections import Counter

def jiaoji(list1, list2):
    l1 = list(set(list1))
    l2 = list(set(list2))
    l1.extend(l2)
    r = Counter(l1)
    return [k for k in r if r[k] > 1]
#测试1
list1 = [4,9,5]
list2 = [9,4,9,8,4]
print(jiaoji(list1, list2))
#测试2
list1 = [1,2,2,1]
list2 = [2,2]
print(jiaoji(list1, list2))
```

```
[9, 4]
[2]
```

实现思路2：
遍历列表list1,判断list1中元素是否在list2中，如果在list2中则记录该元素；

代码实现

```python
def jiaoji(list1, list2):
    vals = []
    for val in list1:
        if val in list2 and val not in vals:
            vals.append(val)
    return vals
#测试1
list1 = [4,9,5]
list2 = [9,4,9,8,4]
jiaoji(list1, list2)
```

```
[4, 9]
```

旋转字符串
字符串s的左旋转操作：将字符串前面的若干个字符转移到字符串的尾部；

定义一个函数实现字符串左旋转操作的功能；

例如：输入字符串"abcdefg"和数字2，返回左旋转两位得到的结果"cdefgab"。

限制条件：1 <= k < len(s)

实现思路：

1.

```python
def reverse_left_words(s, k):
    lens = len(s)
    if k > 0 and k < lens:
        start = s[k:]
        end = s[:k]
        return start+end

s = "abcdefg"
k = 2
reverse_left_words(s,k)
```

```
'cdefgab'
```

反转字符串
将字符列表进行反转，例如：

['a', 'b', 'c', 'd'] -> ['d', 'c', 'b', 'a']
['a', 'b', 'c', 'd', 'e'] -> ['e', 'd', 'c', 'b', 'a']
要求：在现有的列表中进行处理，不使用python默认方法；

基本操作：

获取列表长度；

初始索引为start, 结束索引为end；

start与end对应的元素交换；且start加1，end减一；

结束条件：start<end；

代码实现：

```python
def my_reverse(lists):

    start = 0
    end = len(lists)-1

    while start < end:
        lists[start], lists[end] = lists[end], lists[start]
        start += 1
        end -= 1

l = list('abcdefg')
print(l)
my_reverse(l)
print(l)
l = list('ab')
print(l)
my_reverse(l)
print(l)
```

```
['a', 'b', 'c', 'd', 'e', 'f', 'g']
['g', 'f', 'e', 'd', 'c', 'b', 'a']
['a', 'b']
['b', 'a']
```

翻转字符串中单词
给定一个字符串，逐个翻转字符串中的每个单词。
说明：

无空格字符构成一个 单词 。

输入字符串可以在前面或者后面包含多余的空格，但是反转后的字符不能包括。

如果两个单词间有多余的空格，将反转后单词间的空格减少到只含一个。

例如：
输入："the sky is blue"
输出："blue is sky the"
输入："  hello world!  "
输出："world! hello"
输入："a good   example"
输出："example good a"
输入：s = "  Bob    Loves  Alice   "
输出："Alice Loves Bob"

实现思路：

对字符串进行切分，

使用列表解析过滤掉空白字符，

对单词列表进行翻转；

使用字符串join方法进行拼接；

```python
def my_reverse(lists):

    start = 0
    end = len(lists)-1

    while start < end:
        lists[start], lists[end] = lists[end], lists[start]
        start += 1
        end -= 1

def reverse_words(s):
    wds = s.split()
    wds = [wd for wd in wds if wd.strip()]
    my_reverse(wds)
    return ' '.join(wds)

list_s = ["the sky is blue", "  hello world!  ","a good   example","  Bob    Loves  Alice   "]
for s in list_s:
    print('[%s]->[%s]'%(s, reverse_words(s)))
```

合并两个有序列表
给定两个有序列表l1, l2;将其合并成新的有序列表；

例如：l1 = [1,2,2,3], l2 = [0,1,3]，结果：[0,1,1,2,2,3,3,]

注意：不能使用sort方法

实现思路：
定义空列表；

遍历l1与l2,并对其比较，将较小值插入新列表；

如果一个列表遍历完成，将另一个列表剩余元素添加到新列表中；

```python
def megre_list(list1, list2):
    #初始索引
    index1 = 0
    index2 = 0
    #获取列表长度
    lens1 = len(list1)
    lens2 = len(list2)
    new_list = []
    #遍历两个列表
    while index1 < lens1 and index2 < lens2:
        v1 = list1[index1]
        v2 = list2[index2]
        #对元素进行比较
        if v1 <= v2:
            new_list.append(v1)
            index1 += 1
        else:
            new_list.append(v2)
            index2 += 1
    #处理l1中剩余元素
    if index1 < lens1:
        new_list.extend(list1[index1:])
    #处理l2中剩余元素
    if index2 < lens2:
        new_list.extend(list2[index2:])
    return new_list
l1 = [-1, 1,2,3,3]
l2 = [0,1,2,2]
megre_list(l1, l2)
```

```
[-1, 0, 1, 1, 2, 2, 2, 3, 3]
```

解压缩编码列表
给你一个以行程长度编码压缩的整数列表nums；
列表中两个元素：

[freq, val, freq, val, ...]
freq与val成对出现，freq代表val出现频次；

将nums解压成为新的列表；

例如：

输入：nums = [1,2,3,4]
输出：[2,4,4,4]

实现思路：
遍历列表nums;

将每对值进行扩展到新列表中；

```python
def decompress_list(nums):
    lens = len(nums)
    i = 0
    new_list = []
    while i < lens:
        freq = nums[i]
        val = nums[i+1]
        i += 2
        new_list.extend([val] * freq)
    return new_list
nums = [1,2,3,4]
decompress_list(nums)
```

```
[2, 4, 4, 4]
```

数字列表加法操作
需求：给定一个数字列表，每个数字范围：0~9；

数字列表：

数字189使用列表表示：num1 = [1,8,9]
数字21使用列表表示：num2 = [2,1]
num1与num2相加结果：[2,1,0]
题目分析：在C，C++等语言中，受限于计算机位数，整数最大值有限制；为了防止越界，导致计算结果错误，会使用巨型数组替代数字进行计算；

计算规则：

计算最低位，并检查是否有进位；

计算次低位与进位，检查是否有进位；

如果两个数字列表长度不同，将为完成计算的插入到前面，并检查进位；

逻辑如下图：

```python
def list_add(num1, num2):
    lens1 = len(num1)
    lens2 = len(num2)
    #进位处理
    carry = 0
    res = []
    #获取两个列表最小长度
    min_index = min(lens1, lens2) * -1
    #从最后一个开始计算
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
            min_index = lens1*-1
        else:
            last_list = num2
            min_index = lens2*-1

        while i >= min_index:
            v = last_list[i]+ carry
            if v >= 10:
                carry = 1
                res.insert(0, v - 10)
            else:
                carry = 0
                res.insert(0, v)
            i-=1
    if carry:
        res.insert(0, carry)

    return res

num1 = [1]
num2 = [2]
list_add(num1, num2)
```

排队问题
n名战士站成一排。每个战士都有唯一的评分；

每3个战士可以组成一个作战单位，分组规则如下：

从队伍中选出下标分别为 i、j、k 的 3 名战士，他们的评分分别为 Si,Sj,Sk；

队伍需满足： Si<SjSj>Sk，其中:0 <= i < j < k < n；

给定一组数据，按上述规则可以组建的作战单位数量及对应的值；

例如：

输入：l = [2,5,3,4,1]
输出：3
说明：队伍序号，(2,3,4)、(5,4,1)、(5,3,1) ；
输入：l = [2,1,3]
输出：0
解释：不符合条件。

问题：

我们要找什么？

如何去找？

关键点1：从前到后所有的组合(3个元素)

所有组合如下：

[2,5,3]
[2,5,4]
[2,5,1]
[2,3,4]
[2,3,1]
[2,4,1]
[5,3,4]
[5,3,1]
...
[3,4,1]

关键点2：找打符合规则的组合
条件1：v1>v2>v3；

条件2：v1<v2<v；

实现思路：

1.三层遍历：

第一层：依次取：i_1,..i_n

第二层：依次取：i_2,..i_n

第三层：依次取：i_3,..i_n

组合形式：(i_1, i_2,i_3),(i_1,i_2,i_4)...(i_1,i_2,i_n)

以2开头组合，如下图：

```python
def count_teams(l):
    for index,val in enumerate(l):
        sub_list = l[index+1:]
        for sub_index, sub_val in enumerate(sub_list):
            last_list = l[index+sub_index+2:]
            if val > sub_val:
                for last in last_list:
                    if sub_val>last:
                        print(val, sub_val, last)
            else:
                for last in last_list:
                    if sub_val<last:
                        print(val, sub_val, last)
l = [2,5,3,4,1]
count_teams(l)
```

```
2 3 4
5 3 1
5 4 1
```

计算和的最大乘积
给定一个正整数 n，将其拆分为至少两个正整数的和，并使这些整数的乘积最大化，返回这些加数的最大乘积。

例如：10 = 3+3+4，结果：3x3x4 = 36

问题：如何让加数的乘积最大?

从1到n开始拆解：

1不能拆解；

2 = 1+1, 积：1；

3 = 2+1, 积：2；

4 = 2+2, 积：4， 不用拆解；

5 = 3+2, 积：6，可以拆解；

6 = 3+3, 积：9， 可以拆解；

7 = 3+4, 积：12，可以拆解；

8 = 3+3+2，积：18，可以拆解；
....
N. n = 3+3...+x,

规则：数字n>4，可以将其拆解成：n = 3k+x

实现思路(n>4)：

n%3 == 1, 3的数量：k=(n-4)//3，结果：pow(3, k)x4

n%3 == 2, 3的数量：k=n//3， 结果：pow(3,k)x(n%3)

n%3 == 0, 3的数量：k=n//3，结果：pow(3,k)

```python
def integer_break(n):
    n_map = {1:1,2:1,3:2, 4:4}
    val = n_map.get(n, 0)
    k = 0
    if not val:
        tmp = n%3
        if tmp == 1:
            k = (n-4)//3
            tmp = 4
        elif tmp == 2:
            k = n//3
        else:
            k = n//3
            tmp = 1
        val = pow(3, k) * tmp
    return val

for n in [1,3,4,5,10,12,100]:
    print(n,integer_break(n))
```

```
1 1
3 2
4 4
5 6
10 36
12 81
100 7412080755407364
```

n的第K个因子
给定两个正整数n,k；

如果正整数i满足n %i == 0，i就是n的因子，将n的所有因子升序排序；

需求：如果n因子数量大于等于k, 返回第k对应的因子,否则返回 -1。

接口：

def kthFactor(n,k):
    pass

实现思路1：
从1到n找到n所有的因子；

将因子保存到列表中，并使其有序；

根据k选择对应因子

```python
def kthFactor(n,k):
    list_fac = []
    for i in range(1, n+1):
        if n % i == 0:
            list_fac.append(i)
    if len(list_fac) >= k:
        return list_fac, list_fac[k-1]

print(kthFactor(10,2))
print(kthFactor(100,2))
```

```
([1, 2, 5, 10], 2)
([1, 2, 4, 5, 10, 20, 25, 50, 100], 2)
```

实现思路2：

问题：整数N最大因子？最小因子？

N的最大因子：N，最小因子：1；

记录最大因子：max_fac=n, 最小因子:min_fac = 1；

如果min_fac < max_fac, 则继续查找N的因子；否则结束查找；

min_fac +=1,

如果N%min_fac == 0,max_fac = n//min_fac，记录min_fac与max_fac;

逻辑如下图：

插入顺序：
插入位置索引：i=0；

找到一对因子；

插入大数：l.insert(-1xi, max_fac)；

如果两个因子不等，插入小数：l.insert(-1xi, min_fac)；

i+=1，继续查找；

```python
def kthFactor(n,k):
    list_fac =[]
    min_val, max_val = 1, n
    i = 0
    if n > 1:
        while min_val < max_val:
            if n % min_val == 0:
                t = n // min_val
                max_val = t
                if max_val != min_val:
                    list_fac.insert(-1*i, t)
                list_fac.insert(i,min_val)

                i += 1
            min_val += 1
    else:
        list_fac.append(n)

    lens = len(list_fac)
    if lens >= k:
        return list_fac, list_fac[k-1]
    else:
        return list_fac, -1
```

```python
print(kthFactor(100,2))
print(kthFactor(1, 1))
```

```
([1, 2, 4, 5, 10, 20, 25, 50, 100], 2)
([1], 1)
```

合并区间

给出一个有序的区间的集合，请合并所有重叠的区间。

例1：
输入: [[1,3],[2,6],[8,10],[15,18]]
输出: [[1,6],[8,10],[15,18]]
解释: 区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
例2:
输入: [[1,4],[4,5]]
输出: [[1,5]]
解释: 区间 [1,4] 和 [4,5] 可被视为重叠区间。
关键点分析：两个区间如何合并：

前提：有序区间集合items，以：s1，s2为例：

s1.left <= s2.left, s1.right < s2.right；

创建新的区间:res，并将s1添加到res中；

如果s1.right < s2.left, 则s1与s2没有重合；将s2添加新的集合中；

如果s1.right >= s2.left，则修改s1.right，s1.right = s2.right;

对其他的区间s3,s4..sn按照上面流程统一处理；

```python
def merge_list(intervals):
    if len(intervals)<=1:
            return intervals
    res=[]
    start = 0
    end = -1
    intervals = sorted(intervals,key = lambda item: item[start])
    res.append(intervals[0])

    for i in range(1,len(intervals)):
        if res[-1][end] < intervals[i][start]:
            res.append(intervals[i])
        elif intervals[i][end] > res[-1][end]:
            res[-1][end] = intervals[i][end]
    return res

l = [[1,3],[2,6],[8,10],[15,18]]
merge_list(l)
```

```
[[1, 6], [8, 10], [15, 18]]
```
### 37. 递归问题
递归函数
递归函数实质：

函数自身调用自身；

函数中必须有一个明确的结束条件；

递归函数限制：递归函数有层数限制；

Python中递归最大深度：

import sys
sys.getrecursionlimit()

N的阶乘
阶乘实现：

N! = N*(N-1)*(N-2)*(N-3)...*2*1

实现思路1：
正向循环

```python
def factorial(n):
    total = 1
    while n >= 1:
        total *=n
        n -= 1
    return total
factorial(5000)
```

实现思路2：
使用递归

```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)
factorial(5)
```

斐波那契（Fibonacci）数列
求斐波那契（Fibonacci）数列的第 n 项。

斐波那契数列的定义如下：

F(0) = 0
F(1) = 1
F(2) = F(1)+F(0)
F(3) = F(2)+F(1)
...
F(N) = F(N - 1) + F(N - 2)
其中 N > 1.

思路1：递归实现:
函数自己调用自身；

递归结束条件：n = 1；

代码实现：

```python
def fib_func(n):
    if n <= 1:
        return n
    return fib_func(n-1)+fib_func(n-2)
fib_func(10)
```

```
55
```

思路2：递推

初始值：a=1,b=1

f(2):1, b = a+b=2

f(3):2, b = a+b = 3

f(4):3, b = a+b = 5

f(5):5, b = a+b = 8

...

a b, = b, a+b；a为最后的值

```python
def fib_func(n):
    a,b=1,1
    if n == 0:
        return 0
    while n > 1:
        a,b = b, a+b
        n -= 1
    return a
fib_func(6)
```

计算和
求1+2+3+...+n，要求不能使用乘除法、for、while、if、else语句；

题目分析：使用递归与逻辑运算符

```python
def mysum(val):
    tmp = val
    tmp += val>0 and mysum(tmp -1)
    return tmp
mysum(10)
```

```
55
```

遍历多维列表
给定多维数字列表，找到大于x的所有数字：

例如：

l = [[1,2,3],[4],[2,3,4],[[4,5,6],[7],[1,2,3]]]
x = 5
结果：[6,7]
题目分析：

遍历列表；

判断列表元素是否是列表；

递归调用结束条件；

```python
nums = [0,[1,2,3],[4],[2,3,4],[[4,5,6],[7,[8,[9],[10]]],[1,2,3]]]
def find_x(nums, x, res):
    for item in nums:
        if isinstance(item, list):
            find_x(item, x, res)
        else:
            if item > x:
                res.append(item)
result = []
find_x(nums, 5, result)
result
```

```
[6, 7, 8, 9, 10]
```

实现列表全排列
一个例子：

[1,2,3]的全排列：
(1, 2, 3)
(1, 3, 2)
(2, 1, 3)
(2, 3, 1)
(3, 1, 2)
(3, 2, 1)

实现方式1：permutations

```python
from itertools import permutations
for item in list(permutations([1,2,3])):
    print(item)
```

实现方式2：递归实现

基本思路：

取第一个元素；后面元素做全排列；val1 + 剩余元素全排列

剩余元素全排列：重复上一个步骤，

截止条件：列表中只有一个元素，返回；

例如：

array = [1,2,3]
1. f([1,2,3])
2. 取第一个元素：1与f([2,3])进行操作；
3. 剩余元素操作：f([2,3])；
4. f(2,3)：取第一个元素，2与f([3])操作；
5. f(2,3)：取第二个元素，3与f([2])操作；
6. f(2，3)返回：[3]+[2]，[2]+[3];
7. 依次返回，得到最终结果；
具体如下图：

```python
def permutation(array):#全排列数组-通过递归
    output = []
    if len(array) == 1:
        return [array]#当数组只有一个元素时直接返回该数组
    else:
        for i in range(len(array)):
            sub_array = list(array)
            val = sub_array.pop(i)
            for item in permutation(sub_array):
                new_array = [val]+item
                output.append(new_array)

    return output

permutation([1,2,3])
```
### 38. 回溯算法
回溯法
回溯法（探索与回溯法）是一种选优搜索法，又称为试探法；

使用场景：
当需要找出解集或者什么解是满足某些约束条件的最佳解时，往往要使用回溯法。

回溯法实现：递归或者递推

特点：

程序结构明确，可读性强，易于理解，而且通过对问题的分析可以大大提高运行效率。

对于可以得出明显的递推公式迭代求解的问题，还是不要用回溯法，因为它花费的时间比较长。

三个概念：

约束函数

约束函数是根据题意定出的。通过描述合法解的一般特征用于去除不合法的解，从而避免继续搜索出这个不合法解的剩余部分

状态空间树

状态空间树是一个对所有解的图形描述，树上的每个子节点的解都只有一个部分与父节点不同。

扩展节点、活结点、死结点

扩展节点：就是当前正在求出它的子节点的节点，在DFS中，只允许有一个扩展节点；

活结点：通过与约束函数的对照，节点本身和其父节点均满足约束函数要求的节点；

死结点：不必求出其子节点

深度优先搜索（DFS）和广度优先搜索（BFS）

DFS(Depth First Search): 每一个可能的分支路径深入到不能再深入为止，而且每个节点只能访问一次；

Breadth First Search：属于一种盲目搜寻法，目的是系统地展开并检查图中的所有节点，以找寻结果;

实现步骤：

按选优条件向前搜索，以达到目标;

但当探索到某一步时，发现原先选择并不优或达不到目标，就退回一步重新选择;

这种走不通就退回再走的技术为回溯法，而满足回溯条件的某个状态的点称为“回溯点”。

组合总和
给定一个无重复元素的数组nums和一个目标数target，找出数组中所有可以使数字和为target的组合；

nums中的数字可以无限制重复被选取。

基本思想：对nums进行排序，从最小值开始探索一切可能；

基本步骤：

对nums排序；

取第一个元素，以第一个为基础，开始探索；

第一个元素与N个第一个元素相加；(v1+v1+v1+v1....)

第一个元素与第二个元素相加；(v1+v1+v1+v1+v2+..., v1+v1+v2+v2,....)

如果当前数字组合相加等于目标值，将当前组合加入 res；

如果当前数字加上当前和大于目标数，放弃当前数字，换成下一个数字。

如果当前数字之后的所有数字都太大，就返回到当前数字之前的那个数字，放弃它，换成下一个数字，再重复以上步骤。

截止条件：

当前组合和大于目标数；

当前数字索引大于nums长度；

找到目标值；

具体过程：

l = [2,3,6,7], target = 8
[]
[2]
[2, 2]
[2, 2, 2]
[2, 2, 2, 2]
[2, 2, 3]
[2, 3]
[2, 3, 3]
[2, 6]
[3]
[3, 3]
[6]
[7]

回溯函数接口：
def backtrack(nums, i, tmp, target, res):
  pass
nums：给定数字列表；
i：找到第几个元素；
tmp：列表，当前的数字组合；
target：目标值
res：列表，保存符合条件的组合

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
        backtrack(nums, j, tmp+[nums[j]], target, res)
    return res

l = [2,3,6,7]
x = 8
res = []
backtrack(l, 0, [],x, res)
```

括号生成
给定数字n，生成n对括号的所有可能有效组合。

例如：

输入：n = 3
输出：[
       "((()))",
       "(()())",
       "(())()",
       "()(())",
       "()()()"
     ]

题目分析：

括号左右成对；

括号中可以包含括号；

找到所有的可能组合；

基本思想：

左括号数量大于等于右括号；

左括号的个数最大为指定值n；

截止条件：左边与右边括号数都为n；

实现思路：

函数接口：gen_parenthesis(res, tmp, left, right)；

res用于存放符合规则的字符串；tmp为字符串变量，用于记录当前的值；

设置left与right数量为n;

如果left大于0， 则添加左括号；同时left-1,然后回调；

如果right > left, 则添加右括号；同时right-1,然后回调；

回调结束条件：left == 0 且 right == 0;

代码实现：

```python
def backtrack(res, tmp, left, right):
    if left == 0 and right == 0:
        res.append(tmp)
        return
    if left>0:
        backtrack(res, tmp+'(', left-1, right)
    if right > left:
        backtrack(res, tmp+')', left, right-1)
    return res

n = 4
res = []
backtrack(res, '', n, n)
```

全排列组合
给定一个没有重复数字的序列，返回其所有可能的全排列。

示例:

输入: [1,2,3]
输出:
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]
要求：使用回溯法实现

基本思想：

每个元素都要再组合的前面；

遍历nums索引，0<=i<len(nums)，创建nums副本tmp_list，每次从tmp_list中删除对应的索引i；

创建临时列表：[val], 开始递归调用自己；

结束条条件：nums的列表为空；

过程：

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

nums = [1,2,3,4]
res = []
permute(nums, res, [])
print(res)
```

```
[[1, 2, 3, 4], [1, 2, 4, 3], [1, 3, 2, 4], [1, 3, 4, 2], [1, 4, 2, 3], [1, 4, 3, 2], [2, 1, 3, 4], [2, 1, 4, 3], [2, 3, 1, 4], [2, 3, 4, 1], [2, 4, 1, 3], [2, 4, 3, 1], [3, 1, 2, 4], [3, 1, 4, 2], [3, 2, 1, 4], [3, 2, 4, 1], [3, 4, 1, 2], [3, 4, 2, 1], [4, 1, 2, 3], [4, 1, 3, 2], [4, 2, 1, 3], [4, 2, 3, 1], [4, 3, 1, 2], [4, 3, 2, 1]]
```

复原IP地址
给定一个只包含数字的字符串，复原它并返回所有可能的 IP 地址格式。

有效的 IP 地址 正好由四个整数（每个整数位于 0 到 255 之间组成，且不能含有前导 0），整数之间用 '.' 分隔。

例如："0.1.2.201" 和 "192.168.1.1" 是 有效的 IP 地址，但是 "0.011.255.245"、"192.168.1.312" 是无效的 IP 地址。

例如：

示例 1：
输入：s = "25525511135"
输出：["255.255.11.135","255.255.111.35"]
示例 2：
输入：s = "0000"
输出：["0.0.0.0"]
示例 3：
输入：s = "1111"
输出：["1.1.1.1"]
示例 4：
输入：s = "010010"
输出：["0.10.0.10","0.100.1.0"]
示例 5：
输入：s = "101023"
输出：["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]

基本思路
IP组成：[p1,p2,p3,p4]，每部分为0或者1~255；

每个P长度1位，2位，或者三位；

p1取第1位，2位，3位，然后找第二个p；

截止条件：原始字符串长度为0且tmp长度为4

```python
def restore_ip_addresses(s, res, tmp):
    if len(s) == 0 and len(tmp) == 4:
        res.append('.'.join(tmp))
        return
    for i in range(min(3, len(s))):
        #取前i位
        p = s[:i + 1]
        #剩余字符串内容
        new_s = s[i + 1:]
        #str(int(p)),若p长度大于1，且以开头，不是合法IP字段
        if p and 0 <= int(p) <= 255 and str(int(p)) == p:
            #寻找下一IP字段
            restore_ip_addresses(new_s, res, tmp + [p])

s = "101023"
res = []
restore_ip_addresses(s, res, [])
res
```

分割回文串
给定一个字符串s，将s分割成一些子串，使每个子串都是回文串。
返回s所有可能的分割方案。
例如：

输入: "aab"
输出:
[
  ["aa","b"],
  ["a","a","b"]
]

回溯法基本思想：

将字符串S切成AB两部分，如果A串为回文，继续切分B串，重复以上逻辑，切分后所有子串长度等于S,则符合规则；

查找过程：

函数接口：split_s(s, tmp, cur_lens, res, max_lens):pass

s:切分后的B串；

tmp：保留每次切分后的A串；

cur_lens:记录当前符合规则的子串长度；

res：保存所有的回文记录；

max_lens:原始字符串的长度；

实现步骤：

将s分成A=s[:i]，B=s[i:]

A如果不是回文，继续切分：A=s[:i+1], B=[i+1:]；

A如果是回文，将A添加到tmp, 并对B继续进行拆分；

split_s(B, tmp+[A], i, res, max_lens)；

如果cur_lens==max_lens说明找到一组回文串；

```python
def split_s(s, tmp, cur_lens, res, max_lens):
    if cur_lens == max_lens:
        res.append(tmp)
        return
    for i in range(1, len(s)+1):
        head = s[:i]
        if head != head[::-1]:
            continue
        split_s(s[i:], tmp+[head],cur_lens+i, res, max_lens)

s = 'aabb'
res = []
split_s(s, [], 0, res, len(s))
res
```

```
[['a', 'a', 'b', 'b'], ['a', 'a', 'bb'], ['aa', 'b', 'b'], ['aa', 'bb']]
```

将数组拆分成斐波那契序列
给定一个数字字符串 S，比如 S = "123456579"，我们可以将它分成斐波那契式的序列 [123, 456, 579]。

对于所有的0 <= i < F.length - 2，都有 F[i] + F[i+1] = F[i+2] 成立。

找到所有的组合

输入："123456579"
输出：[123,456,579]
基本思路：

先找到前两个数，第1个数从0开始，i表示第1个数第结束位置（不包含），第2个数从i开始，j表示第2个数结束位置；

第3个数从j开始，k表示结束位置；

如果num3 == num2 + num1，则保存到res中，继续往下找；否则，无法找到有效第序列，返回非法；i/j继续往下；

前两个数确定后，如果剩余的长度小于前两个数的长度，则i/j继续循环；

如果后面数的长度小于前两个数的长度，则此数抛弃，找到长度更长的数；

```python
def split_fibonacci(s, tmp, res):
    if len(s) == 0 and len(tmp)>2:
        res.append(tmp)
        return
    tmp_lens = len(tmp)
    if tmp_lens >=2:
        next_num = tmp[-1]+tmp[-2]
        next_str = str(next_num)
        if s.startswith(next_str):
            next_index = len(next_str)
            split_fibonacci(s[next_index:], tmp+[next_num], res)
    elif tmp_lens == 0:
        lens = len(s)
        for i in range(1, lens):
            suba = s[:i]
            numa = int(suba)
            subb = s[i:]
            lenb = len(subb)
            if i>1 and suba[0] == '0':
                break
            for j in range(1, lenb+1):

                tmpb = subb[:j]
                if j>1 and tmpb[0] == '0':
                    break
                numb = int(tmpb)
                split_fibonacci(subb[j:], tmp+[numa, numb], res)
s = '1101111'
res = []
split_fibonacci(s, [], res)
res
```

```
[[11, 0, 11, 11], [110, 1, 111]]
```

```python
def split_fib(s, tmp):
    lens = len(s)
    if lens == 0:
        print(tmp)
        return
    if len(tmp)>1:
        next_num = tmp[-1]+tmp[-2]
        next_str = str(next_num)
        if s.startswith(next_str):
            split_fib(s[len(next_str):], tmp+[next_num])
    else:
        for i in range(1, lens):
            stra = s[:i]
            inta = int(stra)
            subb = s[i:]
            #1, 0
            #1.01 无效
            if len(stra)>1 and stra[0] == '0':
                break
            for j in range(1, len(subb)):
                strb = subb[:j]
                intb = int(strb)
                split_fib(subb[j:], tmp+[inta, intb])
```

```python
s = '1101111'
res = []
split_fib(s, [])
```

```
[11, 0, 11, 11]
[110, 1, 111]
```
### 39. 动态规划
动态规划
基本思想
一个决策的前面若干步骤已经确定，从而进入某种状态之后，后面的步骤从按照当前状态开始的最优解必然是整体（包括该状态的情况下）的最优解，则该问题满足最优原理。换个说法：在求解（整体问题）的最优解的时候，后面的步骤选择只与当前状态有关，而与如何到达这个状态的步骤无关。

动态规划特点
对每个子问题只求解一次，并将结果保存下来。如果随后再次需要此子问题的解，只需查找保存的结果，而不必重新计算。因此动态规划算法是付出额外的内存空间来节省计算时间，是典型的时空权衡的例子。

动态规划特性

最优化原理：如果问题的最优解所包含的子问题的解也是最优的，就称该问题具有最优子结构，即满足最优化原理。

无后效性：某阶段状态一旦确定，就不受这个状态以后决策的影响。也就是说，某状态以后的过程不会影响以前的状态，只与当前状态有关。

有重叠子问题：即子问题之间是不独立的，一个子问题在下一阶段决策中可能被多次使用到。
#### 动态规划要素：
动态规划有三要素：阶段、状态和决策。

阶段：

把一个问题的过程，恰当地分为若干个相互联系的阶段，以便于按一定的次序去求解。

描述阶段的变量称为阶段变量。阶段的划分，一般是根据时间和空间的自然特征来进行的，但要便于问题转化为多阶段决策。

状态：

表示每个阶段开始所处的自然状况或客观条件。

决策：

从前一个阶段转化到后一个阶段之间的递推关系,状态转义公式；

动态规划步骤

设计状态变量：对于状态变量的设计可以采取一维状态变量dp[i]和二维状态变量dp[i][0],dp[i][1]。

确定状态转移方程

初始化变量

考虑输出

整了一大堆概念，来看一个基本例子

最大子序和
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

示例:

输入: [-2,1,-3,4,-1,2,1,-5,4]
输出: 6
解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。

暴力破解法：
以第一个元素开始，计算从前向后的所有组合的和，记录最大值；

以第二个元素开始，计算从前向后的所有组合的和，记录最大值；

依次类推，获取最大值；

代码实现：

```python
def max_sub_array(array):
    lens = len(array)
    max_val = nums[0]
    for i in range(lens):
        max_val = max(max_val , array[i])
        for j in range(i+1, lens):
            max_val = max(max_val, array[j])
            print(array[i:j+1])
            sub_sum = sum(array[i:j])
            max_val = max(max_val, sub_sum)
    return max_val

nums = [-2,1,-3,4,-1,2,1,-5,4]
max_sub_array(nums)
```

最长回文子串
给定一个字符串 s，找到 s 中最长的回文子串;

回文串:给定字符串S，S倒序后与S相同:

示例 1：

输入: "babad"
输出: "bab"
注意: "aba" 也是一个有效答案。
示例 2：

输入: "cbbd"
输出: "bb"

动态规划基本思路：

原始字符串为S，子串为subs, 表示为：subs = s[i,...,j]，使用dp[i][j]表示该位置状态；

如果subs为回文串，则：dp[i,j]=1，同理,s[i+1,...j-1]也是回文串， 则：dp[i+1, j-1]=1；

以上问题拆分为一系列子问题，当前状态有子上一个问题与当前比较结果决定；

状态方程：

如果S[i]=S[j]，如果S[i+1...j-1]是回文串，则S[i...j]也是回文串；

如果S[i+1...j-1]不是回文串，则str[i...j]不是回文串；

初始状态：dp[i][j]=1

依次遍历字符串开始对s进行处理

```python
def longest_palindrome(s):
    lens = len(s)
    line = [0]* lens
    max_lens = 0
    max_str = ''
    #构建N*N矩阵
    matrix = [list(line) for i in range(lens)]
    for i in range(0, lens):
        for j in range(0, i+1):
            if i - j <=1 :
                print(i, j)
                if s[i] == s[j]:
                    matrix[j][i] = 1
                    if max_lens < i - j +1:
                        max_lens = i - j +1
                        max_str = s[j:i+1]
            else:
                if s[i] == s[j] and matrix[j+1][i-1]:
                    matrix[j][i] = 1
                    if max_lens < i - j +1:
                        max_lens = i - j +1
                        max_str = s[j:i+1]
    return max_lens, max_str
```

等差数列划分
统计给定数组中为等差数列的子数组个数。

示例:
A = [1, 2, 3, 4]
返回: 3, A 中有三个子等差数组: [1, 2, 3], [2, 3, 4],[1, 2, 3, 4]。
题目分析，核心点：

等差数列条件：nums[i]-nums[i-1] = nums[i-1]-nums[i-2]

状态方程：如果nums[i]满足上面条件，则：dp[i] = dp[i-1]+1;

结果：sum(dp)

例如：

A = [1, 2, 3, 4]
dp = [0,0,1,2]
最终结果：sum(dp) = 3

```python
def count_slices(nums):
    lens = len(nums)
    if lens < 3:
        return 0
    dp = [0] * lens
    for i in range(2, lens):
        if nums[i] - nums[i-1] == nums[i-1] - nums[i-2]:
            dp[i] = dp[i-1]+1
    return sum(dp)

A = [1, 2, 3, 4]
count_slices(A)
```

```
3
```

三角形最小路径和
给定一个三角形，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上。

相邻的结点：下标与上一层结点下标相同或者等于上一层结点下标+1的两个结点。

例如，给定三角形：

[
  [2],
  [3,4],
  [6,5,7],
  [4,1,8,3]
]
自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）；

建议使用O(n) 的额外空间（n 为三角形的总行数）来解决这个问题；

分析：
该题目为动态规划问题；

上下层之间关系：
   2
   | \
   3  4
   | \| \
   6  5  7
   | \| \| \
   4  1  8  3

关键点：使用dp记录每层的步骤；

具体步骤：

三角矩阵定义为：t；每层步骤保存：dp = [0]*len(t)
第一层：i = 0, dp=[2,0,0,0]

第二层：i = 1：dp = [t[1][0]+dp[0], t[1][1]+dp[0]]

第三层：i = 2,焦虑交叉问题：
状态方程
j = [i,i-1,...,0]
j == i: dp[j] = t[i][j] + dp[j-1]
j != i: dp[j] = t[i][j] + min(dp[j],dp[j-1])
j == 0: dp[j] = t[i][j] + dp[j]

第N层也遵循以上逻辑；

结果：min(dp)

```python
def minimum_total(triangle):

    max_dp = len(triangle)
    if max_dp == 0:
        return 0
    dp = [0] * max_dp
    #设置第一个值
    dp[0] = triangle[0][0]
    #从第i行开始查找
    for i in range(1, max_dp):
        j = i
        while j>=0:
            if j == 0:
                dp[j] = dp[j] + triangle[i][j]
            elif j == i:
                #最新的值等于当前行最右侧值+上一行前一列值；
                dp[j] = dp[j-1] + triangle[i][j]
            else:
                dp[j] = triangle[i][j] + min(dp[j-1], dp[j])
            j -= 1
        print(dp)

    return min(dp)

t = [[2],
    [3,4],
   [6,5,7],
  [4,1,8,3],]
t = [[2]]
minimum_total(t)
```

最大正方形
在一个由 '0' 和 '1' 组成的二维矩阵内，找到只包含 '1' 的最大正方形，并返回其面积。

示例：

输入：
matrix = [["1","1","1","0","0"],
          ["1","1","1","0","1"],
          ["1","1","1","0","0"],
          ["0","0","0","1","1"],
          ["0","0","0","1","1"]]

输出：9
正方形例子：

第一行，数字为1则为正方形；

第一列, 数字为1则为正方形，

第二行第二列，dp[i,j]若为1，开始找规律；

dp[i-1,j-1],dp[i-1,j],dp[i,j-1],如果都为1，则dp[i,j]为2x2的正方形；记为2；

dp[i-1,j-1],dp[i-1,j],dp[i,j-1],如果都为2，则dp[i,j]为3x3的正方形；记为3；

dp[i-1,j-1],dp[i-1,j],dp[i,j-1],如果都为0，则dp[i,j]为1x1的正方形；记为1；

规律：如果dp[i,j]为1，dp[i,j]状态由dp[i-1,j-1],dp[i-1,j],dp[i,j-1]决定；

状态方程：dp[i,j] = min(dp[i-1,j-1],dp[i-1,j],dp[i,j-1])+1；

具体如下图：

```python
def max_square( matrix):
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return 0

    max_size = 0
    #计算行列
    rows, columns = len(matrix), len(matrix[0])
    #初始化dp
    dp = [[0] * columns for _ in range(rows)]
    #遍历行
    for i in range(rows):
        #遍历列
        for j in range(columns):
            #如果遇到'1',开始计算最大size
            if matrix[i][j] == '1':
                #如果当前位置处于第一行或者第一列，设置dp[i][j] = 1
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    #根据其他三个位置size计算当前位置size
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                    #更新max_size
                max_size = max(max_size, dp[i][j])

    return max_size * max_size
matrix = [["1","1","1","0","0"],
          ["1","1","1","0","1"],
          ["1","1","1","0","0"],
          ["0","0","0","1","1"],
          ["0","0","0","1","1"]]

max_square(matrix)
```

丑数
编写一个程序，找出第 n 个丑数。

丑数就是质因数只包含 2, 3, 5 的正整数。

示例:
输入: n = 10
输出: 12
解释: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12 是前 10 个丑数。
说明: 1是丑数
题目分析：
每个丑数都是由2,3,5相乘组成，
例如：1,2,3,2x2,5,2x3,2x2x2, 3x3, ....组成；

核心：每个数都要与2,3,5相乘；

初始化dp = [1]

初始化i2,i3,i5索引，均为0；

i2对应的值只能与2相乘，i3对应的值智能与3相乘，i5对应的值只能与5相乘；

每次插入的丑数：min(dp[i2]x2,dp[i3]x3,dp[i5]x5);

最小值对应的dp[ix]加1；保证每个数循环与2,3,5相乘；

```python
def ugly_n(n):
    nums = nums = [1, ]
    i2 = i3 = i5 = 0
    for i in range(0, n):
        #保留i2，i3,i4对应的值
        tmp = [nums[i2] * 2, nums[i3] * 3, nums[i5] * 5]
        #获取最小值
        ugly = min(tmp)
        nums.append(ugly)

        if ugly == tmp[0]:
            #最小值与tmp[0]对应，i2+1
            i2 += 1
        if ugly == tmp[1]:
            #最小值与tmp[1]对应，i3+1
            i3 += 1
        if ugly == tmp[2]:
            #最小值与tmp[2]对应，i5+1
            i5 += 1
    return nums
array = ugly_n(25)
array
```

买卖股票的最大利润
给定一个数组列表，它的第i个元素是一支给定股票第 i 天的价格。

这一期间内最多只允许完成一笔交易（即买入和卖出一支股票一次）， 计算所能获取的最大利润。

注意：你不能在买入股票前卖出股票。

示例：

例1：
输入: [7,1,5,3,6,4]
输出: 5
解释: 在第2天(股票价格 = 1)的时候买入，在第5天（股票价格=6）的时候卖出，最大利润：6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。
例2：
输入: [7,6,4,3,1]
输出: 0
解释: 在这种情况下, 没有交易完成, 所以最大利润为0。

思路1：

记录当前索引前最小值，min_val = nums[0], max_perfit = 0;

遍历nums，

当前值小于最小值，不产生交易，min_val = 当前值；

当前值大于最小值，可以产生交易，当前值减去最小值即为当天收益cur_perfit,

最大收益：max_perfit = max(max_perfit, cur_perfit)

代码实现：

```python
def max_perfit(nums):
    lens = len(nums)
    min_val = nums[0]
    maxPerfit = 0
    for val in nums:
        if val <= min_val:
            min_val = val
        else:
            cur_perfit = val - min_val
            maxPerfit = max(maxPerfit, cur_perfit)
    return maxPerfit

array =  [7,1,5,3,6,4]
max_perfit(array)
```

思路2，使用动态规划：
状态方程：

$$
dp[i]=\begin{cases}
dp[i-1],&if(nums[i] <= min\_val), min\_val = nums[i]\\max(dp[i-1],nums[i]-min\_val) &if(nums[i] > min\_val)
\end{cases}
$$代码实现：

```python
def max_perfit(nums):
    lens = len(nums)
    min_val = nums[0]
    maxPerfit = 0
    dp = [0] * lens
    for i,val in enumerate(nums):
        if val <= min_val:
            min_val = val
            dp[i] = dp[i-1]
        else:
            dp[i] = max(dp[i-1], val - min_val)
    return dp[-1]

array =  [7,1,5,3,6,4]
max_perfit(array)
```

```
5
```

买卖股票最佳时机2
给定数字列表，代表某只股票价格；

需求：最多可以完成两笔交易,计算可以获取最大利益；

注意: 不能同时参与多笔交易(必须在再次购买前出售掉之前的股票)；

示例 1:
输入: [3,3,5,0,0,3,1,4]
输出: 6
解释: 在第4天(股票价格=0)的时候买入，在第6天(股票价格=3)的时候卖出，这笔交易所能获得利润:3-0=3；
    在第7天(股票价格=1)的时候买入，在第8天(股票价格=4)的时候卖出，这笔交易所能获得利润:4-1=3；

示例 2:
输入: [1,2,3,4,5]
输出: 4
解释: 在第1天(股票价格=1)的时候买入,在第5天(股票价格 = 5)的时候卖出,这笔交易所能获得利润:5-1=4；
    注意不能在第1天和第2天接连购买股票，之后再将它们卖出。
    因为这样属于同时参与了多笔交易，你必须在再次购买前出售掉之前的股票。

示例 3:
输入: [7,6,4,3,1]
输出: 0
解释: 在这个情况下，没有交易完成,，所以最大利润为0。

问题：如果计算出第一次收益，如何计算第二次的收益？
状态划分：

某一天无交易：当天价格低于买入价格，不产生交易，当天收益为前一天的收益；

某一天产生交易：收益：第一次收益与当天交易利润和。

核心点：如何找到第二次买入与卖出点？需要理解股票交易过程；

第一次交易产生利润记为：perfit_1；

第二次买入的成本：min_cost = 当天的股票价格-当前收益；

目标：找到第一次交易后，买入的最低成本

动态规划,

创建dp,记录每天交易次数与交易次数收益；

$dp[i*j]$：$i$：代表某天，范围：$[1,len(num)-1]$，$j$：代表最大交易次数$[1,2,3...n]$；

第0次交易收益都是0；

状态方程：

$$
\begin{cases}
min\_cost = nums[i] - dp[i-1][j-1]\ 注意：(dp[i-1][j-1]：代表前一天上一次卖出收益，因为必须先卖在买)\\dp[i][j] = max(dp[i-1][j], nums[i] - min\_cost)
\end{cases}
$$

```python
def max_perfit_2(prices):
    if not prices:
        return 0
    n = 3
    row, col = len(prices), n
    line = [0 for i in range(col)]
    dp = [list(line) for i in range(row)]
    for j in range(1,n):
        min_cost = prices[0]
        for i in range(1, row):
            min_cost = min(min_cost, prices[i] - dp[i-1][j-1])
            dp[i][j] = max(dp[i-1][j], prices[i]-min_cost)
    return dp[row-1][n-1]
```

0-1背包问题：
给定n种物品和一个容量为$C$的背包，物品i的重量是$wi$，其价值为$vi$;

应该如何选择装入背包的物品，使得装入背包中的物品的总价值最大？

先找到如何存放使得物品价值最大
动态规划基本思路：

对每一件物品遍历背包容量，当背包可容纳值大于等于当前物品，与之前已放进去的物品所得价值进行对比，考虑是否需要置换。

通俗理解：

背包容量为$W_{bag}=(1,2,3,....n)$, 物品数量为$C$,每个物品重量为$w_i$,价格为$v_i$;

构建矩阵$dp[n*C]$，所有物品按照顺序放入背包；

第一轮：放入第一件物品，背包容量从1到N，背包容量大于等于物品重量，可以放入该物品，否则不能放入；

结果：第一行数据：背包容量从$1~n$, 可以存放第一件物品的价格；

第二轮：放入第二件物品，背包容量从1到N，背包容量大于等于物品重量，可以放入费物品，否则不能放,当前价值为第一件物品存放价格；

到这里引发一个问题：背包中已经存放物品1或者其他物品，接下来怎么放？

问题1：背包相同从0到N，在某个容量下，我们已经放入物品1， 那么物品2怎么办？

在容量确认情况下，背包中已经存在物品1，取物品1与物品2价格较高的值；

问题2：背包容量大于当前物品重量，怎么放？

放入第二件物品，同时还能放入其他物品；

放入重量：$W_{diff} = W_{bag}-W_2$；

总体价格：$V_{cur}=V_i+dp[0,W_{bag}-W_2]$；

和第一次放入价格对比，最终价格：$max(dp[i-1, w], V_{cur})$

通过上述存放，我们可以得到每次放入物品后，能够存放的最高价格；

通过以上描述得到状态方式：

$$
dp[i, W_{bag}]=\begin{cases}
0,&if(i\ ==\ 0\ or\ W_{bag-j}\ ==\ 0) \\ dp[i-1, w],&if(w_i\ >\ W_{bag-j}) \\max(dp[i-1, W_{bag-j}-w_i]+V_i, dp[i-1, w]) &if(i>0\ and\ W_{bag-j}>=w_i)
\end{cases}
$$$$W_{bag}:包的容量，w_i:商品的重量$$

```python
def bag(n, c, w, v):
    # 置零，表示初始状态
    dp = [[0 for j in range(c + 1)] for i in range(n + 1)]

    for i in range(1, n + 1):
        #背包容量：1~N
        for j in range(1, c + 1):
            dp[i][j] = dp[i - 1][j]
            # 背包总容量够放当前物体，遍历前一个状态,考虑是否置换
            if j >= w[i - 1]:
                #当前背包容量大于商品重量
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w[i - 1]] + v[i - 1])
    for x in dp:
        print(x)
    return dp

n = 5
c = 10
#物品重量
w = [2, 2, 3, 1, 5]
#物品价格
v = [2, 3, 1, 5, 4]
bag(n,c,w,v)
```

```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2]
[0, 0, 3, 3, 5, 5, 5, 5, 5, 5, 5]
[0, 0, 3, 3, 5, 5, 5, 6, 6, 6, 6]
[0, 5, 5, 8, 8, 10, 10, 10, 11, 11, 11]
[0, 5, 5, 8, 8, 10, 10, 10, 12, 12, 14]
```

```
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
 [0, 0, 3, 3, 5, 5, 5, 5, 5, 5, 5],
 [0, 0, 3, 3, 5, 5, 5, 6, 6, 6, 6],
 [0, 5, 5, 8, 8, 10, 10, 10, 11, 11, 11],
 [0, 5, 5, 8, 8, 10, 10, 10, 12, 12, 14]]
```

```python
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
 [0, 0, 3, 3, 5, 5, 5, 5, 5, 5, 5],
 [0, 0, 3, 3, 5, 5, 5, 6, 6, 6, 6],
i-1: [0, 5, 5, 8, 8, 10, 10, 10, 11, 11, 11],
 i：[0, 5, 5, 8, 8, 10, 10, 10, 12, 12, 14]]
```

找到放入哪些物品

前提：获取物品放入的状态；

规律：如果$dp[i][c]!=dp[i-1][c]$,说明将物品i放入背包；c为背包容量；

更新c:$c -= w_i$

从最后一轮开始找，最大容量开始找；

```python
def bag(n, c, w, v):
    # 置零，表示初始状态
    dp = [[0 for j in range(c + 1)] for i in range(n + 1)]

    for i in range(1, n + 1):
        #背包容量：1~N
        for j in range(1, c + 1):
            dp[i][j] = dp[i - 1][j]
            # 背包总容量够放当前物体，遍历前一个状态,考虑是否置换
            if j >= w[i - 1]:
                #当前背包容量大于商品重量
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w[i - 1]] + v[i - 1])
    for x in dp:
        print(x)
    #包的容量
    max_c = c
    #记录存入物品
    res = [0]*(n+1)
    while n>0:
        #本次放入价格与上一次放入不同，说明放入该物品
        if dp[n][max_c] != dp[n-1][max_c]:
            res[n] = 1
            #容量减去当前物品容量
            max_c -= w[n-1]
        n -= 1
    print(res)
    return res[1:]

n = 5
c = 10
#物品重量
w = [2, 2, 3, 1, 5]
#物品价格
v = [2, 3, 1, 5, 4]
bag(n,c,w,v)
```

```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2]
[0, 0, 3, 3, 5, 5, 5, 5, 5, 5, 5]
[0, 0, 3, 3, 5, 5, 5, 6, 6, 6, 6]
[0, 5, 5, 8, 8, 10, 10, 10, 11, 11, 11]
[0, 5, 5, 8, 8, 10, 10, 10, 12, 12, 14]
[0, 1, 1, 0, 1, 1]
```

```
[1, 1, 0, 1, 1]
```
### 40. 贪心算法
贪心算法基础概念
基本概念
贪心算法又称贪婪算法，是一种在每一步选择中都采取在当前状态下最好或最优（即最有利）的选择，从而希望导致结果是最好或最优的算法。

贪心算法理解：在有最优子结构的问题中尤为有效,最优子结构的意思是局部最优解能决定全局最优解；直白理解：贪心算法在求解某个问题时，总是做出眼前的最大利益，也就是说只顾眼前不顾大局，所以他是局部最优解。

贪心法解决问题：图中的最小生成树、哈夫曼编码……对于某些问题，贪心法一般不能得到我们所要求的答案。

贪心算法问题：不能对所有问题都能得到整体最好的解决办法；

贪心算法两个重要的特点是：

贪心策略：选择的贪心策略必须具备无后效性，即某个状态以前的状态不会影响以后的状态，只与当前状态有关；

通过局部最优解能够得到全局最优解；

贪心算法与动态规划异同

相同点：

都是一种推导算法；

都可以分解成子问题来求解，都需要具有最优子结构；

不同点：

贪心策略是由上一步的最优解推导下一步的最优解，而上一部之前的最优解则不作保留，动态规划记录所有的局部最优解；

贪心算法：从上向下遍历最优子树；动态规划：自底向上（从叶子向根）构造子问题的解；

贪心算法不能保证获解释最优的，复杂度低；动态规划本质为穷举法，能够获取最佳解，复杂度高；

跳跃游戏
给定一个非负整数数组，你最初位于数组的第一个位置;

数组中的每个元素代表你在该位置可以跳跃的最大长度;

目标：是使用最少的跳跃次数到达数组的最后一个位置;

示例：

示例 1:
输入: [2,3,1,1,4]
输出: 2；
题目分析：以示例1为例

当前可以跳跃步骤为1,2；

按照每次跳跃最大值计算，需要跳跃索引：0,2,3,4，跳跃3次，并非最优策略；

使用贪心算法：以示例1为例，

当前索引为0，对应的跳跃值为2，最大跳跃长度为2；

索引为0的前提下，下一次跳跃值为：[1+3, 2+1]；

目标：找到调的最远的位置(注意：截止条件，跳跃到最后一个位置)

核心点：找到当前跳跃值与下一次跳跃的值相加的最大值；

具体过程如下图：

```python
def can_junp(nums):
    n = len(nums)
    count = 0
    if n <= 1:
        return count

    #i:记录当前位置
    i = 0
    while i < n:
        #已经跳到最后一个位置，直接退出查找
        if i >= n-1:
            break
        #当前位置+下一次跳跃位置大于列表长度，直接结束；
        tmp = i + nums[i]
        if tmp >= n-1:  #当前位置i不是最后一个位置，所以还需要再跳一步
            count += 1
            break
        max_jump = 0
        #移动一个步骤
        index = i+1
        for j in range(i+1, tmp+1):
            #下一步跳跃位置为0，直接跳过
            next_post = j + nums[j]
            if nums[next_post] == 0:
                continue
            #更新max_jump
            if next_post >= max_jump:
                max_jump = next_post
                #更新j
                index = j
        #重置i
        i = index
        count += 1
    return count

nums = [2,3,1,1,4]
can_junp(nums)
```

```
2
```

实现思路2：
明确目标：统计跳跃的最少次数；遍历nums进行统计；

第一个起跳点可以跳跃的最大距离是$m$，表示后面$m$个格子都可以作为新的起跳点，下一条最远距离：$i+m$；

从该点起跳，为第一次起跳；从后面$m$个格子起跳都可以叫做第$2$次跳跃；

第一条结束为止：end = $i+m$;

在$i~i+m$元素中，可以跳跃的最远的距离记为max_post;

遍历nums,如果$i==end$，需要跳跃，并且重置$end=max\_post$

```python
def can_jump(nums):
    lens = len(nums)
    if lens <= 1:
        return 1
    step, end, max_post = 0, 0, 0
    for i in range(lens-1):
        max_post = max(max_post, i+nums[i])
        if i == end:
            step += 1
            end = max_post
    return step

nums = [2,3,1,1,4,5]
can_jump(nums)
```

```
2
```

找零钱问题
商店卖东西，找给顾客零钱，零钱面值：$[20,10,5,1]$，给定数值x, 找出最少的钱币数量；
例如：

示例1：
输入：x = 25；
输出：2；说明，1张20元，一张5元；
实现思路：尽可能给金额较大数量的钱币；

给定零钱数：x；

20对应的数量：x//20；剩余钱币：x=x%20;

10对应的数量：x//10；剩余钱币：x=x%10;

一次类推，直到x为0；

```python
def give_money(x):
    mlist = [20, 10, 5, 1]
    nums = []
    for i in mlist:
        nums.append(x//i)
        x%=i
    return sum(nums,), nums
give_money(30)
```

```
(2, [1, 1, 0, 0])
```

过河问题
N个人过河，船每次只能坐两个人，每个人过河的所需时间不同$speed[i]$；
每次过河的时间为船上的人的较慢的那个,求最快的过河时间。(船划过去要有一个人划回来)

不同人数过河解决方式：

1.将所有人按找过河时间从小到大排序；

当N=1时，results=speed[0]；

当N=2时，results=speed[1]；

当N=3时，results=speed[0]+speed[1]+speed[2]；速度最快前$p1,p2$过河,$p1$返回去接$p3$，$p3,p1$过河;

当N=>4时，把过河所需要时间最多的两个人送到对岸，有两种方式：

1）最快两人过河，最快返回；最慢两个人过河，次快返回，所需时间为：$speed[0]+2*speed[1]+speed[n-1]$；

2）最快最慢的过河，最快返回，最快次慢过河，最快返回，所需时间为：$2*speed[0]+speed[n-2]+speed[n-1]$；

如果剩余人数为小于3，重复以上步骤；

具体实现代码如下所示：

```python
def cross_river(array):
    n = len(array)
    array.sort()
    sp_times = 0

    splist = array[::]
    while n>=4:
        #第一种耗时
        ts1 = 2 * splist[0] + splist[n-1] + splist[n-2]
        #第二种耗时
        ts2 = 2 * splist[1] + splist[0] + splist[n-1]
        #选择耗时较少的方式
        sp_times += min(ts1, ts2)
        #每次岸边人数减2
        splist = splist[:-2]
        n-=2
    if n == 3:
        #三人时间
        sp_times += splist[0]+splist[1]+splist[2]
    elif n == 2:
        sp_times += splist[1]
    else:
        sp_times += splist[0]
    return sp_times
s =[1,2,3,4,5]
cross_river(s)
```

```
16
```
### 41. 分治算法
分治算法

分治法：

把复杂的1个问题分成两个或多个相同或相似的子问题，再把子问题分成更小的子问题，直到最后子问题可以简单地直接求解，原问题的解即子问题的解的合并；

基本思想：

将一个难以直接解决的大问题，分割成一些规模较小的相同问题，以便各个击破，分而治之。

分治策略：

对于一个规模为n的问题，若该问题规模小可以直接解决，否则将其分解为k个规模较小的子问题；

K个子问题互相独立且与原问题形式相同，可以递归或者递推地解决这些子问题，

将各个子问题的解合并得到原问题的解;

如果不满足上述条件，考虑使用贪心算法或者动态规划；

分治法的基本步骤

分解：将原问题分解为若干个规模较小，相互独立，与原问题形式相同的子问题

解决：若子问题规模较小而容易被解决则直接解，否则递归地解各个子问题

合并：将各个子问题的解合并为原问题的解

分治法解决常见问题：

二分搜索；

大整数乘法；

合并排序；

快速排序；

线性时间选择；

最接近点对问题；

循环赛日日程等；

漂亮的数组
对于某些固定的N，如果数组A由1~n组成，A满足下面条件：

对于每个i<j，都不存在k满足i<k<j使得A[k] * 2 = A[i] + A[j]；那么数组A是漂亮数组。

需求：给定 N，返回任意漂亮数组 A（保证存在一个）。

示例1：
输入：4
输出：[2,1,4,3]
示例 2：
输入：5
输出：[3,1,2,5,4]

基本思路：
漂亮数组+漂亮数组=漂亮数组；

如果一个数组不是漂亮数组，将其拆分，然后进行拼接；

按照奇偶取值，将数组拆分成两份；

对子数组进行拆分，如果子数组数量小于等于2，合并数组；

例如：对[1,2,3,4,5,6,7]进行处理：

[1,3,5,7]->[1,5] + [3,7]->[1,5,3,7]

[2,4,6]->[2,6] + [4]->[2,6,4]

[1,5,3,7] + [2,6,4]->[1,5,3,7,2,6,4]

基本思路：
漂亮数组+漂亮数组=漂亮数组；
如果一个数组不是漂亮数组，将其拆分，然后进行拼接；

按照奇偶取值，将数组拆分成两份；

对子数组进行拆分，如果子数组数量小于等于2，合并数组；

例如：对[1,2,3,4,5,6,7]进行处理：

```python
def split_list(nums):
    if len(nums) <= 2:
        return nums
    left = split_list(nums[::2])
    right = split_list(nums[1::2])
    return left+right
n = 10
split_list(list(range(1,n+1)))
```

```
[1, 9, 5, 3, 7, 2, 10, 6, 4, 8]
```

为运算表达式设计优先级
给定一个含有数字和运算符的字符串，为表达式添加括号，改变其运算优先级以求出不同的结果。

需要给出所有可能的组合的结果，有效的运算符号包含'+/-/*'。

示例 1:
输入: "2-1-1"
输出: [0, 2]
解释:
((2-1)-1) = 0
(2-(1-1)) = 2

示例 2:
输入: "2*3-4*5"
输出: [-34, -14, -10, -10, 10]
解释:
(2*(3-(4*5))) = -34
((2*3)-(4*5)) = -14
((2*(3-4))*5) = -10
(2*((3-4)*5)) = -10
(((2*3)-4)*5) = 10
分治法实现：

整体分解：按运算符分成左右两部分，分别求解；

子问题处理：递归调用，对子问题进行处理，直到只剩下数字，并根据运算符计算对应的解

子结果合并：根据运算符合并左右两部分的解，得出最终解

具体过程：

s = "2*3-4*5"为例；

s第一次拆分：left = 2, right = 3-4*5；

对right进行拆分，left=3, right=4*5；或者left=3-4, right = 5；

right可以产生两个值，left分别对两个值进行操作，并保留结果；

重复上面步骤对s继续拆分；

```python
def diff_ways_compute(s):
    # 如果只有数字，直接返回
    if s.isdigit():
        return [int(s)]
    res = []
    for i, char in enumerate(s):
        if char in ['+', '-', '*']:
            #1.遇到运算符，分解字符串，计算左右两侧的结果集；
            #2. 递归调用，计算子问题的结果；
            left = diff_ways_compute(s[:i])
            right = diff_ways_compute(s[i+1:])
            #3.合并结果：根据左右计算结果与运算符合并子问题结果
            for l in left:
                for r in right:
                    if char == '+':
                        res.append(l + r)
                    elif char == '-':
                        res.append(l - r)
                    else:
                        res.append(l * r)
    return res
s = "2*3-4*5"
diff_ways_compute(s)
```

```
[-34, -10, -14, -10, 10]
```

```python
def diff_ways_compute(s):
    # 如果只有数字，直接返回
    if s.isdigit():
        return [int(s)]
    res = []
    for i, char in enumerate(s):
        if char in ['+', '-', '*']:
            #1.遇到运算符，分解字符串，计算左右两侧的结果集；
            #2. 递归调用，计算子问题的结果；
            left = diff_ways_compute(s[:i])
            right = diff_ways_compute(s[i+1:])
            #3.合并结果：根据左右计算结果与运算符合并子问题结果
            for l in left:
                for r in right:
                    if char == '+':
                        res.append(l + r)
                    elif char == '-':
                        res.append(l - r)
                    else:
                        res.append(l * r)
    return res
s = '2-3+5*2'
diff_ways_compute(s)
```

```
[-11, -14, 9, -12, 8]
```

```python
(2-3)+5*2
```

```python
2-
```
## 附录 合并版 PDF（与正文章节内容有重复）
### 42. 附录 A：PDF合并PY1（Python 入门综合）
主要内容  
1. 为什么学习 Python ？ 
2. 如何选择安装版本？ 
3. 开发工具选择？ 
4. 第三方模块如何管理？ 

#### 1 零基础为什么推荐学习 Python?  
一句话：应用领域广，就业市场大，学习成本低； 
#### 2 Python 版本选择  
我们可以选择安装： Python ， MiniConda ， Anaconda
#### 2.1 Windows 下官网 Python 安装  
主要步骤： 
1. 下载安装包，地址： https://www.python.org/
2. 根据本机系统选择版本并下载； 
3. 双击安装，并配置环境变量； 
4. 测试是否安装成功；

#### 2.1.1 版本选择  
两个问题： 
1. 系统：根据不同系统选择对应的安装包； 
2. 版本： Python 有多个版本，建议下载 Python3.6 及以上版本； 
下载页面如下： 
注意： 
1. Python3.9 及以上版本不支持 Windows7
2. 如果 Windows 系统中想要安装 Python3.7 版本，可以点击 Widnows ，选择版本进行下载安装 
#### 2.1.2 安装过程  
安装方式： 
1. 选中复选框，将 Python 安装路径添加到环境变量； 
2. 可以选择 Python 的安装路径； 
如果安装过程中，如果没有选中： "Add Python 3.10 To PATH" ，需要做下面操作； 

#### 2.1.3 配置环境变量  
#### 1 ）打开系统变量： 
window10 下的操作：

#### 2 ）添加环境变量 
#### 2.1.4 验证  
#### 1 ）打开 " 命令提示符 "

#### 2 ）测试： 
到这里 Python 开发环境安装完成； 

#### 2.2 Anaconda 与 Miniconda  
Anaconda ：如果想要从事数据分析，数据挖掘，推荐安装 Anaconda
1. 下载地址： https://www.anaconda.com
2. Anaconda 安装方式与 Python 类似， 
3. Anaconda 是 Python 与科学计算包的组合，其内部的 Python 版本比官网慢； 
4. 注意点： Anaconda 在安装时候，推荐选择添加环境变量，如下图：

Miniconda ：轻量级的 Anaconda ，能够使用 conda 管理环境， 
下载地址： https://conda.io/en/latest/miniconda.html

注意： 
1. 为了避免环境引发其他问题，建议安装一个环境即可； 
2. 若果想要学习数据分析，建议：卸载掉其他版本，重新安装 Anaconda ； 

#### 3 开发工具选择  
问题： Python 环境有了，如何进行代码的编写？ 
推荐的 Python 开发工具： 
1. Vscode ： https://code.visualstudio.com/， 
2. Pycharm ： https://www.jetbrains.com/pycharm/，（ Community 为免费版） 
3. Jupyter Notebook ， ( 使用 pip 命令安装 )
重点内容： Vscode ， JupyterNotebook 
#### 3.1 vscode  
目标 ：安装，插件，中英文切换，工作目录，代码编写，代码运行； 
操作如下： 
#### 1 ）打开官网： https://code.visualstudio.com/，根据系统选择版本，下载并安装；

#### 2 ）插件安装：按照下图安装插件； 
推荐插件： Python ， Python for VSCode ， Chinese (Simplified) ( 简体中文 ) 

#### 3 ）切换中英文 
1. 在 vscode 中按下快捷点： ctrl + shit + p ；

2. 在提示框输入： Configure Display Language ，并回车； 
3. 选择语言； 
#### 4 ） vscode 下代码编写与运行 
1. 打开文件夹，文件名称最好以英文开头，不要包含中文 
2. 在文件夹中创建文件，并编写代码 
3. 代码运行过程如下： 

#### 3.3 常见问题：  
#### 1 ）在 Python 命令行中执行文件； 
#### 2 ） vscode 中进入 python 命令行，然后运行文件；

#### 3.2 Jupyter notebook 安装与使用  
如果使用 Anaconda ，不需要安装，否则需要使用 pip 命令安装，具体操作： 
#### 1 ）进入 “ 命令提示符 ” ，输入： 
等待安装完成 
#### 2 ）配置 Jupyter 工作目录： 
输出结果： 
#### 3 ）使用 vscode 打开文件，设置工作目录，修改如下： 
#### 4 ）运行 Jupyter ： 
在命令提示符输入： 
或者（通过这种方式，其他电脑也可以远程使用服务）： 
pip install jupyter
jupyter notebook --generate-config
Writing default config to: C:\Users\v1\.jupyter\jupyter_notebook_config.py
jupyter notebook

复制下面红色连接，在浏览器 ( 推荐 chrome) 中打开即可访问； 
#### 5 ） Jupyter 使用： 
在浏览器中点击： New 创建 Python3 文件，输入代码并运行，结果如下： 
#### 6 ）帮助查看： 
jupyter notebook --ip=172.201.22.8

到这里完成开发环境的搭建； 
#### 4 第三方包的管理  
Python 中有丰富的第三方包，使用 pip 来进行包的安装与卸载； 
安装方式： 
pip 直接安装 
pip+whl 文件安装 
源码安装 
#### 4.1 使用 pip 安装卸载模块：  
pip 常用命令： 
目标：安装卸载 requests 模块 , 操作如下： 
进入命令提示符，执行 
问题：如果安装包因为网络问题不能正常下载可以使用国内源； 
具体操作如下： 
安装命令： pip install pacakgename
升级命令： pip install --upgrade pacakgename
卸载命令： pip uninstall packagename
显示包信息： pip show packagename
pip 升级： python -m pip install --upgrade pip
# 安装
pip install requests
# 卸载
pip uninstall requests

#### 4.2 使用 whl 文件安装  
whl 格式本质上是一个压缩包，里面包含了 py 文件，以及经过编译的 pyd 文件， 
whl 文件下载地址： https://pypi.org/
使用方式： 
#### 4.3 使用源代码进行安装  
目标：使用源码安装 requests
源码下载地址： https://github.com/psf/requests/archive/master.zip
解压并进入目录，目录中有 setup.py 文件 
使用源码安装后，只能手动删除卸载。具体方式： 
所有安装文件记录到 files.txt 中，删除文件中记录文件即可。 
总结：  
主要内容： 
1. Python 版本选择 
2. 开发工具选择 
3. 安装包的管理 
课后练习： 
1. 熟悉 vscode 的应用，创建目录，完成第一个 Python 文件的编写运行； 
2. 熟悉 Jupyter notebook ，完成第一行代码编写； 
3. 使用 pip 完成 requests 模块安装与卸载； 


升级： pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pacakgename
更新： pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pacakgename
# 安装 wheel
pip install xxxx.wheel
# 升级 wheel
pip install -U xxxx.whl
# 卸载
pip uninstall xxxx
# 安装：
python setup.py install
python setup.py install --record files.txt

#### 1 主要内容 
#### 2 python 程序运行过程 
#### 2.1 计算机程序执行过程： 
1. 输入：网络，文件，数据库，输入设备； 
2. 逻辑与算法：程序的功能，算法实现； 
3. 输出：网络，文件，数据库，触发行为； 
#### 2.2 Python 代码执行过程：

从图中得到信息：

1. 源码中如果有语法问题，源码转成字节码过程中，Python解释器会提示错误；
2. 程序在运行中出现错误，Python解释器会提示异常，但是逻辑错误，需要自己排查；

#### 3 基本语法

Python中的一切皆对象；

#### 3.1 如何定义变量？

变量：程序的基本组成，不同语言定义变量方式不同，Python定义变量语法：

标识符 = 对象
#例如：
name = "sun"

变量名命名规则：
1：必须下划线或者字母开头，
2：必须数字，字母，下划线组成,
3：不能使用关键字,

问题：如何查看Python中的关键字？
jupyter中，通过下面命令进行操作：

help("keywords")

#### 1 1a = 20

File "<ipython-input-3-a1b182b6197e>", line 1
1a = 20
^
SyntaxError: invalid syntax

1 if = 10

File "<ipython-input-4-563084b3e606>" , line 1
if = 10
^
SyntaxError : invalid syntax

#### 1 help("keywords")

Here is a list of the Python keywords. Enter any keyword to get more help.

False class from or
None continue global pass
True def if raise
and del import return
as elif in try
assert else is while
async except lambda with
await finally nonlocal yield
break for not

练习：尝试定义几个变量；人名，英雄级别，薪资等；

1 name = "sun"

#### 3.2 某些时候使用变量为什么会报错？

1. 变量名必须赋值才能够使用，否则会报语法问题；
2. 变量名与对象是一个绑定关系；

1 tmp = 0
#### 2 tmp

0

#### 3.3 这个变量是什么类型？

Python中一切皆是对象,使用type查看类型;

print(type(10))
print(type("python"))

#### 1 type(name)

str

#### 1 type(tmp)

int

#### 3.4 如何改掉随意命名的坏习惯？

下面两段代码:

def f(x, y):
#### 2 return y * x ** 2
3
def cirle_area(r, pi):
#### 5 return pi * r ** 2

大家可以得出什么信息？

1. 第一个函数：只能编写者自己懂，后来也就忘了；
2. 第二个函数：代码阅读性好，利于维护；

官网推荐命名规范：

变量名尽量小写, 如有多个单词，用下划线隔开;
例如：first_name = "sun"

驼峰式命名规范：

1. 变量名有多个单词组成，第一个单词首字母小写，其他单词首字母大写，例如：
firstName = "sun"；
2. 变量名有多个单词组成，每个单词首字母大写，例如：FirstName = "sun"；

功能性命名：

1. 循环变量， i, j;
2. 临时变量, tmp, item;
3. 返回值等, ret;

#循环变量
2 i= 0
3 j = 1
#### 4 #变量
5 user_level = "青铜"
#### 6 #返回值
7 ret = False

#### 3.5 这种赋值方式见过没？

#直接赋值
2 a = 10
#### 3 #多重复值
4 b = c = 10
#### 5 #多元赋值
#### 6 m, n = 10, 20
#### 7 p , q = 10, 'test'
8
#### 9 #其他赋值
#### 10 a += 2
#### 11 a -= 3
#### 12 a *= 4
#### 13 a /= 4

#### 4 输入与输出语句

#### 4.1 第一条程序：helloworld

#### 1 print("helloworld")

问题：print是什么？
print实质是一个函数:

print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

参数说明：

参数 说明

value 打印的对象

... 可选项

| 方法/项 | 说明 |
|---|---|
| sep | 指定分隔符,默认空格 |
| 参数 | 说明 |
| end | 结束符，换行 |
file输出到哪里，默认到终端

flush 是否强制输出

#例如：
2 what = 'eat'
#### 3 print("I", "like", what)

#### 1 print("I", "like", what, sep=',')

1

#### 4.2 函数使用说明如何查看？

1. 使用help函数，例如：help(print)
2. jupyter中使用：print?
3. 通过网络查找；

1

#### 4.3 输入语句

input函数：从键盘读入，返回值为字符串
input一般调试或者学习时候使用
例如：

1 what = input("你喜欢什么：")
#### 2 print(what)

#### 1 print("test")

1

#### 4.4 格式化打印

格式化打印
我们常看到这种输出方式：

1 name = "sun"
2 age = 15
#### 3 print("name=%s, age=%d"%(name, age))
4
#### 5 print(f"name={name}, age={age}")

#### 1 "name=%s, age=%d"%(name, age)

#### 1 f"name={name}, age={age}"

问题：为什么会出现这种结果？

1. 通过格式化语句，转成字符串；
2. 通过print输出；

%分析：

1. 字符串中的%：占位符；
2. 字符串后的%：格式化符号；
3. 字符串中的%与变量一一对应；

常用的占位符：

| 方法/项 | 说明 |
|---|---|
| 符号 | 说明 |
| %s | 字符串 |
| %c | 单个字符 |
| %d | 整数 |
| %f | 浮点数 |
| %.nf | 浮点数，小数点保留n位 |
f字符串：

f字符串为Python3.6+提供新语法，生成新的字符串；

1 pi = 3.1415926
2 r = 10
#### 3 print("pi=%.2f r=%d"%(pi, r))

1

#### 5 Python基本语法

#### 5.1 代码对齐

python中使用对齐控制代码段，一般使用4个空格；

def test():
#### 2 print("this is test")
3
#### 4 test()

错误例子

a = 10
2 b = 20

#### 5.2 字符串定义的三种方式

方法：使用成对的引号：单引号，双引号，三引号

1 s1 = 'one'
2 s2 = "two"
3 s3 = '''three'''
4 s4 = """three"""

错误方式：

1 s1 = '123"

字符使用注意点：

1. 字符串以单引号开头结尾，中间不能使用单引号；
2. 字符串以双引号开头结尾，中间不能使用双引号；

#### 5.3 如何添加注释？

两种方式：

1. 单行注释：#开头；
2. 多行注释：三引号开头结尾；

#单行注释
2 pi = 3.14
3
#### 4 """
#### 5 多行注释
#### 6 123
#### 7 234
#### 8 """
#### 9 '''
#### 10 多行注释
#### 11 '''
12 r = 10

1

#### 5.4 转义符

问题：如果想要在字符串中添加换行，使用单引号如何处理？
使用转义符好：

| 方法/项 | 说明 |
|---|---|
| 符号 | 说明 |
| \' | 单引号 |
| \" | 双引号 |
| \n | 换行 |
| \r | 回车 |
\t横向table

\ 反斜杠

#引号
#### 2 print('this\'s test')
#### 3 #换行
#### 4 print('sun\nli')
#### 5 #table
#### 6 print('line1\tline2')

#### 6 运算符

#### 6.1 算数运算符

符号 说明

+,-,*,/加减乘除

** N次方

// 地板除

% 求余数

1 a = 10
2 b = 20

#### 1 b + a

30

#### 1 b - a

10

#### 1 b * a

200

#### 1 b / a

2.0

#### 1 b ** 2

400

#### 1 b // a

2

#### 1 5 % 3

2

1

#### 6.2 比较运算符

| 方法/项 | 说明 |
|---|---|
| 符号 | 说明 |
| >,< | 大于,小于 |
| >=,<= | 大于等于，小于等于 |
| == | 恒等于 |
| != | 不等于 |
注意：

1. 逻辑运算符结果：True或者False
2. 比较对象必须为相同类型

1 a = 10
2 b = 20
3 c= 10

#### 1 a > b

False

1 a == b

False

#### 1 a != b

True

1 a == c

True

#### 1 a >= c

True

1

1 a = 10
2 b = 20
3 c= 10
#### 4 print('a>b:', a> b)
#### 5 print('a<b:', a< b)
#### 6 print('a==c:', a== c)

1

#### 6.3 逻辑运算符

| 方法/项 | 说明 |
|---|---|
| 符号 | 说明 |
| and | 逻辑与 |
| or | 逻辑或 |
| not | 逻辑非 |
Python中的真假

真：非0数字，非空序列，字典等
假：0，False, 空序列等

and返回值：

1.如果操作对象有假，返回第一个不为真的对象；
2.如果操作对象都为真，返回最后一个为真的对象；

or返回值：

1.如果操作对象有真，返回第一个为真的对象
2.如果操作对象都为假，返回最后一个为假的对象；

1 a = 0
2 b = True
3 c = 1

#### 1 a and c

0

#### 1 b and c

1

#### 1 1 and 2 and 0 and 2

0

1

1

def test():
#### 2 print("test")
#### 3 return True

#### 1 test()

test

True

#### 1 1 or 2 or 3 or test()

1

#### 1 (0 and Flase) or (2 and 3)

3

1

#### 1 not 0

True

#### 1 not 1

False

1

1
#### 2 print(a and b)
#### 3 print(a or b)
#### 4 print(b and c)
#### 5 print(a or b or c)

1

#### 7 总结：

1. 能够定义变量，编写代码注意对齐问题；
2. 能够定义字符串；
3. 能够使用help查看文档；
4. 能够使用print与input函数；
5. 掌握运算符，理解Python中的真与假；

1

#### 1 条件语句 
学习目标：掌握条件语句，学习逻辑思维； 
知识点： if/elif/else 语句 
需求 1 ：  
给定一个业绩： 
1. 业绩大于等于 10W ，输出： " 优秀 " ，  
2. 大于等于 8W, 输出： " 合格 " ，  
3. 小于 8W 输出： " 不合格 " ，  
思考：基本逻辑是什么？  
尝试写出伪代码； 
#### 2 条件判断 
Python 中，使用 if 语句处理条件判断，基本语法： 
if 表达式： 
执行代码1
与 else 一起使用： 
if 表达式： 
执行代码1 
else: 
执行代码2
语法说明： 
1. if ：关键字；   
2. 表达式：就是一条语句，例如： 10 ， True, False, a > 60 ；  
3. else 必须与 if 对应； 
基本逻辑：

一个例子：给定一个业绩value，value大于10W，为合格，否则为不合格；

1 value = 11

if value > 10:
#### 2 print("合格")
else :
#### 4 print("不合格")

合格

1 value = 7
if value >= 10:
#### 3 print("优秀")
4
if value >= 8 and value < 10:
#### 6 print("合格")
7
if value < 8:
#### 9 print("不合格")

不合格

#### 3 if与elif语句

基本语法：

if 表达式1:
执行代码1
elif 表达式2：
执行代码2
elif 表达式3：
执行代码3
else:
执行代码4

基本逻辑：

需求：给定一个业绩：

1. 业绩大于等于10W，输出："优秀"，
2. 大于等于8W,输出："合格"，
3. 小于8W输出："不合格"，

实现：

1 value = 7
if value >= 10:
elif value >= 8 and value <10:
#### 5 print("合格")
else :
#### 7 print("不合格")

不合格

1 value = 7
if value >= 10:
elif value >= 8:
else:

不合格

#### 4 练习

抽奖对应奖励如下：

绩效 奖励

[90~100] '价值40元的麻辣香锅'

[80, 89]'价值30元的黄焖鸡米饭'

[70, 79] '价值20元的炸酱面'

其他 '公司免费的自来水一瓶'

思考：实现思路是什么？如何去实现？
基本思路：

1. 理解需求，确认输入与输出；
2. 问题或者需求拆解，第一步做什么，第二步做什么；
3. 整理逻辑，明确使用的知识点；
4. 代码编写；
5. 代码调试；
6. 代码整理与测试；

1 score = 100
#### 2 print("恭喜您获得下面奖励：", end= "")
if score >= 90:
#### 4 print("价值40元的麻辣香锅")
elif score >= 80:
#### 6 print("价值30元的黄焖鸡米饭")
elif score >= 70:
#### 8 print("价值20元的炸酱面")
else:
#### 10 print("公司免费的自来水一瓶")

恭喜您获得下面奖励：价值20元的炸酱面

1

#### 1 内容

学习目标：掌握循环语句while, break,continue；
知识点：while语句,if语句

需求：
给定一个年份，判断是否是闰年，闰年判断条件：

1. 能够被4整除且不能被100整除
2. 能够被400整除

思考：基本逻辑是什么？
写出伪代码

#### 2 闰年判断

需求：判断某个年份是否是闰年

1 year = 2020
if year % 4 == 0 and year % 100 != 0:
#### 3 print("%d is leap year"% year)
elif year % 400 == 0:
#### 5 print("%d is leap year"% year)
else :
#### 7 print("%d is not leap year"% year)

#### 2020 is leap year

1

#### 3 多个闰年判断

#### 3.1 基本语法

while 表达式:
代码1

while语句说明：

while：关键字；
表达式：条件表达式；

#### 3.2 基本逻辑

while执行过程：

1. 判断表达式值是否为真；
2. 如果条件表达式为真，执行代码1；
3. 如果条件表达式为假，退出循环；

#### 3.3 while语句注意点

退出条件设置，避免出现死循环；

1

#### 3.4 判断奇偶

需求：找出1~20之间所有的偶数

代码实现：

1 i = 1
while i <= 20:
if i % 2 == 0:
#### 4 print(i, end= " ")
#### 5 i += 1

#### 2 4 6 8 10 12 14 16 18 20

1

1

1 i = 1
while i <= 20:
if i % 2 == 0:
#### 6 print()

#### 3.5 找出2000到2021之间所有的闰年

代码实现：

1 year = 2000
while year < 2021:
if year % 4 == 0 and year % 100 != 0:
#### 4 print(year, end= " ")
elif year % 400 == 0:
#### 6 print(year, end= " ")
#### 7 year += 1

#### 2000 2004 2008 2012 2016 2020

1

#### 4 while与else

基本语法：

while 条件表达式：
逻辑1
else:
逻辑2

基本逻辑：
如果"条件表达式"结果为假，执行逻辑2；

#### 5 break 与 continue 语句 
#### 5.1 break 语句 
break 语句必须与 while ， for 结合使用；  
作用：跳出当前循环，  
基本语法：  
while 表达式:  
if 表达式1:  
break
基本逻辑： 
需求：循环从键盘循环读入键值，遇到 q 退出： 
代码实现：

while True:
2 value = input('请输入:')
if value == 'q':
#### 4 print('退出while循环')
#### 5 break
#### 6 print(value)

请输入:1
1
请输入:e
e
请输入:q
退出while循环

#### 5.2 continue语句

continue语句必须与while,for循环配合使用;
作用：结束本次循环,
基本语法：
基本语法：

while 表达式：
...
continue
...

一般使用方式：

while 表达式:
if 表达式x:
continue
code1

基本逻辑：

需求：0~20之间输出偶数；
知识点：if语句，while语句，continue语句；
代码实现：

1 i = 0
2
while i <= 20:
if i%2:
#### 6 continue
#### 7 print(i, end = " ")
#### 8 i += 1

#### 0 2 4 6 8 10 12 14 16 18 20

1

1

1

1

1

1 i = 0
while i <= 20:
if i% 2:
#### 4 i += 1
#### 5 continue
#### 6 #continue后的代码不在执行，直接去执行while语句
#### 7 print(i, end= ',')
#### 9 print()

1

#### 1 内容 
小目标：掌握 for 语句 
主要内容： for ，  break ，  continue ，逻辑思维强化 
#### 2 for 语句 
for 语句主要用来遍历可迭代对象；  
一个概念：可迭代对象，一般指容器可被循环遍历获取内部所有元素；例如：字符串，列表等； 
#### 2.1 for 语句基本语法 
基本语法： 
# for, in 为关键字 
for item in iters: 
代码1
逻辑如下图 :
#### 2.2 for 语句理解 
for 语句主要用于在迭代对象中取数据，直到取完。  基本理解： 
#### 1 ：每次从 iters 中取一个对象；  
#### 2 ：将取出对象赋值给 item; 
#### 3 ：执行代码 1; 
#### 4 ：继续重复 1 ，直到 items 中值取完 ; 
一个例子，遍历字符串： s = '123456789'

1 s = '123456789'

for val in s:
#### 2 print(val, end= "")

123456789

1

#### 2.3 for语句处理异常

问题：for遍历时候，如何结束?

1. 遍历结束，会触发异常:StopIteration;
2. for语句处理异常，然后结束；

来看一个例子：

#iter方法：字符串转成iterator；
2 items = iter('12')
#### 3 #使用next函数，每次取一直元素
#### 4 print(next(items))
#### 5 print(next(items))
#### 6 #2个元素取完，在次获取报异常
#### 7 print(next(items))

1
2

--------------------------------------------------------------------------
-
StopIteration Traceback (most recent call last)
<ipython-input-14-8ef22fa708f6> in <module>
#### 5 print( next( items))
----> 7 print(next( items))

StopIteration :

#使用for循环：
for item in "12":
#### 3 print(item)

1
2

#### 3 break与continue

for与break，continue使用与while类似， 需求：给定一个字符串，打印到终端，并将非数字字符替换成'*'；
例如：'abc1b23c3'，输出：'***1*23*3'；
代码实现：

1 s = 'abc1b23c3'
2 rchar = "*"
for val in s:
if "0" <= val <= "9":
#### 5 print(val, end= "")
7
#### 8 print(rchar, end= "")

1 s = 'abc1b23c3'
for val in s:
if val >='1' and val <= '9':
#### 4 print(val, end= '')
#### 6 print('*', end= '')

#### 4 range与enumerate函数

range函数：用于产生range对象，对象中的每个元素为数字;
enumerate函数：将可迭代对象转成enumerate对象

#### 4.1 range函数

range(stop) -> range object
range(start, stop[, step]) -> range object

参数说明：

1. start为初始值；
2. stop为结束值，最大值为stop-1；
3. step为步进值，[, step]这种参数为可选参数；

函数说明：

1. 只有stop， 产生：0,1,2...stop-1数字；
2. 有start与stop，产生：start,start+1,start+2, ..., stop-1数字；
3. 如果有step，产生：start, start+step, start+2*step, ..., stop-1数字；

需求：

1. 产生0~9数字：
2. 产生0~10之间偶数；
3. 产生10~1之间的数字；

for val in range(10):
#### 2 print(val, end= " ")

#### 0 1 2 3 4 5 6 7 8 9

for val in range(0, 11, 2):

#### 0 2 4 6 8 10

for val in range(10, 0, - 1):

#### 10 9 8 7 6 5 4 3 2 1

#### 4.2 enumerate函数

enumerate：将可迭代对象转成enumerate对象，函数原型：

enumerate(iterable, start=0)

enumerate对象内容：iterable索引与索引对应的元素：

(0, seq[0]), (1, seq[1]), (2, seq[2]), ...

如果指定start，enumerate对象内容：

(0+start, seq[0]), (1+start, seq[1]), (2+start, seq[2]), ...

1 s = "123456"
for val in enumerate(s):
#### 3 print(val)

(0, '1')
(1, '2')
(2, '3')
(3, '4')
(4, '5')
(5, '6')

for index, val in enumerate(s):
#### 2 print(index, val)

#### 0 1
#### 1 2
#### 2 3
#### 3 4
#### 4 5
#### 5 6

#### 5 综合练习

统计1900到2020之间所有的闰年，并进行优化；

for year in range(1900, 2021):
if year % 4 == 0 and year % 100 != 0:
#### 3 print(year, end= ",")
elif year % 400 == 0:
#### 5 print(year, end= ",")

1 start_year = 987
#### 2 #调试阶段可以将end设置为较小的值
3 end_year = 1899
#### 4 #4年之内必定有一个闰年
for year in range(start_year, start_year+ 4):
if year % 4 == 0 and year % 100 != 0:
#### 7 print(year, end= ",")
#### 8 #找到第一个闰年退出
#### 9 break
elif year % 400 == 0:
#### 11 print(year, end= ",")
#### 12 #退出
#### 13 break
14
#### 15 #起始年份：第一个闰年；
#### 16 #step:设置为4；
for year in range(year, end_year, 4):
#### 18 print(year, end= ",")

1

#### 1 需求

1. 如何实现代码复用
2. 掌握函数

#### 2 一个例子

判断一个数字是否是奇数，例如：a = 11，代码实现：

1 a = 11
if a % 2 == 1:
#### 3 print("%d is odd"%a)

#### 11 is odd

#### 2.1 问题

给定多个数值，如何判断？
例如：11到20， 30到40

#### 3 2. 函数

python中函数定义的语法：

def func(args):
pass
func()

说明：

def：函数定义关键字；
func：函数名称；
args：函数参数；
函数：默认返回值为None；
函数调用：func(args)；如果有参数，需要加对应的参数；

#### 3.1 第一函数

判断一个数字是否为奇数

def is_odd(val):
if val % 2:

#### 1 is_odd(11)

11

#### 4 函数定义三要素

函数三要素：函数名，函数参数，函数返回值。

#### 4.1 函数名

函数名实质是一个指向函数的变量名，Python中函数名命名规则：

1. 函数名必须具备一定的可读性；
2. python遵循 pep8，一般是小写字母加下划线命名，例如：get_value_by_id(id)；

#### 4.2 函数参数

python函数支持无参，形参，可边长参数，在后面函数章节我们在详细讲解； 函数参数定好之后，一般不会修
改，即使修改也要做好向前兼容； 例如：

def get_pi(): pass

def count_area(r): pass

def my_add(x, y): pass

#### 4.3 函数返回值

Python函数中使用关键字 return显示返回值；

一个问题：isodd这个函数要不要加返回值，我们希望这函数功能：

1. 接受一个值a，判断a是否是奇数；
2. 如果是奇数，返回True；
3. 如果是偶数，返回False；

1 a = is_odd(10)

def is_odd(val):
if val % 2:
#### 4 return False


True

#### 1 is_odd(1,2)

--------------------------------------------------------------------------
-
TypeError Traceback (most recent call last)
<ipython-input-23-10f08bfd1b84> in <module>
----> 1 is_odd(1 ,2)

TypeError : is_odd() takes 1 positional argument but 2 were given

#### 4.4 函数调用

调用函数之前，需要确认三个事情：

1. 调用者,传入参数必须符合函数定义要求；
2. 传入参数类型，顺序要符合函数要求；
3. 理解函数作用，根据需求决定是否接受函数返回值；

1 a = range(10)
### 43. 附录 B：PDF合并2-3章（列表等章节合并）
#### 1 主要内容

主要内容：

如何创建列表
可变数据结构
列表相关函数
列表相关方法

#### 2 列表基础

1. 列表定义方式：[value1, value2, ....]
2. 列表理解：理解为容器，可以存放任意对象；
3. 列表支持：修改，插入，删除；

```python
l = [1, "1", "123", None ]
```

```python
l
```
[1, '1', '123', None]

#### 2.1 列表创建方式

1. 直接定义列表：list1 = [1,'1','2',3']
2. 多维列表：list2 = [1,2,3,['a','b', 'c']]
3. 使用list函数：list(iterable=(), /)

```python
s = "qimao"
```

```python
tmp = list(s)
tmp
```
['q', 'i', 'm', 'a', 'o']

```python
"".join(tmp)
```
'qimao'

#### 2.2 列表遍历

1. 使用while+索引；
2. 使用for循环进行遍历；
3. 多维列表访问：list2[3][0]

练习：遍历二维列表

scores = ["class_1", ["sun",80, 60], ["zhao", 70, 90]]

```python
scores = ["class_1", ["sun",80, 60], ["zhao", 70, 90]]
```
```python
type(scores)
```
list

```python
isinstance(scores, list)
```
True

```python
isinstance(scores, str)
```
False

```python
for item in scores:
if isinstance(item, list):
for val in item:
print(val)
else :
print(item)
```
class_1
sun
80
60
zhao
70
90

```python
scores
```
['class_1', ['sun', 80, 60], ['zhao', 70, 90]]

```python
scores[0:2]
```
['class_1', ['sun', 80, 60]]

#### 2.3 列表修改

列表是一种可变的数据结构，修改列表中的某个元素，列表不变；

listv = [60, 90, 59]
listv[1] = 62

练习：给定一个成绩列表，如果成绩为-1，将其修改为0；
例如：a = [96, 80, -1, 66]

例如：a [96, 80, 1, 66]

```python
listv = [60, 90, 59]
listv[1] = 62
print(listv)
```

```python
a = [96, 80, - 1, 66]
for index, val in enumerate(a):
if val == -1:
a[index] = 0
```

#### 3 列表相关函数

方法 说明

list(iterable=(), /) 将迭代对象转成列表

max/min(iterable, [key=func]) 获取最大最小值

len(obj) 获取长度

sum(iterable, start=0, /)迭代对象求和，迭代对象元素必须为数字；

练习：给定字符串列表，找出对应的数字的最大元素，
例如：listnum = ['200', '798','1000'],返回值：'1000'

```python
listnum = ['200', '798','1000']
```

```python
max(listnum, key= int)
```
'1000'

```python
l = [100, 200, 400, 599]
```
```python
sum(l)
```
1299

#### 4 列表相关方法

#### 4.1 列表中添加元素

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| l.append(obj) | 在列表尾部添加元素 |
| l.insert(index, obj) | 指定索引插入元素 |
L.extend(iterable)在尾部扩展列表，将可迭代对象元素添加到列表尾部

```python
l = [1,2,3]
#尾部添加4
l.append(4)
print(l)
#在起始位置插入-1
l.insert(0,- 1)
print(l)
#extend添加可迭代对象
s = '567'
l.extend(s)
print(l)
```
```python
l = [1,2,3]
#尾部添加4
l.append(4)
```

```python
l
```
[1, 2, 3, 4]

```python
#在起始位置插入-1
l.insert(0,- 1)
print(l)
```
[-1, 1, 2, 3, 4]

```python
s = '567'
l.extend(s)
print(l)
```
[-1, 1, 2, 3, 4, '5', '6', '7']

#### 4.2 列表统计与查找

方法 说明

L.count(value) 统计value在L中出现次数

L.index(value, [start, [stop]])返回value第一次出现位置，不存在报异常

示例：

```python
l = [1,2,3,4,3,5,3]
print('3出现次数：',l.count(3))
print('3第一次出现位置:',l.index(3))
#注意返回值，认为该元素在列表中实际的位置
print('3在索引为3之后，第一次出现位置:',l.index(3,3))
```
```python
l = [1,2,3,4,3,5,3]
print('3出现次数：',l.count(3))
```
3出现次数： 3

```python
print('3第一次出现位置:',l.index(3))
```
3第一次出现位置: 2

```python
print('3在索引为3之后，第一次出现位置:',l.index(3,3))
```
3在索引为3之后，第一次出现位置: 4

#### 4.3 列表删除

方法 说明

l.pop(index=-1, /) 删除并返回index对应的value,默认值为-1

l.remove(value, /)删除第一次出现value的值，如果不存在产生异常

l.clear() 清空列表

示例：

```python
l = [1,4,2,4,3,4]
#删除最后一个元素
l.pop()
print(l)
#删除第一个元素
l.pop(0)
print(l)
#删除第一个4
l.remove(4)
print(l)
#清空列表
l.clear()
print(l)
```
```python
l = [1,4,2,4,3,4]
#删除最后一个元素
l.pop()
print(l)
```
[1, 4, 2, 4, 3]

```python
l.pop(0)
print(l)
```
[4, 2, 4, 3]

```python
l.remove(4)
print(l)
```
[2, 4, 3]

```python
l.clear()
print(l)
```
[]

#### 4.4 列表陷阱

动态删除列中，可能造成某些问题，达不到想要的效果，例如：删除列表中重复元素；

```python
vals = [1,2,3,4,4,5,4,5,6]
for val in vals:
if vals.count(val) > 1:
vals.remove(val)
print(vals)
print(vals)
```
[1, 2, 3, 4, 4, 5, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 4, 5, 6]
[1, 2, 3, 4, 5, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 6]
[1, 2, 3, 4, 4, 5, 6]

```python
vals = [1,2,1,2,3,4,4,5,4,5,6]
while True :
for item in vals:
if vals.count(item) > 1:
vals.remove(item)
break
else :
break
print(vals)
```
[1, 2, 3, 4, 5, 6]

#### 5 元组

元组与列表类似，但是元组不可变；

#### 5.1 创建元组:

1. 方式1：t1 = (1,2,3)
2. 方式2：t2 = tuple("123")

```python
t1 = (1,2,3)
t1
```
(1, 2, 3)

```python
1,2,3
```
(1, 2, 3)

```python
tuple("1234")
```
('1', '2', '3', '4')

```python
tuple([1,2,3,4])
```
(1, 2, 3, 4)

```python
a, b,c = (1,2,3)
```

#### 5.2 元组常用的方法

方法 说明

T.count(value) 统计value在L中出现次数

T.index(value, [start, [stop]])返回value第一次出现位置，不存在产生异常

#### 5.3 问题：元组和列表类似，为什么还要使用元组？

元组不可变，在某些场景下，我们希望数据不变化的时候，就可以使用元组;

```python
t1 = (1,2,3)
```
```python
t1[0] = -1
```
---------------------------------------------------------------------------
TypeError Traceback (most recent call last)
<ipython-input-64-dfabc5d41138> in <module>
----> 1 t1[0] = -1

TypeError : 'tuple' object does not support item assignment

#### 6 列表强化练习

#### 6.1 练习1：

在有序列表中插入元素，需求：

1. 给定有序的数字列表，
2. 从键盘读取输入数字，将输入值插入到列表中，使其有序，
3. 输入值为：q,退出循环
例如：
v = [1,2,3]
输入：2
结果：[1,2,2,3]
输入：5
结果：[1,2,2,3,5]

基本思路如图：

```python
def insert_value(listnum):
while True :
val = input("输入数字:")
if val == "q":
break
val = int(val)
for index, item in enumerate(listnum):
if val <= item:
listnum.insert(index, val)
break
else :
listnum.append(val)
print(listnum)
listn = [1,2,3]
insert_value(listn)
```
输入数字:1
[1, 1, 2, 3]
输入数字:0
[0, 1, 1, 2, 3]
输入数字:1000
[0, 1, 1, 2, 3, 1000]
输入数字:20
[0, 1, 1, 2, 3, 20, 1000]
输入数字:q

#### 6.2 练习2：

数字转成数字列表，例如：

输入：320,输出：[3,2,0]
输入：9527,输出：[9,5,2,7]

```python
def num_to_list(num):
result = []
snum = str(num)
for value in snum:
result.append(int(value))
return result
```

```python
num_to_list(320)
```
[3, 2, 0]

```python
num_to_list(9527)
```
[9, 5, 2, 7]

#### 6.3 练习3：

需求：将两个有序列数字列表进行合并，并使其有序，例如：

v1 = [1,2,3,4]
v2 = [2,5,8]
结果：
v = [1,2,2,3,4,5,8]

要求：不要使用默认排序算法；

```python
def megre_list(n1, n2):
result = []
l1 = len(n1)
l2 = len(n2)
index1, index2 = 0, 0
while index1 < l1 and index2 < l2:
print(f"index1:{index1}, index2:{index2}")
if n1[index1] <= n2[index2]:
result.append(n1[index1])
index1 += 1
else :
result.append(n2[index2])
index2 += 1
if index1 < l1:
tail = n1[index1:]
else :
tail = n2[index2:]
result.extend(tail)
print(result)
return result
```
```python
v1 = [1,2,3,4, 10]
v2 = [0,1,2,5,8]
megre_list(v1, v2)
```
index1:0, index2:0
index1:0, index2:1
index1:1, index2:1
index1:1, index2:2
index1:2, index2:2
index1:2, index2:3
index1:3, index2:3
index1:4, index2:3
index1:4, index2:4
[0, 1, 1, 2, 2, 3, 4, 5, 8, 10]

[0, 1, 1, 2, 2, 3, 4, 5, 8, 10]


列表解析语法
列表解析应用

#### 2 列表解析详解

基本概念：列表解析：在一个序列中应用表达式，并将结果保存到列表中；

#### 2.1 列表解析基本使用方式

基本语法：

[expr for iter in iterable]

主要参数：

参数 说明

iterable 迭代对象

iteriterable中的元素

expr 表达式

执行流程：

#### 2.2 列表解析基本练习

1. 生成列表：[1,2,3,4,5]
2. 生成列表：["0", "1", "2", "3", "4", "5"]
3. 将520转成：[5,2,0]

```python
[val for val in range(1, 6)]
```
[1, 2, 3, 4, 5]

```python
[val ** 2 for val in range(1, 6)]
```
[1, 4, 9, 16, 25]

```python
[pow(val, 2) for val in range(1, 6)]
```
[1, 4, 9, 16, 25]

```python
[str(val) for val in range(0, 6)]
```
['0', '1', '2', '3', '4', '5']

```python
[int(val) for val in str(520)]
```
[5, 2, 0]

```python
import random
```
```python
[random.randint(1, 100) for i in range(10)]
```
[18, 53, 68, 53, 72, 18, 33, 49, 84, 37]

#### 2.3 列表解析与判断条件

基本语法：

[expr(value) for value in iter if cond_expr(value)]

执行过程：

#### 2.4 列表解析条件判断练习

1. 生成1~100之间偶数列表；
2. 给定成绩：[59, 100, 20, 30, 80]，过滤出成绩大于等于60的成绩；
3. 给定一段英文歌曲，统计每个单词长度与总长；

英文歌曲部分歌词：

When I was young I'd listen to the radio
Waiting for my favorite songs
When they played I'd sing along,

It made me smile.

```python
res = [val for val in range(1, 101) if val% 2==0]
print(res)
```
[2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100]

```python
scores = [59, 100, 20, 30, 80]
[score for score in scores if score >= 60]
```
[100, 80]

```python
scores = [59, 100, 20, 30, 80]
[score >= 60 for score in scores]
```
[False, True, False, False, True]

```python
words = """
When I was young I'd listen to the radio
Waiting for my favorite songs
When they played I'd sing along,
It made me smile.
"""
```

```python
word_len = [len(word) for word in words.split()]
```
```python
word_len
```
[4, 1, 3, 5, 3, 6, 2, 3, 5, 7, 3, 2, 8, 5, 4, 4, 6, 3, 4, 6, 2, 4, 2, 6]

```python
sum(word_len)
```
98

#### 2.5 多重循环列表解析

基本语法：

[expr(v1,v2) for v1 in iters1 for v2 in iters2]

执行过程：

1：取v1,
2：顺序去v2,
3：执行expr(v1,v2),
4：重复1~3步骤，

```python
[(v1, v2) for v1 in range(1,4) for v2 in range(1,4)]
```
[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

#### 2.6 多重循环列表解析练习

1. 给定两个数字列表，计算两两的乘积；
2. 使用列表解析完成1~9乘法口诀； 输出结果：

['1*1=1', '1*2=2', '2*2=4', '1*3=3', '2*3=6', '3*3=9', '1*4=4', '2*4=8', '3*4=12', '4*4=16', '1*5=5', '2*5=10', '3*5=15', '4*5=20', '5*5=25', '1*6=6', '2*6=12', '3*6=18', '4*6=24', '5*6=30',
'6*6=36', '1*7=7', '2*7=14', '3*7=21', '4*7=28', '5*7=35', '6*7=42', '7*7=49', '1*8=8', '2*8=16', '3*8=24', '4*8=32', '5*8=40', '6*8=48', '7*8=56', '8*8=64', '1*9=9', '2*9=18', '3*9=27', '4*
9=36', '5*9=45', '6*9=54', '7*9=63', '8*9=72', '9*9=81']

```python
[v1 * v2 for v1 in range(1,4) for v2 in range(1,4)]
```
[1, 2, 3, 2, 4, 6, 3, 6, 9]

```python
res = [f"{j}*{i}={i* j}" for i in range(1, 10) for j in range(1, 10) if i >= j]
print(res)
```
['1*1=1', '1*2=2', '2*2=4', '1*3=3', '2*3=6', '3*3=9', '1*4=4', '2*4=8', '3*4=12', '4*4=16', '1*5=5', '2*5=10', '3*5=15', '4*5=20', '5*5=25', '1*6=6', '2*6=12', '3*6=18', '4*6=24', '5*6=30', '6*6=3
6', '1*7=7', '2*7=14', '3*7=21', '4*7=28', '5*7=35', '6*7=42', '7*7=49', '1*8=8', '2*8=16', '3*8=24', '4*8=32', '5*8=40', '6*8=48', '7*8=56', '8*8=64', '1*9=9', '2*9=18', '3*9=27', '4*9=36', '5*9=4
5', '6*9=54', '7*9=63', '8*9=72', '9*9=81']

```python
l = [f"{j}*{i}={i* j}" for i in range(1, 10) for j in range(1, 10) if i>= j]
```

#### 1 数据结构

主要内容：

目标：

1. 熟练应用数据结构解决当前问题；
2. 锻炼思维，提升编程能力；
3. 掌握当下，用在未来；

#### 2 数字部分内容

如图：

#### 3 数字类型

主要类型：

| 方法/项 | 说明 |
|---|---|
| 类型 | 说明 样例 |
| int | 整数 1,2,3,100... |
| float | 浮点 3.14, 2.1.... |
| complex | 复数 complex(1, 2) |
| bool | 布尔值 只有：True与False |
定义数字变量：

1. 定义pi
2. 定义半径
3. 定义布尔值

```python
pi = 3.14
```
```python
r = 5
```

```python
b = False
```
```python
pi
```
3.14

#### 4 数字计算与类型转换

#### 4.1 数字相关运算符

1. 支持比较运算符
2. 支持算数运算符
3. 支持逻辑运算符

```python
#直播带货，帽子销量100，T-shirt销量120，对比销售量大小；
hat_total = 100
tshirt_total = 120
```
```python
hat_total > tshirt_total
```
False

```python
#计算销售额
hat_price = 40
tshirt_price = 30
hat_sales = hat_price * hat_total
tshirt_sales = tshirt_price * tshirt_total
```

```python
hat_sales
```
4000

```python
tshirt_sales
```
3600

#### 4.2 不同数字类型进行计算，结果如何?

1. Python中，整数与浮点数处理结果？
2. Python中，浮点数与布尔值处理结果？

```python
pi = 3.14
r = 5
```
```python
2 * pi * r
```
31.400000000000002

```python
1 + True
```
2

```python
1 == True
```
True

```python
1.0 == True
```
True

#### 4.3 默认转换规则

默认转换顺序：

complex > float > int > bool

#### 4.4 数字类型强制转换

数据类型强制转换：

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 示例 |
| int([x]) | 将x转成整数 int(3.14)->3 |
| int(x, base=10) | 将数字字符串转整数 int('3')->3 |
float(x=0)将数字或者字符串转浮点 float('3')->3.0

bool(x) 将任意对象转成bool bool(1)->True

```python
#圆面积只保留整数
r = 5
pi = 3.14
```

```python
tmp = pi * (r ** 2)
```
```python
int(tmp)
```
78

```python
int(pi)
```
3

```python
bool(pi)
```
True

```python
bool(0.0)
```
False

```python
int("10", base= 16)
```
16

#### 5 数字相关函数

#### 5.1 基本函数

函数 说明

round(number, ndigits=None)指定小数后位数

pow(x, y, z=None, /)x**y或者x**y%z

abs(x, /) x的绝对值

```python
#对每个计算结果保留2位
#求绝对值
```

```python
pi = 3.14
r = 5
```
```python
tmp = 2*pi* r
tmp
```
31.400000000000002

```python
round(tmp, 1)
```
31.4

```python
pow(2,3)
```
8

```python
a = - 1
```

```python
abs(a)
```
1

#### 5.2 math模块

math模块相关数学函数
使用方式：

import math

#### 5.3 数学常数

函数, math. 说明

pi 表示圆周率，3.141592653589793

e 自然对数的底， 2.718281828459045

#### 5.4 三角函数

函数, math. 说明

sin(x)/cos(x) 返回的x弧度的正/余弦值

asin(x)acos(x)返回x的反正/反余弦弧度值

tan(x) 返回x弧度的正切值

atan(x) 返回x的反正切弧度值

#### 5.5 指数函数等

函数, math. 说明

factorial(x) 计算阶乘，返回x！

sqrt(x) 返回x的平方根

floor(x)取最接近x的整数，返回整数<x

| 方法/项 | 说明 |
|---|---|
| log(x[, base]) | 以 Base 为底的 x 的对数 |
| log10(x) | 以10为底的x的对数 |
| log2(x) | 以2为底的x的对数 |
```python
import math
```

```python
math.sin(0.3)
```
0.29552020666133955

#### 6 强化练习

#### 6.1 给定数字，计算其对应的阶乘

需求：

1）给定数字n，
2）n! = n*(n-1)*(n-2)....*1；
例如：5! = 5*4*3*2*1

思路：

```python
def func(n):
ret = 1
for i in range(1, n+ 1):
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

示例：

1）给定数字：23456，输出:65432
2）给定数字：230，输出：032
3）给定数字：1，输出数字1

```python
def reverse_digit(num):
if num < 10:
print(num)
else :
while num > 0:
print("num:", num)
tmp = num % 10
print(tmp, end= "")
num //= 10
```
```python
reverse_digit(23456)
```
num: 23456
6num: 2345
5num: 234
4num: 23
3num: 2
2

#### 1 random模块

#### 1.1 模块导入

主要方式：

#导入模块
import xxx
#在模块中导入某个属性
from xxxx import xx
#导入之后起别名
import xxxx as xx

例如：

import random
import random as rd
from random import randint

```python
import random
```
```python
from random import randint
```
```python
randint(0, 4)
```
1

#### 1.2 random模块主要方法

random模块数字相关方法：

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| random() | 产生[0,1]之间随机浮点数 |
| uniform(a,b) | 产生(min(a,b), max(a,b))之间随机浮点数 |
| randint(a,b) | 产生[a,b] 之间随机整数 |
| seed(a=None, version=2) | 设置随机数生成器的种子 |
randrange([start], stop, [,step])指定范围内，按step递增的集合中取一个随机数，step缺省值为1

练习：

1. 生成0~1之间随机数
2. 生成0~10之间随机数
3. 生成0~10之间随机偶数

```python
random.random()
```
0.8148861899801072

```python
random.uniform(10, 1)
```
3.255903623455204

```python
random.seed(0)
random.randint(0,10)
```
6

```python
random.randrange(0, 11, 2)
```
6

#### 2 猜数字小游戏

需求：

1.游戏开始每次产生随机数字，
2.读取用户输入，如果猜中，提示中奖,
3.如果猜错，进行合理的提示,

过程如下图：

```python
def guess_num():
x = randint(1, 100)
while True :
tmp = input("输入数字：")
tmp = int(tmp)
if tmp == x:
print("猜中了")
break
elif tmp > x:
print("输入过大")
else :
print("输入过小")
```

```python
guess_num()
```
输入数字：5
输入过小
输入数字：8
猜中了

```python
tmp = int(tmp)
```
```python
x == tmp
```
True

```python
type(tmp)
```
int

```python
type(x)
```
int

#### 3 生成4随机数字验证码

1. 生成4个随机数字
2. 将4个数字生成图片

#### 3.1 生成4个数字组成的字符串

#### 3.2 使用PIL模块生成随机码图片

安装PIL模块:

pip install pillow

导入模块：

from PIL import Image,ImageDraw,ImageFont

```python
def getRandomColor():
'''获取一个随机颜色(r,g,b)格式的'''
c1 = random.randint(0,255)
c2 = random.randint(0,255)
c3 = random.randint(0,255)
return (c1,c2,c3)
def createRandomImage(s):
# 获取一个Image对象，参数:RGB模式,宽,高，随机颜色
image = Image.new('RGB',(100,30),getRandomColor())
# 创建一个Draw对象
draw = ImageDraw.Draw(image)
# 创建字体，字体与字体大小
font= ImageFont.truetype(r"C:\Windows\Fonts\Arial\arial.ttf",size= 32)
# 在图片上写东西,参数是：定位，字符串，颜色，字体
draw.text((15,0),s,getRandomColor(),font= font)
return image
#image.save(open('test.png','wb'),'png')
createRandomImage("1235")
```


如图

重点：

1. 掌握序列的通用方法
2. 重点掌握字符串列表使用；
3. 学习编程思路，提升代码编写与调试能力

#### 2 序列

#### 2.1 主要对象

如图：

#### 2.2 序列结构

问题：如何去理解序列？

注意：

1. 索引起始值为：0
2. 索引最大值：(序列长度)-1
3. 负向索引，最后一个元素为索引为：-1

#### 2.3 序列访问方式

如图：

```python
s = "123"
```
```python
s[0],s[-1]
```
('1', '3')

```python
s[100]
```
---------------------------------------------------------------------------
IndexError Traceback (most recent call last)
<ipython-input-28-2a138df92e52> in <module>
----> 1 s[ 100]

IndexError : string index out of range

基本语法：

s = "helloCoCo"
#第一个元素
s[0]
#最后一个元素
s[-1]
#切片操作
s[:2]
s[2:]

注意：

1. 序列访问不能越界
2. 重点理解切片操作，灵活使用索引

#### 2.4 序列访问示意图

如图：

#### 2.5 序列遍历

序列遍历方式：

1. 使用for循环
2. 使用while循环

```python
s
```
'helloCoCo'

```python
for val in s:
print(val)
```
h
e
l
l
o
C
o
C
o

#### 2.6 序列运算符

如图：

常见操作：

1. 比较运算符
2. not操作
3. 加法操作
4. 乘法操作

#### 2.7 序列相关函数

序列支持通用函数：

| 方法/项 | 说明 |
|---|---|
| 函数 | 说明 |
| len(obj) | 获取可迭代对象长度 |
| max(iterable, *[, default=obj, key=func]) | 获取迭代对象中最大值，func为元素处理函数 |
| min(iterable, *[, default=obj, key=func]) | 获取迭代对象中最小值，func为元素处理函数 |
val in seq val在seq中返回True, 否则返回False

val not in seq val不在seq中返回True, 否则返回False

all(iterable, /)如果iter中每个对象x, 其bool(x)都为真，返回真，否则返回False

any(iterable, /)如果iter中每个对象x, 其bool(x)有一个为真，返回真，否则返回False

zip(*iterables) 将多个可迭代队形进行合并，返回zip对象

sorted(iterable, /, *, key=None, reverse=False) 对迭代对象进行排序，默认从小到大,返回列表

#### 2.8 理解max，min中的key

给定一个数字列表：

vals = [1, -10, 3, -11, 8, -3]

需求：

1. 获取列表中最大的元素
2. 获取列表中绝对值最大的元素

```python
vals = [1, -10, 3, -11, 8, -3]
max(vals, key=abs), max(vals)
```

对key的理解

1. 设置key函数,
2. 每个元素使用key函数进行处理,
3. max,min函数根据处理后结果选择最大或者最小值；
4. 返回最大最小值对应的元素；

处理过程如图：


定义字符串
字符串类型
字符串编码格式
生成字符串
字符串相关函数
字符串相关方法

#### 2 定义字符串

字符串：单引号(')，双引号(")，三引号(''', """)开头结尾； 例如：

s1 = "Python"
s2 = 'hat'
s3 = """project"""

常见的错误定义方式：

```python
#引号前后不一致
s = "qimao'
```
File "<ipython-input-1-3a96f76982fa>" , line 2
s = "qimao'
^
SyntaxError : EOL while scanning string literal

```python
#引号中间包含相同引号
s = 'it's me'
```
File "<ipython-input-2-6593473f4b33>" , line 2
s = 'it's me'
^
SyntaxError : invalid syntax

```python
s = "it's me"
```

```python
s = 'it\'s me'
```

```python
s
```
"it's me"

#### 3 字符串类型

>1. 普通字符串:引号开头结尾，例如："this", 'python';
>2. 原字符串：r开头，例如：r'c\c++\Python';
>3. Byte类型：b开头，例如：b'test';

注意点：

1. 原字符串不会对转义符进行转义；
2. Byte类型一般处理编码数据，媒体数据(图片，音乐等)；

```python
s = r'c\c++\Python'
```
```python
s = "it\'s me"
s
```
"it's me"

```python
s1 = r"it\'s me"
s1
```
"it\\'s me"

#### 4 编码格式

基本概念：

是计算机科学领域里的一项业界标准，包括字符集、编码方案等。Unicode是为了解决传统的字符编码方案的局限而产生的，它为每种语言中的每个字符设定了统一并且唯一的二进制编码，以满足跨语言、跨平台进行文
本转换、处理的要求。

编码格式：gbk, utf-6, utf-16, gb2312等；
Unicode是Python3默认编码格式,编码格式转换关系：

编码格式操作；

```python
s = "香蕉"
#编码方式：utf-8
s1 = s.encode('utf-8')
print(type(s1), s1)
#解码方式必须为utf-8
print(s1.decode('utf-8'))
#错误操作：
#print(s1.decode('gb2312'))
```
<class 'bytes'> b'\xe9\xa6\x99\xe8\x95\x89'
香蕉

```python
s = "香蕉"
#编码方式：utf-8
s1 = s.encode('utf-8')
s1
```
b'\xe9\xa6\x99\xe8\x95\x89'

```python
print(type(s1), s1)
```
<class 'bytes'> b'\xe9\xa6\x99\xe8\x95\x89'

```python
s1.decode("utf8")
```
'香蕉'

```python
s1.decode("gb2312")
```
---------------------------------------------------------------------------
UnicodeDecodeError Traceback (most recent call last)
<ipython-input-22-28804593a97d> in <module>
----> 1 s1.decode( "gb2312" )

UnicodeDecodeError : 'gb2312' codec can't decode byte 0x99 in position 2: illegal multibyte sequence

#### 5 创建字符串

#### 5.1 使用%格式化

使用%号，构建字符串，常见例子：

user_name = "name=%s"%("sun")
user_info = "name=%s, age=%d"%("sun", 14)

%s, %d被称为占位符，主要的占位符包括：

| 方法/项 | 说明 |
|---|---|
| 符号 | 说明 |
| %s | 对象str方法的返回值(一般选择这种方式) |
| %r | 对象的repr方法的返回值 |
| %d、%i | 数字格式化 |
| %f | 浮点数格式化 |
| %.nf | 浮点数保留n位小数 |
| %x，%X | 数字格式化为16进制(x,X大小写) |
| %c | 格式化字符及其 ASCII 码 |
| %e | 科学计数法表示的浮点数(e小写) |
```python
s = '%.2f'%(1/3)
s
```
'0.33'

#### 5.2 f字符串

f字符串是python3.6版本中新增语法，语法格式如下：

f'{var1} {var1}'

f字符串特点:

1. 字符串以f或者F开头，f'{a}',a变量必须定义
2. f字符串优点：使用更加方便

练习： 给定英雄与类型：

hero_names = ["程咬金", "马超","蔡文姬", "王昭君", "曹操"]
hero_types = ["坦克", "刺客","游走", "法师", "战士"]

输出结果：

程咬金:坦克
马超:刺客
蔡文姬:游走
王昭君:法师
曹操:战士

```python
hero_names = ["程咬金", "马超","蔡文姬", "王昭君", "曹操"]
hero_types = ["坦克", "刺客","游走", "法师", "战士"]
```
```python
for name, t in zip(hero_names, hero_types):
line = f"{name}:{t}"
print(line)
```
程咬金:坦克
马超:刺客
蔡文姬:游走
王昭君:法师
曹操:战士

```python
for item in zip(hero_names, hero_types):
print(item)
```
('程咬金', '坦克')
('马超', '刺客')
('蔡文姬', '游走')
('王昭君', '法师')
('曹操', '战士')

#### 6 字符串相关函数

#### 6.1 字符串相关函数

函数 说明

str(object='') 将对象转成字符串对象

sorted(iterable,key=None, reverse=False)对迭代对象排序，返回列表

| 方法/项 | 说明 |
|---|---|
| ord(c) | 将字符转成ASCII码 |
| chr(i) | 将ASCII码转成字符 |
| int(str) | 将字符串转成数字 |
| float(str) | 将字符串转成浮点数 |
```python
str(10)
```
'10'

```python
l = [1,2,3]
```
```python
str(l)
```
'[1, 2, 3]'

ASSIC码表

#### 6.2 练习1

输出下面内容：
给定字符列表，输除其对应的ASCII码，例如：

listchr = ['a', 'z', 'c']
输出结果：

```python
listchr = ['a', 'z', 'c']
for char in listchr:
print(char, ord(char))
```
a 97
z 122
c 99

#### 6.3 练习2

给定两个字符，输出两个字符之间所有的字符 例如：

1. 给定[a,d],输出：abcd；
2. 给定[d,z],输出：defg...z;

```python
def func(start, end):
s = ""
for val in range(ord(start), ord(end)+ 1):
s += chr(val)
print(s)
return s
```
```python
func("d", "z")
```
d
de
def
defg
defgh
defghi
defghij
defghijk
defghijkl
defghijklm
defghijklmn
defghijklmno
defghijklmnop
defghijklmnopq
defghijklmnopqr
defghijklmnopqrs
defghijklmnopqrst
defghijklmnopqrstu
defghijklmnopqrstuv
defghijklmnopqrstuvw
defghijklmnopqrstuvwx
defghijklmnopqrstuvwxy
defghijklmnopqrstuvwxyz

'defghijklmnopqrstuvwxyz'

#### 7 字符串相关方法

#### 7.1 查找

查找：查找子串位置

方法 说明 参数

S.find(sub[, start[, end]])从前向后查找，返回sub在S第一次出现位置，不存在返回-1 start与stop限定查找范围

| 方法/项 | 说明 |
|---|---|
| S.rfind(sub[, start[, end]]) | 从后向前查找，功能同上， 同上 |
| S.index(sub[, start[, end]]) | 功能同S.find, 不同：子串不存在报异常 同上 |
| S.count(sub[, start[, end]]) | 返回子串在S中出现次数 同上 |
练习：

给定字符串：phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'，
需求:解析小米11的价格

```python
phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'
```
```python
start = phoneprice.find("小米11:")
end = phoneprice.find(",", 13)
```
```python
phoneprice[start+ len("小米11:"):end]
```
'3599'

```python
phoneprice.find("9")
```
11

```python
phoneprice.rfind("9")
```
33

#### 7.2 替换

替换：将指定子串替换成新的字符串

方法 说明

S.replace(old, new[, count])将old使用new替换，返回新的字符串

| 方法/项 | 说明 |
|---|---|
| 参数：old | 被替换字符串 |
| 参数：new | 替换后内容 |
| 参数：count | 替换数量，默认替换所有 |
练习：

给定：s="li:level1, sun:level2, liu:level2"
替换：s = "li:A+， sun:A, liu:A"

```python
s = "age:9899"
new_s = s.replace("9", "*", 1)
```

```python
new_s
```
'age:*899'

```python
s= "li:level1, sun:new_s, liu:level2"
new_s = s.replace("level1", "A+")
```

```python
levels = ["level1", "level2", "level3"]
new_level = ["A+", "A", "B+"]
new_str = "li:level1, sun:level2, liu1:level2, liu2:level3"
for old, new_s in zip(levels, new_level):
new_str = new_str.replace(old, new_s)
print(new_str)
```
li:A+, sun:A, liu1:A, liu2:B+

```python
new_s = new_s.replace("level2", "A")
```
```python
new_s
```
'li:A+, sun:A, liu:A'

#### 7.3 字符串切分

切分：将字符串按照指定分隔符进行分割，得到字符串列表

方法 说明

S.split(sep=None, maxsplit=-1)从前向后通过sep对S切分，返回切分子串组成的列表

| 方法/项 | 说明 |
|---|---|
| S.rsplit(sep=None, maxsplit=-1) | 从后向前切分，功能同上 |
| 参数：sep | 分隔符，默认所有空字符， |
| 参数：maxsplit | 指定切分数量，默认所有的都要切分 |
练习：

1. 程序员A技能："python C++ C Java Mysql Hive",问：A掌握几门技能？
2. 图片地址："http://i1.umei.cc/uploads/tu/201711/9999/6e312a86a7.jpg" (http://i1.umei.cc/uploads/tu/201711/9999/6e312a86a7.jpg"), 问：如何获取图片名称及图片类型？
3. 给定字符串：phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'，解析字符串中所有手机类型及对应的价格

```python
skills = "python C++ C Java Mysql Hive"
```
```python
len(skills.split())
```
6

```python
url = "http://i1.umei.cc/uploads/tu/201711/9999/6e312a86a7.jpg"
```

```python
pic_name = url.rsplit("/", 1)[- 1]
pic_name.split(".")[- 1]
```
'jpg'

```python
pic_name
```
'6e312a86a7.jpg'

```python
phoneprice = '荣耀50Pro:3689,小米11:3599,vivoX60:4498'
```
```python
items = phoneprice.split(",")
```
```python
for item in items:
name, price = item.split(":")
print(f"{name}的售价：{price}")
```
荣耀50Pro的售价：3689
小米11的售价：3599
vivoX60的售价：4498

```python
s = "1\n2\n3"
```
```python
s.split()
```
['1', '2', '3']

#### 7.4 字符串拼接

拼接：使用指定分隔符将可迭代字符串组成新的字符串

方法 说明

S.join(iterable)使用S将迭代对象中的元素(字符串类型)拼接成新的字符串

S 指定的连接符

iterable 字符串迭代对象

练习： skills = ['c++', 'Python', 'Java']，将技能列表进行拼接，结果：'c++/Python/Java'

```python
skills = ['c++', 'Python', 'Java']
```

```python
"/".join(skills)
```
'c++/Python/Java'

```python
";".join(skills)
```
'c++;Python;Java'

#### 7.5 strip方法：

strip方法：用于对字符串头尾进行处理，示意图如下：

方法 说明

S.strip(chars=None)从S头尾处理，删除在chars中的元素，如果元素不在chars中，停止删除

| 方法/项 | 说明 |
|---|---|
| S.lstrip(chars=None) | 从S的开始位置开始处理，功能同上 |
| 方法 | 说明 |
| s.rstrip(chars=None | 从S的结尾位置开始处理，功能同上 |
| 参数：chars | 为指定字符集，默认为空白字符 |
```python
s = " \n msg "
```

```python
s
```
' \n msg '

```python
s.strip()
```
'msg'

```python
s = "#-msg#-"
```

```python
s.strip("-#")
```
'msg'

```python
s.lstrip("#-")
```
'msg#-'

```python
s.rstrip("#-")
```
'#-msg'

#### 7.6 字符串开头结尾判断

字符串判断开头或结尾：

方法 说明

S.startswith(prefix[, start[, end]])S以指定子串开头返回True，否则返回False

S.endswith(suffix[, start[, end]])S以指定子串结尾返回True, 否则返回False

| 方法/项 | 说明 |
|---|---|
| 参数：prefix | 子串 |
| 参数：start | 起始索引 |
| 参数：end | 结束索引 |
练习：过滤出所有的小米手机

mi = 'xiaomi'
listphone = ['xiaomi11', 'huaweimeta20', 'xiaomi11Pro', 'xiaomi10']

输出结果：

xiaomi11
xiaomi11Pro
xiaomi10

```python
s = "hello"
sub_s = "he"
```
```python
s.endswith("e")
```
False

```python
mi = 'xiaomi'
listphone = ['xiaomi11', 'huaweimeta20', 'xiaomi11Pro', 'xiaomi10']
```

```python
for phone in listphone:
if phone.startswith(mi):
print(phone)
```
xiaomi11
xiaomi11Pro
xiaomi10

#### 7.7 字符串大小写转换

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 返回值 |
| S.lower() | 将字符串中所有大写字符为小写 返回新字符串 |
| S.upper() | 将字符串中的小写字母转为大写字母 同上 |
| S.title()字符串标题化，将每个单词首字母大写，其他小写 | 同上 |
| S.capitalize() | 将字符串中的首字母大写，其他小写 同上 |
| S.swapcase() | 将字符串中的大小写交换 同上 |
练习：

```python
s = 'Python CookBook'
print('原字符串：',s)
print('字符全部小写：',s.lower())
print('字符全部大写：',s.upper())
print('单词首字母大写：',s.title())
print('首字母大写：',s.capitalize())
print('大小写转换：',s.swapcase())
```
原字符串： Python CookBook
字符全部小写： python cookbook
字符全部大写： PYTHON COOKBOOK
单词首字母大写： Python Cookbook
首字母大写： Python cookbook
大小写转换： pYTHON cOOKbOOK

#### 7.8 format方法

format：

1. 可以使用{}用来代替%，且参数位置与个数不受限制：
2. 指定位置{n}对应第n个参数;
3. 指定参数{name}；

练习：

```python
f = '{} age is {}'
print(f.format('sun', 18))
print(f.format('li', 19))
f = '{1} age is {0}'
#{1}对应zhang, {0}对应20
print(f.format(20, 'zhang'))
#指定参数
f = '{name} age is {age}'
print(f.format(name = 'zhao', age = 20))
```

```python
f = '{} age is {}'
print(f.format('sun', 18))
print(f.format('li', 19))
```
sun age is 18
li age is 19

```python
f = '{1} age is {0}'
#{1}对应zhang, {0}对应20
print(f.format(20, 'zhang'))
```
zhang age is 20

```python
#指定参数
f = '{name} age is {age}'
print(f.format(name = 'zhao', age = 20))
```
zhao age is 20

#### 7.9 字符串判断相关方法

主要内用于大小写，字符类型判断：

| 方法/项 | 说明 |
|---|---|
| 方法 | 说明 |
| S.isalpha() | 判断字符串中所有字符为字母 |
| S.isdigit() | 判断字符串中所有字符为数字 |
| S.islower/isupper() | 判断字符串中所有字符为小/大写字母 |
| S.isspace() | 判断字符串中所有字符为空格 |
S.istitle()判断字符串中所有的单词拼写首字母是否为大写，且其他为小写

```python
s = "12345"
s.isdigit()
```
True

```python
s = "abcd1"
s.isalpha()
```
False


## 附录 C 来源文件清单

| 章节 | 源文件 |
|---|---|
| 1. 数字 | `数字.txt` |
| 2. 字符串详解 | `字符串详解.txt` |
| 3. 列表 | `列表.txt` |
| 4. 列表解析 | `列表解析.txt` |
| 5. 序列 | `序列.txt` |
| 6. 字典 | `字典.txt` |
| 7. 集合 | `集合.txt` |
| 8. 拷贝问题（深浅拷贝） | `拷贝问题.txt` |
| 9. 模块与导入 | `1_模块与导入.txt` |
| 10. collections 模块 | `collections模块.txt` |
| 11. 随机数模块 | `随机数模块.txt` |
| 12. 时间处理 | `1_时间处理.txt` |
| 13. 函数基础详解 | `1_函数基础详解.txt` |
| 14. 匿名函数与函数式编程 | `2_匿名函数与函数式编程.txt` |
| 15. 递归函数 | `3_递归函数.txt` |
| 16. 闭包 | `4_闭包.txt` |
| 17. 装饰器 | `5_装饰器.txt` |
| 18. 生成器函数 | `6_生成器函数.txt` |
| 19. 文件详解 | `1_文件详解.txt` |
| 20. CSV 文件详解 | `2_csv文件详解.txt` |
| 21. Excel 文件详解 | `3_excel文件详解.txt` |
| 22. JSON 与 Pickle | `4_json与picke.txt` |
| 23. INI 配置文件处理 | `5_ini配置文件处理.txt` |
| 24. OS 模块目录处理 | `2_os模块目录处理.txt` |
| 25. 正则表达式 | `3_正则表达式.txt` |
| 26. 错误和异常 | `2_错误和异常.txt` |
| 27. 面向对象编程 | `1_面向对象编程.txt` |
| 28. 面向对象基础（课上练习） | `1_面向对象基础_课上练习.txt` |
| 29. 继承与反射 | `2_继承 _反射.txt` |
| 30. 班级练习（Jupyter） | `3_班级练习_jupyter.txt` |
| 31. 多进程详解与应用 | `2_多进程详解与应用.txt` |
| 32. 多线程详解与应用 | `3_多线程详解与应用.txt` |
| 33. MySQL 数据库操作 | `1_mysql数据库操作.txt` |
| 34. NumPy | `numpy.txt` |
| 35. Matplotlib | `matplotlib.txt` |
| 36. 逻辑强化（算法入门练习） | `1_逻辑强化_.md` |
| 37. 递归问题 | `2_递归问题.md` |
| 38. 回溯算法 | `4_回溯算法.md` |
| 39. 动态规划 | `5_动态规划.md` |
| 40. 贪心算法 | `6_贪心算法.md` |
| 41. 分治算法 | `7_分治算法.md` |
| 42. 附录 A：PDF合并PY1（Python 入门综合） | `PDF合并PY1.txt` |
| 43. 附录 B：PDF合并2-3章（列表等章节合并） | `PDF合并2-3章.txt` |
