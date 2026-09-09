#!/usr/bin/env nextflow

include { PREPROCESS }           from './subworkflows/qc/preprocess/main.nf'
include { ALIGNMENT_STAR }       from './subworkflows/alignment/star/main.nf'
include { QUANTIFICATION_FEATURECOUNTS } from './subworkflows/quantification/featurecounts/main.nf'
include { INTERPRETATION }       from './subworkflows/interpretation/main.nf'
include { MULTIQC }              from './modules/multiqc/main.nf'

workflow {
    ch_samplesheet = Channel.fromPath(params.samplesheet)
    ch_fasta       = file(params.fasta)
    ch_gtf         = file(params.gtf)
    ch_bed         = file(params.rseqc_bed)

    ch_reads = ch_samplesheet
        .splitCsv(header: true, sep: ',')
        .map { row ->
            def meta = [ id: row.sample, condition: row.condition ]
            def root = "${projectDir}/.."
            tuple(meta,
                  file("${root}/${row.fastq_1}".toString()),
                  file("${root}/${row.fastq_2}".toString()))
        }

    PREPROCESS(ch_reads)

    ALIGNMENT_STAR(ch_fasta, ch_gtf, PREPROCESS.out.trimmed_reads, ch_bed)

    QUANTIFICATION_FEATURECOUNTS(ch_gtf, ALIGNMENT_STAR.out.bam)
    INTERPRETATION(QUANTIFICATION_FEATURECOUNTS.out.counts)
    MULTIQC(PREPROCESS.out.fastqc_zips.map { meta, zip -> zip }.collect(),
            PREPROCESS.out.fastp_json.map { meta, json -> json }.collect(),
            ALIGNMENT_STAR.out.log_final.map { meta, log -> log }.collect(),
            ALIGNMENT_STAR.out.samtools.map { meta, stats -> stats }.collect(),
            ALIGNMENT_STAR.out.rseqc.map { meta, rqc -> rqc }.collect())
}
