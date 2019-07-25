# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 14:32:37 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click
import gzip
import numpy as np
import pandas as pd


def loadsamples(infile):
    with gzip.open(infile, 'rb') as f:
        samples = []
        for line in f:
            tline = line.decode().strip().split()
            sample = tline[2]
            if sample not in samples:
                samples.append(sample)
            else:
                break
    nsamples = len(samples)
    print(f'nsamples: {nsamples}')
    return samples, nsamples


def reform(df):
    df['count2'] = df['NCHROBS'].values - df['MAC'].values
    df['treemix'] = df['MAC'].astype(str) + ',' + df['count2'].astype(str)
    return df.pivot_table(index='SNP', columns='CLST', values='treemix', aggfunc=lambda x: x)



@click.command()
@click.option('--infile', help='plink --freq output file (.frq.strat(.gz))')
@click.option('--chuncksize', help='how many snp per loop, default=100000000', type=int, default=100000000)
@click.option('--outfile', help='treemix.frq.gz')
def main(infile, chuncksize, outfile):
    """
    convert plink freq file to treemix input file
    plink --bfile chrAuto --chr-set 29 --chr 1-29 --freq --missing --double-id --out popfreq --within Pop.cluster
    """
    reader = pd.read_csv(infile, sep='\s+', iterator=True, usecols=['SNP', 'CLST', 'MAC', 'NCHROBS'],
                         dtype={'SNP': str,
                                'CLST': str,
                                'MAC': np.int16,
                                'NCHROBS': np.int16})
    # 第一次读，输出有header
    odf = reform(reader.get_chunk(chuncksize))
    odf.to_csv(outfile, index=False, sep=' ', compression='gzip')
    # 后面的不输出header
    loop = True
    while loop:
        try:
            odf = reform(reader.get_chunk(chuncksize))
            odf.to_csv(outfile, index=False, sep=' ', header=False, compression='gzip', mode='ab')
        except StopIteration:
            loop = False
            print('Done!')


if __name__ == '__main__':
    main()
