from fastapi import FastAPI

from score import score
from title import title
from difficult import difficult
from judge import judge

app = FastAPI()


@app.post('/')
def upload_file(url):
    scoreData = score(url)
    titleData = title(url)
    difficultData = difficult(url)
    judgeData = judge(url)

    return {'score': scoreData, 'music': titleData, 'difficult': difficultData, 'judge': judgeData}
