# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 16:23:12 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click
import numpy as np
import pandas as pd



@click.command()
@click.option('--frqstrat', help='outfile(.frq.strat) from plink --freq')
@click.option('--outprefix', help='output file prefix')
def main(frqstrat, outprefix):
    """
    --freqstrat file produced by plink --freq when used with --within/--family
    https://www.cog-genomics.org/plink2/formats#frq_cc
    """
    df = pd.read_csv(frqstrat, sep='\s+')
    df1 = df.pivot_table(columns=['CLST'], index='SNP', values='MAF')
    df2 = df.pivot_table(columns=['CLST'], index='SNP', values='NCHROBS')
    # 没allele的频率设为NAN
    df1[df2 == 0] = np.nan
    df1.to_csv(f'{outprefix}.freq.csv.gz', compression='gzip')
    df1.to_csv(f'{outprefix}.alleCount.csv.gz', compression='gzip')


if __name__ == '__main__':
    main()
