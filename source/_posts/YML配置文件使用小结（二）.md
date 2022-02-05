---
title: YML配置文件使用小结（二）
date: 2022-01-10 01:43:49
tags: YML
categories: 配置文件语言
---

咱们书接上回。说到了我想要配置hexo中的封面背景图片。但是有几个问题急需解决。第一个就是我想要大量的图片源，这些可能是外链、也有可能是本地图片。（大概率是本地图片，因为我想要对网络图片进行压缩之后再作上传处理）。然后**我想要交给一个脚本进行定期的更新，每次操作都会载入100张全新的图片进入yml配置文件。**打算分为以下几个步骤：

## 步骤一：使用python脚本爬取网络图片并且进行压缩

![](https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpictures37a1f0278433ff8ae9dc802f03861b5.png)

![](https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpictures20220110031701.png)

这里直接使用了网络上一个爬取4K壁纸的爬虫，略加修改得到的。每次都会定期爬取大约100张图片，并且清空原有的文件夹中的图片。

然后我们使用`PIL`库，也就是我们熟知的pillow中的Image功能组件，对图片进行压缩处理。**这里有一个比较坑的地方是`resize()`方法中的长和宽是要加上括号的，是一个二元组。**

![](https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpictures20220110112406.png)

这样一来所有压缩后的图片就已经完全躺在了compressed文件夹中了。每次我们会通过遍历文件夹中的文件数来确定新的文件应该如何命名。

## 步骤二： 读入YAML文件并且对其进行修改

这一块我们依然使用上一次的Python脚本进行批量处理。我们想要做到的是随机选取60张图片作为图片库，注入到yml文件。

- 首先，我们需要引入`yaml`库，这一块需要`pip install pyyaml`来安装包。

- 然后我们使用Load方法打包yaml文件中的内容，获取其中的解析格式。

- 最后我们将修改后的列表插入到解析的字典当中替换原列表，然后通过`dump`方法加载到config文件中

这样我们的就大功告成了，可以通过脚本每次完成自动更新，更换主页的图片。

![](https://raw.githubusercontent.com/wenqi-wang20/img/main/img/MDpictures20220110150813.png)
