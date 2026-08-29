#!/usr/bin/env bash
# ==============================================================================
# RNA-seq Pipeline Environment Verification Script (Bash / POSIX)
# ==============================================================================
set -e

echo "================================================================================"
echo "          RNA-seq Pipeline - Bash / POSIX Environment Verification              "
echo "================================================================================"

check_cmd() {
    local cmd=$1
    local name=$2
    if command -v "$cmd" &> /dev/null; then
        local ver
        ver=$("$cmd" --version 2>&1 | head -n 1 || true)
        printf "%-20s %-10s %s\n" "$name" "[OK]" "$ver"
    else
        printf "%-20s %-10s %s\n" "$name" "[MISSING]" "Not found in PATH"
    fi
}

echo -e "\n[1] Checking Core Runtimes & Workflow Engines:"
check_cmd "git" "Git"
check_cmd "java" "Java (JVM)"
check_cmd "nextflow" "Nextflow"
check_cmd "python3" "Python 3"
check_cmd "R" "R Environment"
check_cmd "conda" "Conda/Mamba"

echo -e "\n[2] Checking RNA-seq Command-Line Tools:"
check_cmd "fastqc" "FastQC"
check_cmd "fastp" "fastp"
check_cmd "STAR" "STAR Aligner"
check_cmd "samtools" "SAMtools"
check_cmd "featureCounts" "featureCounts"
check_cmd "salmon" "Salmon"
check_cmd "multiqc" "MultiQC"
check_cmd "read_distribution.py" "RSeQC"

echo -e "\n================================================================================"
echo "If any tools are [MISSING], please activate the conda environment:"
echo "    conda activate rnaseq-pipeline"
echo "================================================================================"
