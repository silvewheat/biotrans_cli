# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:56:49 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import gzip
import time
import click
import random


def shuffle(chunks):
    index = list(range(len(chunks)))
    random.shuffle(index)
    for i in index:
        yield chunks[i]

def writechunk(chunks, outfile):
    print('shuffling and writing')
    with gzip.open(outfile, 'ab') as f2:
        for chunk in shuffle(chunks):
            if chunk:
                f2.write(''.join(chunk).encode())


@click.command()
@click.option('--vcffile', help='gziped vcffile')
@click.option('--seed', type=int, default=None)
@click.option('--chunk-size', type=int, help='size of bootstrap chunks [5000000]', default=5000000)
@click.option('--outfile', help='output gziped vcffile')
def main(vcffile, seed, chunk_size, outfile):
    """
    plink在读入vcf时会自动按pos排序，要是后续用于plink的话，得把vcf的pos列改一下
    """
    if not seed:
        seed = int(time.time())
    random.seed(seed)
    print(f'random seed: {seed}')
    chunks = []
    # 写header，确认初始染色体号及指针位置
    with gzip.open(vcffile, 'rb') as f1, gzip.open(outfile, 'wb') as f2:
        flag = True
        while flag:
            line = f1.readline().decode()
            if line[0] == '#':
                f2.write(line.encode())
            else:
                last_chrom = line.split()[0]
                stream_pos = f1.tell()
                flag = False
    print('header writed')
    print(f'chromsome: {last_chrom}')

    with gzip.open(vcffile, 'rb') as f1:
        f1.seek(stream_pos)
        for line in f1:
            chrom, pos = line.decode().split()[:2]
            chunk_index = (int(pos) - 1) // chunk_size
            if chrom == last_chrom:
                while chunk_index > len(chunks)-1: # 用while循环避免连续多个空chunk（chunksize过小）
                    chunks.append([])
                chunks[chunk_index].append(line.decode())
            else:
                writechunk(chunks, outfile)
                print(f'chromsome: {chrom}')
                chunks = []
                while chunk_index > len(chunks)-1:
                    chunks.append([])
                chunks[chunk_index].append(line.decode())
            last_chrom = chrom
        else:
            writechunk(chunks, outfile)


if __name__ == '__main__':
    main()