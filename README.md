![binb](https://raw.githubusercontent.com/lpinca/binb/master/public/img/binb-logo.png)

binb is a simple, realtime, multiplayer, competitive music listening game.
This fork improves the installation by providing scripts to easily add tracks to the database.

To play the game: [https://binb.co](https://binb.co)

## Basic installation using docker-compose

Make sure that [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) is installed.

Run:
```console
$ docker-compose up
```

## Basic installation using docker

Make sure that [docker](https://docs.docker.com/engine/install/) is installed.

### Creating the docker image

First, create a docker image of binb using the supplied Dockerfile:
```console
$ docker build . -t binb
```

### Run a container for the redis database

To connect a redis container to your binb container, it is recommended to create a specific network.
You can choose any valid subnet, here we will be using `172.18.0.0/16`:

```console
$ docker network create binb-net --subnet 172.18.0.0/16
```

Now run a redis server using our new network:

```console
$ docker run --name redis-server -d --network binb-net redis
```

Verify that the container is running:

```console
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS      NAMES
d17192393b71   redis     "docker-entrypoint.s…"   55 seconds ago   Up 54 seconds   6379/tcp   redis-server
```

### Run the binb container (using lpinca's sample tracks)

All that is left now is to start a container running the binb image we created in step 1.
However, we also need to supply the IP address of the redis-server, so that binb can connect to it.

To fetch the IP adress, use the following command:

```console
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-server
172.18.0.2
```

Run a binb container (make sure to replace the REDIS_URL value with the IP we retrieved in the previous step):

```console
$ docker run --name binb -e REDIS_URL=172.18.0.2 --network binb-net -p 8138:8138/tcp -p 8138:8138/udp -d binb
```

### Run the binb container (without adding lpinca's sample tracks)

If you run the redis server container with the option `-p 6379:6379`, you can access it from the host and add values to the database before starting the binb container.
Take a look at the [README](https://github.com/nnamua/binb/blob/master/util/README.md) file in the `util` directory to find useful scripts to get started.

After adding values to the database, run the binb container:

```console
$ docker run --name binb -e REDIS_URL=172.18.0.2 --network binb-net -p 8138:8138/tcp -p 8138:8138/udp -d binb npm start
```

## Basic installation without docker

Unless previously installed you'll need the following packages:

- [Node.js](http://nodejs.org/)
- [Redis](http://redis.io/)
- [Cairo](http://cairographics.org/)

Please use their sites to get detailed installation instructions.

### Install binb

The first step is to install the dependencies:

```console
$ npm install
```

Then you need to minify the assets:

```console
$ npm run minify
```

Now make sure that the Redis server is running and load some sample tracks:

```console
$ npm run import-data
```

Finally run `npm start` or `node app.js` to start the app.

Point your browser to `http://127.0.0.1:8138` and have fun!

#### Possible errors

Some package managers name the Node.js binary `nodejs`. In this case you'll get
the following error:

```console
sh: node: command not found
```

To fix this issue, you can create a symbolic link:

```console
$ sudo ln -s /usr/bin/nodejs /usr/bin/node
```

and try again.

## Browser compatibiliy

binb requires a browser that supports the WebSocket protocol.

Refer to this [table](http://caniuse.com/websockets) for details on
compatibility.

## Useful tipps

* You can edit the contents of `config.json` on container start. Call `docker run ... binb -h` to see all options.
* Instead of storing tracks and user data in the same database, you can have 2 separate redis server running. View [`redis-client.js`](https://github.com/nnamua/binb/blob/master/lib/redis-clients.js) for more information.
* Use [volumes](https://docs.docker.com/storage/volumes/) for persistent storage with docker containers.

## Shout out to

- [beatquest.fm](http://beatquest.fm) for inspiration.

## Bug tracker

Have a bug? Please create an issue [here](https://github.com/nnamua/binb/issues) or [here](https://github.com/lpinca/binb/issues)
on GitHub, with a description of the problem, how to reproduce it and in what
browser it occurred.

## Copyright and license

binb is released under the MIT license. See [LICENSE](LICENSE) for details.
