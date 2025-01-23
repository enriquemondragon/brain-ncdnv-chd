#========================================#
#       Getting the nearest gene         #
#========================================#
# code snippet
library(GenomicRanges)
library(ChIPpeakAnno) 
library(TxDb.Hsapiens.UCSC.hg38.knownGene)

prioritized_variants <- read.table("/file/to/prioritized_variants.bed", stringsAsFactors = F)

colnames(prioritized_variants) <- c("seqnames", "start", "end")

# from dataframe to Granges
myPeakList <- makeGRangesFromDataFrame(prioritized_variants,
                                       ignore.strand = T, start.field = "start", 
                                       end.field = "end", seqnames.field = "seqnames")
# annotation data
annoData <- toGRanges(TxDb.Hsapiens.UCSC.hg38.knownGene, 
                      feature = "gene")

nearest_annotation <-  annotatePeakInBatch(myPeakList, AnnotationData = annoData, 
                                           output = "nearestLocation",
                                           multiple = FALSE, maxgap=-1L, 
                                           PeakLocForDistance = "middle",
                                           FeatureLocForDistance = "TSS",
                                           select = "all",
                                           ignore.strand = TRUE)

annotated_nearest_gene <- addGeneIDs(annotatedPeak = nearest_annotation,
                                     orgAnn = "org.Hs.eg.db",
                                     feature_id_type = "entrez_id",
                                     IDs2Add = "symbol")

file_for_go <- data.frame(annotated_nearest_gene)

colnames(file_for_go)[(ncol(file_for_go)-8):ncol(file_for_go)] <- c("nearest_entrez", 
                                                                       "nearest_start", 
                                                                       "nearest_end", 
                                                                       "nearest_strand", 
                                                                       "nearest_position", 
                                                                       "nearest_distance", 
                                                                       "nearest_shortest", 
                                                                       "nearest_category",
                                                                       "nearest_gene")
