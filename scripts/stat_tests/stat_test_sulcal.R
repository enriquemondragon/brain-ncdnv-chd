#========================================#
#   Regression models with sulcal data  #
#========================================#
# By Enrique Mondragon Estrada, March 2024

getwd();
workingDir = "/path/to/working/dir";
setwd(workingDir);

library(ggplot2)
library(RColorBrewer)

data4lm <- read.csv("/path/to/sulcal_data.csv", sep=",");

N_SULCAL_TRAITS <- 50
extra_cols <- ncol(data4lm) - N_SULCAL_TRAITS
results <- data.frame(matrix(nrow = N_SULCAL_TRAITS, ncol = 7)) 
colnames(results) <- c("area","lm1_chd_coeff","lm1_chd_pval","lm2_chd_coeff",
                     "lm2_chd_pval","lm2_magnet_coeff","lm2_magnet_pval")

# regression models
for (col in (extra_cols+1):ncol(data4lm)) {
  uni<-lm(data4lm[,col] ~ factor(data4lm$CHD))
  mult<-lm(data4lm[,col] ~ factor(data4lm$CHD) + factor(data4lm$Field))
  
  results$area[col-extra_cols] <- colnames(data4lm)[col]
  results$lm1_chd_coeff[col-extra_cols] <- summary(uni)$coefficients[2,1]
  results$lm1_chd_pval[col-extra_cols] <- summary(uni)$coefficients[2,4]
  results$lm2_chd_coeff[col-extra_cols] <- summary(mult)$coefficients[2,1]
  results$lm2_chd_pval[col-extra_cols] <- summary(mult)$coefficients[2,4]
  results$lm2_magnet_coeff[col-extra_cols] <- summary(mult)$coefficients[3,1]
  results$lm2_magnet_pval[col-extra_cols] <- summary(mult)$coefficients[3,4]
}

results$FDR_lm1_chd_pval <- p.adjust(results$lm1_chd_pval, method = "fdr")
results$FDR_lm2_chd_pval <- p.adjust(results$lm2_chd_pval, method = "fdr")
results$FDR_lm2_magnet_pval <- p.adjust(results$lm2_magnet_pval, method = "fdr")

results$different_lm1_chd_pval <- results$FDR_lm1_chd_pval<0.05
results$different_lm2_chd_pval <- results$FDR_lm2_chd_pval<0.05
results$different_lm2_magnet_pval <- results$FDR_lm2_magnet_pval<0.05
results$different_lm2 <- results$FDR_lm2_chd_pval<0.05 & results$FDR_lm2_magnet_pval<0.05

# volcano plot
results$region <- substr(results$area,start=1,stop=2)
results$measure <- substr(results$area,start=3,stop=length(results$area))
results$region <- as.factor(results$region)
colours <- brewer.pal(name="RdYlBu", n=rev(nlevels(results$region)))
names(colours) <- rev(levels(results$region))

p <- ggplot(results,
            aes(lm2_chd_coeff, -log10(FDR_lm2_chd_pval), label = area, 
                fill=region, color=region)) +
  geom_point(aes(colour = region, shape= measure),size = 5)

p + scale_shape_manual(values=c(21, 22, 21, 24,25)) +
  scale_fill_manual(values=colours) +
  scale_colour_manual(values=colours) +
  theme_classic() +
  annotate("text", x=-0.016, y=-log10(0.05)+0.006, 
           label="p-value=0.05 \n(FDR corrected)") +
  geom_hline(yintercept=-log10(0.05),linetype='dotted') +
  geom_vline(xintercept=-0.01,linetype='dotted') +
  geom_vline(xintercept=0.01,linetype='dotted') +
  xlab("Coefficients") + ylab("-log10(p-value)")

