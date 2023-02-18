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

## result

```
{
  "score": {
    "score": "596068"
  },
  "title": {
    "title": "Brand New Day",
    "id": 128,
    "credibility": 1
  },
  "difficult": {
    "musicDifficulty": "EXPERT",
    "credibility": 0.9230769230769231,
    "ocr": "SEXPERT"
  }
}
```