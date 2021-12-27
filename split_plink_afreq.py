# -*- coding: utf-8 -*-
"""
Created on 2021-12-15

@author: Yudongcai

@Email: yudong_cai@163.com
"""

import gzip


def split_to_allel(group):
    afreqfile = f'{group}.afreq'
    outfreqfile = f'{group}.afreq.allel.tsv.gz'
    with open(afreqfile) as fi, gzip.open(outfreqfile, 'wb') as fo:
        _ = fi.readline()
        header = 'CHROM\tPOS\tID\tAllELE\tFREQ\tOBS_CT\n'
        fo.write(header.encode())
        for line in fi:
            tline = line.strip().split()
            refline = tline[:4] + [tline[5], tline[7]]
            fo.write(('\t'.join(refline)+'\n').encode())
            for allel, freq in zip(tline[4].split(','), tline[6].split(',')):
                altline = tline[:3] + [allel, freq, tline[7]]
                fo.write(('\t'.join(altline)+'\n').encode())