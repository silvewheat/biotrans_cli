# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:37:53 2021

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import gzip
import typer


def load_queried_id(seqidfile):
    """

    Parameters
    ----------
    seqidfile : str
        输入的是gzip压缩的文件名，只有@开头的会被读取，且只有空白符号前的字符串被当做ID.
        因此可以直接把fastq作为输入，也可以光把ID提取出来单独生成一个文件作为输入
    Returns
    -------
    包含seqidfile中的所有ID的集合

    """
    seqids = []
    with gzip.open(seqidfile, 'rb') as f:
        for line in f:
            tline = line.decode()
            if tline[0] != '@':
                pass
            else:
                seqids.append(tline.split()[0])
    return set(seqids)


def main(seqidfile: str = typer.Option(..., help="需要保留的fastqID,每行以@开头,文件用gzip压缩,也可以直接给一个fastq文件"),
         infq1: str = typer.Option(..., help="待过滤的fastq1文件, gzip压缩"),
         infq2: str = typer.Option(..., help="待过滤的fastq2文件, gzip压缩"),
         outfq1: str = typer.Option(..., help="输出的fastq1文件, gzip压缩"),
         outfq2: str = typer.Option(..., help="输出的fastq2文件, gzip压缩")):
    """
    按照seqidfile中的ID来筛选fastq文件中的reads
    """
    seqids = load_queried_id(seqidfile)
    nline = 0
    required = False
    with gzip.open(infq1, 'rb') as f_in_1, gzip.open(infq2, 'rb') as f_in_2, \
         gzip.open(outfq1, 'wb') as f_out_1, gzip.open(outfq2, 'wb') as f_out_2:
        for line1, line2 in zip(f_in_1, f_in_2):
            nline += 1 # 第一行是1
            if nline % 4 != 1:
                if required:
                    f_out_1.write(line1)
                    f_out_2.write(line2)
                else:
                    continue
            else:
                name1 = line1.decode().strip().split()[0]
                name2 = line2.decode().strip().split()[0]
                assert name1 == name2
                if name1 in seqids:
                    required = True
                    f_out_1.write(line1)
                    f_out_2.write(line2)
                else:
                    required = False

if __name__ == '__main__':
    typer.run(main)