# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 17:17:25 2021

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import gzip
import typer

def write_header(infile, outfile):
    with gzip.open(infile, 'rb') as f1, \
         gzip.open(outfile, 'wb') as f2:
        header = f1.readline()
        last_snp = None
        groups = []
        for line in f1:
            tline = line.decode().strip().split()
            if not last_snp:
                last_snp = tline[1]
                snp = tline[1]
            if tline[1] != last_snp:
                break
            groups.append(tline[2])
        out_header = ' '.join(groups) + '\n'
        f2.write(out_header.encode())
        return len(groups)
    


def main(infile: str = typer.Argument(..., help="plink的频率文件"),
         outfile: str = typer.Argument(..., help="输出的treemix文件(.gz)")):
    """
    把plink计算的群体频率文件转换为treemix的输入格式
    """
    ngroups = write_header(infile, outfile)
    with gzip.open(infile, 'rb') as f1, \
         gzip.open(outfile, 'ab') as f2:
        header = f1.readline()
        outlist = []
        for nline, line in enumerate(f1, 1):
            tline = line.decode().strip().split()
            n_ref = int(tline[6])
            n_alleles = int(tline[7])
            n_alt = n_alleles - n_ref
            outlist.append(f'{n_ref},{n_alt}')
            if nline % ngroups == 0:
                outline = ' '.join(outlist) + '\n'
                f2.write(outline.encode())
                outlist = []
                

if __name__ == '__main__':
    typer.run(main)