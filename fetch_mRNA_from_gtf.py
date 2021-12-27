# -*- coding: utf-8 -*-
"""
Created on 2021-10-27

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import typer
import numpy as np
import pandas as pd
import pyranges as pr
from pyfaidx import Fasta


def main(fastafile: str = typer.Option(..., help="fasta file"),
         gtffile: str = typer.Option(..., help="gtf file"),
         outfile: str = typer.Option(..., help="output mRNA fasta file")):
    """根据gtf提取基因的mRNA序列，同一基因的不同转录本会merge起来，每个基因只输出一个合并后的mRNA序列"""
    gr = pr.read_gtf(gtffile)
    df = gr.merge(by=["Feature", "gene_id"], strand=False).as_df()
    seq = Fasta(fasta)
    with open(outfile, 'w') as f:
        for gene, gdf in df.loc[df['Feature']=='exon', :].groupby('gene_id'):
            f.write(f'>{gene}\n')
            content = []
            for chrom, start, end in gdf.sort_values('Start')[['Chromosome', 'Start', 'End']].values:
                content.append(seq[chrom][start:end].seq)
            else:
                f.write(''.join(content)+'\n')

if __name__ == '__main__':
    typer.run(main)
