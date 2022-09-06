# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 22:05:06 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click
import pandas as pd


@click.command()
@click.option('--infile')
@click.option('--sample1')
@click.option('--sample2')
@click.option('--outfile')
@click.option('--noheader', is_flag=True, default=False, help='加了不输出header')
def main(infile, sample1, sample2, outfile, noheader):
    """parse realSFS的结果"""
    df = pd.read_csv(infile, sep='\s+', header=None,
                     names=['A', 'D', 'G', 'B', 'E', 'H', 'C', 'F', 'I', 'drop'])
    del(df['drop'])
    df['nSites'] = int(df.sum(axis=1)[0])

    df['HETHET'] = df['E']
    df['IBS0'] = df['C'] + df['G']
    df['IBS1'] = df['B'] + df['D'] + df['F'] + df['H']
    df['IBS2'] = df['A'] + df['E'] + df['I']
    df['fracIBS0'] = df['IBS0'] / df['nSites']
    df['fracIBS1'] = df['IBS1'] / df['nSites']
    df['fracIBS2'] = df['IBS2'] / df['nSites']
    df['fracHETHET'] = df['E'] / df['nSites']

    # the derived stats
    df['R0'] = df['IBS0'] / df['HETHET']
    df['R1'] = df['HETHET'] / (df['IBS0'] + df['IBS1'])
    # KING-robust kinship
    df['Kin'] = (df['HETHET'] - 2*(df['IBS0'])) / (df['IBS1'] + 2*df['HETHET'])
    df['Fst'] = (2*df['IBS0'] - df['HETHET']) / \
        (2*df['IBS0'] + df['IBS1'] + df['HETHET'])
    df['sample1'] = sample1
    df['sample2'] = sample2
    df[['sample1', 'sample2', 'nSites', 'Kin', 'R0', 'R1']].to_csv(
        outfile, sep='\t', index=False, header=bool(1-noheader))


if __name__ == '__main__':
    main()
