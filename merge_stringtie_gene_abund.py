# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 11:20:35 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import os
import click
import pandas as pd


def loadtable(file, smid):
    print(smid, file)
    df = pd.read_csv(file, sep='\t', usecols=['Gene ID', 'Gene Name', 'Reference', 'Strand', 'Start', 'End', 'FPKM'])
    df.columns = ['geneID', 'geneName', 'Reference', 'Strand', 'Start', 'End', smid]
    return df.set_index(['geneID', 'geneName', 'Reference', 'Strand', 'Start', 'End'])



@click.command()
@click.option('--filelist', help='gene_abund file list')
@click.option('--outfile', help='outfile (merged FPKM)')
def main(filelist, outfile):
    filelist = [x.strip() for x in open(filelist).readlines()]
    smids = [os.path.basename(x).split('.')[0] for x in filelist]
    dfs = []
    for smid, file in zip(smids, filelist):
        dfs.append(loadtable(file, smid))
    print('merge...')
    df = pd.concat(dfs, axis=1, join='outer')
# =============================================================================
#     # fill missed gene Name
#     df['geneName'] = df['geneName'].apply(lambda x: x.values[x.values == x.values][0], axis=1)
#     # remove duplicated col (geneName)
#     df.columns.duplicated()
# =============================================================================
    print('write...')
    df.reset_index().to_csv(outfile, sep='\t', index=False)


if __name__ == '__main__':
    main()


