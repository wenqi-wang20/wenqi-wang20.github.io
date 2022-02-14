---
title: DLG的代码实现
date: 2022-02-05 12:03:56
tags: 梯度泄漏
categories: 深度学习
---

上一章我们简单地说明了$Deep \ Leakage \ from \ Gradients$具体是利用什么方法实现的攻击，是一个非常简单清晰的思路，那就是通过“模拟梯度”来模拟输入和输出数据。最终实验的效果也非常地好。加上最近发现了一个非常好的论文代码实现网站：[paperswithcode](https://www.paperswithcode.com)，在这个网站上几乎所有的学术论文都能找到相对应的代码，所以我也打算复现一下这个攻击实验，以加深印象，同时也为联邦学习的发展打下基础。

作者的源代码其实思路比较简单，首先利用$torchvision$库给予的CIFAR100图片下载，然后取出第一章图片进行还原。作者提供了卷积神经网络$LeNet$和$ResNet$两种方法，我使用第一种方法，卷积通道数为12。

```python
class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        act = nn.Sigmoid
        self.body = nn.Sequential(
            nn.Conv2d(3, 12, kernel_size=5, padding=5 // 2, stride=2),
            act(),
            nn.Conv2d(12, 12, kernel_size=5, padding=5 // 2, stride=2),
            act(),
            nn.Conv2d(12, 12, kernel_size=5, padding=5 // 2, stride=1),
            act(),
        )
        self.fc = nn.Sequential(
            nn.Linear(768, 100)
        )

    def forward(self, x):
        out = self.body(x)
        out = out.view(out.size(0), -1)
        # print(out.size())
        out = self.fc(out)
        return out
```

因为我用的是macbook，所以没有N卡来训练，用的设备就是CPU。中间还出了一个小插曲，那就是下载数据的时候出现了$'str' \ object \ has \ no \ attribute \ '…'$，找了很长时间都没有找到问题，后来看到一篇博客说，这是ssl安全证书验证的问题，需要加上这一段话即可：

```python
import ssl

# 取消安全证书的检验，方便下载数据
ssl._create_default_https_context = ssl._create_unverified_context
```

理解了pytorch的语法和工作原理之后，整体的思路还是比较清晰的。作者采用的是交叉熵损失函数来判定损失程度。训练300轮之后，再看$dummy \ input$如何。在这里，我刚开始无论怎么训练都没办法还原图像，300轮之后始终全是噪声，loss也没有丝毫的下降。延长了轮数也没有导致收敛速度的加快。到最后我发现，我仅仅将$torch.manualseed()$的值从作者所给的1234改成了随便一个数字78483847，图片就完美地收敛了，而且在第一轮的loss就从原先的1000多下降到了70左右，40轮之后loss就下降到了0.1以内。最终的效果也是非常地好，在这里贴上效果图（前一张是随机生成的伪输入，后一张是经过训练之后的效果图）：

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/dummy.png" style="zoom:72%;" />

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/result.png" style="zoom:72%;" />

### 总结

从这个实验我们可以看出尽管这个方法非常地巧妙，但是有一个问题就是，必须要在第一次尝试$dummy \ imput$的loss足够的小，这样才能顺利地收敛，不然的话很可能无法起到攻击的效果。但是实话说，看到这个结果的时候我还是非常震撼的，确实能够在不接触数据，仅仅从梯度就几乎还原原图像，这样的结果是很令人不安的。
