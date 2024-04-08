import json
from datetime import datetime
import re

with open('response.json', encoding='utf-8' , mode='r') as file:
        data = json.load(file)

res = []
for product in data['products']:
    tmp = {}
    tmp['ID'] = product['uid']
    tmp['Title'] = product['title']
    tmp['Excerpt'] = product['descr']
    tmp['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmp["Post Type"] = "post"
    tmp["Image URL"] = product['editions'][0]['img']

    match = re.search(r"до (\d+) кг", product['descr'])
    if match:
        weight_limit = int(match.group(1))
        if weight_limit % 1000 == 0:
              weight_limit = int(weight_limit / 1000)
        else:
              weight_limit = weight_limit / 1000
        tmp["categories"] = str(weight_limit) + " т"
    res.append(tmp)

with open("result.json", encoding='utf-8', mode='w') as file:
        json.dump(res, file, ensure_ascii=False, indent=4)