# Chapter 32: AWS Cloud Computing

> Running the RNA-seq pipeline on cloud infrastructure for on-demand
> scale, elastic storage, and reproducibility.

---

## 1. What is it?

**Amazon Web Services (AWS)** is a cloud platform providing on-demand
compute, storage, and services. For bioinformatics, the relevant
pieces are:

- **EC2** -- virtual machines (compute)
- **S3** -- object storage (FASTQ/BAM/results)
- **AWS Batch** -- managed batch job execution
- **Nextflow on AWS Batch / AWS Genomics CLI**
- **IAM / security** -- permissions & access control

---

## 2. Why do we need it?

- No local cluster or HPC node (Ch 31) available.
- **Elastic scale**: spin up many nodes for a big dataset, then shut
  down.
- Persistent, cheap **S3 storage** for huge files.
- Reproducible, scriptable infrastructure; teams can share results.

---

## 3. Where does it fit?

```
Nextflow (Ch 25) -> AWS Batch -> EC2 nodes (ephemeral)
data/results saved in S3
```

AWS is the compute/storage backend for Nextflow in the cloud.

---

## 4. Input

- AWS account, configured credentials (`aws configure`)
- An S3 bucket for input/output data
- A Nextflow config targeting AWS Batch

---

## 5. Output

- Completed pipeline results stored in S3 (`s3://bucket/results/`)
- EC2 instances launched, run jobs, then terminate.

---

## 6. How it works

1. **Upload data** to S3:
   ```bash
   aws s3 cp data/raw s3://my-bucket/rnaseq/raw --recursive
   ```
2. **Run Nextflow** with AWS Batch profile; each process launches an
   EC2 task.
3. **Results saved back to S3**:
   ```bash
   aws s3 cp results s3://my-bucket/rnaseq/results --recursive
   ```
4. EC2 instances terminate when finished.

Nextflow config:

```groovy
process {
  executor = 'awsbatch'
  queue    = 'rnaseq-job-queue'
  container = 'nfcore/rnaseq:latest'
}
aws {
  region = 'us-east-1'
  batch.cliPath = '/home/ec2-user/miniconda/bin/aws'
}
```

---

## 7. Biology behind it

- Cloud scale lets you analyze **many samples in parallel** without
  local hardware limits.
- S3 provides durable storage for large raw + processed data.
- Reproducible infrastructure means results can be regenerated
  identically on demand.

---

## 8. Command

```bash
# Configure credentials
aws configure

# Upload input data
aws s3 cp data/raw s3://my-bucket/rnaseq/raw --recursive

# Run Nextflow on AWS Batch
nextflow run main.nf -profile awsbatch \
    --input s3://my-bucket/rnaseq/samplesheet.csv

# Download results
aws s3 cp s3://my-bucket/rnaseq/results results --recursive
```

---

## 9. Example

A whole-genome cohort that would take days locally runs overnight by
launching dozens of parallel EC2 instances via AWS Batch, with all
inputs/outputs in S3.

---

## 10. How to read the output

- **AWS Batch console**: job status (SUBMITTED, RUNNING, SUCCEEDED,
  FAILED).
- **S3 console / CLI**: outputs appear under `s3://bucket/...`.
- **CloudWatch**: logs and cost tracking.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Credentials not configured | `aws configure` |
| Batch job definition missing | Create compute env + job queue |
| Permissions (AccessDenied) | IAM roles for S3/Batch/EC2 |
| Unexpected cost | Set budget alerts; terminate idle instances |
| Region mismatch | Keep all resources in one region |

---

## 12. Limitations

- Cloud **costs money** (compute + storage) -- monitor usage.
- Requires DevOps setup (IAM, compute envs).
- Network transfer of large data can be slow/costly.

---

## 13. How our project uses it

- **Future** phase: optional AWS Batch execution of the workflow.
- S3 for data/results; reproducible infrastructure.
- Documented as the cloud scaling path beyond local/WSL2.

---

## 14. Official documentation

- **AWS**:
  https://aws.amazon.com/
- **AWS Batch**:
  https://aws.amazon.com/batch/
- **Nextflow & AWS Batch**:
  https://www.nextflow.io/docs/latest/awsbatch.html

---

## 15. Mini exercise

1. What are EC2, S3, and AWS Batch used for in bioinformatics?
2. How does Nextflow run on AWS Batch?
3. Why is S3 good for storing large FASTQ/BAM files?
4. What are two risks of cloud computing, and how do you mitigate
   them?
5. How would you upload pipeline results to S3?

---

**End of Infrastructure phase.**

> **Next**: [Chapter 33: Platform Architecture](../12_platform/architecture.md)
