# version: python 3.6
# corona的数据与economy的数据不完全一一对应，需要进行数据预处理
# 原因是股票并不是每天都开盘

import pandas as pd

if __name__ == "__main__":
    corona_file = "corona_data.csv"
    corona_pd = pd.read_csv(corona_file)

    economy_file = "economy.csv"
    economy_pd = pd.read_csv(economy_file)

    # 找到所有economy中包含的日期
    date_list = list(economy_pd.loc[:,"date"])

    # 对于未开盘的中间几天，把corona的新增数据进行调整
    # 调整xzqz（新增确诊），增加xzsw（新增死亡）
    new_corona = []
    last_ljqz = None
    last_ljsw = None
    for index, row in corona_pd.iterrows():
        date = row["date"]
        ljqz = row["ljqz"]
        ljsw = row["ljsw"]
        if date not in date_list:
            continue
        else:
            if last_ljqz is None:
                last_ljqz = ljqz
                last_ljsw = ljsw
            else:
                xzqz = ljqz - last_ljqz
                xzsw = ljsw - last_ljsw

                last_ljqz = ljqz
                last_ljsw = ljsw

                # 获取当天的economy数据
                economy_dict = economy_pd[economy_pd['date'].isin([date])].to_dict()
                new_corona.append({
                    "date": date,
                    "ljqz": ljqz,
                    "ljsw": ljsw,
                    "xzqz": xzqz,
                    "xzsw": xzsw,
                    "kpj": list(economy_dict["kpj"].values())[0],
                    "zgj": list(economy_dict["zgj"].values())[0],
                    "zdj": list(economy_dict["zdj"].values())[0],
                    "spj": list(economy_dict["spj"].values())[0],
                    "zde": list(economy_dict["zde"].values())[0],
                    "zdf": list(economy_dict["zdf"].values())[0],
                    "cjl": list(economy_dict["cjl"].values())[0],
                    "cjje": list(economy_dict["cjje"].values())[0],
                })

    # 插入预处理后的数据
    filename = "corona_economy_preprocess.csv"
    pd.DataFrame(new_corona).to_csv(filename, encoding='utf-8', index=False)
    print("finish")