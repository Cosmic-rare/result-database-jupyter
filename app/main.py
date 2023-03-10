from fastapi import FastAPI

from score import score
from title import title
from difficult import difficult

app = FastAPI()


@app.post("/")
def upload_file(url):
    scoreData = score(url)
    titleData = title(url)
    difficultData = difficult(url, titleData["music"]["id"])

    return {"score": scoreData, "title": titleData, "difficult": difficultData}
