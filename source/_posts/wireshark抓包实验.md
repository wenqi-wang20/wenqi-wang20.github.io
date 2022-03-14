---
title: wireshark抓包实验
date: 2022-03-05 08:13:29
tags: 计算机网络原理
categories: 实验报告
---

## 抓包实验一

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220305082106.png" style="zoom:25%;" />

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220305082250.png" style="zoom: 25%;" />

1. 观察上述抓包过程可以得知，涉及到39.156.66.14(www.baidu.com)的ping功能采取的都是$ICMP \ protocol$。
2. 主机host会先向远程服务器发送一个request请求，并且携带时间戳；然后服务器返回一个response的事件，这样就可以计算出ping的延时。



## 抓包实验二

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220313215119.png" style="zoom:25%;" />

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220313221113.png" style="zoom:25%;" />

<img src="https://raw.githubusercontent.com/wenqi-wang20/img/main/blog/20220313221143.png" style="zoom:25%;" />

1. 我们观察发现，抓取中国政府网(http://www.gov.cn/)的数据是可以从中直接看到html网页源代码内容的。
2. 抓取清华首页(https://www.tsinghua.edu.cn/)的数据得到的是乱码，无法获取html网页源代码的内容。



## 抓包实验三

<img src="/Users/wangwenqi/Library/Application Support/typora-user-images/image-20220313224114381.png" alt="image-20220313224114381" style="zoom:25%;" />

我们首先关闭foxmail的ssl安全连接，然后登陆tsinghu邮箱，然后开启wireshark进行抓包。紧接着我们开启smtp过滤，这样就可以专注地看到和邮件收发相关的信息。紧接着我们看到user，password以及发送邮箱的from和to以及内容都可以看见，只不过是经过**base64加密后的数据**。

1. 可以看见发送邮件的收发方以及发送内容等等信息。
2. 我们可以直接使用在线的base64解码器获取user的密码信息，可见不加ssl安全验证证书的连接是极其不安全的。



## 协议分层结构

ICMP协议：

ICMP -> IPV4 -> Ethernet II -> Frame数据帧 -> 物理层

http协议：

HTTP -> TCP -> IPV4 -> Ethernet II -> Frame 数据帧 -> 物理层

邮件协议（SMTP协议）:

SMTP -> TCP -> IPV4 -> Ethernet II -> Frame数据帧 -> 物理层 
