from fastapi import FastAPI, APIRouter, Depends, File, HTTPException, UploadFile, status
from score import score
from title import title
from difficult import difficult

app = FastAPI()

@app.post("/upload/")
def upload_file(url):
    scoreData = score(url)
    titleData = title(url)
    difficultData = difficult(url)

    return {
            "score": {
                "score": scoreData
            }, 
            "title": {
                "title": titleData["title"],
                "id": titleData["id"],
                "credibility": titleData["result"]
            }, 
            "difficult": {
                "musicDifficulty": difficultData["difficult"],
                "credibility": difficultData["credibility"],
                "ocr": difficultData["data"]
            }
        }
