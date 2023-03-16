imgs = [
  'https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/normal.png',
  'https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/wide.png',
  'https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/fastlate.png',
  'https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/target.jpg'
]

import requests

response = requests.post('http://localhost:8080', params={'url': 'https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/normal.png'})
print(response.status_code)
print(response.text)