# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 08:54:21 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import gzip
import click
from cyvcf2 import VCF


@click.command()
@click.option('--invcf')
@click.option('--outfile', help='gziped file name (XX.gz)')
def main(invcf, outfile):
    with gzip.open(outfile, 'wb') as f:
        f.write('DP\tAD\tMQ0F\tMQ\n'.encode())
        for variant in VCF(invcf):
            ostr = '%s\t%s\t%s\t%s\n' % (variant.INFO.get('DP'), sum(variant.INFO.get('AD')),
                                         variant.INFO.get('MQ0F'), variant.INFO.get('MQ'))
            f.write(ostr.encode())


if __name__ == '__main__':
    main()
