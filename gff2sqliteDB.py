# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 10:40:11 2019

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click
import gffutils


@click.command()
@click.option('--gfffile', help='输入的gff3文件')
@click.option('--outdb', help='输出的sqlite database文件')
def main(gfffile, outdb):
    '''
    用gffutils把gff3文件为sqlite database
    python gff2sqliteDB.py --gfffile in.gff --out out.db
    '''
    db = gffutils.create_db(data=gfffile, dbfn=outdb, force=True, keep_order=True,
                            merge_strategy='merge', sort_attribute_values=True)


if __name__ == '__main__':
    main()