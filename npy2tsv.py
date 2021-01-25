# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:01:41 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click
import numpy as np


@click.command()
@click.option('--npyfile')
@click.option('--outfile')
def main(npyfile, outfile):
    array = np.load(npyfile)
    np.savetxt(outfile, array, delimiter='\t', fmt='%.0f')

if __name__ == '__main__':
    main()

