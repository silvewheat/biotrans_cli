# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 22:49:17 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""


import gzip
import click
import random


@click.command()
@click.option('--invcf', help='输入的vcf.gz文件')
@click.option('--outvcf', help='输出的vcf.gz文件')
def main(invcf, outvcf):
    with gzip.open(invcf, 'rb') as f1, gzip.open(outvcf, 'wb') as f2:
        for line in f1:
            tline = line.decode()
            if tline[0] == '#':
                f2.write(line)
            else:
                tline = tline.strip().split()
                gts = [x.split(':')[0] for x in tline[9:]]
                newgts = []
                for gt in gts:
                    if gt == r'0/1' or gt == r'1/0':
                        if random.random() > 0.5:
                            newgts.append(r'1/1')
                        else:
                            newgts.append(r'0/0')
                    else:
                        newgts.append(gt)
                outline = tline[:9] + newgts
                outstring = '\t'.join(outline) + '\n'
                f2.write(outstring.encode())

if __name__ == '__main__':
    main()

