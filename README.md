## targets

[https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/normal.png](https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/normal.png)

[https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/wide.png](https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/wide.png)

[https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/fastlate.png](https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/fastlate.png)

[https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/target.jpg](https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/target.jpg)

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
$ ./venv/bin/activate
```

### requirements.txt

```bash
$ pip freeze > requirements.txt

$ pip install -r requirements.txt
```

## Memo

```python
img = cv2.imread('./img.png')
# numpy.ndarra
```

```python
img = Image.open('./img.png')
# PIL.Image
```

```python
# numpy to pillow
pil_img = Image.fromarray(numpy_img)

# pillow to numpy
numpy_img = np.array(pil_img)
```

## API-Memo

### builders

1. number-6
2. number-7
3. text-whitelist-6
4. text-whitelist-7
5. text-6
6. text-7
