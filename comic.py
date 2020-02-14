from selenium import webdriver  # �����
from bs4 import BeautifulSoup
import requests
import time
import os
path = "C:\\Users\\pipizhu\\Desktop\\����Ů��"
def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + '�����ɹ�')
    else:
        print(path + 'Ŀ¼�Ѵ���')


def get_pic_from_url(url, path, number):
    try:
        pic_content = requests.get(url, stream=True).content
        open(path + '\\' + str(number)+ '.jpg', 'wb').write(pic_content)
    except:
        print("�����" + number + "ͼƬʧ��")


def get_html_dynamic(url):
    try:
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome(chrome_options=option)  # ���������
        browser.implicitly_wait(3)
        browser.get(url)  # �������Ԥ����ַ
        time.sleep(5)
        html = browser.page_source
        browser.quit()
        soup = BeautifulSoup(html, 'lxml')
        a = soup.find_all('a')
        return soup
    except:
        print("��̬ҳ����ȥʧ��")
        return False


# ��Ҫ����̬��Ⱦ����վ���ٶȽϿ졣
def get_html_static(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'UTF-8'
        time.sleep(10)
        print('��̬ҳ����������ɹ�')
        return r.text
    except:
        print("��̬ҳ����ȡʧ��")


# ��ȡ�����������½ڵ�����������
def get_menu(url):
    try:
        html = get_html_static(url)
        soup = BeautifulSoup(html, 'lxml')
        print('������ҳ���ݳɹ�')
        menu_name_list = []
        menu_link_list = []
        ulList = soup.find('ul', id='chapter-list-1')
        aList = ulList.find_all('a')
        for i in aList:
            menu_name = i.get('title')
            menu_link = i.get('href')
            menu_name_list.append(menu_name)
            menu_link_list.append(menu_link)
        return menu_name_list, menu_link_list
    except:
        print("��ȡ�½ں�����ʧ��")

    # ��ȡ����������


def get_picture_link(soup):
    try:
        div = soup.find_all('img')
        link = div[2].get("src")
        print(link)
        return link
    except:
        print("���ӻ�ȡʧ��")
    # ��ȡ��һ��������ҳ��


def get_number(soup):
    try:
        select = soup.find('select', id="page_select")
        option = select.find_all('option')
        number = 0
        for i in option:
            number = number + 1
        return number
    except:
        print("����ҳ����ȡʧ��")
        return False




# ��ȡ�ض�һҳ������
def get_mange(url, path, number):
    menu_name = path[34:]
    try:
        soup = get_html_dynamic(url)
    except:
        print(menu_name + "�ĵ�" + number + "����ʧ��")
        return False
    try:
        picture_link = get_picture_link(soup)
    except:
        print(menu_name + "�ĵ�" + number + "����ʧ��")
        return False
    try:
        get_pic_from_url(picture_link, path, number)
    except:
        print(menu_name + "�ĵ�" + number + "����ʧ��")
        return False


# ���ļ�ȫ��������
def make_folder(menu_name_list):
    try:
        mkdir(path)
        for i in range(len(menu_name_list)):
            path_menu = path + '\\' + menu_name_list[i]
            print(path_menu)
            mkdir(path_menu)
    except:
        print("�ļ��д������ִ���")


# ����ѯ�ֵ䴴����
def make_dictory(*args):
    menu_name_list=args[0]
    menu_link_list=args[1]
    url=args[2]
    dictory_menu=[]
    for i in range(len(menu_name_list)):
        try:
            soup = get_html_dynamic(url + menu_link_list[i])
        except:
            print("�е�����")
            continue
        try:
            number = get_number(soup)
        except:
            print("����������")
            continue
        for x in range(number):
            dictory = {}
            if (x == 0):
                dictory['url'] = url + str(menu_link_list[i])
                dictory['book_number'] = i
                dictory['page'] = 1
                dictory['path'] = path + "\\" + menu_name_list[i]
                dictory['true'] = 'false'
                print(dictory)
                with open('C:\\Users\\pipizhu\\Desktop\\����Ů��.txt','+a')as f:
                    f.write(str(dictory)+'\n')
            else:
                dictory['url'] = url + str(menu_link_list[i]) + '?p=' + str(x + 1)
                dictory['page'] = x + 1
                dictory['book_number'] = i
                dictory['path'] = path + "\\" + menu_name_list[i]
                dictory['true'] = 'false'
                print(dictory)
                with open('C:\\Users\\pipizhu\\Desktop\\����Ů��.txt','+a')as f:
                    f.write(str(dictory)+'\n')
            dictory_menu.append(dictory)
    return dictory_menu


# ��һ�ν����е���������һ��
def main_picture(dictory_menu):
    for i in range(len(dictory_menu)):
        try:
            get_mange(str(dictory_menu[i]['url']), str(dictory_menu[i]['path']), str(dictory_menu[i]['page']))
            dictory_menu[i]['true'] = 'true'
        except:
            print(str(dictory_menu[i]['book_number']) + "��" + str(dictory_menu[i]['page']) + "ҳ" + "����ʧ��")
            continue
    return dictory_menu

# ��һ�μ�鿴�Ƿ����е�������������������
def main_check(dictory_menu):
    for i in range(len(dictory_menu)):
        if (dictory_menu[i]['true'] == 'flase'):
            try:
                get_mange(dictory_menu[i]['url'], dictory_menu[i]['path'], dictory_menu[i]['page'])
            except:
                continue
    return dictory_menu

def twice_check(dictory_menu):
    wrong_number = 0
    for i in range(len(dictory_menu)):
        if (dictory_menu[i]['true'] == 'flase'):
            wrong_number = wrong_number + 1
    if (wrong_number == 0):
        return True
    else:
        main_check(dictory_menu)
        twice_check(dictory_menu)



def main(url):
    try:
        menu_name_list, menu_link_list = get_menu(url)
    except:
        return False
    url = url[:-20]
    make_folder(menu_name_list)
    make_dictory(menu_name_list,menu_link_list,url)

    '''
    dictory_menu=main_picture(dictory_menu)
    dictory_menu=main_check(dictory_menu)
    twice_check(dictory_menu)
    '''
main('https://www.manhuadui.com/manhua/jiayounvyou/')