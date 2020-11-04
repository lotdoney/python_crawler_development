import re
import csv
#读入文件
with open('inter.txt','r',encoding='utf-8') as f:
    source = f.read()
#按照每一层进行分割
every_result = re.findall('l_post l_post_bright j_l_post clearfix  "(.*?)p_props_tail props_appraise_wrap">',
                          source,re.S)
#在每一层中取找到用户名，头衔，发帖时间等
result_list =[]
for every in every_result:
    result = {}
    result['username'] = re.findall('username="(.*?)"',every,re.S)[0]
    if "class=\"d_badge_title \"" in every:
        result['rank'] = re.findall('class="d_badge_title ">(.*?)<',every,re.S)[0]
    elif "d_badge_title_bawu\"" in every:
        result['rank'] = re.findall('d_badge_title_bawu">(.*?)<', every, re.S)[0]
    result['content'] = re.findall('j_d_post_content " style="display:;">(.*?)<'
                                ,every,re.S)[0].replace('            ','')
    result['time'] = re.findall('class="tail-info">(2020.*?)<',every,re.S)[0]
    result_list.append(result)

with open('inter.csv','w',encoding='utf-8') as f:
    wirter = csv.DictWriter(f,fieldnames=['username','rank','content','time'])
    wirter.writeheader()
    wirter.writerows(result_list)