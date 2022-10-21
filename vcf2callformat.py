# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 11:02:12 2018

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click
import pysam

def toIUPAC(nuclears):
    """
    nuclears: list
    ['A', 'C'] etc.
    https://en.wikipedia.org/wiki/Nucleic_acid_notation
    """
    nuc2code = {'A': 1,
                'C': 2,
                'G': 4,
                'T': 8,
                'R': 5,
                'Y': 10,
                'W': 9,
                'S': 6,
                'M': 3,
                'K': 12,
                'B': 14,
                'H': 11,
                'D': 13,
                'V': 7,
                'N': 0,
                None: 0}
    code2nuc = {v: k for k,v in nuc2code.items()}
    code2nuc[15] = 'N'
    code2nuc[0] = 'N'
    return code2nuc[sum([nuc2code[x] for x in set(nuclears)])]



@click.command()
@click.option('--vcffile', help='.vcf/.vcf.gz/.bcf')
@click.option('--outfile', help='outfile name')
def main(vcffile, outfile):
    var = pysam.VariantFile(vcffile)
    samples = list(var.header.samples)
    newheader = ['scaffold', 'position'] + samples
    with open(outfile, 'w') as f:
        f.write('\t'.join(newheader) + '\n')
        for record in var:
            gts = [x.alleles for x in record.samples.values()]
            nucs = []
            for gt in gts:
                nucs.append(toIUPAC(gt))
            f.write(f'{record.chrom}\t{record.pos}\t' + '\t'.join(nucs) + '\n')


if __name__ == '__main__':
    main()

