import requests
import time
import os
import re
import random
from bs4 import BeautifulSoup


# 抓取网页的函数
def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'GBK'
        # print(r.text)
        time.sleep(random.random() * 3)
        return r.text
    except:
        return "ERROR"


# 存储各个排名的网站地址
def mkdir(path):
    os.makedirs(path)


# 存储各个排名的网站地址
def get_content(url):
    url_list = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    category_list = soup.find_all('ul', class_="ultops")
    for cate_list in category_list:
        year = cate_list.find_all('a')
        for i in year:
            years = i.string
            link = i.get('href')
            url_list.append(link)
    return url_list


# 获取每一年的排名的书和链接
def get_book(url):
    booklist = []
    bookname = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    book_list = soup.find_all('table', class_='grid')
    # 只取文库部门
    for book in book_list:
        book1 = book.find_all('a')
        book1_cut = book1[1::2]
        for book2 in book1_cut:
            book_name = book2.get_text()
            book_link = book2.get('href')
            booklist.append(book_link)
            bookname.append(book_name)
    return booklist, bookname


# 进入书的目录里面
def get_menu(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    book_menu = soup.find_all('div', attrs={'style': 'text-align:center'})
    book_menu = book_menu[0]
    for i in book_menu:
        url = i.get('href')
    return url


# 获得同一本书的全部章节
def get_menu_all(url):
    print('开始执行这该死的程序')
    menu_all = []  # 书的链接
    menu_menu_all = []  # 书的名字
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    book_menu_all = soup.find_all('td', attrs={'class': 'ccss'})
    for i in book_menu_all:
        link = i.find_all('a')
        for p in link:
            book_menu_link = p.get('href')
            menu_menu_name = p.contents
            menu_all.append(book_menu_link)
            menu_menu_all.append(menu_menu_name)
    return menu_all, menu_menu_all


def get_value(url,name,year,novel_name):
    print(url,name,year,novel_name,)
    url=str(url)
    name=str(name)
    year=str(year)
    novel_name=str(novel_name)
    try:
        html=get_html(url)
        soup=BeautifulSoup(html,'lxml')
        name=''.join(name)
        print(soup)
        #full_path=text_create(year,name,novel_name)
        book_value=soup.find('div', id='content').text.replace('chaptererror();', '')
        print(book_value)
        print(name+'请求成功')
        full_path = "C:\\Users\\pipizhu\\Desktop\\novel\\"+str(year)+"\\"+str(novel_name)+"\\"+str(name)+".txt"
        print(full_path)
        try:
            with open(full_path,"w",encoding='utf-8')as f:
                     f.write(book_value);
            print(name+'保存成功')
        except:
            print("文件打开失败")
    except:
        print(name+'尝试重新执行')
        #get_value(url,name,year,novel_name)


def text_create(year, name, novel_name):
    desktop_path = "C:\\Users\\pipizhu\\Desktop\\novel\\" + str(year) + "\\" + str(novel_name) + "\\"  # 新创建的txt文件的存放路径
    try:
        full_path = desktop_path + str(name) + '.txt'  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w')
    except:
        print("txt创建失败")
    return full_path

def create(url):
    url_list = get_content(url)
    mkdir("C:\\Users\\pipizhu\\Desktop\\" + "novel")
    print('成功创建基本文件夹')
    for url in url_list:
        url1 = url[-8:-4]
        mkdir("C:\\Users\\pipizhu\\Desktop\\novel\\" + url1)
        print('成功创建' + url1 + '文件夹')
        a, b = get_book(url)  # 获取每一本书的链接和书名
        print(a, b)
        print('成功获取' + url1 + '每一本书的链接和书名')
        for book_name in b:
            try:
                mkdir("C:\\Users\\pipizhu\\Desktop\\novel\\" + url1 + "\\" + book_name)
                print('成功创建' + book_name + '文件夹')
            except:
                b = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', book_name, re.S)  # 只要字符串中的中文，字母，数字
                b = "".join(b)
                mkdir("C:\\Users\\pipizhu\\Desktop\\novel\\" + url1 + "\\" + b)
                print('成功创建' + b + '文件夹')
        for i in range(len(a)):
            try:
                html = get_menu(a[i])  # 获得进到目录里面后的链接
                print("成功获得进到" + b[i] + "目录里面的链接" + html)
                menu_all, menu_menu_all = get_menu_all(html)
                print("成功获得进入" + b[i] + str(menu_menu_all))
            except:
                print("获得进入" + b[i] + "链接以及名字失败")

            print(html)
            a1 = html[:-9]
            print(a1)
            for number in range(len(menu_all)):
                try:
                    menu_menu_all_menu=str(menu_menu_all[number])
                    print(menu_menu_all_menu)
                    menu_menu_all_menu = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', menu_menu_all_menu, re.S)  # 只要字符串中的中文，字母，数字
                    menu_menu_all_menu="".join(menu_menu_all_menu)
                    print(a1 + menu_all[number], menu_menu_all_menu)
                    get_value(a1 + menu_all[number], menu_menu_all_menu, url1, b[i])
                except:
                    print("保存小说失败")


def mkdir(path):
    # 引入模块

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

create('https://www.wenku8.net/zt/sugoi/2020.php')
#get_value('https://www.wenku8.net/novel/2/2527/95416.htm','序章',2020,'七魔剑支配天下(七柄魔剑将其支配)')