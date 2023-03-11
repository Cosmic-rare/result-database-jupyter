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

## ToDo

- 特徴点マッチングで位置は特定できそう
- 精度は未知数だから、なるべく検索範囲を縮めたうえでマッチングを行うようにする
- ~~似ている基準点を２つ見つけて、距離からDPIを揃えるための比率を計算する~~
- その比率から`img2`(検索する部分)を拡大・縮小して、`template-matching`を行う