import requests
from bs4 import BeautifulSoup
import pprint
import json
'''
                        ПЕРЕД ЗАПУСКОМ ПРОГРАММЫ НЕОБХОДИМО ОБНОВИТЬ Cookie в headers
'''

'https://www.technopark.ru/noutbuki/otzyvy/'

Domain = 'https://www.technopark.ru'
url_domain = f'{Domain}/noutbuki/otzyvy'

headers = {
'authority': 'www.technopark.ru',
'method': 'GET',
'path': '/noutbuki/otzyvy/?utm_referrer=https%3A%2F%2Fwww.technopark.ru%2Fnoutbuki%2Fotzyvy%2F%3Fp%3D5',
'scheme': 'https',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'cache-control': 'max-age=0',
    # Перед запуском необходимо обновить cookie
'cookie': '__utmz=24718655.1675970333.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided); stest201=1; stest207=acc0; stest209=ct1; tp_city_id=36966; _userGUID=0:ldxhgtiv:LSicM3bSFWVXCUU3kmfchS7V7Q~Yneso; c2d_widget_id={"9eb3fbdda817d48faffc65c3446228e8":"[chat] b085ed20a7ae2e8c7a09"}; promo1000closed=true; user_public_id=rG7769ixeVirPjKiaWDcRoZpfVrCxs+nG8gj5huddNNpa2rEv7/4akwMzvGHa3sJ; TP_auth=MI49/W9Au8BCFmMzU3cySMLJSG2g9gIRr2MZm68ViSupFnDnnjq0RgzpjGgVAmT2; qrator_jsr=1676208874.409.55sYNTHN5RjjhUZA-ao9uu3jhh0v5eboro1lcodmbl86ba657-00; __utma=24718655.218871119.1675970333.1676123029.1676208876.11; __utmc=24718655; __utmt=1; qrator_jsid=1676208874.409.55sYNTHN5RjjhUZA-a2ekq1drartropvnkvqsrcog1i52pbaj; PHPSESSID=6f1ae6de8509f4f7a94445a4e384ff3a; visitedPagesNumber=1; __utmb=24718655.2.10.1676208876',

# 'if-none-match': '"93564-XsmwJOoGldAVO6U0yd6ef9u6Xa4"',
'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


get = requests.get(url_domain, headers=headers)         # Узнаём количество страниц
soup = BeautifulSoup(get.text, 'html.parser')
pages = (soup.find_all('button', class_='tp-pagination-button')[-1].text).replace(' ', '')


results = []                                    # Список с результатами поиска
for page in range(1, int(pages) + 1):            # Перебираем страницы с товарами
    print(f'Ищем на странице {page}')
    if page == 1:
        page = '/'
    else:
        page = f'/?p={str(page)}'

    response = requests.get(f'{url_domain}{page}', headers=headers)
    print(response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')

    big_head_class = soup.find_all('article', class_='nuxt-review-card catalog-reviews-page__review tp-box tp-box--black-tp tp-box--p-none nuxt-review-card')  # Поиск всех тегов с ноутами на странице
    for head in big_head_class:             # Перебираем результаты поиска на одной странице

        result = {
            'name': None,
            'price': None,
            'foto': None,
            'url': None,
            'reviews': None
        }

        result['name'] = head.img.get('alt')  # Название модели ноута

        price = head.find('div', class_='nuxt-review-card__price')  # Цены на ноутбуки
        result['price'] = price.meta.get('content')

        result['foto'] = head.meta.get('content')  # Фото ноута

        url = head.a.get('href')
        result['url'] = f'{Domain}{url}'  # Ссылка на ноутбук

        # Поиск отзывов и комментариев

        comments = {}           # Ищем в теге с отзывами
        teg_div = head.find_all('div', class_='nuxt-review-card__body nuxt-review-card__body--with-product')

        for teg in teg_div:
            comments_nout = teg.find_all('div', class_='nuxt-review-card__text')

            for comment in comments_nout:
                # print(str(list(comment.strings)[0]).replace('\n', ''))
                # print((str(list(comment.strings)[1])).replace('\n', ''))
                key = str(list(comment.strings)[0]).replace('\n', '')           # Убираем из строк символы \n
                value = [str((list(comment.strings)[1])).replace('\n', '')]

                if len(comments) < 3:  # Создаём пары ключ, значение
                    comments[key] = value
                else:
                    comments[key].extend(value)  # Расширяем списки по ключам

                # comments.setdefault(key, value)  # Добавляем ключ значение если таких нет

            result['reviews'] = comments  # Добавляем комментарии в словарь

        results.append(result)

pprint.pprint(results)

print(f'Количество найденных результатов: {len(results)}')    # Сохраняем результат в файл json
with open('results_parsing.json', 'w') as f:
    json.dump(results, f)

