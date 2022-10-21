# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 21:41:46 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import sys
import gzip
import click
import numpy as np
import pandas as pd


def read_vcfheader(filename):
    allheaders = []
    if filename.split('.')[-1] == 'gz':
        gziped = True
        f = gzip.open(filename, 'rb')
    else:
        f = open(filename)
        gziped = False
    for line in f:
        if gziped:
            line = line.decode()
        allheaders.append(line)
        if line[:2] == '#C':
            header = line.strip().split('\t')
            return header, allheaders



def print_chunk(n):
    sys.stdout.write(' ' * 30 + '\r')
    sys.stdout.flush()
    sys.stdout.write(f'chunk {n}' + '\r')
    sys.stdout.flush()



@click.command()
@click.option('--infile', help='input xx.vcf(.gz) file')
@click.option('--samples', help='ancient samples list file, one sample per line')
@click.option('--maskstring', help='use this string to mask, default is ./.', default='./.')
@click.option('--chuncksize', help='一次处理XX行，默认10000', default=10000, type=int)
@click.option('--outfile', help='output masked vcf.gz file')
def main(infile, samples, maskstring, chuncksize, outfile):
    """
    ！！！注意：提取出来的vcf用bcftools提取课题时会有异常！！！
    """
    header, allheaders = read_vcfheader(infile)
    samples = [x.strip() for x in open(samples).readlines()]
    with gzip.open(outfile, 'wb') as f:
        oheader = ''.join(allheaders)
        f.write(oheader.encode())
    nuc2code = {'A': 0,
                'C': 1,
                'G': 2,
                'T': 3}
    reader = pd.read_csv(infile, sep='\t', comment='#', header=None, names=header, iterator=True)
    loop = True
    nchunk = 0
    while loop:
        nchunk += 1
        print_chunk(nchunk)
        try:
            chunk = reader.get_chunk(chuncksize)
            ref = chunk['REF'].map(nuc2code).values
            alt = chunk['ALT'].map(nuc2code).values
            chunk.loc[np.fabs(ref - alt) == 2, samples] = maskstring
            chunk.to_csv(outfile, sep='\t', index=False, header=False, compression='gzip', mode='ab')
        except StopIteration:
            loop = False
            print('Done!')


if __name__ == '__main__':
    main()

