# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 10:15:42 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""


import os
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
import allel
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from itertools import cycle
from pathlib import Path


def sites2regions(df):
    """
    df 是直接sprime的.score输出文件转成的dataframe
    """
    mdf = []
    for i in range(df['SEGMENT'].max()+1):
        tdf = df.loc[df['SEGMENT']==i, :]
        chrom = tdf['CHROM'].min()
        start = tdf['POS'].min()
        end = tdf['POS'].max()
        length = end - start + 1
        score = tdf['SCORE'].max()
        n_snps = tdf.shape[0]
        mdf.append([chrom, start, end, length, i, score, n_snps])
    mdf = pd.DataFrame(mdf, columns=['chrom', 'start', 'end', 'length', 'segment_index', 'score', 'n_snps'])
    return mdf

@click.group()
def main():
    """处理sprime的输出结果"""


@main.command('merge')
@click.option('--scorefile', help='sprime的后缀为.score的输出文件')
@click.option('--outdir', help='输出文件目录（空目录或未创建的目录）')
def merge(scorefile, outdir):
    """合并.score为区域，并进行基本统计"""
    sdf = pd.read_csv('chrAuto.score', sep='\t')
    
    # 合并位点为区域
    mdf = sites2regions(sdf)
    outdir = Path(outdir)
    outfile = outdir / 'sprime_regions.tsv.gz'
    mdf.to_csv(outfile, sep='\t', index=False, compression='gzip')
    
    # 区域分数分布情况
    outfile = outdir / 'sprime_regions_stat.tsv.gz'
    mdf[['length', 'n_snps', 'score']].describe().reset_index().to_csv(outfile, sep='\t', float_format='%.0f', index=False)
    
    # 区域分数分布图
    outfile = outdir / 'sprime_regions_pairplot.jpg'
    g = sns.pairplot(sdf[['length', 'n_snps', 'score']], diag_kind="kde")
    g.map_lower(sns.kdeplot, levels=4, color=".2")
    g.savefig(outfile, dpi=300)



@main.command('plotregions')
@click.option('--scorefile', help='sprime的后缀为.score的输出文件')
@click.option('--regionfile', help='merge产生的sprime_region.tsv.gz')
@click.option('--outdir', help='输出存放图片的目录（空目录或未创建的目录）')
def merge(scorefile, outdir):
    """合并.score为区域，并进行基本统计"""
    sdf = pd.read_csv('chrAuto.score', sep='\t')
 





if __name__ == '__main__':
    main()

    