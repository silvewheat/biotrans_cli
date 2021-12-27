# -*- coding: utf-8 -*-
"""
Created on 2021-12-21

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import typer
import numpy as np
from typing import Tuple
from cyvcf2 import VCF, Writer


def find_miss(v):
    # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
    gts = v.gt_types
    n_samples = len(v.gt_types)
    indicies = np.arange(0, n_samples, 1)

    miss_mask = gts==2
    indicies_mask = []
    indicies_mask.extend(indicies[miss_mask])
    return indicies_mask



def main(original_vcf: str = typer.Argument(..., help="原始的包含miss的vcf文件"),
         phased_vcf: str = typer.Argument(..., help="phase后的vcf文件"),
         masked_vcf: str = typer.Argument(..., help="输出的mask后的vcf文件")
         ):
    """
    由于phase的时候一般都会impute，这个脚本是把impute的mask掉，只保留phase信息。
    输入impute前的原始vcf，根据原始vcf来mask掉phased vcf中填充进来的GT。
    """
    original_vcf =  VCF(original_vcf)
    phased_vcf = VCF(phased_vcf)
    w = Writer(masked_vcf, phased_vcf)
    for v1, v2 in zip(original_vcf, phased_vcf):
        indicies_mask = find_miss(v1)
        if indicies_mask:
            for index in indicies_mask:
                v2.genotypes[index] = [-1]*v2.ploidy + [False]
            v2.genotypes = v2.genotypes
        w.write_record(v2)
    w.close()
    original_vcf.close()
    phased_vcf.close()


if __name__ == '__main__':
    typer.run(main)