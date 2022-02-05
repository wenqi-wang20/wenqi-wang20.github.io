#!/usr/bin/env python
# coding: utf-8
# @Desc  : 爬取彼岸图网壁纸

import requests
import shutil
import yaml
from PIL import Image
from bs4 import BeautifulSoup
import os,re

# 创建目录
def createDir(filePath):
    if not os.path.exists(filePath):
        os.mkdir(filePath)

# 获取壁纸超链接
def getAndSavehref(url,pagenum):
    try:
        # createDir(os.getcwd()+"\source\img")
        f = open(os.getcwd()+'\source\img\html_href.txt', 'w', encoding='utf-8')
        # 请求头
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        for i in range(1, pagenum):
            if i==1 :
                r = requests.get(url, headers=head)
            else:
                r = requests.get(url +'/index_' +str(i)+'.html', headers=head)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'html.parser')
            content =soup.select('div>ul>li')
            i=0
            for h in content:
                href=h.find("a").attrs['href']
                if re.match('.*tupian.*',href):
                    r = requests.get('http://pic.netbian.com'+href)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    f.write('http://pic.netbian.com'+soup.select_one('#img>img').attrs['src'] + '\n')
        f.close()
        print("爬取壁纸地址成功！")
    except:
        print("爬取壁纸地址失败！")

# 保存图片链接
def save_img():

        # 此处先强制删除整个文件夹，再重新新建，相当于更新整个文件夹
        shutil.rmtree(os.getcwd()+"\source\img\images")
        createDir(os.getcwd()+"\source\img\images")
        f_read = open(os.getcwd()+'\source\img\html_href.txt', 'r+', encoding='utf-8')
        number = 1
        for line in f_read:
            try:
                print(os.getcwd()+"\source\img\images\image" + str(number) + '.jpg')
                line = line.rstrip("\n")
                # 根据个数顺序重命名名称
                f_write = open(os.getcwd()+"\source\img\images\image" + str(number) + '.jpg', 'wb')
                r = requests.get(line)
                # 如果图片地址有效则下载图片状态码200，否则跳过。
                if r.status_code == 200:
                    f_write.write(r.content)
                    # 若保存成功，则命名顺序+1
                    number += 1
                    print("当前保存第" + str(number) + "张图片。")
                f_write.close()
            except:
                print("下载图片出错！！")
        f_read.close()

# 压缩图片
def compressed():
    filepath = os.getcwd() + "\source\img\images"
    dsatpath = os.getcwd() + "\source\img\compressed_images"

    # 统计已有的文件数目
    cnt = 0
    all_files = os.listdir(dsatpath)
    for file in all_files:
        if os.path.isfile(file):
            cnt += 1

    for filename in os.listdir(filepath):
        srcfile = filepath + "\\" + filename
        dstfile = dsatpath + "\\" + "image" + str(cnt+1) + ".jpg"
        if os.path.isfile(srcfile):
            try:
                with Image.open(srcfile) as im:
                    w, h = im.size
                    dImg = im.resize((int((9*w)/10), int((9*h)/10)), Image.ANTIALIAS)
                    dImg.save(dstfile,quality=100,optimize=True)
                    print(filename+"压缩成功")
                    cnt += 1
            except:
                print(filename+"压缩失败")

# 读取yaml
def getyml():
    coverpath = os.getcwd() + "\source\img\compressed_images"
    configpath = os.getcwd() + "\_config.yml"
    f = open(configpath, 'r')
    cont = f.read()
    x = yaml.load(cont, Loader=yaml.FullLoader)
    f.close()

    print(x)
    coverlist = []
    all_files = os.listdir(coverpath)
    for file in all_files:
        filepath = "/img/compressed_images/" + file
        print(filepath)
        coverlist.append(filepath)

    x["cover"] = coverlist
    fw = open(configpath, 'w')
    yaml.safe_dump(x, fw)
    fw.close()
    print(coverlist)



if __name__ == "__main__":
    # try:
    #     print('默认爬取4K风景：http://pic.netbian.com/4kfengjing，其他可选地址如http://pic.netbian.com/4kdongman等')
    #     url = input('如需要爬取其他大类壁纸，在此输入网址，否则按Enter建继续：')
    #     pagenum=input('输入一个数字，表示下载多少页，默认（5）：')
    #     if not url:
    #         url ='http://pic.netbian.com/4kfengjing'
    #     if not pagenum:
    #         pagenum=5
    #     getAndSavehref(url,pagenum=int(pagenum))
    #     save_img()
    #     input('壁纸已下载到当前目录，按任意键退出：')
    # except:
    #     input('输入错误，检查网址和页数，按任意键退出：')
    #
    # compressed()

    getyml()
