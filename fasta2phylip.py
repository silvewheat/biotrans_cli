#!/stor9000/apps/users/NWSUAF/2012010954/Software/Anaconda4.4_py3.6/bin/python
# -*- coding: utf-8 -*-
import click
from Bio import AlignIO

@click.command()
@click.argument('fasta')
@click.argument('phylip')
def main(fasta, phylip):
    AlignIO.convert("%s" % fasta, "fasta", "%s" % phylip, "phylip-sequential")

main()
