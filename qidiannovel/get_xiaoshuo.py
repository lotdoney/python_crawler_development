import requests
import json
import re
from lxml import etree
def get_qidian(url):


    # 设置全局变量
    some_ = ''
    # 提取bookid
    bid = url.split("/")[-1]
    print(bid)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    #print(res.text)
    # 提取后面用到的refer
    new_url = 'https:' + re.search(re.compile(r'<a class="red-btn J-getJumpUrl " href="(.*?)"'), res.text).group(1)
    # 提取小说名字
    title = re.search(re.compile('《(.*?)》'), res.text).group(1)

    # 两种提取cookie成字典模式
    # 第一种
    # print(res.cookies.list_domains())
    # print(res.cookies.list_paths())
    # print(res.cookies.get_dict(res.cookies.list_domains()[0],res.cookies.list_paths()[0]))

    # 第二种
    print(res.cookies)
    #以字典的形式返回
    cookie = requests.utils.dict_from_cookiejar(res.cookies)
    print(cookie)
    Token = cookie['_csrfToken']

    # 更新字典的headers
   # headers.update({"x-requested-with": "XMLHttpRequest", "referer": new_url})
    headers.update(cookie)
    # 解码返回的内容
    res = requests.get(f'https://read.qidian.com/ajax/book/category?_csrfToken={Token}&bookId={bid}',
                       headers=headers).text.encode("raw_unicode_escape").decode()
    #把返回的内容转为json格式
    res = json.loads(res)
    #print(res)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    }
    # 提取列表
    for s in res['data']['vs']:
        # 提取目录内容
        for i in s['cs']:
            # 提取章节名字
            chapter = i['cN']
            # 提取链接后半部分
            ch_url = 'https://read.qidian.com/chapter/' + i['cU']
            # print(chapter)
            # print(ch_url)
            # https://read.qidian.com/chapter/
            # <div class="read-content j_readContent">
            res = requests.get(ch_url, headers=headers).text
            # print(res)
            # 通过etree提取每一章的内容
            selector = etree.HTML(res)
            txt_ = selector.xpath('//div[@class="read-content j_readContent"]/p/text()')
            # print(txt_)
            all_txt = ''
            for g in txt_:
                # 对每一条内容进行处理
                g = str(g)
                g = g.replace('\u3000\u3000', '').replace('\n', '').strip() + '\n'
                all_txt = all_txt + g
            # 把所有内容放在一个变量里，最后再保存
            all_txt = chapter + '\n\n' + all_txt
            some_ = some_ + all_txt
    # 把所有处理好了，进行写出保存
    with open(f'{title}.txt', 'w') as f:
        f.write(some_)
        f.close()


if __name__ == '__main__':
    get_qidian('https://book.qidian.com/info/1021131637')