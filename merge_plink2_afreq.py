# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 22:07:06 2021

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import os
import typer
import numpy as np
import pandas as pd



def main(filelist: str = typer.Argument(..., help="afreq文件列表，文件后缀为.afreq或.afreq.gz"),
         outfile: str = typer.Argument(..., help="输出文件名")):
    """
    \b
    合并plink2 --freq 产生的来自不同分组的afreq文件
    filelist中为文件列表
    https://www.cog-genomics.org/plink/2.0/basic_stats#freq
    https://www.cog-genomics.org/plink/2.0/formats#afreq
    """
    files = [x.strip() for x in open(filelist)]
    basenames = [os.path.basename(x) for x in files]
    groups = [x[:-6] if x.endswith('.afreq') else x[:-9] for x in basenames] # 文件名后缀为.afreq或.afreq.gz
    # siteinfo
    dfs = []
    dfs.append(pd.read_csv(files[0], sep='\t',
                           usecols=['#CHROM', 'ID', 'REF', 'ALT'],
                           dtype={'#CHROM': 'category', 'ID': str, 'REF': str, 'ALT': str}))
    # merge
    for file, group in zip(files, groups):
        dfs.append(pd.read_csv(file, sep='\t', header=None, skiprows=1,
                               names=['#CHROM', 'ID', 'REF', 'ALT', f'{group}_ALT_FREQS', f'{group}_OBS_CT'],
                               usecols=[f'{group}_ALT_FREQS', f'{group}_OBS_CT'],
                               dtype={f'{group}_ALT_FREQS': float, f'{group}_OBS_CT': int}))
    df = pd.concat(dfs, axis=1)
    assert len(np.unique([df.shape[0] for df in dfs])) == 1, '输入文件的行数不一致'
    df.to_csv(outfile, sep='\t', index=False)

if __name__ == '__main__':
    typer.run(main)
