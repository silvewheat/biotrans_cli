# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:00:32 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import os
import gzip
import click



@click.command()
@click.option('--inbeagle')
@click.option('--outprefix')
def main(inbeagle, outprefix):
    with gzip.open(inbeagle, 'rb') as f:
        header = f.readline().decode().strip().split()
        nsample = int((len(header) / 3) - 1)
        for i, name in zip(range(1, nsample+1), header[4::3]):
            a = i + 3
            b = a + 1
            c = b + 1
            cmd = """zcat %s | awk '{print $1"\t"$2"\t"$3"\t"$%s"\t"$%s"\t"$%s}' | gzip -c > %s_%s.beagle.gz""" % (inbeagle, a, b, c, outprefix, name)
            print(f'{i}/{nsample}')
            os.system(cmd)


if __name__ == '__main__':
    main()
