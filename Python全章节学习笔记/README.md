# Python 全章节学习笔记 📘

从课程课件（PDF + Jupyter HTML）自动提取整理的 **Python 学习笔记**，覆盖基础语法 → 函数式编程 → 文件与数据 → 面向对象 → 并发 → 数据库 → 数据分析 → 算法，共 **43 个章节**。

## 📄 核心内容

- **[Python全章节学习笔记.md](./Python全章节学习笔记.md)** — 汇总笔记（约 350KB / 1.6 万行）
  - 12 大部分 + 附录，43 个章节
  - 代码块完整保留（算法章节来自 Jupyter 笔记，含运行输出）
  - PDF 课件中的"方法/说明"已自动转为 Markdown 表格
  - 文末附来源文件清单

## 📂 目录结构

```
├── Python全章节学习笔记.md   # 汇总笔记（主文件）
├── 算法解压/                 # 算法章节原始 Jupyter HTML（逻辑强化/递归/回溯/动态规划/贪心/分治）
└── scripts/                  # 提取与生成脚本
    ├── extract_all.py        # HTML 笔记提取
    ├── extract2.py           # PDF 提取（layout 顺序恢复 + 侧栏清理 + 表格化）
    ├── build_md.py           # 组装汇总 Markdown
    ├── ocr.swift             # macOS Vision OCR（恢复图片型幻灯片文字）
    └── ocr_batch.sh          # OCR 批处理
```

## 📚 章节大纲

| 部分 | 内容 |
|---|---|
| 一 | 数字、字符串、列表、列表解析、序列、字典、集合、深浅拷贝 |
| 二 | 模块与导入、collections、随机数、时间处理 |
| 三 | 函数基础、匿名函数、递归、闭包、装饰器、生成器 |
| 四 | 文件、CSV、Excel、JSON/Pickle、INI、OS |
| 五~六 | 正则表达式、错误和异常 |
| 七 | 面向对象、继承与反射、课堂练习 |
| 八 | 多进程、多线程 |
| 九~十 | MySQL、NumPy、Matplotlib |
| 十一 | 算法与数据结构（逻辑强化、递归、回溯、动态规划、贪心、分治） |
| 附录 | 合并版 PDF 内容 |

## 🔧 重新生成笔记

```bash
cd scripts
python3 extract2.py        # 从 PDF 提取（依赖 pypdf）
python3 build_md.py        # 生成 Python全章节学习笔记.md
```

> 原始课件 PDF 体积较大（约 20MB），未包含在本仓库中；如需要可自行补充（去除 `.gitignore` 中的 `*.pdf` 即可）。

## 📝 说明

- 内容由课件自动提取整理，个别图片型幻灯片通过 macOS Vision OCR 补充（可能有少量识别误差，已在文中标注"OCR 补充"）
- 面向 Python 3.x，算法章节基于 Jupyter Notebook
