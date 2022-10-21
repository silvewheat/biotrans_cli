# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 11:44:43 2016

@author: Caiyd
"""
import re
import os
import click

@click.command()
@click.argument('dir')
def main(dir):
    ROOT_DIR = dir
    dir_list = os.listdir(ROOT_DIR)

    mapping_rate = re.compile(r"""
                              number\s+of\s+mapped\s+reads\s+=\s+[\d,]*
                              \s+
                              [(](?P<mp_rate>.*)[)]
                              """, re.VERBOSE)
    duplication_rate = re.compile(r"""
                                  duplication\s+rate\s+=
                                  \s+
                                  (?P<du_rate>.*%)
                                  """, re.VERBOSE)
    insert_size = re.compile(r"""
                             median\s+insert\s+size\s+=
                             \s+
                             (?P<in_size>\b[\d]*\b)
                             """, re.VERBOSE)
    mean_depth = re.compile(r"""
                            mean\s+coverageData\s+=
                            \s+
                            (?P<m_depth>[\d.,]*X)
                            """, re.VERBOSE)
    X3_depth = re.compile(r"""
                         There\sis\sa\s
                         (?P<X3_depth>[\d.]*%)
                         \sof\sreference\swith\sa\scoverageData
                         \s>=\s3X
                         """, re.VERBOSE)
    X4_depth = re.compile(r"""
                         There\sis\sa\s
                         (?P<X4_depth>[\d.]*%)
                         \sof\sreference\swith\sa\scoverageData
                         \s>=\s4X
                         """, re.VERBOSE)

    print("sample\tmapping_rate\tduplication\tinsert_size\tmean_depth\t3X\t4X\tX_depth\tY_depth")
    for dir_name in dir_list:
        file_list = os.listdir(ROOT_DIR + '/' + dir_name)
        if 'genome_results.txt' in file_list:
            file_name = ROOT_DIR + '/' + dir_name + '/' + 'genome_results.txt'
            with open(file_name) as f_read:
                x_depth = 'NA'
                y_depth = 'NA'
                for line in f_read:
                    tline = line.strip().split()
                    try:
                        if tline[0] == 'X':
                            x_depth = tline[3]
                        elif tline[0] == 'Y':
                            y_depth = tline[3]
                    except IndexError:
                        pass

                f_read.seek(0)
                whole_text = f_read.read()
                try:
                    mp_rate = mapping_rate.search(whole_text).group("mp_rate")
                except:
                    mp_rate = "NA"
                try:
                    du_rate = duplication_rate.search(whole_text).group("du_rate")
                except:
                    du_rate = "NA"
                try:
                    in_size = insert_size.search(whole_text).group("in_size")
                except:
                    in_size = "NA"
                try:
                    m_depth = mean_depth.search(whole_text).group("m_depth")
                except:
                    m_depth = "NA"
                try:
                    x3_depth = X3_depth.search(whole_text).group("X3_depth")
                except:
                    x3_depth = "NA"
                try:
                    x4_depth = X4_depth.search(whole_text).group("X4_depth")
                except:
                    x4_depth = "NA"
        else:
            mp_rate = "NA"
            du_rate = "NA"
            in_size = 'NA'
            m_depth = 'NA'
            x3_depth = 'NA'
            x4_depth = 'NA'
        print("\t".join([dir_name, mp_rate, du_rate, in_size, m_depth,
                         x3_depth, x4_depth, x_depth, y_depth]))

if __name__ == '__main__':
    main()

