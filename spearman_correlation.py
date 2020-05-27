# version: python 3.6
# calculate the spearman correlation of each pair of variable

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

if __name__ == "__main__":
    data_file = "corona_economy_preprocess.csv"
    data = pd.read_csv(data_file)

    # 计算spearman相关系数
    spearman_result = data.corr('spearman')

    # 绘制热力图
    f, ax = plt.subplots(figsize=(9, 6))  # 定义一个子图宽高为9和6 ax存储的是图形放在哪个位置
    ax = sns.heatmap(spearman_result, square=True, annot=True, linecolor='white', cmap="coolwarm",
                     linewidths=0.1,vmax=1.0, fmt='.2g')
    ax.set_title("spearman correlation heatmap")
    f.savefig('spearman_heatmap.png', bbox_inches='tight')

    print("finish")