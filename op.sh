git status
git add --all
git commit -m "mac部署"
git push origin master:source
hexo clean && hexo g && hexo d