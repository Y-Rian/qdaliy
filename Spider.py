'''
@Author  : Y-Rian
@Time    : 2018/1/28 21:50
'''
import requests
from bs4 import BeautifulSoup
base_url='http://www.qdaily.com/categories/19.html'
# url_more='http://www.qdaily.com/categories/categorymore/19/'
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
}

def get_last_key(url):
    respons=requests.get(base_url)
    respons.encoding='utf-8'
    html=respons.text
    soup=BeautifulSoup(html,'lxml')
    tag=soup.find('div',class_='packery-container articles')
    last_key=tag['data-lastkey']
    div_tag=soup.find_all('div',class_='pic imgcover')
    urls_list=[]
    for div in div_tag:
        img_url=div.find('img')['data-src']
        # print(div)
        # print(img_url)
        urls_list.append(img_url)
    # print(urls_list)

    # 保存封面图片
    for url in urls_list:
        img=requests.get(url,headers=header).content
        name=str(url[43:73])
        # img//为文件夹路径
        with open('img//'+name+'.jpg','wb') as f:
            f.write(img)
    return last_key
# 下一页
def get_next_page(last_key):
    url_more=base_url.replace('categories','categories/categorymore')[:-5]
    url=url_more+'/'+last_key+'.json'
    data=requests.get(url).json()
    numb=len(data['data']['feeds'])
    more_last_key=data['data']['last_key']

    print('last_key=',more_last_key)
    print(numb)
    for num in range(numb):

        new_img=data['data']['feeds'][num]['image']

        img=requests.get(new_img).content
        filename='img//'+new_img[43:73]+'.jpg'
        with open(filename,'wb') as fb:
            fb.write(img)
        # print(new_img)
        # print(data)
    # print(last_key)
    # print(url)
    # print()
    get_next_page(str(more_last_key))

key=get_last_key(base_url)

get_next_page(key)