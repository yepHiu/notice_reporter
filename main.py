import re
from bs4 import BeautifulSoup
import requests
import prettytable as pt



def request_url():
    url="https://www1.szu.edu.cn/board/infolist.asp"
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    html=requests.get(url,user_agent)
    html.encoding='gbk'
    return html.text

def notice_filter(text):
    soup=BeautifulSoup(text,'html.parser')

    _category=soup.find_all('a', href=re.compile('\?infotype'), title='')
    _category=[c.text for c in _category]

    _organization = soup.find_all('a', href='#')
    _organization = [c.text for c in _organization]

    _title=soup.find_all('td', align='left')
    _title = [c.text for c in _title]

    _time=soup.find_all('td', style="font-size: 9pt", align="center")
    _time = [c.text for c in _time if '-' in c.text]

    buffer=[]

    for i in  range(len(_title)):
        category=_category[i]
        title=_title[i]
        time=_time[i]
        organization=_organization[i+1]

        data={
            'category':category,
            'organization':organization,
            'title':title,
            'time':time
        }

        buffer.append(data)
    return buffer

def print_screen(data:list):
    table=pt.PrettyTable(['分类','部门','标题','时间'])
    for i in data:
        table.add_row([i['category'],i['organization'],i['title'],i['time']])
    print(table)

def main():
    print_screen(notice_filter(request_url()))

if __name__=='__main__':
    main()

