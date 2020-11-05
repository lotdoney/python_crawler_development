import requests
import re
import os
from  multiprocessing.dummy import Pool

commonurl = 'https://read.qidian.com/chapter/'
def query(url):
    return  requests.get(url).content.decode()

def chapter_query(url):
    bid = url.split("/")[-1]
    headers ={
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    res = requests.get(url,headers=headers)
    title = re.search('《(.*?)》',res.text).group(1)
    cookie = requests.utils.dict_from_cookiejar(res.cookies)
    Token = cookie['_csrfToken']
    res = requests.get(f'https://read.qidian.com/ajax/book/category?_csrfToken={Token}&bookId={bid}',
                       headers=headers).text.encode("raw_unicode_escape").decode()
    return res

def get_chapter(html):
    total_url_list = []
    total_list = re.findall('"cU":"(.*?)"',html,re.S)
    for each in total_list:
        total_url_list.append(commonurl+each)
    return total_url_list

def get_content(html):
    title = re.findall('<span class="content-wrap">(.*?)<',html,re.S)[0]
    content = re.findall('j_readContent ">\n            <p>(.*?)</div>',html,re.S)[0]
    content = content.replace('<p>', '\n')
    return title,content

def save(title,content):
    os.makedirs('路易的奇幻冒险',exist_ok=True)
    with open(os.path.join('路易的奇幻冒险',title+'.txt'),'w',encoding='utf-8') as f:
        f.write(content)

def url_answer(url):
    answer = query(url)
    title,content = get_content(answer)
    save(title,content)

if __name__ == '__main__':
    res = chapter_query('https://book.qidian.com/info/1021131637')
    chapter_list = get_chapter(res)
    pool = Pool(5)
    pool.map(url_answer,chapter_list)