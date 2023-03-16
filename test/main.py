imgs = [
  {
    "url": "https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/normal.png",
    'score': '1161441',
    'title': 'ブリキノダンス',
    'difficult' : 'MASTER',
    'PERFECT': '958',
    "GREAT": '9',
    'GOOD':'0',
    "BAD": '0',
    "MISS": '0'
  },
  {
    "url": "https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/wide.png",
    'score': '596068',
    'title': 'Brand New Day',
    'difficult' : 'EXPERT',
    'PERFECT': '1238',
    "GREAT": '22',
    'GOOD':'0',
    "BAD": '0',
    "MISS": '0'
  },
  {
    "url": "https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/fastlate.png",
    'score': '1504818',
    'title': 'ぼくらの16bit戦争',
    'difficult' : 'MASTER',
    'PERFECT': '1521',
    "GREAT": '0',
    'GOOD':'0',
    "BAD": '0',
    "MISS": '0'
  },
  {
    "url": "https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/target.jpg",
    'score': '462/13',
    'title': 'インビジブル',
    'difficult' : 'EXPERT',
    'PERFECT': '1283',
    "GREAT": '82',
    'GOOD':'4',
    "BAD": '0',
    "MISS": '16'
  },
]

judges = ['PERFECT','GREAT','GOOD','BAD','MISS']
content = ['score','title','difficult','judge']

data = {
  'score': {
    "builder1": 0,
    "builder2": 0,
    "builder3": 0,
    "builder4": 0,
    "builder5": 0,
    "builder6": 0
  },
  'title': {
    "builder1": 0,
    "builder2": 0,
    "builder3": 0 
  },
  'difficult': {
    "builder1": 0,
    "builder2": 0,
    "builder3": 0,
    "builder4": 0
  },
  'judge': {
    "builder1": 0,
    "builder2": 0,
    "builder3": 0,
    "builder4": 0,
    "builder5": 0,
    "builder6": 0
  }
}

import requests
import json
import difflib

for ind in range(len(imgs)):
  img = imgs[ind]
  response = requests.post(
    "http://localhost:8080",
    params={
      "url": img['url']
    },
  )

  res = json.loads(response.text)

  # score
  for i in range(1,7):
    data['score']['builder' + str(i)] += difflib.SequenceMatcher(None, res['score']['builder' + str(i)], img['score']).ratio()

  # title
  for i in range(1,4):
    data['title']['builder' + str(i)] += difflib.SequenceMatcher(None, res['music']['builder' + str(i)]['ocr'], img['title']).ratio()

  # difficult
  for i in range(1,5):
    data['difficult']['builder' + str(i)] += difflib.SequenceMatcher(None, res['difficult']['builder' + str(i)]['ocr'], img['difficult']).ratio()

  # judge
  for i in range(1,7):
    avg = 0
    for j in judges:
      avg += difflib.SequenceMatcher(None, res['judge']['builder' + str(i)][j], img[j]).ratio()

    data['judge']['builder' + str(i)] += avg / 5

  print('finished:', ind)


# score
for i in range(1,7):
  data['score']['builder' + str(i)] = data['score']['builder' + str(i)] / len(imgs)

# title
for i in range(1,4):
  data['title']['builder' + str(i)] = data['title']['builder' + str(i)] / len(imgs)

# difficult
for i in range(1,5):
  data['difficult']['builder' + str(i)] = data['difficult']['builder' + str(i)] / len(imgs)

# judge
for i in range(1,7):
  data['judge']['builder' + str(i)] = data['judge']['builder' + str(i)] / len(imgs)


print(data)