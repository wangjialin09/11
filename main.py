import requests
import json
import time
import re

CommentList = [['昵称', 'ID', '发表时间', '评论内容', '点赞数', '回复数']]
headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 及时更换cookie，否则取不到location这个变量，最终整个程序报错。单次使用时也可以删除第6行的IP属地列，然后注释掉51行和61行，最后删除“hlist.append('IP属地')”这一列及第6行的内容
    # 'cookie' : "buvid3=F8310CC8-8B03-D7E4-A9C4-5584145E22C857391infoc; b_nut=1687623157; _uuid=A671013DC-4E3D-98FB-51410-A6438C1258E257734infoc; buvid4=9705AA53-8F88-ECFC-D12B-C41DB2A8AF6458593-023062500-RGrZ9spAgTkpUylipaSmKg%3D%3D; rpdid=|(u~)uJ~Jl))0J'uY)~Y)mRu|; buvid_fp_plain=undefined; fingerprint=d20ca4f3dd5048943de2f44a587a7f9b; i-wanna-go-back=-1; buvid_fp=fdf04d5dbbaf185e62e1c33705ab200d; header_theme_version=CLOSE; home_feed_column=5; DedeUserID=152029959; DedeUserID__ckMd5=e89cdf2c62e851de; nostalgia_conf=-1; b_ut=5; FEED_LIVE_VERSION=V8; CURRENT_QUALITY=64; browser_resolution=1512-768; enable_web_push=DISABLE; SESSDATA=087489ae%2C1713185286%2C5e53d%2Aa2CjBz-l25Zm4pD18fQ-aUNEAnwM8Mo8DldgD0AyogmnahVftQU1eSnI-wFeayHYCIzMESVko0SHNxYll3UUsxVzItZEtwaFJjZ29VNGZXMXVrZWVDU3B6bmd1Y1FhQ0VwLXdVWjMxUkhaOExhY3lQdDNiaTZOblVJRFRuc3BxajIxU3BaY0dZWUhRIIEC; bili_jct=25b4c6375fba7535805be1c71b07d14c; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTc4OTI1MzksImlhdCI6MTY5NzYzMzI3OSwicGx0IjotMX0.QaNIaN5PM5uc2YdxPW3A5mRzl1a7Ex148WtaIvGx-NI; bili_ticket_expires=1697892479; sid=7flfd8if; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; bp_video_offset_152029959=854201744600596484; bsource=search_baidu; PVID=1; b_lsid=7CCF658C_18B483F1C3C" ,
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/video/BV1FG4y1Z7po/?spm_id_from=333.337.search-card.all.click&vd_source=69a50ad969074af9e79ad13b34b1a548',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}


def fetchURL(url):
    # response = requests.get(url = url , headers=headers)
    # print('Have got the html\n')
    # return response.text
    return requests.get(url=url, headers=headers).text


def parseHtml(html):
    s = json.loads(html)
    # print(f"the type of html is {type(html)}\n")  Str
    # print(f"the type of s is {type(s['data']['replies'])}\n")       # Dictionary
    # the function 'json.loads' turned string into dictionary
    # '''
    # CommentList = []
    # hlist = []
    # hlist.append('IP属地')
    # hlist.append('昵称')
    # hlist.append('ID')
    # hlist.append('发表时间')
    # hlist.append('评论内容')
    # hlist.append('点赞数')
    # hlist.append('回复数')
    # CommentList.append(hlist)
    # '''
    '''
        CommentList = [] 
        hlist = []
        hlist.append('昵称')
        hlist.append('ID')
        hlist.append('发表时间')
        hlist.append('评论内容')
        hlist.append('点赞数')
        hlist.append('回复数')
        CommentList.append(hlist)
    '''

    for i in range(0, 15):
        comment = s['data']['replies'][i]
        # location = comment['reply_control']['location'][5:]
        # print(location[5:])
        uname = comment['member']['uname']
        ID = comment['member']['mid']
        stris = "'"
        ctime = stris + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment['ctime']))  # time of comment
        content = comment['content']['message']
        like = comment['like']
        rcount = comment['rcount']

        alist = []
        # alist.append(location)
        alist.append(uname)
        alist.append(ID)
        alist.append(ctime)
        alist.append(content)
        alist.append(like)
        alist.append(rcount)
        CommentList.append(alist)

    # print('Have got CommentList\n')
    # return CommentList


def Write2Csv(List, title):
    import pandas as pd
    dataframe = pd.DataFrame(List)
    # print(title)
    # filepath ='D:\Desktop\SpiderOfComment\CSVComment\\' + title + '.csv'
    filepath = title + '.csv'
    # print(filepath)
    dataframe.to_csv(filepath, index=False, sep=',', header=False, encoding='utf_8_sig')
    # dataframe.to_excel('')
    # print('Have written to the csv\n')


def GetTitle(url):
    page_text = requests.get(url=url, headers=headers).text
    # print(page_text)
    ex = '<h1 title="(.*?)".*?</h1>'
    title = re.findall(ex, page_text, re.S)[0]
    # print(type(title))
    return title


def GetOid(url):
    page_text = requests.get(url=url, headers=headers).text
    ex = '</script><script>window.__INITIAL_STATE__={"aid":(.*?),"bvid":'
    #  </script><script>window.__INITIAL_STATE__={"aid":269261816,"bvid"
    oid = re.findall(ex, page_text, re.S)[0]
    return oid


if __name__ == '__main__':
    print('请输入B站视频url：')
    temp_url = input()
    title = GetTitle(temp_url)
    # print(type(title))
    oid = GetOid(temp_url)
    url0 = 'https://api.bilibili.com/x/v2/reply?type=1&oid=' + oid + '&sort=2&pn='
    # print(url)
    print('Wait……')
    for i in range(1, 20):
        url = url0 + str(i)
        html = fetchURL(url)
        parseHtml(html)
        # Write2Csv(CommentList)
        if (i % 5 == 0):
            time.sleep(1)
    Write2Csv(CommentList, title)
    print('成功咯！\n')



