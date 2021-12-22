# 🥧 Raspberry Pi Server

> Stop writing custom scripts and worrying about deploying and scheduling them to run on your Pi. Instead, interact with your Pi through RESTful services - using whatever technology you'd like.

`raspberry-pi-server` is a server component designed to be ran on a Raspberry Pi which provides RESTful services to control the GPIO pins of the Raspberry Pi. This project was created in an effort to eliminate the need to create custom python scripts and constantly maintain, update, and schedule them on a Raspberry Pi. Rather, you can deploy one single service on the Pi (raspberry-pi-server), and never have to logon to the Pi again. Interaction to the Pi can be done through RESTful services using whatever client/technology you'd like. For example, check out the [raspberry-pi-client project](https://github.com/rustygreen/raspberry-pi-client)

## 🏁 Getting Started

Follow the steps below to get the service running on your Pi.

### Raspberry Pi Setup

1. Install [Git](https://git-scm.com/) on your Raspberry Pi

```batch
$ sudo apt update
$ sudo apt install git
```

2. Install [Python 3](https://www.python.org/) and [Pip 3](https://pypi.org/project/pip/) on your Raspberry Pi

```batch
$ sudo apt update
$ sudo apt install python3 idle3 pip3
```

### Deploy Server to Pi

2. Clone the repository

```batch
$ cd /home/pi # Or wherever you want to store your code.
$ git clone https://github.com/rustygreen/raspberry-pi-server.git
```

3. Install Python dependencies

```batch
$ cd raspberry-pi-server
$ pip3 install -r requirements.txt
```

4. Run Server

```batch
$ sudo python3 server.py
```

5. Consume the services

```batch
$ curl http://localhost:8080/pins
```

You should get back a JSON list of the GPIO pins and their current state.

## TODOs

[ ] Add unit tests
[ ] Create Docker image and compose file
[ ] Update docs to show Docker use
[ ] Add other Raspberry Pi commands (restart, etc.)
[ ] Finish documentation
