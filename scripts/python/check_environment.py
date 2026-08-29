#!/usr/bin/env python3
"""
Environment Verification Script for RNA-seq Pipeline
Checks availability and versions of all required command-line tools, Python libraries, and R packages.
"""

import sys
import shutil
import subprocess
from typing import List, Tuple

def check_cli_tool(name: str, version_flag: str = "--version") -> Tuple[bool, str]:
    path = shutil.which(name)
    if not path:
        return False, "NOT FOUND"
    try:
        res = subprocess.run([name, version_flag], capture_output=True, text=True, timeout=10)
        out = res.stdout.strip() or res.stderr.strip()
        first_line = out.split("\n")[0] if out else "Found (version unknown)"
        return True, first_line
    except Exception as e:
        return True, f"Found at {path} (error running check: {e})"

def check_python_package(pkg_name: str) -> Tuple[bool, str]:
    try:
        mod = __import__(pkg_name)
        ver = getattr(mod, "__version__", "Available (no __version__)")
        return True, str(ver)
    except ImportError:
        return False, "NOT INSTALLED"

def check_r_package(pkg_name: str) -> Tuple[bool, str]:
    rscript = shutil.which("Rscript")
    if not rscript:
        return False, "Rscript not available"
    cmd = [rscript, "-e", f"if (!requireNamespace('{pkg_name}', quietly=TRUE)) {{ quit(status=1) }}; cat(as.character(packageVersion('{pkg_name}')) )"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0:
            return True, res.stdout.strip()
        return False, "NOT INSTALLED"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    print("=" * 80)
    print("       RNA-seq Bioinformatics Pipeline - Environment Health Check")
    print("=" * 80)

    # 1. CLI Tools
    cli_tools = [
        ("git", "--version"),
        ("java", "-version"),
        ("nextflow", "-version"),
        ("fastqc", "--version"),
        ("fastp", "--version"),
        ("STAR", "--version"),
        ("samtools", "--version"),
        ("featureCounts", "-v"),
        ("salmon", "--version"),
        ("multiqc", "--version"),
        ("read_distribution.py", "--version"),
        ("Rscript", "--version")
    ]

    print("\n[1] Command-Line Tools & Runtimes:")
    print(f"{'Tool':<25} {'Status':<12} {'Details / Version'}")
    print("-" * 80)
    all_cli_pass = True
    for tool, flag in cli_tools:
        found, msg = check_cli_tool(tool, flag)
        status = "[OK]" if found else "[MISSING]"
        if not found:
            all_cli_pass = False
        print(f"{tool:<25} {status:<12} {msg[:40]}")

    # 2. Python Packages
    py_packages = ["pandas", "numpy", "scipy", "matplotlib", "seaborn", "Bio", "pytest", "yaml"]
    print("\n[2] Python Scientific Packages:")
    print(f"{'Package':<25} {'Status':<12} {'Version'}")
    print("-" * 80)
    for pkg in py_packages:
        found, ver = check_python_package(pkg)
        status = "[OK]" if found else "[MISSING]"
        print(f"{pkg:<25} {status:<12} {ver}")

    # 3. R / Bioconductor Packages
    r_packages = ["DESeq2", "clusterProfiler", "pheatmap", "ggplot2", "tximport", "ggrepel"]
    print("\n[3] R / Bioconductor Packages:")
    print(f"{'Package':<25} {'Status':<12} {'Version'}")
    print("-" * 80)
    for rpkg in r_packages:
        found, ver = check_r_package(rpkg)
        status = "[OK]" if found else "[MISSING]"
        print(f"{rpkg:<25} {status:<12} {ver}")

    print("\n" + "=" * 80)
    if all_cli_pass:
        print("ALL CRITICAL CORE BIOINFORMATICS TOOLS ARE DETECTED AND READY.")
    else:
        print("NOTICE: Some tools are missing in the current active environment.")
        print("If you are in Windows PowerShell, set up WSL2 / Ubuntu or activate the Conda environment.")
    print("=" * 80)

if __name__ == "__main__":
    main()
