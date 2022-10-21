# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 15:32:33 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import gzip
import click



@click.command()
@click.option('--beaglefile', help='gzipped beagle file')
@click.option('--region', help='chr:start-end')
@click.option('--outfile', help='gzipped')
def main(beaglefile, region, outfile):
    """
    beagle文件的第一列marker必须是chr_pos这种形式
    """
    chrom = region.split(':')[0]
    start, end = region.split(':')[1].split('-')
    start = int(start)
    end = int(end)
    with gzip.open(beaglefile, 'rb') as f1, gzip.open(outfile, 'wb') as f2:
        header = f1.readline()
        f2.write(header)
        len_chrom = len(chrom)
        for line in f1:
            if line.decode()[:len_chrom] == chrom:
                marker = line.decode().split()[0]
                scaffold, pos = marker.split('_')
                if scaffold == chrom:
                    if start <= int(pos) <= end:
                        print(marker)
                        f2.write(line)


if __name__ == '__main__':
    main()
