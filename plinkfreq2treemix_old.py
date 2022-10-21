# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 09:32:17 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click
import numpy as np
import pandas as pd


@click.command()
@click.option('--infile', help='plink --freq output file (.frq.strat(.gz))')
@click.option('--outfile', help='treemix.frq.gz')
def main(infile, outfile):
    """
    convert plink freq file to treemix input file
    plink --bfile chrAuto --chr-set 29 --chr 1-29 --freq --missing --double-id --out popfreq --within Pop.cluster
    """
    df = pd.read_csv(infile, sep='\s+', usecols=['SNP', 'CLST', 'MAC', 'NCHROBS'],
                     dtype={'SNP': str,
                            'CLST': str,
                            'MAC': np.int16,
                            'NCHROBS': np.int16})
    print('plink file loaded')
    print(df.info())
    df['count2'] = df['NCHROBS'].values - df['MAC'].values
    print('allele2 counted')
    print(df.info())
    del(df['NCHROBS'])
    df['treemix'] = df['MAC'].astype(str) + ',' + df['count2'].astype(str)
    del(df['MAC'])
    del(df['count2'])
    print('treemix counted')
    print(df.info())
    df.pivot_table(index='SNP', columns='CLST', values='treemix', aggfunc=lambda x: x)\
      .to_csv(outfile, index=False, sep=' ', compression='gzip')


if __name__ == '__main__':
    main()
