# 🥧 Raspberry Pi Server

> Stop writing custom scripts and worrying about deploying and scheduling them to run on your Pi. Instead, interact with your Pi through RESTful services - using whatever technology you'd like.

`raspberry-pi-server` is a server component designed to be ran on a Raspberry Pi which provides RESTful services to control the GPIO pins of the Raspberry Pi. This project was created in an effort to eliminate the need to create custom python scripts and constantly maintain, update, and schedule them on a Raspberry Pi. Rather, you can deploy one single service on the Pi (raspberry-pi-server), and never have to logon to the Pi again. Interaction to the Pi can be done through RESTful services using whatever client/technology you'd like. For example, check out the [raspberry-pi-client project](https://github.com/rustygreen/raspberry-pi-client)

> This project is a good option for those who do not want to regularly work with Python on their Raspberry Pi. Rather, you can run the server and then interact with it through REST services.

## 🏁 Getting Started

Follow the steps below to get the service running on your Pi.

### Quick Start

From your rasperry Pi:

#### Docker

```
docker run --privileged -d --restart=unless-stopped -p 80:5000 ghcr.io/rustygreen/raspberry-pi-server:main
```

#### Docker Compose

docker-compose.yml

```yml
version: "2"
services:
  # Raspberry pi server
  pi-server:
    image: ghcr.io/rustygreen/raspberry-pi-server:main
    restart: unless-stopped
    privileged: true
    ports:
      - 8081:5000
```

```bash
docker-compose up
```

If you don't want to use Docker check out the [Run without Docker docs](./docs/run-without-docker.md)

### Usage

Once the server is running you will have a number of services available to interact with your Pi GPIO pins. Below are a few examples:

```bash
GET http://YOUR_PI/pins # Retrieves a list of pins and their states
```

### Development

See [Development docs](./docs/development.md)

## TODOs

- [x] Create Docker image and compose file
- [ ] Add unit tests
- [ ] Add socket.io
- [ ] Add swagger docs
- [ ] Update docs to show Docker use
- [ ] Add other Raspberry Pi commands (restart, etc.)
- [ ] Finish documentation
