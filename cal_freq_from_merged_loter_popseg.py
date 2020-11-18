# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 16:16:01 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""
import click
import numpy as np
import pandas as pd


@click.command()
@click.option('--infile', help='用merge_loter_result得出的popseg文件')
@click.option('--outfile')
@click.option('--sourceindex', help='popseg中的哪个source', type=int)
def main(infile, outfile, sourceindex):
    df = pd.read_csv(infile, sep='\t')
    haps = df.columns[3:]
    n_haps = len(haps)
    df['freq'] = df[haps].apply(lambda x: np.sum((x==sourceindex)) / n_haps, axis=1)
    df['length'] = df['end'] - df['start'] + 1
    df[['chr', 'start', 'end', 'length', 'freq']].to_csv(outfile, sep='\t', index=False)

if __name__ == '__main__':
    main()

