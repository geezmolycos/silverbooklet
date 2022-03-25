# 「施法拼书」工具简介

silver booklet（施法拼书）是款供个人使用的印前拼版工具，用于个人借助普通打印机制作小册子、图书、广告单等。可在支持 Python 语言的多平台（包括但不限于 Windows, Linux, Mac OS）上使用。其使用 [Coconut](http://coconut-lang.org/) 写成。

# 主要特性

- 使用pdf格式作为输入输出，可与各类排版软件配合使用
- 可直接制作骑马钉、n合1、折页等版式
- 具有描述批量纸张操作的专用编程语言，以供个人设计编写自定的版式，可扩展性强
- 可兼容各种尺寸的纸张
- 命令行接口，可从stdin读取文件，方便自动化

# 目标用途

该工具并非内容排版工具，而是在已经制作好印刷品的pdf后，将多页合成一页（或一页拆成多页）以供普通打印机打印用的。该工具不同于传统拼版工具，没有图形界面，而是采取专用编程语言来描述拼版流程。本工具提供了一些常用的预设。

# 命令行用法

```plaintext
silver_cmd --argv [-h] [-o OUTPUT] [-p PRESET] [-c CODE] [--arg-preset ARG_PRESET] [--args ARGS] [--arrange {f,s,i,1,2}] [--arrange-flip {n,x,y,xy}]
                     input_file

必选参数:
  input_file            要排版的输入源文件

可选参数:
  -h, --help            显示帮助信息
  -o OUTPUT, --output OUTPUT
                        输出文件名，若双面排列方式设定为'f'，则会在设定名称后增加'_front'及'_back'后缀，以区分正反面文件
  -p PRESET, --preset PRESET
                        从文件中读取页面操作指令
  -c CODE, --code CODE  直接设置页面操作指令，优先度高于文件读取
  --arg-preset ARG_PRESET
                        从文件中读取页面操作参数，即预先执行的代码
  --args ARGS           直接设置页面操作参数
  --arrange {f,s,i,1,2}
                        双面排列方式。
                        'f'(默认): 将正反面结果分别保存到两个文件中
                        's': 依序排列，先输出正面，再输出反面
                        'i': 穿插排列，依次输出每张纸的正面和反面
                        '1': 只输出正面
                        '2': 只输出反面
  --arrange-flip {n,x,y,xy}
                        反面的翻转方向（n代表不翻转，默认为x）
```

# 语言参考文档

排版过程基于一种描述纸张操作的专用语言进行，通过模仿打印出来之后将纸裁剪、折叠后产生成品的过程，反向推导出每页应该印到哪里。

该语言构造简单，基于栈传递指令参数、进行计算。程序的运行环境包括程序存储器、指令计数器、操作数栈、变量存储器、纸篮子(basket)、手持纸空间(hand)。程序运行前，会将指令序列读取到程序存储器中，从第一条指令开始，进行指令(instruction)的解释。

每一条指令由一个无空格的字符串表示。指令有三种类型，分别为数字常数、字符串常数、命令(command)。

- 数字常数以`$`开头，后紧接python中可传入float的内容，表示一个浮点数
  - 例如 `$297`, `$0.2`, `$-87`, `$3e2`
- 字符串常数以`@`开头，后紧接字符串的内容
  - 例如 `@b1`, `@margin`, `@left`
- 命令以字母或下划线开头
  - 例如 `add`, `newpaper`, `transform`

数字常数和字符串常数指令会直接将其代表的值放入栈（操作数栈）顶。命令指令会执行规定好的某些操作，现列出如下：

## 数学命令

数学命令从栈中弹出若干个对象，进行数学运算后将其压回栈中，出栈顺序与「参数」一栏中所写的相反，也就是说，参数按照「参数」一栏所述的的顺序入栈。部分命令也适用于向量对象和仿射对象运算。
|命令|参数|功能|
|----|----|----|
|`neg, abs`|a|相反数、绝对值|
|`add, sub, mul, div, pow`|a, b|四则运算及乘方|
|`max, min`|a, b|计算最大最小值|
|`floor, ceil, round`|a|向上、向下和舍入取整|
|`aeq`|a, b|判断a和b是否近似相等(math.isclose)，相等则输出1.0，否则输出0.0|
|`aneq`|a, b|上述命令的否定|
|`eq, neq`|a, b|判断a和b是否严格（不）相等|
|`gt, lt`|a, b|判断a是否大于（小于）b|
|`ge, le`|a, b|判断a是否大于等于（小于等于）b|
|`not`|a|逻辑非，将非0.0的值变为0.0，0.0变为1.0|
|`or, and, xor`|a, b|逻辑或、与、异或|
|`vec`|float x, float y|将两个数合成一个2d向量对象|
|`vecup`|vec2 v|将2d向量对象分成两个数|
|`affine`|vec2 i, vec2 j, vec2 t|将三个向量组合成一个仿射变换对象，三个向量分别为基向量i，基向量j，位移向量t|
|`affineup`|affine a|将仿射变换对象分成上述三个向量|
|`affineinv`|affine a|求仿射变换的逆变换|
|`rotate`|float deg|求旋转仿射变换，旋转度数单位是角度|
|`translate`|vec2 v|求位移仿射变换|
|`scale`|vec2 v|求缩放仿射变换，将v的坐标视作缩放倍数|
|`flipx`||沿x轴翻转的仿射变换|
|`flipy`||沿y轴翻转的仿射变换|
|`identity`||单位仿射变换|

## 栈操作命令

栈操作命令可用来操作栈顶对象的顺序，类似Forth语言。

|命令|出栈|入栈|
|----|----|----|
|`swap`|ab|ba|
|`dup`|a|aa|
|`over`|ab|aba|
|`rot`|abc|bca|
|`drop`|a|-|

除此以外，还有`rev`命令，接受一个数字`n`，反转栈顶的`n`个元素的次序。`manip`命令，接受两个字符串，将其当作模板，替换栈顶元素，例如`@abc @bca manip`，其功能同`rot`命令。

## 实用命令

以下命令包括实现纸张操作功能和模拟印刷操作的命令，也包括一些杂项命令。纸空间是可以放一叠有顺序纸张的地方，每张纸有大小，有自己的变换（位移、旋转等仿射变换）。

|命令|参数|功能|
|----|----|----|
|`store`|thing, str name|将thing存储到变量存储器的name变量中|
|`load`|str name|读取变量存储器的name变量，放入栈中|
|`paperdim`|vec v|设置新纸张的尺寸|
|`newpaper`|float n|取n张新纸，放入手持空间|
|`takepaper`|str basket, float n|从篮子basket中取n张纸，叠加到手持空间上方，保持这些纸的变换|
|`takeallpaper`|str basket|取篮子basket中的所有纸，叠加到手持空间上方|
|`putpaper`|str basket|将手中的纸全部叠加到basket纸叠上方|
|`swappaper`|str basket|将手中的纸和basket中的纸交换|
|`cutpaper`|str b1, str b2|将手中的纸复制到篮子b1和b2中，保持变换，可用来模拟切分操作，但是现实中切分后的叠纸，在模拟时需要结合位移和叠加操作|
|`reversepaper`||手中的纸不翻面，反转顺序|
|`transform`|affine a|将仿射变换应用到手中的纸上|
|`transformflip`|affine a|类似上一条，但是如果仿射变换会改变手性（即镜像性），则翻转纸的正反面。可用来模拟给纸翻面|
|`printaffine`|affine a|设置印刷区域（以下所有的区域均指单位正方形经仿射变换后的区域）|
|`pageamount`||获取源页面数量|
|`printidx`|float n|设置下一次印刷时的开始页数|
|`pagedim`||获取源页面的尺寸|
|`print1`||获取等同于手中纸数量的源页面，按照印刷区域，一张纸印一页|
|`print2`||类似上一条命令，但是获取源页面时，每隔一页获取一页|
|`printdoublex`||获取两倍于手中纸数量的页面，关于x轴翻转，双面印刷到手中纸上|
|`printdoubley`||类似上一条，y轴翻转|
|`countbasket`|str basket|获取basket中纸的张数|
|`debuglog`|thing|将thing显示到程序输出中，以便于调试|
|`matplothand`||使用matplotlib画出手拿的纸|

## 流程控制命令

(TODO)