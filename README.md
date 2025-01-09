# Noncoding variants and sulcal patterns in congenital heart disease: Machine learning to predict functional impact
![MIT License](https://badgen.net/static/license/MIT/blue)
[![doi](https://badgen.net/badge/doi/10.1016%2Fj.isci.2024.111707)](https://doi.org/10.1016/j.isci.2024.111707)

### Overview

This repository contains the code used in the study: Mondragon-Estrada et al., Noncoding variants and sulcal patterns in congenital heart disease: Machine learning to predict functional impact, iScience (2024), https://doi.org/10.1016/j.isci.2024.111707

<p align="center">
    <img width=60% height=60% src="https://github.com/MortonLabBCH/brain-ncdnv-chd/blob/main/figures/graphical_abstract.png">
</p>

The main analyses were:

*   Variant score prediction using deep learning models [Basenji2](https://github.com/calico/basenji) and [Enformer](https://github.com/deepmind/deepmind-research/tree/master/enformer)
*   Weighted correlation network analysis ([WGCNA](https://cran.r-project.org/web/packages/WGCNA/index.html))
*   Gene set enrichment analysis ([clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler))

--------
### Requirements 

#### Hardware requirements
Deep learning predictions were carried out in GNU/Linux workstations with 128 GB of RAM and NVIDIA GPUs.

#### OS requirements 
Scripts were executed on `Linux (Ubuntu 20.04.1)`. Deep learning models are implemented in `Python3` and their corresponding usage and requirements can be seen in their repositories. WGCNA and GO enrichment analysis were performed in `R 4.1.2`.
