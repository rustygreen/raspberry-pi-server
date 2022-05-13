# Run Without Docker

The following steps can be used to run the `raspberry-pi-server` without using a container (Docker, Kubernetes, etc.).

NOTE: Alternatively you can run the following command from your Raspberry Pi to perform these steps for you:

```bash
sudo curl -fL https://github.com/rustygreen/raspberry-pi-server/blob/main/scripts/setup.sh | sh -
```

Review the [setup.sh script](./scripts/setup.sh) before executing (don't just trust me).

### Raspberry Pi Setup

1. Install [Git](https://git-scm.com/) on your Raspberry Pi

```bash
$ sudo apt update
$ sudo apt install git
```

2. Install [Python 3](https://www.python.org/) and [Pip 3](https://pypi.org/project/pip/) on your Raspberry Pi

```bash
$ sudo apt update
$ sudo apt install python3 idle3 pip3
```

### Deploy Server to Pi

2. Clone the repository

```bash
$ cd /home/pi # Or wherever you want to store your code.
$ git clone https://github.com/rustygreen/raspberry-pi-server.git
```

3. Install Python dependencies

```bash
$ cd raspberry-pi-server
$ pip3 install -r requirements.txt
```

4. Run Server

```bash
$ sudo python3 server.py
```

5. Consume the services

Returns a list of pins and their state (1 or 0)

```bash
$ curl http://localhost:8080/pins
```

Returns the state for GPIO pin #7

```bash
$ curl http://localhost:8080/pins/7
```

Sets the state of GPIO pin #7 to 1 (high)

```bash
$ curl http://localhost:8080/pins/7/1
```

You should get back a JSON list of the GPIO pins and their current state.
