---
title: knowledge in distillation
date: 2022-03-06 14:38:13
tags: [联邦学习，知识蒸馏]
categories: 深度学习 
---

今天这一篇我们主要介绍三种基于不同知识的知识蒸馏方法的技术概括。

## Response-based knowledge

这也是最常见，最容易理解的知识蒸馏：
$$
q_{i}=\frac{\exp \left(z_{i} / T\right)}{\sum_{j} \exp \left(z_{j} / T\right)}
$$
神经网络通常使用softmax层来揭示分类任务的预测概率，我们可以改变蒸馏温度$T$，然后使得概率分布更加的平滑化。紧接着小模型可以模拟大模型在同一个数据集上的softmax输出的概率表现，同时结合hard-labels给出的预测误差，来共同训练一个更小、更容易部署的student model。下面分别是蒸馏损失和student模型预测的交叉熵损失，训练损失是二者的线性组合：
$$
L_{\operatorname{Res} D}\left(p\left(z_{t}, T\right), p\left(z_{s}, T\right)\right)=\mathcal{L}_{R}\left(p\left(z_{t}, T\right), p\left(z_{s}, T\right)\right) \\
\mathcal{L}_{C E}\left(y, p\left(z_{s}, T=1\right)\right) \\
\mathcal{L} = \alpha \mathcal{L}_{R} + \beta \mathcal{L}_{CE}
$$
![image-20220306151204550](/Users/wangwenqi/Library/Application Support/typora-user-images/image-20220306151204550.png)

## Feature-based Knowledge

在训练student model，尤其是更深更窄的神经网络上，加入中间特征层的引导有时候能够起到很好的效果。

### FitNet

核心的思想是：

> We introduce *intermediate-level hints* from the teacher hidden layers to guide the training process of the student, *i.e.*, we want the student network (FitNet) to learn an intermediate representation that is predictive of the intermediate representations of the teacher network.

FitNet的目的是为了加强KD的学习，训练一个更深、更窄的学生网络模型，因为更深的模型往往具有更好的非线性，在做出决策时往往有更好的表现。

![](https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220307232850.png)

> - 主要分为两个部分，第一部分是利用训练好的教师模型对student模型的中间层参数进行正则化处理，是一个预训练的过程
>
> - 第二部分是对于整个student model的KD训练

$$
stage-1:& \  
\mathcal{L}_{H T}\left(\mathbf{W}_{\text {Guided }}, \mathbf{W}_{\mathbf{r}}\right)=\frac{1}{2}\left\|u_{h}\left(\mathbf{x} ; \mathbf{W}_{\mathbf{H i n t}}\right)-r\left(v_{g}\left(\mathbf{x} ; \mathbf{W}_{\mathbf{G u i d e d}}\right) ; \mathbf{W}_{\mathbf{r}}\right)\right\|^{2} \\ 
stage-2:& \
\mathcal{L}_{K D}\left(\mathbf{W}_{\mathbf{S}}\right)=\mathcal{H}\left(\mathbf{y}_{\text {true }}, \mathrm{P}_{\mathrm{S}}\right)+\lambda \mathcal{H}\left(\mathrm{P}_{\mathrm{T}}^{\tau}, \mathrm{P}_{\mathrm{S}}^{\tau}\right)
$$

### Attention Maps

> - 将注意力作为知识在不同网路之间转移的机制
> - 提出了activation-based 和 gradient-based 的特征空间注意力映射。
