# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:29:02 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import os
import click
import numpy as np
import pandas as pd
from cyvcf2 import VCF



@click.command()
@click.option('--vcffile', help='input genotype file')
@click.option('--querylist', help='最终输出这些个体(文本文件, 一行一个个体)')
@click.option('--outfile', help='输出Treemix的输入文件')
def main(vcffile, querylist, outfile):
    """
    把vcf文件转为treemix的输入文件，不进行群体合并，每个个体都是分开的
    ！！！！！！这个脚本还没写完呢！！！！！！
    """
    querysamples = [x.strip() for x in open(querylist)]
    vcf_query = VCF(vcffile, gts012=True, samples=querysamples)
    if len(querysamples) > len(vcf_query.samples):
        miss = set(querysamples) - set(vcf_query.samples)
        print(f'query sample miss: {miss}')
        for ind in miss:
            querysamples.remove(ind)
    df = []
    index = []
    for variant_query in vcf_query(region):
        arr = variant_query.gt_types  # 0=HOM_REF, 1=HET, 2=HOM_ALT, 3=UNKNOWN
        df.append(arr.tolist())
        index.append(variant_query.POS)

    df = pd.DataFrame(df, columns=vcf_query.samples, index=index)
    df = df[querysamples] # 排序
    df = df.replace(3, np.nan) # 自动 int to float
    print(f'{os.path.basename(vcffile)} {region}:\n{df.shape}')

    # 改名
    id2groups = loadgroup(groupfile)
    df.columns = [f'{id2groups[x]}_{x}' for x in df.columns]

    # MAF筛选
    freqs = df.sum(axis=1).values / (df.count(axis=1).values * 2)
    df = df.loc[((1-maf)>=freqs)&(freqs>=maf), :]
    print(f'filter maf({maf}):\n{df.shape}')

    # 画图
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.set_facecolor("grey")
    sns.heatmap(df.T, yticklabels=1, cmap='OrRd', ax=ax)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(ticklabelsize)
    plt.savefig(outfile, dpi=dpi)
    plt.close()


if __name__ == '__main__':
    main()


