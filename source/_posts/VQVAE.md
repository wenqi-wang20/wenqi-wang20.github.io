---
title: VQ-VAE
date: 2022-07-18 10:52:18
tags: 机器学习
categories: [深度学习, CV]
---

## VAE

先让我们简单地看一下 VQGAN+CLIP 的效果。这是 2021 年开源的一套自然语言+视觉处理的结合实验，人类可以输入一些句子和短语，在经过分析之后，从 text 转为 image 的过程。并且在合成图片的过程中，模型还会注意风格的融合。最新的研究成果是谷歌发布的 DALLE-2，风格非常炫酷，可惜没有开源，只有“内部人员”才能玩。下面是我在 Colab 上训练了 10 min 的结果，输入的 texts 是 `grown bears in the grass. |  a beautiful forest.`

![movie](https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpicturesmovie.gif)

现实中，很多输入的信息大量都是冗余无用的，我们可以使用某些压缩的、离散的表示就能够概括大部分内容。什么是 `AE`？自编码器，一般由三个部分构成：编码器、解码器以及中间隐藏层表示。我们可以将高维度的输入编码为低维度的表示，然后再通过解码器对该特征表示进行重建，**训练的损失就是重建的输出与原始输入之间的误差。**这样训练完成之后的编码器，可以结合 `few-shot learning` 进行特征学习，然后将学习后的特征用于分类任务；解码器则可以用于在特征空间上采样，生成新的输出。

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpicturesMDpicturesv2-ba9d7206d08e072b82401cec25415d2b_720w.jpg" alt="img" style="zoom: 67%;" />

而所谓 `VAE`，就是变分自编码器。为什么要产生变分自编码器？因为仅仅使用自编码器时，产生的隐式空间往往是离散的，如果我们从训练集没有覆盖的特征空间进行采样时，往往无法达到很好的效果，导致生成的图片 “四不像”。所以我们可以学习一个分布，编码器产生一个均值和另一个类似于 “标准差” 的输出，然后我们从正态分布中进行采样来给图片的特征向量加一个噪声。我们将这种扰动后的特征进行重建来生成输出。**训练损失我们采用重建后的误差 + 与混合高斯分布之间的 KL 散度两项**。

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpicturesimage-20220713111254448.png" alt="image-20220713111254448" style="zoom: 25%;" />

混合模型 `GMM`，$P(x)=\sum_{m}P(m)P(x|m) \quad x|m \sim N(\mu(m), \sigma(m))$。为了学习更加连续的分布，采用积分神经网路的方法，生成无限个高斯组件拟合真实分布，$P(x) = \int P(m)P(x|m)$。我们采用一个向量$z \sim N(0, 1)$来生成分布。编码器把输入向量 `x` 映射到最可能的高斯分布 `z` 上，然后解码器将该分布生成网络。但是生成的图片质量往往较低。

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpicturesimage-20220713123751929.png" alt="image-20220713123751929" style="zoom:25%;" />
$$
KL(N(\mu, \sigma), N(0, 1)) = \log \frac{1}{\sigma} + \frac{\sigma^2 + \mu^2}{2} - \frac{1}{2}
$$


## Neural Discrete Representation Learning

`Aaron van den Oord Oriol Vinyals Koray Kavukcuoglu， NIPS'17`

- `the Vector Quantised Variational AutoEncoder (VQ-VAE)`矢量量化自动微分编码器
- `It can successfully model important features that usually span many dimensions in data space as opposed to focusing or spending capacity on noise and imperceptible details which are often local.` 成功让潜在空间离散化，能够更加充分地屏蔽噪声，更好地利用潜在空间。

虽然说是 VAE，但其实模型建立过程中几乎没有涉及到变分的环节，看起来和 AE 倒是更像。

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpicturesimage-20220718102702579.png" alt="image-20220718102702579" style="zoom:60%;" />

## Generating Diverse High-Fidelity Images with VQ-VAE-2

VQ-VAE 的进阶版本，本质上并没有作出结构上的创新。主要针对经典版本作出了以下两点修改：

- 对原始像素图片进行了分层编码，分层量化，并且最终根据分层的结果重建图像。这样的方法可以充分把握全局视野，也可以细化局部细节，生成更加逼真，细节更加清晰的图像。

- 在对离散编码的先验知识的拟合阶段，采用了 PixelCNN 网络结构。

  <img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpicturesimage-20220718102402641.png" alt="image-20220718102402641" style="zoom: 67%;" >

## VECTOR-QUANTIZED IMAGE MODELING WITH IMPROVED VQGAN

这篇工作可以说是对 VQGAN 的改进，但其实我读的也不是特别明白，他到底改进了个啥……

- 当然，第一个改进的地方就是把带有局部注意力模块的 CNN 编码器干脆直接换成了 Vision Transformer。
- 第二个改进是在 codebook 方面。这篇工作首先将 codebook 因子化，简单来说可能就是先从低维的空间寻找匹配的 latent code, 然后再映射到更高维度的 latent code。这样做可以提高码本的使用率和重建图像的质量。
- 第三个小的 trick 就是文章将 latent code 进行了二范数归一化，所有向量的二范数都是一样大的，所以向量之间的欧氏距离就变成了类似余弦相似度，进一步提高了训练的稳定性。

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpicturesimage-20220718102746627.png" alt="image-20220718102746627" style="zoom:67%;" />

## MaskGIT: Masked Generative Image Transformer

这一连着的四篇工作都是出自谷歌的实验室。这一篇其实也是将 NLP 中的 BERT 模型的优化方法带到了图像合成的任务中。作者认为，在做序列译码的时候，从左上到右下进行逐个译码是非常不自然的行为。首先将图像全部展平会导致图像序列非常长，很少有实际的自然语言任务需要这么长的序列。其次，人类画家在创造作品的时候，也并不是按照从左上到右下进行绘画的，他们一般都是先绘画出一部分的轮廓，再跳到另一部上色……等等，具有一定的随机性。所以这篇文章也是借用了这种思想。

- 第一阶段训练 Encoder 和 Decoder 的设置和 VQGAN 相比没有太大的差别，作者沿用了之前的配置。
- 第二阶段训练先验分布的时候，文章采用了 MVTM 的方法，使用双向 Transformer 的机制并且设计掩码函数来帮助 Transformer 快速且并行地学习压缩后的 code matrix。

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpicturesimage-20220718102820012.png" alt="image-20220718102820012" style="zoom: 60%;" />

