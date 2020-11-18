# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 17:15:15 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click
import numpy as np
import pandas as pd


@click.command()
@click.option('--matrix', help='输入的矩阵文件')
@click.option('--posfile', help='两列，染色体 pos')
@click.option('--samples', help='样本ID，一个一行')
@click.option('--outprefix', help='输出文件前缀')
def main(matrix, posfile, samples, outprefix):
    """
    """
    samples = [x.strip() for x in open(samples)]
    hapIDs = [[f'{i}_1', f'{i}_2'] for i in samples]
    hapIDs = [i for j in hapIDs for i in j]
    pdf = pd.read_csv(posfile, sep='\s+', header=None, names=['chr', 'pos'])
    if matrix[-4:] == '.npy':
        df=pd.DataFrame(np.load(matrix).T, dtype=np.int8)
    else:
        df = pd.read_csv(matrix, sep='\s+', header=None, dtype=np.int8).T
    df.columns = hapIDs
    chroms = pdf['chr'].unique()
    assert len(chroms) == 1
    chrom = chroms[0]
    del(chroms)
    df['chr'] = chrom
    df['pos'] = pdf['pos']
    cols = ['chr', 'pos'] + hapIDs
    df[cols].to_csv(f'{outprefix}_perSite.tsv.gz', sep='\t', index=False, compression='gzip')
    del(pdf)

    # merge the consecutive rows with same values
    print('merge introgressed segments in pop level')
    cumindex = (df[hapIDs] != df[hapIDs].shift()).apply(max, axis=1).cumsum()
    fundict = {'pos': [min, max]}
    fundict.update(dict(zip(hapIDs, [max]*len(hapIDs)))) # same for 'max' and 'min'
    mdf1 = df.groupby(cumindex).agg(fundict)
    mdf1.columns = ['start', 'end'] + hapIDs
    mdf1['chr'] = chrom
    cols = ['chr', 'start', 'end'] + hapIDs
    mdf1[cols].to_csv(f'{outprefix}_popSeg.tsv.gz', sep='\t', index=False, compression='gzip')
    del(mdf1)

    # merge the consecutive rows for each indiv
    print('merge introgressed segments in indiv level')
    df = df.melt(id_vars=['chr', 'pos'], value_vars=hapIDs,
                 var_name='hapID', value_name='sourceID')
    cumindex = (df[['hapID', 'sourceID']] != df[['hapID', 'sourceID']].shift()).apply(max, axis=1).cumsum()
    fundict = {'chr': max, 'pos': [min, max], 'hapID': max, 'sourceID': max}
    mdf2 = df.groupby(cumindex).agg(fundict)
    mdf2.columns = ['chr', 'start', 'end', 'hapID', 'sourceID']
    mdf2.to_csv(f'{outprefix}_indSeg.tsv.gz', sep='\t', index=False, compression='gzip')
    print('Done!')


if __name__ == '__main__':
    main()
