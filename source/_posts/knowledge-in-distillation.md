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

### FitNet(hint layers)

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

### Attention Maps (multi-layer group)

> - 将注意力作为知识在不同网路之间转移的机制
> - 提出了activation-based 和 gradient-based 的特征空间注意力映射。

#### activation-based attention

卷积神经网络的激活张量$A \in R^{C \times H \times W}$，含义是C张包括大小为$H \times W$的特征平面，同时我们可以利用以下的映射来帮助我们“压缩”到一个平面上
$$
\mathcal{F}: R^{C \times H \times W} \rightarrow R^{H \times W}
$$
![](https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220311150304.png)

可以用以下几种方式来产生activation-based 的注意力映射

- $F_{\operatorname{sum}}(A)=\sum_{i=1}^{C}\left|A_{i}\right|$
- $F_{\text {sum }}^{p}(A)=\sum_{i=1}^{C}\left|A_{i}\right|^{p}$，对激活程度更高的某些神经元所在的空间位置给予更多的权重
- $F_{\max }^{p}(A)=\max _{i=1, C}\left|A_{i}\right|^{p}$，每次仅仅携带单个激活程度最好的神经元

我们可以挑选教师模型和学生模型特定的residual block之后的输出层作为注意力映射匹配的pair:
$$
\mathcal{L}_{A T}=\mathcal{L}\left(\mathbf{W}_{S}, x\right)+\frac{\beta}{2} \sum_{j \in \mathcal{I}}\left\|\frac{Q_{S}^{j}}{\left\|Q_{S}^{j}\right\|_{2}}-\frac{Q_{T}^{j}}{\left\|Q_{T}^{j}\right\|_{2}}\right\|_{p}
$$
上面是定义的损失函数，其中Q代表的是注意力映射函数的向量化表示，p是范数，通常采用l-2范数进行归一化。

#### Gradient-based Attention

简而言之就是可以看成为一个输入敏感性映射，在某些空间位置的attention的意思就是代表这个空间位置的输入的微小改变能够带来结果上的很大变化，也就是需要**特别关注的地方**。

我们先定义教师和学生网络关于输入的梯度：
$$
J_{S}=\frac{\partial}{\partial x} \mathcal{L}\left(\mathbf{W}_{\mathbf{S}}, x\right), J_{T}=\frac{\partial}{\partial x} \mathcal{L}\left(\mathbf{W}_{\mathbf{T}}, x\right)
$$
然后再定义优化函数，也就是需要让学生网络靠近教师网络关注的目标：
$$
\mathcal{L}_{A T}\left(\mathbf{W}_{\mathbf{S}}, \mathbf{W}_{\mathbf{T}}, x\right)=\mathcal{L}\left(\mathbf{W}_{\mathbf{S}}, x\right)+\frac{\beta}{2}\left\|J_{S}-J_{T}\right\|_{2}
$$

### Activation Boundaries (Pre-ReLU)

这篇文章主要想做的就是在学生网络开始训练之前就将教师有关神经元的相关信息转移到学生模型上。之前的损失函数都是基于神经元的响应的均方差损失，但是这些损失都是建立在强响应上的，但是神经元的决策边界通常是介于零响应和无响应的
$$
\mathcal{L}(\boldsymbol{I})=\|\sigma(\mathcal{T}(\boldsymbol{I}))-\sigma(\mathcal{S}(\boldsymbol{I}))\|_{2}^{2}
$$
![](https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220311162135.png)

所以他们定义了一种元素级别的激活指标函数来表示，并且给出了离散形式的损失函数
$$
\rho(x)=\left\{\begin{array}{ll}
1, & \text { if } x>0 \\
0, & \text { otherwise }
\end{array}\right. \\
\mathcal{L}(\boldsymbol{I})=\|\rho(\mathcal{T}(\boldsymbol{I}))-\rho(\mathcal{S}(\boldsymbol{I}))\|_{1}
$$
为了使得这种损失可以被梯度下降的方法进行优化，作者采取了在支持向量机里用到的一种损失：hingle loss，并且给出了在不同的情况下，损失函数求导的结果：
$$
\mathcal{L}(\boldsymbol{I})=\| \rho(\mathcal{T}(\boldsymbol{I})) \odot \sigma(\mu \mathbf{1}-\mathcal{S}(\boldsymbol{I})) 
+(\mathbf{1}-\rho(\mathcal{T}(\boldsymbol{I}))) \odot \sigma(\mu \mathbf{1}+\mathcal{S}(\boldsymbol{I})) \|_{2}^{2} \\
-\frac{\partial \mathcal{L}(\boldsymbol{I})}{\partial s_{i}}=\left\{\begin{array}{ll}
2\left(s_{i}-\mu\right), & \text { if } \rho\left(t_{i}\right)=1 \text { and } s_{i}<\mu \\
-2\left(s_{i}+\mu\right), & \text { if } \rho\left(t_{i}\right)=0 \text { and } s_{i}>-\mu \\
0, & \text { otherwise. }
\end{array}\right.
$$
以上方法是建立在老师和学生模型的神经元数量完全一致的情况下。当我们 考虑到模型压缩的时候，老师和学生模型的结构就会产生差别，所以一般会使用一个全连接层或者是批处理规范化层。定义一连接器的功能将学生的response的大小转化为和老师一样的respense向量的大小。



## Relation-based Knowledge

之前的方法主要关注的都是单个数据本身能够体现的知识，并且利用教师模型中某些特定层的输出。我们可以考虑基于relation的知识，这种关系有两种来源：来自不同层之间的关系，以及来自不同样本数据之间的关系。

### Singular Value Decomposition in KD (between layers)

- 用奇异值分解的方法对特征信息进行降维，并且通过一个RBF函数来描述特征映射函数之间的关系，也就是通常的核学习（kernalize learning）
- 采用自监督的方法，自己产生标签。这可以解决知识遗忘问题，并且提供更有力的正则化手段。

方法没怎么看懂

### Information Flow Model. (between data samples)

这个方法对于教师模型的不同层之间的信息流进行建模。

实验表明，在训练的早期，会形成神经元之间的关键连接道路，经过了这几轮训练之后，信息可塑性就会下降，事实上学生模型能够从教师模型那里学到的知识就会变得有限。那么文章提出了一种可能性，就是在模型训练的不同阶段，使用不同强度的监督。具体来说，采用以下的方法：

- 设计辅助教师模型（size和学生模型差不多）来帮助在教师模型和学生模型之间建立一对一的、有效的匹配
- 在关键学习路径上模仿教师模型的信息流

需要用到核函数（$Kernal \ Function$），待研究。



