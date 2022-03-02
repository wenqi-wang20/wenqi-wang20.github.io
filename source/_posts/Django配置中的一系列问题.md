---
title: Django配置中的一系列问题
date: 2022-03-02 19:25:03
tags: [Pycharm, git]
categories: [配置文件语言]
---

## pycharm

这两天在配置Django的时候，又遇到了关于pycharm配置虚拟环境的问题。

整体来说，我们需要看下面这一张图，这是关于项目配置信息的：

![](https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220302194058.png)

我们可以看到“工具”-“终端”里面有shell的路径，一般来说，我们的shell都是会默认使用系统base的路径。这会导致在pycharm自带的终端下进行操作会使用环境变量的包（当然这些都是windows上面的问题，上述图片是mac的，不过意思大致相同）

有两种方法：

- 第一种是在shell路径的后面  +  `/k + "虚拟环境路径中的activate脚本"`
- 第二种方法是去到venv文件夹里，手动执行activate，然后再回来看，就发现终端已经变成虚拟环境了

就像这样：

![](https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220302194942.png)

## git

最近学到了一些新的命令

```bash
git log --graph
```

这个基本上可以展示当前仓库里所有的分支提交和合并的记录，以图片的形式展示。

比较麻烦的主要是CI/CD的部署。

CI/CD，我的理解就是，能够在提前配置好任务的情况下，在你push代码到云端的时候，在一个指定的container里面跑你的测试。

总体来说就是分为三步：

- 配置Dockerfile，用来指定容器的规模。
- 配置.gitlab-ci.yaml，用来指定要完成的任务。
- 配置gitlab-runner，用来配置容器。
