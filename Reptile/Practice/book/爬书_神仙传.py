# -*-coding:utf-8-*-
# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
from lxml import etree


def downloadBook():
    url = 'https://www.xstt5.com/gudian/10231/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'
    }

    response = requests.get(url=url, headers=headers)
    # 解决乱码问题
    response.encoding = 'GBK'
    response.encoding = 'utf-8'

    page_text = response.text
    # 注意点，当获取的响应内容被注释，可以使用替换注释符号
    page = page_text.replace('<!--', '')
    tree = etree.HTML(page)
    title = tree.xpath('//div[@class="jieshao"]/img/@alt')[0]
    list_href = tree.xpath('//ul[@class="am-avg-sm-4 am-thumbnails list hide"]//li/a/@href')
    a = qie(list_href)
    a = sort(a)
    writeBook(a, headers, title)
    # soup = BeautifulSoup(page, 'lxml')
    # title = soup.select('.bktitle h1')
    # # print(soup.find('ul', class_='list'))
    # li_list = soup.select('.list ul li a')


# 切分
def qie(list_href):
    a = []
    for num in list_href:
        # print(num)
        n = num.split('/')[-1]
        n = n[0:6]
        a.append(n)
    return a


def sort(a):
    # 冒泡排序
    for t in range(len(a) - 1):
        for j in range(len(a) - 1):
            if a[j] > a[j + 1]:
                temp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = temp
    return a


def writeBook(book, headers, title):
    filename = '../../Data/book/' + title + ".txt"
    fp = open(filename, 'w', encoding='utf-8')
    c = [i for i in range(len(book))]

    for li, i in zip(book, c):
        d_url = 'https://www.xstt5.com/gudian/10231/' + li + '.html'
        print(d_url)
        # 对详情页发送请求
        res = requests.get(url=d_url, headers=headers)
        # 解决乱码问题
        res.encoding = 'GBK'
        res.encoding = 'utf-8'

        detail_text = res.text
        # print(detail_text)
        d_soup = BeautifulSoup(detail_text, 'lxml')
        div_tag = d_soup.find('div', class_='zw')
        content = div_tag.text
        label = juan(i)
        # print(label)
        fp.write(label + ' : ' + content + '\n')
    print('爬取结束！！！')


def juan(num):
    numbers = {
        0: "序",
        1: "卷一",
        2: "卷二",
        3: "卷三",
        4: "卷四",
        5: "卷五",
        6: "卷六",
        7: "卷七",
        8: "卷八",
        9: "卷九",
        10: "卷十"
    }
    return numbers.get(num, None)


if __name__ == "__main__":
    downloadBook()
