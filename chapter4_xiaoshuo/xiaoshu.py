from multiprocessing.dummy import Pool
import re
import requests
import os
import time
start_url = 'https://www.kanunu8.com/book3/8256/'

def get_toc(html):
    """
    获取每一章的链接，存储到一个列表中并返回
    :param html:目录页源代码
    :return :每章链接
    """
    toc_url_list = []
    toc_block = re.findall('正文(.*?)</tbody>',html,re.S)[0]
    toc_url = re.findall('href="(.*?)"',toc_block,re.S)
    print(toc_url)
    for url in toc_url:
        toc_url_list.append(start_url+url)

    return toc_url_list

def qury(url):
    html = requests.get(url).content.decode(encoding='gbk')
    return  html

html = qury(start_url)
toc_url_list = get_toc(html)


def get_content(html):
    """
    :param html:
    :return:
    """
    title = re.search('size="4">(.*?)<',html,re.S).group(1)
    content = re.search('<p>(.*?)</p>',html,re.S).group(1)
    content = content.replace('<br />','')
    return title,content


def save(chapter,ariticle):
    os.makedirs('红高粱', exist_ok=True)
    with open(os.path.join('红高粱',chapter+'.txt'),'w',
              encoding='utf-8')as f:
        f.write(ariticle)

def query_article(url):
    ariticle_html =qury(url)
    chapter,ariticle = get_content(ariticle_html)
    save(chapter,ariticle)

if __name__ =='__main__':
    start = time.time()
    pool = Pool(5)
    pool.map(query_article,toc_url_list)
    end = time.time()
    print(f'消耗时间为：{end-start}')