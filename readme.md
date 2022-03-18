# silver booklet

silver booklet 是一个命令行小程序，可以根据一种方便的表示方法，按照用户描述的装订方式，将pdf文件排列组合成可供普通打印机直接打印的版式。

使用基于工序的排版流程描述。通过描述如何用打印出的纸，经过一系列「裁剪」工序，制作出成品书，来自动生成排版方案。
有以下几个操作：

```plaintext
工序的过程，涉及若干个放纸的地方，叫做basket，还有操作的地方，叫做hand。
使用basket也可以访问到hand，名字就是hand，还有空basket，类似/dev/null，名字叫scrap
基于栈的语言，数据以$开头表示数字，字母或_开头代表命令，@开头表示字符串
使用后项式，即从前向后执行
以下命令参数从后向前为出栈顺序
存储空间包括：操作栈、变量储存器、页面存储器、手(hand)、篮子(basket)
- 数学操作
st <thing> <name> : 储存一个栈上的值，名称为name
ld <name> : 读取名称name到栈中
affineinv <affine> : 求仿射变换的逆变换
neg, add, sub, mul, div, pow, abs, floor, ceil, round
eq, neq, gt, lt, ge, le, not, or, and, xor
swap, dup, over, rot, drop
manip: 弹出两个字符串模板，根据模板操作栈顶的元素
rev <n>: 颠倒栈顶n个元素的次序
vec <x> <y> : 生成一个2维向量对象，压入栈
affine <mati> <matj> <tsl> : 生成一个仿射变换对象，压入栈
upvec, upaffine : 解包上述对象
rotate <degree> : 生成绕原点旋转<degree>度(逆时针)的affine对象。
translate <vec> : 
flipx, flipy : 
- 流程控制
if-fi if获取栈中的值，若读到的值为0，则跳转到配对的fi处
wh-hw 执行到hw的时候，会向前方跳转到配对的wh处 (实现while效果，wh 判断条件 if ... hw fi)
for-rof 从栈中弹出一个数字，循环这么多次，每一次向栈里面放一个数字，表示当前循环次数，从0开始($4 for .. rof)
- 手纸操作
originc : 将原点重定向到最上层纸bounding box的左下角。(todo)
originm : 将原点重定向到最上层纸的中心。(todo)
origin <vec> : 将原点重定向到最上层纸指定比例的位置(0~1)。(todo)
reverse : 颠倒手中纸的上下次序。
afftrans: 对手中的所有纸进行仿射变换。
trim : 清除没有大小的空纸(todo)
glue : 将奇数和偶数的纸粘到一起，只露出奇数的正面和偶数的反面，合成一张纸。(todo)
- 拿放操作
takepaper <basket> <quantity>: 从basket拿纸到手中放到手上方。
takeall <basket>
putpaper <basket>: 把手中的纸放到basket上方。
swappaper <basket> : 交换手中和basket中的纸。
- 切分操作 (之后可能会实现，现在只有一个cut命令)
cutx <b1> <b2> 沿x轴切分, b1是负半轴的去向
cuty <b1> <b2> 沿y轴切分
cut2x, cut2y <basket1> <basket2> : 沿x/y向对半切分手中的纸，将下叠放到basket1，上叠放到basket2。
cutnx, cutny <basket1> <basket2> ... <n>: 沿某向n等分手中的纸
mntx, mnty : 沿某向山峰折叠并切割手中的纸，留在手中，左下角纸的取向不变
vlyx, vlyy : 山谷
- 印刷操作
printaffine <affine> : 设置印刷区域仿射变换
pageamount : 获取页数
pagedim: 获取页面大小
print2 : 从印刷指针处取和手纸数量相同的页数，根据printdim设置，隔一页印一次到正面。
printdblx : 双面打印，沿x翻转。
printdbly : 双面打印，沿y翻转。
print1 : 同上，连续取页。
printidx <n> : 设置印刷指针
- 新纸操作
paperdim <vec> : 设置来源纸张大小
newpaper <n> : 获取n张新纸，放到手中（上面），上面是第0张，下面是第n-1张

```
