# 缘由
豆瓣小组虽然夹杂着大量的中介，但是还是有不少房东直租，而且图片也靠谱。但是由于贴子特别多
(某上海租房小组每天要刷100页)，而且由于标题各异没有特定格式，看起来很费劲，所以写了程序自动爬取页面。

程序按照预设的关键词筛选出感兴趣的区域的贴子，然后去重，贴子以简单的网页形式(地址http://127.0.0.1:8000/zufang/all) 展示出来以方便浏览。

![示例](img/douban_zufang_spider_demo.png)

此程序可以以后台程序跑在服务器VPS上(有个人网站/域名的话还可以挂到个人网站/域名下)，会每隔几分钟（按配置文件的设置）重新爬取一次，
刷新网页链接即可拿到最新贴子。

因为浏览器都有历史记录，所以点击过的链接都是红色的，
所以没点击过的链接一目了然，刷豆瓣租房贴的效率极大提高了。

# 配置文件详解

* 关键词和权值，贴子的标题每匹配到一个词，就会有加上一个分数。分数达到一定分值，
才会被筛选出来。

    ```ini
    [DEFAULT]
    keywords =
        宜山路=5
        桂林公园=5
        漕宝路=5
        桂林路=5
        漕河泾=4
        虹漕路=4
        龙漕路=4
    ```

* 筛选分值。贴子匹配的分值达到多少才满足条件被筛选出来。
    ```ini
    [Spider]
    score_min = 3
    ```

* 第一次运行时要抓多少天的数据（单位是小时）
    ```ini
    [Spider]
    hours_ago = 24

    ```
* 多久运行一次爬取（单位是秒）
    ```ini
    [Spider]
    interval = 600
    ```

* 最多保存多少天的数据（单位是天）。因为存储没有使用数据库，而是直接存为JSON，所以为了性能，不要把时间设得太久。
    ```ini
    [Spider]
    data_days = 3

    ```

* 要抓取的数据源，即豆瓣小组的链接，可以多少。
    ```ini
    group =
        上海租房,https://www.douban.com/group/SHwoman/
        上海合租族_魔都租房,https://www.douban.com/group/383972/
        上海租房@房东直租,https://www.douban.com/group/467799/
        上海租房---房子是租来的，生活不是,https://www.douban.com/group/homeatshanghai/
        上海合租族_魔都租房,https://www.douban.com/group/383972/
        上海租房,https://www.douban.com/group/shanghaizufang/

    ```
    
# 运行

```
pip3 install -r requirements.txt
python3 service/spider.py &
python3 service/web.py &

```


# TODO
* [ ] 验证发贴人的可靠性
* [X] 贴子列表显示出分值即契合度
* [ ] 爬取贴子页面，跟据图片与文字的多少来打分
* [ ] 过滤掉同一个人在不同小组发的同一房源信息，现在用过标题过滤但似乎还不够
* [ ] 看过的贴子不要显示
