# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 10:53:56 2021

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import typer
import allel
import pandas as pd
from collections import defaultdict



def load_group(groupfile):
    group2samples = defaultdict(list)
    with open(groupfile) as f:
        for line in f:
            sample, group = line.strip().split()
            group2samples[group].append(sample)
    return group2samples


def main(vcffile: str = typer.Argument(..., help="总vcf文件"),
         groupfile: str = typer.Argument(..., help='样本分群信息，两列，一列vcf中的样本ID，一列对应的群体ID。不需要包含vcf中的全部个体。'),
         outfile: str = typer.Argument(..., help='输出文件名(.ac.tsv.gz)'),
         region: str = typer.Option(None, help='只使用指定区域chrom:start-end或者chrom')):
    """把vcf文件转换为treemix的输入格式，可以只转指定区域指定样本"""
    group2samples = load_group(groupfile)
    df = {}
    for group, samples in group2samples.items():
        callset = allel.read_vcf(vcffile, fields=['calldata/GT', 'samples'], numbers={'ALT': 1}, region=region)
        samples_missed = set(samples) - set(callset['samples'])
        if samples_missed:
            print(f'{len(samples_missed)} / {len(samples)} samples missed in {group}:')
            print(','.join(samples_missed))
        df[group] = pd.DataFrame(allel.GenotypeArray(callset['calldata/GT']).count_alleles()).apply(lambda x: ','.join([str(x[0]), str(x[1])]), axis=1).values
    df = pd.DataFrame(df)
    df.to_csv(outfile, sep=' ', index=False, compression='gzip')

if __name__ == '__main__':
    typer.run(main)
    