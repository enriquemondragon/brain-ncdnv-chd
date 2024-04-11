#==============================================================================#
#                   Weighted Correlation Network Analysis:                     #
#                               Positive scores                                #
#==============================================================================#
# Author: Mondragon-Estrada E. et al.                                          #
# Last reviewed: April 2024                                                    #
# Copyright (c) Mondragon-Estrada E. et al., 2024                              #
#==============================================================================#

getwd();
workingDir = "/path/to/working/dir";
setwd(workingDir);

library(WGCNA);
options(stringsAsFactors = FALSE);

sadData = read.csv("/home/enrique/Documents/P1_Sulcal/WGCNA/data/maxbe/be/sad_match.csv",sep="\t");
dim(sadData);
names(sadData);

#========================================#
#              Data cleaning             #
#========================================#

datExpr0 = as.data.frame((sadData[, -c(1)])); # removing ID
names(datExpr0) = names(sadData[, -c(1)]);
rownames(datExpr0) = sadData$ID;

#========================================#
#             Data filtering             #
#========================================#

gsg = goodSamplesGenes(datExpr0, verbose = 3); 

if (!gsg$allOK)
{
  if (sum(!gsg$goodGenes)>0) 
    printFlush(paste("Removing genes:", paste(names(datExpr0)[!gsg$goodGenes], collapse = ", ")));
  if (sum(!gsg$goodSamples)>0) 
    printFlush(paste("Removing samples:", paste(rownames(datExpr0)[!gsg$goodSamples], collapse = ", ")));
  datExpr0 = datExpr0[gsg$goodSamples, gsg$goodGenes]
}

#========================================#
#         Hierarchical clustering        #
#========================================#

sampleTree = hclust(dist(datExpr0), method = "average"); 

sizeGrWindow(12,9)
par(cex = 0.6);
par(mar = c(0,4,2,0))
plot(sampleTree, main = "Sample clustering to detect outliers", sub="", xlab="", cex.lab = 1.5, 
     cex.axis = 1.5, cex.main = 2)

#========================================#
#             Remove outliers            #
#========================================#

abline(h = 2000, col = "red");
clust = cutreeStatic(sampleTree, cutHeight = 2000, minSize = 10)
table(clust)

keepSamples = (clust==1)
datExpr = datExpr0[keepSamples, ]
nGenes = ncol(datExpr)
nSamples = nrow(datExpr)

#========================================#
#              Read trait data           #
#========================================#

traitData = read.csv("/home/enrique/Documents/P1_Sulcal/WGCNA/data/maxminbe/sulcal_match.csv",sep="\t");

dim(traitData)
names(traitData)

#========================================#
#            Data cleaning               #
#========================================#

allTraits = traitData[, -c(2,3,4,5,6,57,58)];
dim(allTraits)
names(allTraits)

Samples = rownames(datExpr);
traitRows = match(Samples, allTraits$ID); 
datTraits = allTraits[traitRows, -1];
rownames(datTraits) = allTraits[traitRows, 1];

collectGarbage();

#========================================#
#  Sample dendrogram and trait heatmap   #
#========================================#

sampleTree2 = hclust(dist(datExpr), method = "average")
traitColors = numbers2colors(datTraits, signed = FALSE);

plotDendroAndColors(sampleTree2, traitColors,
                    groupLabels = names(datTraits), 
                    main = "Sample dendrogram and trait heatmap",
                    cex.colorLabels = 0.4)

#========================================#
#        Soft threshold β picking        #
#========================================#

powers = c(c(1:10), seq(from = 12, to=20, by=2))
sft = pickSoftThreshold(datExpr, powerVector = powers, verbose = 5, networkType = "signed hybrid")
sizeGrWindow(9, 5)
par(mfrow = c(1,2));
cex1 = 0.9;
# soft-thresholding power vs scale-free topology fit index
plot(sft$fitIndices[,1], -sign(sft$fitIndices[,3])*sft$fitIndices[,2],
     xlab="Soft Threshold (power)",ylab="Scale Free Topology Model Fit,signed R^2",type="n",
     main = paste("Scale independence"));
text(sft$fitIndices[,1], -sign(sft$fitIndices[,3])*sft$fitIndices[,2],
     labels=powers,cex=cex1,col="red");
abline(h=0.90,col="red")
# soft-thresholding power vs mean connectivity 
plot(sft$fitIndices[,1], sft$fitIndices[,5],
     xlab="Soft Threshold (power)",ylab="Mean Connectivity", type="n",
     main = paste("Mean connectivity"))
text(sft$fitIndices[,1], sft$fitIndices[,5], labels=powers, cex=cex1,col="red")

#========================================#
#           network construction         #
#========================================#

net = blockwiseModules(datExpr, power = 9, 
                       NetworkType=" signed hybrid", deepSplit=2,
                       TOMType = "signed", detectCutHeight=0.995,
                       minModuleSize = min(20, ncol(datExpr)/2),
                       reassignThreshold = 0, mergeCutHeight = 0.25, 
                       numericLabels = TRUE, pamRespectsDendro = FALSE,
                       saveTOMs = TRUE,
                       saveTOMFileBase = "CHDmaxTOM", 
                       verbose = 3)
names(net) 

table(net$colors) 

#========================================#
#      Dendrogram plot with modules      #
#========================================#

sizeGrWindow(12, 9)
mergedColors = labels2colors(net$colors)

plotDendroAndColors(net$dendrograms[[1]], mergedColors[net$blockGenes[[1]]],
                    "Module colors",
                    dendroLabels = FALSE, hang = 0.03,
                    addGuide = TRUE, guideHang = 0.05)

moduleLabels = net$colors
moduleColors = labels2colors(net$colors)
MEs = net$MEs;
geneTree = net$dendrograms[[1]];

#========================================#
#       Correlation's calculations       #
#========================================#

nGenes = ncol(datExpr);
nSamples = nrow(datExpr);
MEs0 = moduleEigengenes(datExpr, moduleColors)$eigengenes
MEs = orderMEs(MEs0)
moduleTraitCor = cor(MEs, datTraits, use = "p");
moduleTraitPvalue = corPvalueStudent(moduleTraitCor, nSamples);

# Multiple comparisons
alpha<-0.05
traits<-50
modules<-dim(MEs)[2]
tests<-traits*modules
# Bonferroni
sum(moduleTraitPvalue<alpha/tests)
which(moduleTraitPvalue<alpha/tests)
# FDR
sum(p.adjust(moduleTraitPvalue,method="fdr") < alpha)

#========================================#
#              Plot heat map             #
#========================================#

labels<-gsub(" ", "", paste("Positive", 1:dim(moduleTraitCor)[1]))
labels[length(labels)]<-"Non-module"

sizeGrWindow(20,6)
textMatrix =  paste(signif(moduleTraitCor, 2), "\n(",
                    signif(moduleTraitPvalue, 1), ")", sep = "");
dim(textMatrix) = dim(moduleTraitCor)
par(mar = c(6, 8.5, 3, 3));
labeledHeatmap(Matrix = moduleTraitCor,
               xLabels = names(datTraits),
               yLabels = names(MEs),
               ySymbols = labels,
               colorLabels = FALSE,
               colors = blueWhiteRed(50),
               textMatrix = ifelse(moduleTraitPvalue<alpha/tests,"*",""),
               textAdj = c(0.5,0.8),
               setStdMargins = FALSE,
               cex.text = 2.5,
               cex.lab.x = 0.8,
               zlim = c(-1,1),
               main = paste("Module-trait relationships"))
