# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 22:04:54 2018

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import gzip
import click


@click.command()
@click.argument('infreq')
@click.argument('nmiss')
@click.argument('outfile')
@click.option('--vcffile', help='对应的vcf文件，位点一定要一一对应', default=None)
@click.option('--outsites', help='输出保留下来的位点信息，用--vcf则需要加这个', default=None)
def main(infreq, nmiss, outfile, vcffile, outsites):
    """
    输出0,0数量小于等于nmiss的位点
    """
    nmiss = int(nmiss)
    print(f'nmiss <= {nmiss}')
    if vcffile:
        import pysam
        var = pysam.VariantFile(vcffile)
        with gzip.open(infreq, 'rb') as f1, \
             gzip.open(outfile, 'wb') as f2, \
             gzip.open(outsites, 'wb') as f3:
            for line, record in zip(f1, var):
                tline = line.decode().strip().split()
                if tline.count('0,0') <= nmiss:
                    f2.write(line)
                    chrom = record.chrom
                    pos = record.pos
                    outloc = f'{chrom}_{pos}\n'
                    f3.write(outloc.encode())
    else:
        with gzip.open(infreq, 'rb') as f1, \
             gzip.open(outfile, 'wb') as f2:
            for line in f1, var:
                tline = line.decode().strip().split()
                if tline.count('0,0') <= nmiss:
                    f2.write(line)


if __name__ == '__main__':
    main()
