---
title: 基于高效同态加密的Cross-silo联邦学习
date: 2021-12-03 12:25:20 
tags: 联邦学习
---

## Background

> 回顾[联邦学习](https://www.zhihu.com/search?q=联邦学习&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})（federated learning，FL）的发展，目前目前主要有Cross-Silo的模式和Cross-device模式。前者面向机构，后者则是针对终端。其次，也有许多工作研究FL中[梯度更新](https://www.zhihu.com/search?q=梯度更新&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})带来的隐私泄露。针对隐私泄露，目前主要通过[安全聚合](https://www.zhihu.com/search?q=安全聚合&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})（e.g., 求和/平均）来实现保护隐私的目的。现在主要的安全聚合方案，主要有基于秘密分享、基于成对加性掩码、基于差分隐私，和基于[同态加密](https://www.zhihu.com/search?q=同态加密&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})（Homomorphic Encryption，HE）的方案。各种方案各有利弊。
> 本文主要针对Cross-Silo场景下，加速基于HE的安全聚合方案，并减少通信开销。
> *Main Contributions: 本文主要提出了一种梯度量化的方法，并对量化梯度进行batch encoding。进一步，在batch encoding的梯度上进行HE 操作。*

![image-20211203123128193](C:\Users\19749\AppData\Roaming\Typora\typora-user-images\image-20211203123128193.png)

## Process

前人的量化方案：将一个 $y \in \left [ -1, 1 \right]$的梯度量化为一个8-Bit的无符号整数，量化函数和解量化函数如下：

![[公式]](https://www.zhihu.com/equation?tex=Q%28g%29%3D%5B255%5Ccdot+%5Cfrac%7Bg-min%7D%7Bmax-min%7D%5D) ，其中 ![[公式]](https://www.zhihu.com/equation?tex=%5B%5D) 是就近[取整函数](https://www.zhihu.com/search?q=取整函数&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})（rounding function）;
![[公式]](https://www.zhihu.com/equation?tex=Q%5E%7B-1%7D%28q_n%29%3Dq_n%5Ccdot+%5Cfrac%7Bmax-min%7D%7B255%7D%2Bn%5Ccdot+min) ，其中 ![[公式]](https://www.zhihu.com/equation?tex=q_n) 是 ![[公式]](https://www.zhihu.com/equation?tex=n) 个量化梯度之和。

但是上述量化方法存在一定的问题：

> 1. 要正确计算 ![[公式]](https://www.zhihu.com/equation?tex=Q%5E%7B-1%7D%28%5Ccdot%29) ，必须事先预知 ![[公式]](https://www.zhihu.com/equation?tex=n) 。因此，每次加入新的用户，需要手动检验调整 ![[公式]](https://www.zhihu.com/equation?tex=n) 的取值；
> 2. 容易溢出。因为所有的[正负梯度](https://www.zhihu.com/search?q=正负梯度&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})都编码为无符号整数，多个用户的[累加值](https://www.zhihu.com/search?q=累加值&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})容易导致溢出；
> 3. 不能区分正溢出和负溢出。

本篇文章进行了一定的改善，主要解决了以下几个问题：

> \1. 有符号量化：梯度被量化为有符号的整数，这样一来正负值相互抵消有助于解决溢出问题；
> \2. 关于[原点对称](https://www.zhihu.com/search?q=原点对称&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})的量化区间：为了保证相反符号数能够正确的抵消，量化区间必须关于原点对称。否则，假设将 ![[公式]](https://www.zhihu.com/equation?tex=%5B-1%2C1%5D) 量化到 ![[公式]](https://www.zhihu.com/equation?tex=%5B-128%2C127%5D) ，那么 ![[公式]](https://www.zhihu.com/equation?tex=%28-1%2B1%29%5CRightarrow%28-128%2B127%29%3D-1) ，结果错误；
> \3. 均匀量化。这是为了保证[量化数值](https://www.zhihu.com/search?q=量化数值&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})的加同态性质需要满足的性质。

粗略来说便是将 ![[公式]](https://www.zhihu.com/equation?tex=%5B-%5Calpha%2C0%5D) 量化到 ![[公式]](https://www.zhihu.com/equation?tex=%5B-%282%5Er-1%29%2C0%5D) ，将 ![[公式]](https://www.zhihu.com/equation?tex=%5B0%2C%5Calpha%5D)量化到 ![[公式]](https://www.zhihu.com/equation?tex=%5B0%2C%282%5Er-1%29%5D) 。；公式化表示如下：
![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Bequation%7D+Q%28g%29%3D+%5Cbegin%7Bcases%7D+%5Clceil+g%5Ccdot+2%5Er%5Crceil%2C+g%5Cin+%5B-%5Calpha%2C0%5D%3B%5C%5C+%5Clfloor+g%5Ccdot+2%5Er%5Crfloor%2C+g+%5Cin+%5B0%2C%5Calpha%5D+%5Cend%7Bcases%7D+%5Cend%7Bequation%7D+) ，其中 ![[公式]](https://www.zhihu.com/equation?tex=%5Clceil+%5Ccdot+%5Crceil) 和 ![[公式]](https://www.zhihu.com/equation?tex=%5Clfloor+%5Ccdot%5Crfloor) 分别是向上取整和向下取整函数；
![[公式]](https://www.zhihu.com/equation?tex=Q%5E%7B-1%7D%28q_n%29%3Dq_n%2F2%5Er) ；
进一步，实用2-bits 表示符号位（[sign-bits](https://www.zhihu.com/search?q=sign-bits&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A326712188})）。如此， ![[公式]](https://www.zhihu.com/equation?tex=0) 便有了两种编码方式。

![image-20211203132307261](C:\Users\19749\AppData\Roaming\Typora\typora-user-images\image-20211203132307261.png)

## Performance

实验的最终表现也是体现出$BatchCrypt$和$stock$相比在通信和计算上都有着很大的提升，但是和$Plaintext Learning$相比还是有很大的进步空间。

<img src="C:\Users\19749\AppData\Roaming\Typora\typora-user-images\image-20211203133101593.png" alt="image-20211203133101593" style="zoom:50%;" />

<img src="C:\Users\19749\AppData\Roaming\Typora\typora-user-images\image-20211203133118275.png" alt="image-20211203133118275" style="zoom:50%;" />

