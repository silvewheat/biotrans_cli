# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 11:27:49 2021

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import typer
import numpy as np
from typing import Tuple
from cyvcf2 import VCF, Writer


def filter_samples(v, mindepth, het_altrange, homref_maxaltrate, homalt_minaltrate):
    # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
    n_samples = len(v.gt_types)
    indicies = np.arange(0, n_samples, 1)
    indicies_mask = []
    gt_alt_freqs = v.gt_alt_depths / v.gt_depths # 直接调用v.gt_alt_freqs会引发numpy警告
    # 杂合位点，深度低于10或者不满足alt reads占比0.25到0.75之间的mask掉
    het_mask = (v.gt_types==1) & ((v.gt_depths<mindepth) | (gt_alt_freqs<het_altrange[0]) | (gt_alt_freqs>het_altrange[1]))
    indicies_mask.extend(indicies[het_mask])
    
    # 纯合ref，alt freq应为0，纯合alt，alt freq为1，深度大于等于10
    homRef_mask = (v.gt_types==0) & ((v.gt_depths<mindepth) | (gt_alt_freqs>homref_maxaltrate))
    homAlt_mask = (v.gt_types==3) & ((v.gt_depths<mindepth) | (gt_alt_freqs<homalt_minaltrate))
    indicies_mask.extend(indicies[homRef_mask])
    indicies_mask.extend(indicies[homAlt_mask])
    return indicies_mask



def main(invcf: str = typer.Argument(..., help="输入的vcf文件"),
         outvcf: str = typer.Argument(..., help="输出的vcf文件"),
         mindepth: int = typer.Option(10, help="最低reads覆盖率"),
         het_altrange: Tuple[float, float] = typer.Option((0.2, 0.8), help="杂合位点的alt频率范围"),
         homref_maxaltrate: float = typer.Option(0, help="纯合ref型GT，最大alt reads比例不超过这个"),
         homalt_minaltrate: float = typer.Option(1, help="纯合alt型GT，最小alt reads比例不低于这个")
         ):
    """
    mask掉满足以下的genotype：
    杂合位点alt reads的频率不在20%到80%范围之内的。
    纯合位点reads支持比例不是100%的。
    覆盖的reads小于10条的。
    """
    vcf =  VCF(invcf)
    w = Writer(outvcf, vcf)
    for v in vcf:
        indicies_mask = filter_samples(v, mindepth, het_altrange, homref_maxaltrate, homalt_minaltrate)
        if indicies_mask:
            for index in indicies_mask:
                v.genotypes[index] = [-1]*v.ploidy + [False]
            v.genotypes = v.genotypes
        w.write_record(v)
    w.close()
    vcf.close()


if __name__ == '__main__':
    typer.run(main)