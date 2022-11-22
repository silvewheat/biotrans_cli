# -*- coding: utf-8 -*-
"""
Created on 2022-11-03

@author: Yudongcai

@Email: yudong_cai@163.com
"""
import typer
import gzip
from ete3 import Tree


def main(infile: str = typer.Argument(..., help="input newick tree file, can be gzipped"),
         samplesfile: str = typer.Argument(..., help="keep only these samples, one sample per row"),
         outfile: str = typer.Argument(..., help="output newick tree file, can be gzipped")):
    infile_suffix = infile[-3:]
    if infile_suffix == '.gz':
        f_in = gzip.open(infile, 'rb')
    else:
        f_in = open(infile)
    
    outfile_suffix = outfile[-3:]
    if outfile_suffix == '.gz':
        f_out = gzip.open(outfile, 'wb')
    else:
        f_out = open(outfile, 'w')
    
    sampleIDs = [x.strip() for x in open(samplesfile)]
    
    for line in f_in:
        if infile_suffix == '.gz':
            tree_seq = line.decode().strip()
        else:
            tree_seq = line.strip()
        t = Tree(tree_seq)
        t.prune(sampleIDs)
        out_tree_seq = t.write()+'\n'
        if outfile_suffix == '.gz':
            f_out.write(out_tree_seq.encode())
        else:
            f_out.write(out_tree_seq)
    f_in.close()
    f_out.close()

if __name__ == '__main__':
    typer.run(main)
