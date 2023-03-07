![binb](https://raw.githubusercontent.com/lpinca/binb/master/public/img/binb-logo.png)

binb is a simple, realtime, multiplayer, competitive music listening game.

To play the game: [https://binb.co](https://binb.co)

## Installation

Unless previously installed you'll need the following packages:

- [Node.js](http://nodejs.org/)
- [Redis](http://redis.io/)
- [Cairo](http://cairographics.org/)

Please use their sites to get detailed installation instructions.

Alternatively, binb can run in Docker containers and orchestrated using `docker-compose`.

### Install binb

The first step is to install the dependencies:

```shell
npm install
```

Then you need to minify the assets:

```shell
npm run minify
```

Now make sure that the Redis server is running and load some sample tracks:

```shell
npm run import-data
```

Finally run `npm start` or `node app.js` to start the app.

Point your browser to `http://127.0.0.1:8138` and have fun!

#### Possible errors

Some package managers name the Node.js binary `nodejs`. In this case you'll get
the following error:

```shell
sh: node: command not found
```

To fix this issue, you can create a symbolic link:

```shell
sudo ln -s /usr/bin/nodejs /usr/bin/node
```

and try again.

### Running in Docker containers

To run binb in a Docker container, [Docker](https://www.docker.com/) needs to be installed. Optionally, [docker-compose](https://docs.docker.com/compose/) can be used to orchestrate the containers.

To start binb in Docker using `docker-compose`, run the following command:

```shell
docker-compose up -d
```

If the project is changed, the containers need to be rebuild. This can be done by running:

```shell
docker-compose up -d --build --force-recreate
```

#### Persisting the redis database
By default, the redis database lives inside the container. To persist it between containers, uncomment the volume mapping in the `docker-compose.yaml` file.

## Browser compatibiliy

binb requires a browser that supports the WebSocket protocol.

Refer to this [table](http://caniuse.com/websockets) for details on
compatibility.

## Shout out to

- [beatquest.fm](http://beatquest.fm) for inspiration.

## Bug tracker

Have a bug? Please create an [issue](https://github.com/lpinca/binb/issues) here
on GitHub, with a description of the problem, how to reproduce it and in what
browser it occurred.

## Copyright and license

binb is released under the MIT license. See [LICENSE](LICENSE) for details.
