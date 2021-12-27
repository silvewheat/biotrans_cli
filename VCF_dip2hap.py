# -*- coding: utf-8 -*-
"""
Created on 2021-12-21

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import typer
import gzip


def find_miss(v):
    # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
    gts = v.gt_types
    n_samples = len(v.gt_types)
    indicies = np.arange(0, n_samples, 1)

    miss_mask = gts==2
    indicies_mask = []
    indicies_mask.extend(indicies[miss_mask])
    return indicies_mask



def main(in_vcf: str = typer.Argument(..., help="原始的包含miss的vcf文件(.vcf.gz)"),
         out_vcf: str = typer.Argument(..., help="phase后的vcf文件(.vcf)")
         ):
    """
    把二倍体的vcf拆分为单倍体。
    """
    with gzip.open(in_vcf, 'rb') as f1, open(out_vcf, 'w') as f2:
    for line in f1:
        tline = line.decode()
        if tline[:2] == '##':
            f2.write(tline)
        elif tline[:2] == '#C':
            tline = tline.strip().split()
            f2.write('\t'.join(tline[:9]))
            for sample in tline[9:]:
                f2.write(f'\t{sample}-1\t{sample}-2')
            f2.write('\n')
        else:
            tline = tline.strip().split()
            f2.write('\t'.join(tline[:9]))
            for gt in tline[9:]:
                f2.write(f'\t{gt[0]}\t{gt[2]}')
            f2.write('\n')


if __name__ == '__main__':
    typer.run(main)