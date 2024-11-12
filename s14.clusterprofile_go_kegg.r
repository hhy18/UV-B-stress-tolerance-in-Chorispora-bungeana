
#	1. 本脚本适用于非模式物种的富集分析
#	2. 运行本脚本需要执行s11,s12,s13脚本获得clusterprofile识别的注释文件
#	3. 需要文件go_annotation.txt, pathway_annotation.txt

library(clusterProfiler)
library(enrichplot)
library(argparser)

#传入参数
argv <- arg_parser('根据genelist进行GO富集分析')
argv <- add_argument(argv, "--genefile",  help = "基因列表，每一行一个基因")
argv <- add_argument(argv,"--backgroud",help="背景基因集注释文件，三行")
argv <- add_argument(argv, "--prefix", help = "结果文件输出前缀")
argv <- parse_args(argv)

genefile <- argv$genefile
prefix <- argv$prefix
backgroud <- argv$backgroud

# 读取进行GO富集分析的目标基因集
gene = read.table(genefile,header=F)
gene = gene$V1

# 读取注释信息及富集分析
data <- read.table(backgroud,header = T,sep = "\t")
go2gene <- data[, c(2, 1)]
go2name <- data[, c(2, 3)]
enrich <- enricher(gene,pAdjustMethod="none",pvalueCutoff = 0.05, TERM2GENE = go2gene,TERM2NAME = go2name)
print(enrich)

# 保存富集分析结果
write.table(enrich, file = paste(prefix, '.enrich.xls', sep = ''), sep = '\t',quote = F, row.names = F)

# 条形图
pdf("1.barplot.pdf")
barplot(enrich, showCategory=20)
dev.off()

#气泡图
pdf("2.dotplot.pdf")
dotplot(enrich, showCategory = 20)
dev.off()

pdf("3.cnetplot.pdf")
cnetplot(enrich,circular = TRUE, colorEdge = TRUE)
dev.off()

pdf("4.heatmap.pdf")
heatplot(enrich)
dev.off()


pdf("5.upset.pdf")
upsetplot(enrich)
dev.off()
