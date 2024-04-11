# Brain ncDNV CHD

### Overview

The main analyses in this study were:

*   Variant score prediction using deep learning models [Basenji2](https://github.com/calico/basenji) and [Enformer](https://github.com/deepmind/deepmind-research/tree/master/enformer)
*   Weighted correlation network analysis ([WGCNA](https://cran.r-project.org/web/packages/WGCNA/index.html))
*   Gene set enrichment analysis ([clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler))

--------
### Requirements 

#### Hardware requirements
Deep learning predictions were carried out in GNU/Linux workstations with 128 GB of RAM and NVIDIA GPUs.

#### OS requirements 
Scripts were executed on `Linux (Ubuntu 20.04.1)`. Deep learning models are implemented in `Python3` and their corresponding usage and requirements can be seen in their repositories. WGCNA and GO enrichment analysis were performed in `R 4.1.2`.
