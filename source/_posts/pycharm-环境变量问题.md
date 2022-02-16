---
title: pycharm 环境变量问题
date: 2022-02-16 10:02:26
tags: Pycharm
categories: Ubuntu
---

前几天在重装fedml系统的时候遇到了一个小小的问题，起因是因为我更换了mac系统，所以也用了新的parallel desktop虚拟机。

> **在这里不得不吐血推荐，pd真的是比vm好了太多。**我虽然不是资深果粉，但是对于苹果系统的流畅和比较良好的生态还是有所耳闻的。pd最好用的一点，也是我觉得最方便的一点就是，**共享文件系统做的很方便，网络也都是预先搭接好的。**甚至可以直接从我的ubuntu里访问mac的所有文件系统。

言归正传，我遇到的问题如下：

![](https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220215183333.png)

就是在pycharm里，我标记了项目根目录为源根，而且无论是控制台还是文件视图里都没有出现报错，也可以正常导入根目录下的包。但是当我在terminal里run一个文件的时候，他就会报出类似：

```bash
ModuleNotFoundError: No Module named 'fedml_api'
```

的错误。实在是让我很破防。

后来我听取网友的建议，在右下角python解释器设置里，添加了解释器路径。在控制台里输出`sys.path`发现也可以找到当前项目路径。但是在终端里就是不行。鉴于需要添加的文件太多，我总不能每次都在文件前面加入

```python
import sys
sys.path.append()
```

我也activate了虚拟环境，仍然出现这种情况，说明系统对于解释器设置的环境变量不认账。所以我决定以逸待劳，直接设置全局的`PYTHONPATH`，把项目目录包括到python的搜索路径里面。

```bash
echo $PYTHONPATH
```

果然什么都没有。于是我在pycharm添加了用户环境变量，重启IDE，发现就可以运行了。这样就可以在venv中直接使用了。

