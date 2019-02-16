# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 11:55:49 2018

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click


def load_fa(fafile):
    seqdict = {}
    with open(fafile) as f:
        seq_id = f.readline().strip().split()[0][1:]
        tmp_seq = []
        for line in f:
            if line[0] != '>':
                tmp_seq.append(line.strip())
            else:
                seqdict[seq_id] = ''.join(tmp_seq)
                seq_id = line.strip().split()[0][1:]
                tmp_seq = []
        seqdict[seq_id] = ''.join(tmp_seq)
    return seqdict


@click.command()
@click.argument('infasta')
@click.argument('outfasta')
@click.option('--miss', help='缺失比例(N)', type=float, default=0.25)
def main(infasta, outfasta, miss):
    seq = load_fa(infasta)
    with open(outfasta, 'w') as f:
        for name, string in seq.items():
            if (string.upper().count('N') / len(string)) < miss:
                f.write(f'>{name}\n{string}\n')


if __name__ == '__main__':
    main()
