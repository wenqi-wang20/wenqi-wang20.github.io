---
title: YML配置文件使用小结
date: 2022-01-10 00:20:44
tags: YML
categories: 配置文件语言
---

今天在配置hexo的时候发现想要更新照片封面必须要编辑yml文件，想到之前捣腾linux的时候也见过这个格式的文件，但是当时不甚了了，今天不如一起了解一下。

## 什么是YML文件

 **YAML（Yet Another Markup Language）**（发音 /ˈjæməl/ ）是 一种基于[Unicode](https://so.csdn.net/so/search?q=Unicode)容易阅读，容易和脚本语言交互的，用来表达资料序列的编程语言。

yaml文件是一种通用的数据串行化格式。（我们在用于模块通信的时候，会将对象序列化为通信流，高效地传输到另一个模块，并且提供反序列化还原数据）

## 基本格式

Yaml语言编辑的文件，后缀为.yml。格式有以下几点基本要求：

- 大小写敏感
- 使用缩进表示层级关系
- 缩进时不允许使用Tab键，只允许使用空格。
- 缩进的空格数目不重要，只要相同层级的元素左侧对齐即可

在yml文件中，$\#$符号表示的注释。yaml支持的数据类型有

- 对象：键值对的集合，又称为映射（mapping）/ 哈希（hashes） / 字典（dictionary）
- 数组：一组按次序排列的值，又称为序列（sequence） / 列表（list）
- 纯量（scalars）：单个的、不可再分的值

#### 对象

```yaml
# conf.yml
animal: pets
hash: { name: Steve, foo: bar }
```

转化为json为：

```json
// conf.json
{
    { "animal": "pets" },
    { "hash": { "name": "Steve", "foo": "bar" } }
}
```

#### 数组

```yaml
# conf.yml
Animal:
 - Cat
 - Dog
 - Goldfish
```

转化为json为：

```json
//conf.json
{ "Animal": [ "Cat", "Dog", "Goldfish" ] }
```

#### 字符串

```yaml
# conf.yml
# 正常情况下字符串不用写引号
str: 这是一行字符串
# 字符串内有空格或者特殊字符时需要加引号
str: '内容： 字符串'
```

#### 空值

```yaml
# conf.yml
parent: ~
```

等价于json中的

```json
{ "parent": null }
```

