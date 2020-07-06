#爬取小说《富婿韩三千》

import requests #用来抓取网站源码
import random  #取随机数
import time #计时
import re  #正则表达式
import urllib
import sys

from bs4 import BeautifulSoup#用于代替正则式，取源码中标签内容



def get_content(url,data = None):
    #模拟浏览器访问
    header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Encoding':'br,gzip,deflate',
        'Accept-Language':'zh-cn',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
    }

    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    #设置一个超时时间,防止被网站认定为爬虫
    timeout = random.choice(range(80,100))

    while True:
        try:
            req = requests.get(url=url,headers=header,timeout=timeout)
            req.encoding = "utf-8"
        #    req.encoding = "GBK"
            break
        except Exception as e:
            print(e)
            time.sleep(random.choice(range(8,15)))
    return req.text


def get_re(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode("utf-8")
    print(html)
#    req = '<li><a href="(.*?)" rel=".*?">(.*?)</a></li>'
    req = '<a href="(.*?)">(.*?)</a>'
    # comment = re.compile(req,re.DOTALL)
    # urls = comment.findall(html)
    urls = re.findall(req, html)
    print(urls)
    a_url = []
    a_name = []
   # server = 'http://www.zongcaidarentilihaoya.com'
    server = 'http://www.78zw.com'
    for i in urls:
        #章节网址
        novel_url = server + i[0]
        #章节名字
        novel_name = i[1]
        if re.search(r'.*?章', novel_name) is None or (novel_url in a_url) :
            pass
        else:
            a_url.append(novel_url)
            a_name.append(novel_name)
    return a_name,a_url

def get_cont(url):
    html = get_content(url)
    bf = BeautifulSoup(html,'html.parser')
    print(bf)
    print('bf end')
    print(str(bf))
    print('str end')

    # req =  r'<br><br>　　"(.*?)"'
    t = re.findall(r"<br><br>(.*?)</br>", str(bf))
    print(t)
    print('t end')
    print(t[0])
    print('t[0] end')
    txt = str(t[0]).replace('<br><br>　　',"\n")#去掉多余的一些广告字符
    txt = txt.replace('⑦⑧中文全网更新最快 ωωω.七8zω.cδм',"")
    txt = txt.replace('78中文更新最快 电脑端:https://m.78zw.com/',"")
    txt = txt.replace('78中文最快 手机端：https:/www.78zw.com/',"")
    txt = txt.replace('78中文首发 www.78zw.com m.78zw.com',"")
    txt = txt.replace('七八中文首发 www.7*8zw.com m.7*8zw.com', "")
    txt = txt.replace('电脑端:https://m.78zw.com/',"")
    txt = txt.replace('手机端：https:/www.78zw.com/',"")

  #  print(txt)
    return txt



#获取下载的目录
def get_download_catalogue(url):
    html = get_content(url)
    bf = BeautifulSoup(html,'html.parser')
    print(bf)
    texts = bf.find_all('div',{'class':'panel-body'},'ul',{'class':'list-group list-charts'})
    print('*'*20)
    print('\n\n')
    print(texts)
    print('*'*25)
    div = texts[0]
    print(div)
   # div = texts
    a_s = div.find_all('a')
    names = []
    urls = []
 #   server = 'http://www.biqugeso.com/book/40838/'
    server = 'http://www.zongcaidarentilihaoya.com'

    nums = len(a_s[12:17])  # 需要去掉重复的最新章节列表 这里只取不重复的前5章
    for each in a_s[12:17]:
        names.append(each.string)
        urls.append(server + each.get('href'))
    return names,urls

def get_download_catalogue2(url):
    html = get_content(url)
    bf = BeautifulSoup(html,'html.parser')
    print(bf)
    texts = bf.find_all('div',{'id':'list'})
    print('\n\n')
    print(texts)
    print('*'*25)
    soup = bf
    # 获取章节名称
    subtitle = soup.select('#htmltimu')[0].text
    # 判断是否有感言
    if re.search(r'.*?章', subtitle) is  None:
        return
    # 获取章节文本
    content = soup.select('#htmlContent')[0].text
    print(content)


def get_download_content(url):#获取下载内容
    # html = get_content(url)
    # bf = BeautifulSoup(html,'html.parser')
    # print(bf)
    # print('content1 end')

    html = urllib.request.urlopen(url).read()
    html = html.decode("utf-8")
    print(html)
    print('*'*20)
    print(str(html))

    reg = '</script>&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<script type="text/javascript">'
    reg = re.compile(reg,re.S)
    c_content = re.findall(reg,url)
    print(c_content)
    print('c end1')

    c_content = c_content[0].replace("&nbsp;&nbsp;&nbsp;&nbsp;","")
    c_content = c_content.replace("<br/>", "")
    print(c_content)

    html = get_content(url)
    bf = BeautifulSoup(html,'html.parser')
    print(bf)
  #  print(bf.text)
    texts = bf.find_all('div',{'class':'panel-heading'})
    print(texts)
    text = texts[0].text

    return text


#将文章写入文件
def writer(name,path,text):

    with open(path,'a',encoding='utf-8') as f:
        f.write(name + '\n')
        f.writelines(text)
        f.write('\n\n')



#主函数部分
if __name__ == '__main__':

    base_url = "http://www.78zw.com/5_5812/"
    path = './富婿韩三千.txt'

    names,urls = get_re(base_url)
    print('re end')

   # names,urls = get_download_catalogue(base_url)
    print(names)
    print('*'*20)
    print(urls)
    print(len(urls))
 #   for i in range(3,len(urls)):
     #   u = urls[i]
      #  t = get_download_content(urls[i])
    begin = 9
    end = 15
    for i in range(begin,end):
        t = get_cont(urls[i])
        name = names[i]

     #   print(t)

    #使用writer进行写入文件
        writer(name,path,t)
        print('第{}章已下载完成'.format(i+1-begin))

    t = get_download_content(url)

    writer(str(1),path,t)
    print("下载完成!")

