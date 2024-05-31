# Brain and Genes study

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

--------
### Preprint
```
Mondragon-Estrada, Enrique and Newburger, Jane W. and DePalma, Steven and Brueckner, Martina and Cleveland, John and Chung, Wendy and Gelb, Bruce D. and Goldmuntz, Elizabeth and Hagler, Donald J. and Huang, Hao and McQuillen, Patrick S. and Miller, Thomas A. and Panigrahy, Ashok and Porter, George and Roberts, Amy E. and Rollins, Caitlin K. and Russell, Mark W. and Tristani-Firouzi, Martin and Grant, Ellen and Im, Kiho and Morton, Sarah U., Using Machine Learning to Predict Noncoding Variant Associations with Sulcal Patterns in Congenital Heart Disease. Available at SSRN: https://ssrn.com/abstract=4845174 or http://dx.doi.org/10.2139/ssrn.4845174 
```