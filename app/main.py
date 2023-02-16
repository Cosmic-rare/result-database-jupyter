from fastapi import FastAPI, APIRouter, Depends, File, HTTPException, UploadFile, status
from score import score
from title import title

app = FastAPI()

@app.post("/upload/")
def upload_file(url):
    scoreData = score(url)
    titleData = title(url)
    return {"score": scoreData, "title": titleData["title"], "id": titleData["id"], "credibility": titleData["result"]}
