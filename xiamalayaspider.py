import csv
import os
import re
from lxml import etree
import requests
import time

#注意修改文件保存路径
start_url='https://www.ximalaya.com/channel/28/'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

# 爬取FM页面内容
def getAllpage(url):
    r = requests.get(url, headers=header)
    html = r.text
    # 通过正则表达式提取页面的最大页数
    result = re.findall(r'<li class="page-item y_J".*?><a class="page-link y_J".*?><span>(.*?)</span>', html, re.S)
    #将最大页数提取数字转为整型
    result=int(result[-1])
    url_list = []
    # 循环获取每个页面
    for i in range(1,result+1):
        if i==1:
            url_list.append(start_url)
        else:
            second_url=start_url+'p{}/'.format(i)
            url_list.append(second_url)
    # print(url_list)将所有网页url放入一个数组中

    for i in range(1,result):
        print(">>>开始爬取第{}页".format(i))
        url=url_list[i-1]
        print(url)
        r=requests.get(url,headers=header)
        response=etree.HTML(r.text)
        time.sleep(0.1)
        #匹配所有播放组件
        allFM=response.xpath('//*[@id="award"]/main/div[1]/div[3]/div[2]/ul/li')
        for i in allFM:
            info = []
            item={}
            #标题
            item['title']=i.xpath(" div / a / span/text()")[0]
            #作者
            item['author'] = i.xpath(" div/a[2]/text()")[0]
            #播放量
            item['playback'] = i.xpath("div/div/a/p/span/text()")[0]
            #链接
            item['href'] = "https://www.ximalaya.com"+i.xpath("div/div/a/@href")[0]

            # 保存图片
            # img_src=i.xpath('/div/div/a/img')[0]
            # img_name = i.xpath(" div / a / span/text()")[0]+ '.jpg'
            # img_path='./img/picture/'+img_name
            # 图片出现越界问题无法爬取

            GetFM_Music(item['href'], change_title(item['title']))
            info.append(item)
            print(item)

            # 以csv文件格式保存内容
            f = open('C:\\Users\\Jason\\PycharmProjects\\shixiseng\\ximalaya\\ximalaya.csv', 'a', newline='', encoding='utf-8')
            csv_a = csv.writer(f)
            csv_a.writerow(info)



#爬取音频
def GetFM_Music(href,title):
    pattern = r'album/(\d+)'
    album_ids = re.findall(pattern, href)
    #匹配每个音频的id
    if album_ids:
        album_id = album_ids[0]
    else:
        print('No match')
    src = 'https://www.ximalaya.com/revision/play/v1/audio?id='+album_id+'&ptype=1'
    r=requests.get(src,headers=header)
    #找到音频文件所在的url
    pattern1 = r'"src":"([^"]+)"'
    match = re.search(pattern1, r.text)
    if match:
        src_value = match.group(1)
        print('音频文件地址',src_value)
        # 下载音频
        foldername = 'C:\\Users\\Jason\\PycharmProjects\\shixiseng\\ximalaya\\'
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        response = requests.get(url=src_value, headers=header).content
        with open(foldername+title +'.m4a', mode='wb') as file:
            file.write(response)
    else:
        print('没有vip，无法下载')


def change_title(title):
    """处理文件名非法字符的方法"""
    pattern = re.compile(r"[\/\\\:\*\?\"\<\>\|]")  # '/ \ : * ? " < > |'
    new_title = re.sub(pattern, "_", title)  # 替换为下划线
    return new_title






if __name__ == '__main__':
    getAllpage(start_url)

