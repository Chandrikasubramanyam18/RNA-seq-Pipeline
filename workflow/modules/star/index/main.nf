// =====================================================
// Module: STAR_INDEX
// Builds the STAR genome index from fasta + GTF.
// Mirrors validated mini_real params: --genomeSAindexNbases 7,
// --sjdbOverhang $(readLength - 1) = 62.
// =====================================================

process STAR_INDEX {
    tag "STAR_INDEX ${genomeFasta}"
    publishDir "${params.outdir}/reference/star_index",
        mode: 'copy', overwrite: true,
        pattern: 'star_index/**'

    input:
    path genomeFasta
    path gtf

    output:
    path "star_index", emit: index

    script:
    """
    STAR \\
        --runMode genomeGenerate \\
        --runThreadN ${task.cpus} \\
        --genomeDir star_index \\
        --genomeFastaFiles ${genomeFasta} \\
        --sjdbGTFfile ${gtf} \\
        --sjdbOverhang ${params.star_sjdb_overhang} \\
        --genomeSAindexNbases ${params.star_sa_index_nbases}
    """

    stub:
    """
    mkdir -p star_index
    touch star_index/Genome
    echo "stub genomeParameters" > star_index/genomeParameters.txt
    """
}