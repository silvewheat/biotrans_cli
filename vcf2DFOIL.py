# -*- coding: utf-8 -*-
"""
Created on Aug 30th, 2022

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import typer
import numpy as np
from cyvcf2 import VCF
from collections import OrderedDict

def gts2comb(gts):
    comb = np.array(['A', 'A', 'A', 'A', 'A'])
    if gts[-1] == 0:
        comb[gts == 1] = 'B'
    elif gts[-1] == 1:
        comb[gts == 0] = 'B'
    else:
        print('Genotype Error!')
    return ''.join(comb)


def main(vcffile: str = typer.Argument(..., help="input vcf file (filtered, see --help)"),
         winsize: int = typer.Argument(100_000, help="window size"),
         outfile: str = typer.Argument(..., help="output DFOIL counts (see https://github.com/jbpease/dfoil)")):
    """
    \b
    从vcf文件中生成DFOIL的count文件。
    VCF需要按P1,P2,P3,P4,PO的顺序提取指定个体并进行过滤。
    bcftools view \\
      -a \\
      -r 29:1-100000 \\
      -s P1,P2,P3,P4,PO \\
      -O u \\
      in.vcf.gz | \\
    bcftools annotate \\
      -x 'INFO,^FMT/GT,^FMT/AD' \\
      -i 'N_MISSING=0 & N_ALT=1 & MAC>0' \\
      -O z \\
      -o out.vcf.gz
    """
    vcf = VCF(vcffile, strict_gt=True, gts012=True)
    samples = vcf.samples
    print(f'P1: {samples[0]}, P2: {samples[1]}, P3: {samples[2]}, P4: {samples[3]}, PO: {samples[4]}')
    
    combs = ['AAAAA', 'AAABA', 'AABAA', 'AABBA',
             'ABAAA', 'ABABA', 'ABBAA', 'ABBBA',
             'BAAAA', 'BAABA', 'BABAA', 'BABBA',
             'BBAAA', 'BBABA', 'BBBAA', 'BBBBA']
    with open(outfile, 'w') as f:
        f.write('#chrom\tposition\t')
        f.write('\t'.join(combs)+'\n')
        counts = OrderedDict(zip(combs, [0]*16))
        win_index = None
        chrom = None
        last_pos = 0
        for variant in vcf:
            offset = variant.start - last_pos - 1
            index = variant.end // winsize
            if (win_index != index) or (chrom != variant.CHROM):
                if chrom: # 不是开头
                    f.write(f'{chrom}\t{win_index}\t')
                    f.write('\t'.join([str(x) for x in counts.values()])+'\n')
                win_index = index
                chrom = variant.CHROM
                counts = OrderedDict(zip(combs, [0]*16))
            allele1 = np.array([x[0] for x in variant.genotypes])
            allele2 = np.array([x[1] for x in variant.genotypes])
            counts[gts2comb(allele1)] += 1
            counts[gts2comb(allele2)] += 1
            counts['AAAAA'] += (offset * 2) # 二倍体
            last_pos = variant.start
        f.write(f'{chrom}\t{win_index}\t')
        f.write('\t'.join([str(x) for x in counts.values()])+'\n')

if __name__ == '__main__':
    typer.run(main)