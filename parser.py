from bs4 import BeautifulSoup
import urllib.request
import time

from tqdm import tqdm
from selenium import webdriver


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def imitate_browser(link, number):
    url = 'https://coursehunter.net' + link
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get("https://coursehunter.net/sign-in")
    login = browser.find_element_by_name("e_mail")
    password = browser.find_element_by_name("password")
    submit = browser.find_element_by_xpath("//button[@type='submit']")
    login.send_keys('login')
    password.send_keys('password')
    submit.click()
    time.sleep(2)
    browser.get(url)
    generated_html = browser.page_source

    download_lessons(generated_html, number)


def my_replace(str):
    newString = ' '.join(
        str.replace('"', '`').replace(':', '--').replace('|', '').replace('?', '').replace('/', '-').split())

    return newString


def download_lessons(html, lessonnumber):
    page = BeautifulSoup(html, 'html5lib')
    lessons = list()
    htmlList = page.find_all('li', class_='lessons-item')
    for item in htmlList:
        lessons.append({
            "url": item.find('link', itemprop='url')['href'],
            "name": item.find('span', class_='lessons-title').text + ' - ' + my_replace(
                item.find('div', class_='lessons-name').text)
        })

    if not lessonnumber:
        pass
    else:
        lessons = lessons[lessonnumber:]

    for lesson in lessons:
        urli = lesson.get('url')
        output = lesson.get('name') + '.mp4'
        print('-----------')
        print(output)
        print('-----------')
        download_url(urli, output)


# myLogin = input("Введите Login: ")
# myPassword = input("Введите Password: ")
courseLink = input("Введите ссылку на курс: ")
numberLesson = (input('Введите номер урока/Или нажмите Enter: '))

numberOfLesson = None

if not numberLesson:
    pass
else:
    numberOfLesson = int(numberLesson)

imitate_browser(courseLink, number=numberOfLesson)
