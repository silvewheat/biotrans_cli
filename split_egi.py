# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 11:41:41 2018

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click


@click.command()
@click.option('--inprefix')
@click.option('--outprefix')
@click.option('--winsize', type=int)
def main(inprefix, outprefix, winsize):
    with open(f'{inprefix}.snp') as f1, \
         open(f'{inprefix}.geno') as f2, \
         open(f'{outprefix}.regionidx', 'w') as f_region:
        idx = -1
        f3 = open(f'{outprefix}.{idx}.snp', 'w')
        f4 = open(f'{outprefix}.{idx}.geno', 'w')
        for line1 in f1:
            tline = line1.strip().split()
            chrom = tline[1]
            pos = int(tline[3])
            nbin = pos // winsize
            if nbin != idx:
                print(f'{chrom}\t{idx * (winsize)+1}\t{(idx+1) * winsize}\t{idx}\n')
                f_region.write(f'{chrom}\t{idx * (winsize)+1}\t{(idx+1) * winsize}\t{idx}\n')
                f3.close()
                f4.close()
                idx = nbin
                f3 = open(f'{outprefix}.{chrom}.{idx}.snp', 'w')
                f4 = open(f'{outprefix}.{chrom}.{idx}.geno', 'w')
            f3.write(line1)
            line2 = f2.readline()
            f4.write(line2)

        f3.close()
        f4.close()


if __name__ == '__main__':
    main()

