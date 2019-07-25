# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 16:05:22 2018

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import os
import click
from itertools import combinations


def load_one_column(file):
    out_list = []
    with open(file) as f:
        for line in f:
            out_list.append(line.strip())
    try:
        out_list.remove("")
    except ValueError:
        pass
    return out_list

def load_popIDs(pop):
    if os.path.isfile(pop):
        print(f'load pop file: {pop}')
        outlist = load_one_column(pop)
        print(f'{len(outlist)} popIDs loaded')
        return outlist
    else:
        print(f'popID: {pop} loaded')
        return [pop]


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def generate_popfile(popids, outprefix, nquadrapules):
    combs = []
    pools = set()
    for pop1 in popids['pop1']:
        for pop2 in popids['pop2']:
            for pop3 in popids['pop3']:
                if len(set([pop1, pop2, pop3])) == 3:
                    comb = f'{pop1}\t{pop2}\t{pop3}'
                    if comb not in pools:
                        combs.append(f'{pop1}\t{pop2}\t{pop3}')
                        pools.add(comb)
                        pools.add(f'{pop2}\t{pop1}\t{pop3}')
                else:
                    print(f'ID repeated in ({pop1}, {pop2}, {pop3})')
    for nfile, comb in enumerate(chunks(combs, nquadrapules), 1):
        with open(f'{outprefix}_{nfile}_popfile', 'w') as f:
            f.write('\n'.join(comb))
    return nfile

def generate_parfile(genotype, snp, indiv, outprefix, nfile):
    for i in range(1, nfile+1):
        with open(f'{outprefix}_{i}_par', 'w') as f:
            f.write(f'genotypename: {genotype}\nsnpname: {snp}\nindivname: {indiv}\npopfilename: {outprefix}_{i}_popfile')


def generate_shell(outprefix, nfile):
    for i in range(1, nfile+1):
        with open(f'{outprefix}_{i}.sh', 'w') as f:
            f.write(f'/stor9000/apps/users/NWSUAF/2015051660/software/AdmixTools-master/src/qp3Pop -p {outprefix}_{i}_par numchrom 29 > {outprefix}_{i}.out')


@click.command()
@click.option('--pop1', help='source1, popID in .ind file, or a file name contain several popIDs')
@click.option('--pop2', help='source2, popID in .ind file, or a file name contain several popIDs')
@click.option('--pop3', help='target, popID in .ind file, or a file name contain several popIDs')
@click.option('--genotype', help='input genotype file name')
@click.option('--snp', help='input snp file name')
@click.option('--indiv', help='input indiv file name')
@click.option('--outprefix', help='output files prefix')
@click.option('--nquadrapules', help='number of quadrapules per file, default is 20', default=20, type=int)
def main(pop1, pop2, pop3, genotype, snp, indiv, outprefix, nquadrapules):
    popids = {}
    for i, pop in enumerate((pop1, pop2, pop3), 1):
        print(f'Pop{i}:')
        popids[f'pop{i}'] = load_popIDs(pop)
    nfile = generate_popfile(popids, outprefix, nquadrapules)
    print(f'chunck size: {nquadrapules}')
    print(f'file number: {nfile}')
    generate_parfile(genotype, snp, indiv, outprefix, nfile)
    generate_shell(outprefix, nfile)


if __name__ == '__main__':
    main()


