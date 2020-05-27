# version: python 3.6

from bs4 import BeautifulSoup
import requests, re
import pandas as pd
import datetime

date_range = ["2020-01-21", "2020-05-25"]

def in_date_range(d):
    # 判断数据是否在我们需要的日期范围之内
    if d >= date_range[0] and d <= date_range[1]:
        return True
    else:
        return False

def str2date(str, date_format="%Y%m%d"):
    date = datetime.datetime.strptime(str, date_format)
    return date


def date2str(date, date_formate="%Y-%m-%d"):
    s = date.strftime(date_formate)
    return s

def format_date(d):
    # 格式化日期为%Y-%m-%d
    d = str2date(d)
    d = date2str(d)
    return d

def format_float(f):
    # 格式化浮点类型数据
    f = f.strip().replace(",", "")
    return float(f)

def which_season(season=1):
    result = []
    # 爬取对应季度的数据
    url = "https://quotes.money.163.com/trade/lsjysj_zhishu_399300.html?year=2020&season=" + str(season)
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    div = soup.find('div', attrs={"class": "inner_box"})
    table = div.table
    trs = table.find_all('tr')
    # 需要第2行到最后一行 （数据是倒序的，所以反向遍历）
    for i in range(len(trs) - 1, 0, -1):
        tr = trs[i]
        tds = tr.find_all('td')
        '''
            第一列是日期，第二列是开盘价，第三列是最高价，第四列是最低价，
            第五列是收盘价，第六列是涨跌额，第七列是涨跌幅，第八列是成交量，第九列是成交金额
        '''
        date = format_date(tds[0].text)
        if in_date_range(date) == False:
            continue # 不需要该数据
        kpj = format_float(tds[1].text)
        zgj = format_float(tds[2].text)
        zdj = format_float(tds[3].text)
        spj = format_float(tds[4].text)
        zde = format_float(tds[5].text)
        zdf = format_float(tds[6].text)
        cjl = format_float(tds[7].text)
        cjje = format_float(tds[8].text)

        result.append({
            "date": date,
            "kpj": kpj,
            "zgj": zgj,
            "zdj": zdj,
            "spj": spj,
            "zde": zde,
            "zdf": zdf,
            "cjl": cjl,
            "cjje": cjje
        })
    return result

if __name__ == "__main__":
    # 爬取第一季度
    s1 = which_season(season=1)
    # 爬取第二季度
    s2 = which_season(season=2)

    # 合并结果
    r = s1
    r.extend(s2)

    # 将结果保存到csv文件中
    filename = "economy.csv"
    pd.DataFrame(r).to_csv(filename, encoding='utf-8',index=False)

    print("finish")