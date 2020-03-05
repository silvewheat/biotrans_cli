# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 22:03:42 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""


import click
from cyvcf2 import VCF



@click.command()
@click.option('--vcffile')
@click.option('--genofile')
@click.option('--snpfile')
@click.option('--samples', help='query sample list file, 和vcf中个体顺序一致')
@click.option('--refindindex', help='原个体在.ind文件中的位置,也是.geno中的位置,1-base', type=int)
@click.option('--outgeno')
def main(vcffile, genofile, snpfile, samples, refindindex, outgeno):
    querysamples = [x.strip() for x in open(samples)]
    nsamples = len(querysamples)
    vcf_query = VCF(vcffile, gts012=True, samples=querysamples)
    with open(genofile) as f_g, open(snpfile) as f_s, open(outgeno, 'w') as f_o:
        for lgeno, lsnp in zip(f_g, f_s):
            loc, chrom, gdist, pdist = lsnp.split()[:4]
            loc = f'{chrom}:{pdist}-{pdist}'
            try:
                record = next(vcf_query(loc))
                gts = record.gt_types # 0=HOM_REF, 1=HET, 2=HOM_ALT, 3=UNKNOWN
                refgeno = lgeno[refindindex-1]
                gts[gts==3] = 9
                gts[gts!=9] = refgeno
                outgeno = lgeno.strip() + ''.join([str(x) for x in gts]) + '\n'
            except StopIteration:
                outgeno = lgeno.strip() + '9'*nsamples + '\n'
            f_o.write(outgeno)


if __name__ == '__main__':
    main()
