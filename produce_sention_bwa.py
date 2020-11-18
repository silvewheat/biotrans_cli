# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 11:19:58 2020

@author: YudongCai

@Email: yudongcai216@gmail.com
"""

import os
import click


def produce_mempe(sentieon, ref, in1fastq, in2fastq, samtools, outfile, rgid, lb, pl, smid, nt):
    return f"""{sentieon} \\
    bwa mem \\
    -R '@RG\\tID:{rgid}\\tLB:{lb}\\tPL:{pl}\\tSM:{smid}' \\
    -t {nt} \\
    {ref} \\
    {in1fastq} \\
    {in2fastq} | \\
{sentieon} \\
    util sort \\
    -o {outfile} \\
    -t {nt} \\
    --sam2bam -i -

"""

def produce_dedup(sentieon, nt, inbam, outscore, outmetrics, outbam):
    return f"""{sentieon} \\
    driver \\
    -t {nt} \\
    -i {inbam} \\
    --algo LocusCollector \\
    --fun score_info {outscore}

{sentieon} \\
    driver \\
    -t {nt} \\
    -i {inbam} \\
    --algo Dedup \\
    --rmdup \\
    --score_info {outscore} \\
    --metrics {outmetrics} \\
    {outbam}
    """


def split_sepe(fastqs):
    fastqs = list(fastqs)
    fastqs.sort()
    sefiles = []
    pefiles = []
    for fastq in fastqs:
        path, file = os.path.split(fastq)
        basename, suffix = file.split('.', 1)
        if basename[-2:] == '_1':
            if (os.path.join(path, basename[:-2] + '_2.' + suffix)) in fastqs: # 如果有对应_1的_2
                pefiles.append(fastq)
                pefiles.append(os.path.join(path, basename[:-2] + '_2.' + suffix))
        elif basename[-2:] == '_2':
            if fastq not in pefiles: # fastqs拍过序，如果是成对的，_1一定在_2之前， 这会儿还没存就是单端了
                sefiles.append(fastq)
        else:
            sefiles.append(fastq)
    return sefiles, pefiles


@click.command()
@click.option('--ref', help='参考基因组的路径')
@click.option('--outdir', help='输出比对结果的文件')
@click.option('--sentieon', help='BWA的路径', default='sentieon')
@click.option('--samtools', help='samtools的路径', default='samtools')
@click.option('--pl', help='测序平台, default is ILLUMINA', default='ILLUMINA')
@click.option('--nt', help='线程数', default=4)
@click.option('--maxmem', help='最大使用内存, 单位G')
@click.argument('infastqs', nargs=-1)
def main(ref, outdir, sentieon, samtools, pl, nt, maxmem, infastqs):
    "python produce_sention_bwa.py [options] /home/data/*.fq.gz"
    sefiles, pefiles = split_sepe(infastqs)
    if sefiles:
        print('These files are not paired:')
        print('\n'.join(sefiles))
    for npair, (in1fastq, in2fastq) in enumerate(zip(pefiles[::2], pefiles[1::2]), 1):
        basename1 = os.path.basename(in1fastq).split('.')[0]
        basename2 = os.path.basename(in2fastq).split('.')[0]
        assert basename1[:-2] == basename2[:-2]
        sortedbam = os.path.join(outdir, f'{basename1[:-2]}.sort.bam')
        dedupbam = os.path.join(outdir, f'{basename1[:-2]}.sort.dedup.bam')
        outscore = os.path.join(outdir, f'{basename1[:-2]}.score.txt.gz')
        outmetrics = os.path.join(outdir, f'{basename1[:-2]}.metrics.txt')
        print(basename1[:-2])
        rgid = basename1[:-2]
        lb = basename1[:-2]
        smid = basename1.split('_')[0]
        cmd1 = produce_mempe(sentieon, ref, in1fastq, in2fastq, samtools, sortedbam, rgid, lb, pl, smid, nt)
        cmd2 = produce_dedup(sentieon, nt, sortedbam, outscore, outmetrics, dedupbam)
        with open(f'bwa_mempe_{npair}.sh', 'w') as f:
            f.write('export SENTIEON_TMPDIR=/stor9000/apps/users/NWSUAF/2012010954/SENTIEONTMP\n')
            f.write(f'export bwt_max_mem={maxmem}G\n')
            f.write(cmd1)
            f.write(cmd2)


if __name__ == '__main__':
    main()
