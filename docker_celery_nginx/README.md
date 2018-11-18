# Docker 安装 Nginx

## 创建 docker_df_celery_nginx 目录

创建目录 docker_df_celery_nginx, 用于存放后面的相关东西

```sh
mkdir docker_df_celery_nginx
cd docker_df_celery_nginx
mkdir www conf logs
```

## 拉取Nginx镜像
```sh
# 查找 Docker Hub 上的 nginx 镜像
docker search nginx
# 拉取官方的镜像
docker pull nginx
# 等待下载完成后，我们就可以在本地镜像列表里查到 REPOSITORY 为 nginx 的镜像
docker images nginx
```

## 使用 nginx 镜像

### 运行容器

```sh
docker run -p 8001:8001 \
--name df_celery_nginx \
-v $PWD/www:/www \
-v $PWD/../static:/www/static \
-v $PWD/conf/nginx.conf:/etc/nginx/nginx.conf \
-v $PWD/logs:/wwwlogs \
-d nginx
```

命令说明：

```sh
-p 8001:8001：        将容器的80端口映射到主机的80端口
--name df_celery_nginx：  将容器命名为 df_celery_nginx
-v $PWD/www:/www：将主机中当前目录下的www挂载到容器的/www
-v $PWD/../static:/www/static  将主机中当前目录的上级目录下的static目录挂载到容器的/www/static
-v $PWD/conf/nginx.conf:/etc/nginx/nginx.conf：将主机中当前目录下的nginx.conf挂载到容器的/etc/nginx/nginx.conf
-v $PWD/logs:/wwwlogs：将主机中当前目录下的logs挂载到容器的/wwwlogs
```

## 查看容器启动情况

```sh
# 查看活跃的容器
docker ps
# 如果没有 df_celery_nginx 说明启动失败 查看错误日志
docker logs df_celery_nginx
# 以 tail -f 的方式查看nginx日志
docker logs -f df_celery_nginx
# 查看 df_celery_nginx 的 ip 挂载 端口映射等信息
docker inspect df_celery_nginx
# 查看 df_celery_nginx 的端口映射
docker port df_celery_nginx
# 查看所有容器
docker ps -a
```

## 容器内部建立 Shell 连接

docker exec命令使我们可以在Docker容器内部执行命令，我们可以通过以下方式与mysql容器建立一个shell连接：

```sh
# mysql-cli 访问
docker exec -it df_celery_nginx bash
# -it 交互的虚拟终端
```

## 其他命令

```sh
# 启动容器 已经停止的容器，我们可以使用命令 docker start 来启动。
docker start df_celery_nginx
#正在运行的容器，我们可以使用 docker restart 命令来重启
docker restart df_celery_nginx
# 停止容器
docker stop df_celery_nginx
# 删除容器 删除容器时，容器必须是停止状态，否则会错
docker rm df_celery_nginx
```

