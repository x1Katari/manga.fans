import re
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from slugify import slugify
import threading


from ...models import Title, Chapter


def parse(page, session, headers):
    print('Страница' + str(page))
    src = session.get(url=f"https://waymanga.ru/manga?page={page}", headers=headers).text
    sp = BeautifulSoup(src, 'lxml')
    cards = sp.find_all('div', class_='position-relative')
    for card in cards:
        manga_name = card.text.strip()  # название
        manga_src = card.find('a').get('href')  # ссылка
        manga_img = card.find('img', class_='wh-100 object-0').get('src')  # картинка
        slug = slugify(manga_name)
        count = 0
        nums = list()

        title = Title(name=manga_name, title_src=manga_src, img_src=manga_img, slug=slug, numbers=nums)
        title.save()

        manga_html = session.get(url=manga_src, headers=headers).text
        bs = BeautifulSoup(manga_html, 'lxml')
        chapters = bs.find_all('div', class_='position-relative bg-card rounded m-1')
        print(manga_name + '\n' + manga_src + '\n' + manga_img)
        for some in chapters:
            chapter_number = re.findall('\d+', some.text.strip())[1]  # номер главы
            chapter_link = some.find('a').get('href')  # ссылка на главу
            chapter_html = session.get(url=chapter_link, headers=headers).text
            bsc = BeautifulSoup(chapter_html, 'lxml')
            pages = [page.get('src') for page in
                     bsc.find('div', class_='ch-show col-12 col-md-9 px-0 m-auto').find_all('img')]
            # pages_str = '|'.join(pages)
            if pages:
                count += 1
                title.count = count
                title.save()

            if chapter_number:
                nums.append(str(chapter_number))
                title.numbers = nums
                title.save()
            chapter = Chapter(title_name=title, number=chapter_number, pages=pages, slug=slug, img_src=manga_img).save()

            print('\t' + chapter_number.__str__() + ' ' + chapter_link)
        print()


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        session = requests.Session()
        url = 'https://waymanga.ru/login'
        catalog = 'https://waymanga.ru/manga'

        result = session.get('https://waymanga.ru/login')
        start = result.text.find('name="_token"') + 21
        stop = result.text.find('">', start)
        token = result.text[start:stop]

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        data = {
            "_token": token,
            "login": "dg",
            "password": "gm59z.MMGrHRv.N"
        }
        session.post(url=url, allow_redirects=True, data=data, headers=headers)

        source = session.get(url=catalog, headers=headers).text
        soup = BeautifulSoup(source, 'lxml')
        page_count = int(soup.find_all('li', class_='page-item')[-2].text)  # Число страниц в каталоге
        for page in range(1, page_count + 1):
            threading.Thread(target=parse, args=(page, session, headers)).start()