# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:01:14 2018

Last edit on Tue May 18 21:48:08 2021

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import os
import sys
import click


def load_samples(varfile):
    return [x.strip() for x in os.popen(f'bcftools query -l {varfile}').readlines()]


def query(varfile, sample):
    """生成迭代器，每次返回80个碱基和一个\n"""
    width = 80
    bases = []
    for base in os.popen(f"bcftools query -f '[%IUPACGT]\n' -s {sample} {varfile}"):
        if base[0] != '.': # 正常是A\n
            bases.append(base.strip())
        else: # 缺失是./.\n
            bases.append('N')
        if len(bases) == width:
            bases.append('\n')
            yield ''.join(bases)
            bases = []
    if len(bases) > 0:
        bases.append('\n')
        yield ''.join(bases)


def base2file(varfile, sample, region, regions_file, outfile):
    """生成迭代器，每次返回80个碱基和一个\n"""
    if os.path.exists(outfile):
        with open(outfile, 'a') as f:
            f.write(f'\n>{sample}\n')
    else:
        with open(outfile, 'a') as f:
            f.write(f'>{sample}\n')
    if regions_file:
        os.system(f"bcftools query -f '[%IUPACGT]' -s {sample} -R {regions_file} {varfile} | sed -e 's/\.\/\./N/g' -e 's/\*\/\*/N/' | sed -e 's/\.\|\./N/g' -e 's/\*\|\*/N/' | sed -e 's/\./N/g'  -e 's/\*/N/g' | sed -e 's/\///g' -e 's/\|//g' | fold -w80 >> {outfile}")
    elif region:
        os.system(f"bcftools query -f '[%IUPACGT]' -s {sample} -r {region} {varfile} | sed -e 's/\.\/\./N/g' -e 's/\*\/\*/N/' | sed -e 's/\.\|\./N/g' -e 's/\*\|\*/N/' | sed -e 's/\./N/g'  -e 's/\*/N/g' | sed -e 's/\///g' -e 's/\|//g' | fold -w80 >> {outfile}")
    else:
        os.system(f"bcftools query -f '[%IUPACGT]' -s {sample} {varfile} | sed -e 's/\.\/\./N/g' -e 's/\*\/\*/N/' | sed -e 's/\.\|\./N/g' -e 's/\*\|\*/N/' | sed -e 's/\./N/g'  -e 's/\*/N/g' | sed -e 's/\///g' -e 's/\|//g' | fold -w80 >> {outfile}")




@click.command()
@click.option('--varfile', help='vcf,bcf文件')
@click.option('--region', help='需要转的区域(如1:1-1000), 默认全部', default=None)
@click.option('--regions-file', help='区域文件，默认None，覆盖--region', default=None)
@click.option('--outfile', help='输出fasta文件名')
def main(varfile, region, regions_file, outfile):
    """
    输入文件不能有indel
    """
    if os.path.exists(outfile):
        sys.exit('outfile exists!')
    samples = load_samples(varfile)
    for nsample, sample in enumerate(samples, 1):
        sys.stdout.write(' ' * 30 + '\r')
        sys.stdout.flush()
        sys.stdout.write(f'{nsample}/{len(samples)} {sample}' + '\r')
        sys.stdout.flush()
        base2file(varfile, sample, region, regions_file, outfile)


# =============================================================================
# @click.command()
# @click.option('--varfile', help='vcf,bcf文件')
# @click.option('--outfile', help='输出fasta文件名')
# def main(varfile, outfile):
#     samples = load_samples(varfile)
#     with open(outfile, 'w') as f:
#         for nsample, sample in enumerate(samples, 1):
#             sys.stdout.write(' ' * 30 + '\r')
#             sys.stdout.flush()
#             sys.stdout.write(f'{nsample}/{len(samples)} {sample}' + '\r')
#             sys.stdout.flush()
#             f.write(f'>{sample}\n')
#             for line in query(varfile, sample):
#                 f.write(line)
# =============================================================================

if __name__ == '__main__':
    main()
