
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