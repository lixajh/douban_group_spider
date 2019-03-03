docker build -t douban_group_spider .


# 2.根据镜像名字或者ID为它创建一个标签，缺省为latest
docker tag douban_group_spider docker-registry.xiaolee.xyz/douban_group_spider:0.1

# 3.推送镜像
docker push docker-registry.xiaolee.xyz/douban_group_spider:0.1

docker run -it -p 8089:8089 docker-registry.xiaolee.xyz/douban_group_spider:0.1
docker run -it -p 8089:8089 localhost:5443/douban_group_spider:0.1