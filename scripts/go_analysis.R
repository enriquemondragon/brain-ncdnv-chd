#==============================================================================#
#                         Gene set enrichment analysis                         #
#==============================================================================#
# Author: Mondragon-Estrada E. et al.
# Last reviewed: April 2024
# Copyright (c) Mondragon-Estrada E. et al., 2024
#===============================================================================

library(dplyr)
library(clusterProfiler)
library(biomaRt)
library(org.Hs.eg.db) 

load("/home/enrique/Documents/P1_Sulcal/code/Gene_ontology_enrichment/protein_all_anno_14Nov18.rda")
load("/home/enrique/Documents/P1_Sulcal/code/Gene_ontology_enrichment/protein_all_tm_26Dec22.rda")

exp1_loc <- read.csv("/home/enrique/Documents/P1_Sulcal/code/Gene_ontology_enrichment/data/h3k9me2_enformer.csv", stringsAsFactors = F)
exp1_loc[1,]
exp1_loc$VarID <- paste(exp1_loc$chr, exp1_loc$pos, sep = "_") 

#========================================#
#     extract top ncDNVs per patient     #
#========================================#

length(unique(exp1_loc$ID)) # 1814 patients
IDs<-unique(exp1_loc$ID)

nvar<-NULL
exp1_loc_temp<-data.frame(matrix(ncol=ncol(exp1_loc),nrow=0))
colnames(exp1_loc_temp) = colnames(exp1_loc)
for (id in IDs){
  n<-dim(exp1_loc[exp1_loc$ID==id,])[1]
  nvar<-append(nvar,n)
  temp<-exp1_loc[exp1_loc$ID==id,]
  ix<-which.max(temp$CHIP_H3K9me2_neural_cell)
  exp1_loc_temp<-rbind(exp1_loc_temp,temp[ix,])
  
}
exp1_loc<-exp1_loc_temp
rm(exp1_loc_temp)

#========================================#
#        multi-hit genes by ncDNVs       #
#========================================#

topmed_freeze1v2_annotated.bed$VarID <- paste(topmed_freeze1v2_annotated.bed$seqnames, topmed_freeze1v2_annotated.bed$end, sep = "_")
topmed_nearest <- topmed_freeze1v2_annotated.bed[!duplicated(topmed_freeze1v2_annotated.bed$VarID),]

gmkf_annotated.bed$VarID <- paste(gmkf_annotated.bed$Chrom, gmkf_annotated.bed$end, sep = "_")
gmkf_nearest <- gmkf_annotated.bed[!duplicated(gmkf_annotated.bed$VarID),]

all_chd_genes <- unique(c(topmed_freeze1v2_annotated.bed$nearest_gene, gmkf_annotated.bed$nearest_gene))
length(all_chd_genes)

for(i in 1:nrow(exp1_loc)){
  if(exp1_loc$VarID[i] %in% gmkf_nearest$VarID){
    exp1_loc$nearest_gene[i] <- gmkf_nearest$nearest_gene[gmkf_nearest$VarID==exp1_loc$VarID[i]]
  } else if(exp1_loc$VarID[i] %in% topmed_nearest$VarID){
    exp1_loc$nearest_gene[i] <- topmed_nearest$nearest_gene[topmed_nearest$VarID==exp1_loc$VarID[i]]
  } else{
    exp1_loc$nearest_gene[i] <- "NA"
  }
}
exp1_gene_list <- unique(exp1_loc$nearest_gene)
exp1_gene_count <- dplyr::count(exp1_loc, nearest_gene)

gene_count <- exp1_gene_count
gene_count[is.na(gene_count)] <- 0
gene_count <- gene_count[!gene_count$nearest_gene=="NA",]

#========================================#
#                GO analysis             #
#========================================#

listEnsembl()

mart <- useDataset("hsapiens_gene_ensembl",
                   useMart('ENSEMBL_MART_ENSEMBL',
                           host =  'https://grch37.ensembl.org'))
exp1_ensembl <- getBM(filters = "external_gene_name",
                      values = gene_count$nearest_gene[gene_count$n>1], attributes = c("ensembl_gene_id", "external_gene_name"), mart = mart)

all_chd_genes_ensembl <- getBM(filters = "external_gene_name",
                           values = all_chd_genes,
                           attributes = c("ensembl_gene_id", "external_gene_name"),
                           mart = mart)

all_genes_ensembl <- getBM(filters = "external_gene_name",
                               values = gene_count$nearest_gene,
                               attributes = c("ensembl_gene_id", "external_gene_name"),
                               mart = mart)

ego <- enrichGO(gene=exp1_ensembl$ensembl_gene_id, universe=all_chd_genes_ensembl$ensembl_gene_id, OrgDb=org.Hs.eg.db, ont="BP", keyType="ENSEMBL", pAdjustMethod = "BH", qvalueCutoff =0.05, readable=TRUE)
ego2 <- as.data.frame(ego)
cluster_summary <- summary(ego2)
dotplot(ego, showCategory=1000)