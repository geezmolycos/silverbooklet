# 「施法拼书」工具简介

silver booklet（施法拼书）是款供个人使用的印前拼版工具，用于个人借助普通打印机制作小册子、图书、广告单等。可在支持 Python 语言的多平台（包括但不限于 Windows, Linux, Mac OS）上使用。其使用 [Coconut](http://coconut-lang.org/) 写成。

# 主要特性

- 使用pdf格式作为输入输出，可与各类排版软件配合使用
- 可直接制作骑马钉、n合1、折页等版式
- 具有描述批量纸张操作的专用编程语言，以供个人设计编写自定的版式，可扩展性强
- 可兼容各种尺寸的纸张
- 命令行接口，可从stdin读取文件，方便自动化

# 目标用途

该工具并非内容排版工具，而是在已经制作好印刷品的pdf后，将多页合成一页（或一页拆成多页）以供普通打印机打印用的。该工具不同于传统拼版工具，没有图形界面，而是采取专用编程语言来描述拼版流程，本工具提供了一些常用的预设。

# 命令行用法

```plaintext
coconut -r silver_cmd.coco --argv input_file [-o output_file] [-p preset] [-c code] [--arg-preset filename] [--args args] [--arrange f|s|i] [--arrange_flip n|x|y|xy]

```

# 语言参考文档

(TODO)
