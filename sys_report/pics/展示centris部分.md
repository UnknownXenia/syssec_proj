### Centris

----

<!-- .slide: data-background="./duo.jpg"-->

![](../../../.typora-assets-0/算法流程-16559057792762.png)

整个流程分为以下两步：

* 构建数据库
* 识别目标项目中重用的代码

----

<!-- .slide: data-background="./duo.jpg"-->

#### 一、构建数据库

![image-20220606202031704](../../../.typora-assets-0/不消除冗余-16559057792773.png)

Note: 很多项目在迭代的过程中并不是迭代全部代码的，是在重用上一版代码的基础上进行的更新。直接把各版本的生态组件源代码直接存到数据库中，会造成大量的冗余

因此我们先需要把这部分的冗余先消除掉

----

<!-- .slide: data-background="./duo.jpg"-->

消除冗余

![image-20220606202031704](../../../.typora-assets-0/冗余消除-16559057792741.png)

Note: 我们的做法是：

1. 首先提取训练集中所有版本的C/C++文件
2. 为每个项目创建于版本总数一样多的bin
3. 当同一份代码出现在i个不同版本中时，将这个文件所属的版本信息以及每个版本的路径信息都会存贮在**<u>第i个</u>**bin中

----

<!-- .slide: data-background="./duo.jpg"-->

![image-20220607134327519](../../../.typora-assets-0/image-20220607134327519-16559057792774.png)

----

<!-- .slide: data-background="./duo.jpg"-->

![image-20220606202031704](../../../.typora-assets-0/LSH-16559057792775.png)

Note: 这里我们储存的是C/C++文件的hash值。我们对源代码进行一些处理(删去注释、统一换行与缩进等)，然后使用LSH(Locality Sensitive Hash)算法。这样能很好的将代码在高纬空间的相似性映射到低维空间去。

----

<!-- .slide: data-background="./duo.jpg"-->

#### 二、重用识别

----

<!-- .slide: data-background="./duo.jpg" style="text-align: left"-->

对待检测项目的操作：

1. 优化组件数据库，保留唯一代码
2. 从所有检测项目中提取代码
3. 识别检测项目中的重用组件

----

<!-- .slide: data-background="./duo.jpg" style="text-align: left"-->

S和P的关系：

- R1：S和P共享广泛使用的代码
- R2：S和P同时重用其他项目
- R3：S重用P
- R4：P重用S

$\phi(S,P)\ge\theta$

Note: 假设S为要检查是否包含第三方软件的项目，检测S与我们的组件数据库中的每个项目之间的公共file，如果数据库中存在一个项目P，P与S有一个或多个公共源码文件，则可以确定S和P的关系属于下述四个类别之一

因为hash算法本身降低了一些精确度，同时一些简单的代码本身存在通用的可能性，所以我们要设定一个阈值来过滤，只有满足以下公式，我们才可以判断为代码重用。

----

<!-- .slide: data-background="./duo.jpg" style="text-align: left"-->

训练集：`glibc-1.09.1` 到 `glibc-2.27` 共49个版本的文件

![image-20220606202031704](../../../.typora-assets-0/test1-1-16559057792776.jpg)

![image-20220606202031704](../../../.typora-assets-0/test1-2-16559057792787.jpg)

Note: 我们把 `glibc-1.09.1` 到 `glibc-2.27` 共49个版本的文件作为训练集，共存在264513个C/C++文件，消除冗余后，数据库中共收录20919条数据.

用 `glibc-2.31` 作为测试集，重用率达53.10%

----

<!-- .slide: data-background="./duo.jpg" style="text-align: left"-->

基于上面的数据库，我们测试了 `gdb-5.2.1`：

![image-20220606213532952](../../../.typora-assets-0/test2-16559057792788.png)

----

<!-- .slide: data-background="./duo.jpg" style="text-align: left"-->

优点：

1. 识别重用不依赖结构信息，无论结构如何变化都可以识别项目重用的代码
2. 无论项目是否嵌套，只要代码复用率大于阈值，就可以识别

----

<!-- .slide: data-background="./duo.jpg" style="text-align: left"-->

改进：

1. 与数据库的比较当前还是简单遍历，当数据库规模较大的时候，运行时间很长。需要探索一种基于阈值的哈希近似的最近邻搜索
2. 有些项目在不同版本间对代码存在些许修改，当前算法没有精确到对应版本（这也可能是file粒度过大的问题，如果是function粒度可以通过加权的方式来确定重用了那个版本代码）

 