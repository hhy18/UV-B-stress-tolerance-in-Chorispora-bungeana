# 对有3个平行的样品进行差异分析 前为对照组-后为处理组 
# 注意 列名顺序跟样品信息 sampleGroup 的行名顺序是一致的
# 使用方法： Rscript s8.deseq2.r data_csv SampleGroup out_csv

library(DESeq2)
library(tidyverse)

args=commandArgs(trailingOnly = TRUE)
data_csv = args[1]
SampleGroup = args[2]
out_csv = args[3]

# 输入数据
countData =read.csv(data_csv,encoding = "UTF-8",header = T)
rownames(countData)=countData[,1]
countData = countData[,-1]
head(countData)

sampleGroup <- read.table(SampleGroup, header = TRUE)
sampleGroup$Group <- factor(sampleGroup$Group, levels = c("Control", "Treatment"))
print(sampleGroup$Group)
# condition <- factor(c("WT","WT","WT","OE","OE","OE"))
# colData <- data.frame(row.names=colnames(countData), condition)

#构建dds
dds = DESeqDataSetFromMatrix(countData = countData,colData = sampleGroup,design = ~Group)
dds=DESeq(dds)

res=results(dds)
res=res[order(res$padj),]
summary(res)

selectresult=subset(res,(log2FoldChange > 1|-log2FoldChange>1)&padj<0.05)
summary(selectresult)
write.table(selectresult,file=out_csv,sep="\t",row.name=T)
print("run completed!!!")
