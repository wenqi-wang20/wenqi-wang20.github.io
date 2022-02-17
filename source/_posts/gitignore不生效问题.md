---
title: gitignore不生效问题
date: 2022-02-17 14:34:12
tags: [git]
Categories: [日常小问题]
---

因为年前换了两台电脑，需要在不同的地方管理我的hexo博客，所以我采取了git存储一份source资源，两边每次都需要先拉取云端资源，再做本地更新，然后再deploy到hexo分支。因为有些步骤是重复的，所以我就写了一个脚本，短短的几句话：

```shell
git status
git add --all
git commit -m "mac部署"
git push origin master:source
hexo clean && hexo g && hexo d
```

但是因为我的mac和win语句不一样，所以显然这个不能被push到source分支里，所以我把它添加到`.gitignore`文件里了。可是最近经过我观察发现，它依然出现在了我的git远程仓库里！不仅如此，`.gitignore`里的文件都没有被忽略，甚至连ignore文件自己都被上传了上去。所以我才研究了一下，发现是我当时添加`.gitignore`文件比较迟，并没有在init的同时添加，导致文件时无效的。解决办法也很简单，只需要用下面的命令删除缓存即可：

```bash
# 注意后面有一个点
git rm -rf --cache .
```

然后在重新添加所有的更改并且commit提交即可。
