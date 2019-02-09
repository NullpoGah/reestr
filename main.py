import pandas as pd
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()
import urllib.request
import ssl
import re

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

baseurl = 'https://reestr.minsvyaz.ru'

# Поиск количества страниц


def find_n():
    req = requests.get('https://reestr.minsvyaz.ru/reestr/?show_count=100', verify=False).text
    res = BeautifulSoup(req, 'lxml').find('div', class_='page_nav_area').find_all('a', class_='nav_item')
    return int(res[3].text)+1


for i in range(1, find_n()):
    # Создание ссылок для всех страниц поиска на сайте реестра (с отображением по 100)
    url = baseurl + '/reestr/?PAGEN_1=' + str(i) + '&show_count=100'
    response = urllib.request.urlopen(url)
    print(url)
    # поиск ссылок на страницы с юридической информации о ПО
    links = re.findall('<a href=\"(/reestr/\d*/)\"', str(response.read()))
    with open('links.txt', mode='a', encoding='utf-8') as myfile:
        for line in links:
            print(baseurl + line, file=myfile)
    myfile.close

# константные значения
links = "links.txt"
# количество уникальных названий ПО
with open(links) as f:
    num = sum(1 for _ in f)
# Имя выводного файла Excel
file = "Данные.xlsx"

# создание словаря для передачи его в последствии датафрейму в пандас
data = pd.read_excel(file, index_col=None, encoding='utf-8')
values = {'Название по': [], 'Название организации': [], 'ФИО': [], 'ИНН': [], 'Сайт': [], 'Альтернатив': [],  'Класс по': []}
values['Название по'] = ['' for element in range(num)]
values['Название организации'] = ['' for element in range(num)]
values['ФИО'] = ['' for element in range(num)]
values['ИНН'] = ['' for element in range(num)]
values['Сайт'] = ['' for element in range(num)]
values['Альтернатив'] = ['' for element in range(num)]
values['Класс по'] = ['' for element in range(num)]

f = open(links)
i = 0
for url in f:
    print(url)
    print(str(i) + ' of ' + str(num))
    req = requests.get(url, verify=False).text
    soup = BeautifulSoup(req, 'lxml')
    # название ПО
    soft = soup.find('h1', id='pagetitle').text
    values['Название по'][i] = soft
    # название организации
    try:
        orgname = soup.find('a', title='Все продукты организации').text
    except AttributeError:
        orgname = ""
        pass
    values['Название организации'][i] = orgname
    # владелец
    try:
        fio = soup.find('a', title='Все продукты').text
    except AttributeError:
        fio = ""
        pass
    values['ФИО'][i] = fio
    # ИНН ^(\d{10}|\d{12})$
    try:
        inn = soup.find('div', text=re.compile("(\d{10}\s|\d{12}\s)")).text
        inn = inn.strip()
    except AttributeError:
        inn = ""
        pass
    values['ИНН'][i] = inn
    # альтернативное название организации
    try:
        altname = soup.find('span', text=re.compile("Альтернативные наименования:")).find_parent('div').text
        altname = re.sub('Альтернативные наименования:', '', altname)
        altname = altname.strip()
    except AttributeError:
        altname = ""
        pass
    values['Альтернатив'][i] = altname

    # сайт производителя
    try:
        site = soup.find('span', text=re.compile("Сайт производителя:")).find_parent('div').find('a').get('href')
    except AttributeError:
        site = ""
    values['Сайт'][i] = site
    # Класс по
    try:
        softclass = soup.find('span', text=re.compile("Класс ПО:")).find_parent('div').text
        softclass = re.sub('Класс ПО:', '', softclass)
        softclass = softclass.strip()
    except AttributeError:
        softclass = ""
        pass
    values['Класс по'][i] = softclass
    i = i + 1
    if i>num:
        break

# запись датафрейма в Excel файл
writer = pd.ExcelWriter(file)
pd.DataFrame.from_dict(values).to_excel(writer, startcol=0, startrow=0, index=False)
writer.save()
print('Всё готово')
