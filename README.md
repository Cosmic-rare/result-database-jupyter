## targets

https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/normal.png

https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/wide.png

https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/fastlate.png

https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/target.jpg

### build

```bash
$ docker build ./ -t example
```

### run

```bash
$ docker container run -it -d -p host:container --name [container-name] [image-name]
```

### docker-compose

```bash
$ docker-compose up

$ docker-compos down
```

## jupyter, venv

### create venv

```bash
$ python3 -m venv /path/to/new/virtual/environment
```

### activate venv

```bash
$ source <venv>/bin/activate.fish
```

### launch jupyter

```bash
$ jupyter-lab
```

### requirements.txt

```bash
$ pip freeze > requirements.txt

$ pip install -r requirements.txt
```
