# What is Docker?

아래 유튜브 자료 참고

- [노마드 코더 - Docker 가 왜 좋은지 5분안에 설명해줌](https://youtu.be/chnCcGCTyBg) 
- [생활코딩 도커 수업](https://www.youtube.com/watch?v=Ps8HDIAyPD0&list=PLuHgQVnccGMDeMJsGq2O-55Ymtx0IdKWf&ab_channel=%EC%83%9D%ED%99%9C%EC%BD%94%EB%94%A9)


# Installation

For Windows/Mac

* Docker-desktop: https://www.docker.com/products/docker-desktop/

For Ubuntu

* Docker: https://docs.docker.com/engine/install/ubuntu/
* docker-compose: https://docs.docker.com/compose/install/linux/

# Working with Docker & Docker-Compose

* start a container with docker-compose

```bash
# build and start docker containers with detached mode(-d) 
$ docker-compose up -d
# start docker containers
$ docker-compose start
# stop docker containers
$ docker-compose stop
# stop and remove docker containers
$ docker-compose down
```

* check current container status

```bash
$ docker ps
```

* run bash shell in the services

```base
$ docker exec -it [container name] bash
```

* attach into the running container

```bash
$ docker attach --name [container name]
```

# Docker Network

```bash
$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' [container name]
```