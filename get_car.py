import requests
import json
from bs4 import BeautifulSoup

def get_urls(url):
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()

        urls = []
        for product in json_data['products']:
            urls.append(product['url'])

    return urls

def collect_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

    with open('jsonformatter.json', encoding='utf-8' , mode='r') as file:
        data = json.load(file)
    
    image_url = soup.find(class_='js-product-img').attrs['data-original']
    data['content'][0]['elements'][0]['elements'][0]['settings']['image']['url'] = image_url

    product_name = soup.find(class_='js-product-name')
    if product_name.find('div') != None:
        product_name = product_name.find('div').text
    else:
        product_name = product_name.text

    data['content'][0]['elements'][1]['elements'][0]['settings']['title'] = product_name

    descr = ""
    descr_tags = (soup.find(field='descr').contents)
    for elem in descr_tags:
        if elem.name == 'a':
            break
        descr += str(elem)
    data['content'][0]['elements'][1]['elements'][2]['settings']['editor'] = descr

    front_image = soup.find(class_='t107').find('img').attrs['data-original']
    data['content'][1]['elements'][0]['elements'][0]['settings']['image']['url'] = front_image

    character = soup.find(class_='t431__data-part2').text.replace('\n', ';').split(';')
    i = 0
    while i < 4:
        data['content'][3]['elements'][0]['settings']['table_header'][i]['text'] = character[i]
        i += 1
    n = len(character) if len(character) < 100 else 100
    while i < n:
        data['content'][3]['elements'][0]['settings']['table_body'][i - 4]['text'] = character[i]
        i += 1
    i -= 4
    m = len(data['content'][3]['elements'][0]['settings']['table_body'])
    while i < m:
        del data['content'][3]['elements'][0]['settings']['table_body'][i]
        m -= 1

    count_del = 0

    image = soup.find_all(class_='t107')
    if len(image) > 1:
        image = image[1].find('img').attrs['data-original']
        data['content'][4]['elements'][0]['settings']['image']['url'] = image
    else:
        del data['content'][4]
        count_del += 1

    features = soup.find(class_='t502')
    if features == None:
         del data['content'][5 - count_del]
         count_del += 1
         del data['content'][6 - count_del]
         count_del += 1
         del data['content'][7 - count_del]
         count_del += 1
    else:
        texts = features.find_all(class_='t502__textwrapper')
        i = 0
        j = 0
        for text in texts:
            name = text.find(class_='t-name_sm').text
            data['content'][6 + j - count_del]['elements'][i]['elements'][1]['elements'][0]['settings']['title'] = name
            descr = text.find(class_='t-descr_xs').text
            data['content'][6 + j - count_del]['elements'][i]['elements'][1]['elements'][1]['settings']['editor'] = descr
            i += 1
            if i == 3:
                i = 0
                j = 1
            if j == 2:
                break

    equipment = soup.find(class_='t1033')
    if equipment == None:
        del data['content'][8 - count_del]
    else:
        lists = equipment.find_all(class_='t-descr')
        data['content'][8 - count_del]['elements'][0]['elements'][2]['settings']['editor'] = str(lists[1].contents[0])
        data['content'][8 - count_del]['elements'][1]['elements'][2]['settings']['editor'] = str(lists[0].contents[0])

    carname = url.replace("https://trf-lift.ru/", "")
    data['title'] = carname
    output_filename = "json/" + carname + ".json"
    with open(output_filename, encoding='utf-8', mode='w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Пример использования
url = 'https://store.tildacdn.com/api/getproductslist/?storepartuid=781608348581&size=220'

urls = get_urls(url)

for url in urls:
    collect_page(url)
