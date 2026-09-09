// =====================================================
// Subworkflow: PREPROCESS
// Validated ordering — FastQC(raw) on both mates, fastp
// trimming, FastQC(clean) on both trimmed mates:
//   FastQC(raw, R1/R2) -> fastp -> FastQC(clean, R1/R2)
// =====================================================

include { FASTQC as FASTQC_RAW }   from '../../../modules/fastqc/main.nf'
include { FASTQC as FASTQC_CLEAN } from '../../../modules/fastqc/main.nf'
include { FASTP }                  from '../../../modules/fastp/main.nf'

workflow PREPROCESS {
    take:
    reads_ch       // channel: [ meta, reads1, reads2 ]

    main:
    ch_fastqc_raw = reads_ch
        .flatMap { meta, reads1, reads2 ->
            [ tuple(meta + [stage: 'raw'], reads1),
              tuple(meta + [stage: 'raw'], reads2) ]
        }
    FASTQC_RAW(ch_fastqc_raw)

    FASTP(reads_ch)

    ch_fastqc_clean = FASTP.out.reads
        .flatMap { meta, r1, r2 ->
            [ tuple(meta + [stage: 'clean'], r1),
              tuple(meta + [stage: 'clean'], r2) ]
        }
    FASTQC_CLEAN(ch_fastqc_clean)

    emit:
    fastqc_raw_html   = FASTQC_RAW.out.html
    fastqc_clean_html = FASTQC_CLEAN.out.html
    fastqc_zips       = FASTQC_RAW.out.zip.mix(FASTQC_CLEAN.out.zip)
    fastp_json        = FASTP.out.json
    trimmed_reads     = FASTP.out.reads
}