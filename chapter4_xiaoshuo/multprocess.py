from multiprocessing.dummy import Pool
import requests
import time

def qury(html):
    requests.get(html)

html_list = []
for i in range(100):
    html_list.append('https://baidu.com')
start = time.time()
num = ''
while num!='quit':
    num = input("请输入你需要的线程数：")
    if num =='quit':
        break
    numbers = int(num)
    pool = Pool(numbers)
    pool.map(qury,html_list)
    end = time.time()
    print(f'消耗时间为：{end-start}')