# corona_economy
## 1. 开发环境: 
```
ide: pycharm 
python version: 3.6.10
```

## 2. 安装&运行:
```
pip install -r requirements.txt # 安装python所需依赖包
python crawler_corona.py # 运行爬虫，爬取新冠病毒相关数据
python crawler_economy.py # 运行爬虫，爬取沪深300相关数据
python pre_processing.py # 运行数据清洗脚本，对数据进行预处理和对齐
python spearman_correlation.py # 运行spearman相关系数计算脚本，并以热力图形式展示
```

## 3. 生成文件说明:
```
corona_data.csv: 新冠病毒爬虫所得相关信息，包含4列（date：日期；ljqz：累计确诊；ljsw：累计死亡；xzqz：新增确诊）
economy.csv: 沪深300爬虫所得相关信息，包含9列（date：日期；kpj：开盘价；zgj：最高价；zdj：最低价；spj：收盘价；zde：涨跌额；zdf：涨跌幅；cjl：成交量；cjje：成交金额）
corona_economy_preprocess.csv: 两份数据的综合结果，包含14列，新增了1列（xzsw：新增死亡）
spearman_heatmap.png: spearman相关系数热力图
```