# version: python 3.6

from bs4 import BeautifulSoup
import requests, re
import pandas as pd
import datetime

def str2date(str, date_format="%Y-%m-%d"):
    date = datetime.datetime.strptime(str, date_format)
    return date


def date2str(date, date_formate="%Y-%m-%d"):
    s = date.strftime(date_formate)
    return s

def format_date(d):
    # 格式化日期为%YYYY-%mm-%dd
    year = "2020"
    month = d.strip().split("月")[0].strip()
    day = d.strip().split("月")[1].split("日")[0].strip()
    d = year+ "-" + month + "-" + day
    d = str2date(d)
    d = date2str(d)
    return d

def get_values(v):
    # 一些格子中是"15152①"这样的内容，只要前面的数值
    r = re.match(r'\d+', v)
    if r is not None:
        return r.group(0)



def first_three_months():
    result = [] # 用来存储结果 {日期, 累计确诊，累计死亡，新增确诊}
    url = "https://www.gswycjc.com/article/show.asp?id=2580"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.table
    trs = table.find_all('tr')
    # 前两行和最后两行不是需要的
    for i in range(2, len(trs) - 2):
        tr = trs[i]
        tds = tr.find_all('td')
        # 第一列是日期， 第二列是累计确诊，第三列是累计死亡，第四列是新增确诊
        date = tds[0].text
        date = format_date(date)
        ljqz = int(get_values(tds[1].text))
        ljsw = int(get_values(tds[2].text))
        xzqz = int(get_values(tds[3].text))
        result.append({
            "date": date,
            "ljqz": ljqz,
            "ljsw": ljsw,
            "xzqz": xzqz
        })
    return result


def fourth_month():
    # 爬取第四月的数据
    result = [] # 用来存储结果 {日期, 累计确诊，累计死亡，新增确诊}
    url = "https://www.gswycjc.com/article/show.asp?id=2711"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.table
    trs = table.find_all('tr')
    # 只要第2到第31行
    for i in range(1, 31):
        tr = trs[i]
        tds = tr.find_all('td')
        # 第一列是日期， 第二列是新增确诊，第三列是累计确诊，第七列是累计死亡
        date = tds[0].text
        date = format_date(date)
        xzqz = int(get_values(tds[1].text))
        ljqz = int(get_values(tds[2].text))
        ljsw = int(get_values(tds[6].text))
        result.append({
            "date": date,
            "ljqz": ljqz,
            "ljsw": ljsw,
            "xzqz": xzqz
        })
    return result


def fifth_month():
    # 爬取第五月的数据
    result = [] # 用来存储结果 {日期, 累计确诊，累计死亡，新增确诊}
    url = "https://www.gswycjc.com/article/show.asp?id=2727"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.table
    trs = table.find_all('tr')
    # 只要第2到第26行
    for i in range(1, 26):
        tr = trs[i]
        tds = tr.find_all('td')
        # 第一列是日期， 第二列是新增确诊，第六列是累计确诊，第九列是累计死亡
        date = tds[0].text
        date = format_date(date)
        xzqz = int(get_values(tds[1].text))
        ljqz = int(get_values(tds[5].text))
        ljsw = int(get_values(tds[8].text))
        result.append({
            "date": date,
            "ljqz": ljqz,
            "ljsw": ljsw,
            "xzqz": xzqz
        })
    return result


if __name__ == "__main__":
    r1_3 = first_three_months()
    r4 = fourth_month()
    r5 = fifth_month()

    # 综合结果
    r = r1_3
    r.extend(r4)
    r.extend(r5)

    # 将结果保存到csv文件中
    filename = "corona_data.csv"
    pd.DataFrame(r).to_csv(filename, encoding='utf-8',index=False)
    print("finish")