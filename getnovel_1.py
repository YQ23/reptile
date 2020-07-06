#爬取小说

import requests #用来抓取网站源码
import random  #取随机数
import time #计时
import sys

from bs4 import BeautifulSoup  #用于代替正则式，取源码中标签内容

# def get_data(html):
#     bf = BeautifulSoup(html,'html.parser')
#     texts = bf.find_all('div',{'class':'showtxt','id':'content'})
#     text = texts[0].text.replace('\xa0'*7,'\n\n')#'\xa0'表示连续的空白格
#     print(text)





def get_content(url,data = None):
    #模拟浏览器访问
    header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Encoding':'br,gzip,deflate',
        'Accept-Language':'zh-cn',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
    }

    #设置一个超时时间,防止被网站认定为爬虫
    timeout = random.choice(range(80,100))

    while True:
        try:
            req = requests.get(url=url,headers=header,timeout=timeout)
            req.encoding = "GBK"  #使用的是GBK编码格式
            break
        except Exception as e:
            print(e)
            time.sleep(random.choice(range(8,15)))
    return req.text

#获取下载的目录
def get_download_catalogue(url):
    html = get_content(url)
    bf = BeautifulSoup(html,'html.parser')
    print(bf)
    print('*'*30)
    texts = bf.find_all('div',{'class':'listmain'})#找到所有class为listmain的文本
    div = texts[0]
    a_s = div.find_all('a')
    names = []
    urls = []
    server = 'http://www.biqukan.com/'

    nums = len(a_s[12:17])  # 需要去掉重复的最新章节列表 这里只取不重复的前5章
    for each in a_s[12:17]:
        names.append(each.string) 
        urls.append(server + each.get('href'))
    return names,urls



#获取下载的具体章节
def get_download_content(url):
    html = get_content(url)
    bf = BeautifulSoup(html,'html.parser')

    texts = bf.find_all('div',{'class':'showtxt','id':'content'})
  #  text = texts[0].text
    text = texts[0].text.replace(' ' * 4, '\n\n')
    #text = texts[0].text.replace('\xa0'*4,'\n\n')#'\xa0'表示连续的空白格
    #  print(text)
    return text


#将文章写入文件
def writer(name,path,text):

    with open(path,'a',encoding='utf-8') as f: #按照utf-8格式写入
        f.write(name + '\n')
        f.writelines(text)
        f.write('\n\n')





if __name__ == '__main__':
    #url = "http://www.biqukan.com/0_790/36873824.html"
    base_url = "http://www.biqukan.com/0_790"
    #base_url = "https://www.biqugeso.com/book/40838/"
    path = './天尊.txt'
    names,urls = get_download_catalogue(base_url)
    print(names)
    print('*'*20)
    print(urls)
    print(len(urls))
    for i in range(0,len(urls)):
     #   u = urls[i]
        t = get_download_content(urls[i])
        name = names[i]
        print(t)
     #   print(t)

      #  writer(name,path,t)
        print('第{}章已下载完成'.format(i+1))

#    t = get_download_content(url)

  #  writer(str(1),path,t)
    print("下载完成!")

