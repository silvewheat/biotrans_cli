# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 21:15:31 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import click


def load_genomefile(gfile):
    """
    第一列染色体ID，第二列长度
    """
    glens = {}
    with open(gfile) as f:
        for line in f:
            tline = line.strip().split()
            glens[tline[0]] = int(tline[1])
    return glens


def produce_shell(i, chrom, start, end):
    return f"""/stor9000/apps/users/NWSUAF/2012010954/Software/bcftools/bcftools-1.10.2/bcftools \\
    mpileup \\
    -C 50 \\
    -q 30 \\
    -Q 20 \\
    -r {chrom}:{start}-{end} \\
    -a INFO/AD,FORMAT/AD,FORMAT/DP,FORMAT/ADF,FORMAT/ADR \\
    -f /stor9000/apps/users/NWSUAF/2012010954/Genome/ASM_gaot/ASM.fa \\
    -b BAM.list | \\
/stor9000/apps/users/NWSUAF/2012010954/Software/bcftools/bcftools-1.10.2/bcftools \\
    call \\
    -v \\
    -m \\
    -f GQ,GP \\
    --threads 2 \\
    --skip-variants indels \\
    -O z \\
    -o /stor9000/apps/users/NWSUAF/2012010954/01_GoatProject/01_data/06_bcftools/V1/out/split/{i}_chr{chrom}.raw.vcf.gz

/stor9000/apps/users/NWSUAF/2012010954/Software/bcftools/bcftools-1.10.2/bcftools \\
    index \\
    /stor9000/apps/users/NWSUAF/2012010954/01_GoatProject/01_data/06_bcftools/V1/out/split/{i}_chr{chrom}.raw.vcf.gz
"""


@click.command()
@click.option('--gfile', help='.genome文件，第一列染色体号，第二列长度。')
@click.option('--blocksize', help='以blocksize为长度创建shell, 单位Mbp, 默认100Mbp', type=int, default=30)
@click.option('--outprefix', help='输出shell前缀')
def main(gfile, blocksize, outprefix):
    blocksize *= 1_000_000
    glens = load_genomefile(gfile)
    i = 0
    for chrom, glen in glens.items():
        for start in range(1, glen+1, blocksize):
            i += 1
            end = start + blocksize - 1
            print(f'file{i} {chrom}:{start}-{end}')
            cmd = produce_shell(i, chrom, start, end)
            with open(f'{outprefix}_{i}.sh', 'w') as f:
                f.write(cmd)


if __name__ == '__main__':
    main()





