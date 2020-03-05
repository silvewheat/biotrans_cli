# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:23:04 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""


import gzip
import click


def repalce(line, pos):
    tline = line.split('\t')
    tline[1] = pos.strip()
    tline[7] = '.'
    return '\t'.join(tline)


@click.command()
@click.option('--invcf', help='输出的vcf.gz文件')
@click.option('--poslist', help='将输出的vcf中的pos按顺序替换为这个文件中的pos, 不提供这参数的话则从1开始顺序编码', default=None)
@click.option('--outvcf', help='输出的vcf.gz文件')
def main(invcf, poslist, outvcf):
    flag = True
    if poslist:
        with gzip.open(invcf, 'rb') as f1, open(poslist) as f2, gzip.open(outvcf, 'wb') as f3:
            while flag:
                line = f1.readline().decode()
                if line[0] == '#':
                    f3.write(line.encode())
                else:
                    flag = False
                    pos = f2.readline().strip()
                    outstring = repalce(line, pos)
                    f3.write(outstring.encode())

            for line, pos in zip(f1, f2):
                outstring = repalce(line.decode(), pos)
                f3.write(outstring.encode())
    else:
        pos = 1
        with gzip.open(invcf, 'rb') as f1, gzip.open(outvcf, 'wb') as f3:
            while flag:
                line = f1.readline().decode()
                if line[0] == '#':
                    f3.write(line.encode())
                else:
                    flag = False
                    outstring = repalce(line, str(pos))
                    f3.write(outstring.encode())

            for line in f1:
                pos += 1
                outstring = repalce(line.decode(), str(pos))
                f3.write(outstring.encode())

if __name__ == '__main__':
    main()
