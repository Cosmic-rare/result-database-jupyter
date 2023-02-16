FROM python:3.9-slim

WORKDIR /app

RUN apt-get update
# RUN apt-get install -y software-properties-common
# RUN add-apt-repository -y ppa:alex-p/tesseract-ocr5
RUN apt-get install -y tesseract-ocr
RUN apt-get -y install tesseract-ocr tesseract-ocr-jpn libtesseract-dev libleptonica-dev tesseract-ocr-script-jpan
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app/ .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]