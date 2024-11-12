#install.packages('BiocManager') 
#BiocManager::install('WGCNA')
library("WGCNA")
args=commandArgs(trailingOnly = TRUE)

data_csv = args[1]
gene <- read.csv(data_csv, row.names = 1, check.names = FALSE)

#可选过滤低表达值的基因，例如只保留平均表达值在1以上的
gene <- subset(gene, rowSums(gene)/ncol(gene) >= 1)

#筛选中位绝对偏差前75%的基因，至少MAD大于0.01
m.mad <- apply(gene,1,mad)
geneVar <- gene[which(m.mad > max(quantile(m.mad, probs=seq(0, 1, 0.25))[2],0.01)),]
gene <- as.data.frame(t(geneVar))

#检测缺失值
gsg = goodSamplesGenes(gene, verbose = 3)
gsg$allOK
if (!gsg$allOK){
  if (sum(!gsg$goodGenes)>0) 
    printFlush(paste("Removing genes:", 
                     paste(names(gene)[!gsg$goodGenes], collapse = ",")));
  if (sum(!gsg$goodSamples)>0) 
    printFlush(paste("Removing samples:", 
                     paste(rownames(gene)[!gsg$goodSamples], collapse = ",")));
  gene = gene[gsg$goodSamples, gsg$goodGenes]
}

nGenes = ncol(gene)
nSamples = nrow(gene)
dim(gene)
head(gene)[,1:8]

#检查离散样品
pdf("1.样本离散检测.pdf")
sampleTree = hclust(dist(gene), method = "average")
plot(sampleTree, main = "Sample clustering to detect outliers", sub="", xlab="", cex.lab = 1.5,cex.axis = 1.5, cex.main = 2)
dev.off()

#确定软阈值
powers = c(c(1:10), seq(from = 12, to=30, by=2))
sft <- pickSoftThreshold(gene, powerVector = powers, verbose = 5)

#拟合指数与power值散点图
pdf("2.软阈值power筛选.pdf")
plot(sft$fitIndices[,1], -sign(sft$fitIndices[,3])*sft$fitIndices[,2], type = 'n',xlab = 'Soft Threshold (power)', 
ylab = 'Scale Free Topology Model Fit,signed R^2',main = paste('Scale independence'))
text(sft$fitIndices[,1], -sign(sft$fitIndices[,3])*sft$fitIndices[,2],labels = powers, col = 'red');
abline(h = 0.90, col = 'red')
#平均连通性与power值散点图
plot(sft$fitIndices[,1], sft$fitIndices[,5],
xlab = 'Soft Threshold (power)', ylab = 'Mean Connectivity', type = 'n',main = paste('Mean connectivity'))
text(sft$fitIndices[,1], sft$fitIndices[,5], labels = powers, col = 'red')
dev.off()

#确定powers值
powers <- sft$powerEstimate
powers = 18
#经验power (无满足条件的power时选用)
if (is.na(power)){
  power = ifelse(nSamples<20, ifelse(type == "unsigned", 9, 18),
          ifelse(nSamples<30, ifelse(type == "unsigned", 8, 16),
          ifelse(nSamples<40, ifelse(type == "unsigned", 7, 14),
          ifelse(type == "unsigned", 6, 12))       
          )
          )
}

adjacency <- adjacency(gene, power = powers)
tom_sim <- TOMsimilarity(adjacency)
rownames(tom_sim) <- rownames(adjacency)
colnames(tom_sim) <- colnames(adjacency)
tom_sim[1:6,1:6]

#输出拓扑矩阵
#write.table(tom_sim, '2.TOMsimilarity.txt', sep = '\t', col.names = NA, quote = FALSE)

#查看此时的网络的无标度拓扑特征
k <- softConnectivity(datE = gene, power = powers)
pdf("3.拓扑特征.pdf")
par(mfrow = c(1, 2))
hist(k) #会呈现一种幂律分布的状态
scaleFreePlot(k, main = 'Check Scale free topology')
dev.off()

#共表达模块划分 相异度 = 1 - 相似度
tom_dis  <- 1 - tom_sim
#层次聚类树，使用中值的非权重成对组法的平均聚合聚类
geneTree <- hclust(as.dist(tom_dis), method = 'average')
pdf("4.层次聚类树.pdf")
plot(geneTree, xlab = '', sub = '', main = 'Gene clustering on TOM-based dissimilarity', labels = FALSE, hang = 0.04)
dev.off()

#使用动态剪切树挖掘模块，详情 ?cutreeDynamic
minModuleSize <- 30  #模块基因数目
dynamicMods <- cutreeDynamic(dendro = geneTree, distM = tom_dis,deepSplit = 2, pamRespectsDendro = FALSE, minClusterSize = minModuleSize)
table(dynamicMods)

#模块颜色指代
dynamicColors <- labels2colors(dynamicMods)
table(dynamicColors)
pdf("5.模块分类.pdf")
plotDendroAndColors(geneTree, dynamicColors, 'Dynamic Tree Cut',dendroLabels = FALSE, addGuide = TRUE, hang = 0.03, guideHang = 0.05,
main = 'Gene dendrogram and module colors')
dev.off()


#基因表达聚类树和共表达拓扑热图，详情 ?TOMplot
plot_sim <- -(1-tom_sim)
#plot_sim <- log(tom_sim)
diag(plot_sim) <- NA
png("6.可视化基因网络.png")
TOMplot(plot_sim, geneTree, dynamicColors,main = 'Network heatmap plot, selected genes') 
dev.off()

##模块特征基因
#计算基因表达矩阵中模块的特征基因（第一主成分），详情 ?moduleEigengenes
MEList <- moduleEigengenes(gene, colors = dynamicColors)
MEs <- MEList$eigengenes
head(MEs)[1:6]

#输出模块特征基因矩阵
write.table(MEs, '7.moduleEigengenes.txt', sep = '\t', col.names = NA, quote = FALSE)

##共表达模块的进一步聚类
#通过模块特征基因计算模块间相关性，表征模块间相似度
ME_cor <- cor(MEs)
ME_cor[1:6,1:6]

#绘制聚类树观察
METree <- hclust(as.dist(1-ME_cor), method = 'average')
pdf("7.聚类树.pdf")
plot(METree, main = 'Clustering of module eigengenes', xlab = '', sub = '')

#探索性分析，观察模块间的相似性
#height 值可代表模块间的相异度，并确定一个合适的阈值作为剪切高度
#以便为低相异度（高相似度）的模块合并提供依据
abline(h = 0.2, col = 'blue')
abline(h = 0.25, col = 'red')

#相似模块合并，以 0.25 作为合并阈值（剪切高度），在此高度下的模块将合并
#近似理解为相关程度高于 0.75 的模块将合并到一起
merge_module <- mergeCloseModules(gene, dynamicColors, cutHeight = 0.3, verbose = 3)
mergedColors <- merge_module$colors
table(mergedColors)

#基因表达和模块聚类树
plotDendroAndColors(geneTree, cbind(dynamicColors, mergedColors), c('Dynamic Tree Cut', 'Merged dynamic'),
    dendroLabels = FALSE, addGuide = TRUE, hang = 0.03, guideHang = 0.05)
dev.off()

png("6.可视化基因网络2.png")
TOMplot(plot_sim, geneTree, mergedColors,main = 'Network heatmap plot, selected genes') 
dev.off()

pdf("8.合并后模块聚类.pdf")
plotDendroAndColors(geneTree, mergedColors,'Merged dynamic',
                    dendroLabels = FALSE, addGuide = TRUE, hang = 0.03, guideHang = 0.05)
dev.off()
write.csv(table(mergedColors),"5.模块分类.csv",row.names = FALSE)

dir.create('cytoscape', recursive = TRUE)

for (mod in 1:nrow(table(mergedColors))) {
    modules <- names(table(mergedColors))[mod]
    probes <- colnames(gene)
    inModule <- (mergedColors == modules)
    modProbes <- probes[inModule]
    modGenes <- modProbes
    modtom_sim <- tom_sim[inModule, inModule] 
    dimnames(modtom_sim) <- list(modProbes, modProbes)
    outEdge <- paste('cytoscape/', modules, '.edge_list.txt',sep = '')
    outNode <- paste('cytoscape/', modules, '.node_list.txt', sep = '')
    exportNetworkToCytoscape(modtom_sim,
        edgeFile = outEdge,
        nodeFile = outNode,
        weighted = TRUE,
        threshold = 0.3,  #该参数可控制输出的边数量，过滤低权重的边
        nodeNames = modProbes,
        altNodeNames = modGenes,
        nodeAttr = mergedColors[inModule])
}

dir.create("gene_heatmap",recursive = TRUE)

for (mod in 1:nrow(table(mergedColors))){
  modules <- names(table(mergedColors))[mod]
  if(modules == "grey") next
  ME=MEs[,paste("ME",modules,sep="")]
  pdf(paste("gene_heatmap/wgcna.", modules, ".express.barplot.pdf", sep=""))
  par(mfrow=c(2,1),mar=c(0.3,5.5,3,2))
  plotMat(t(scale(gene[,mergedColors==modules])), 
          nrgcols=30,rlabels=F,rcols=modules,main=modules,cex.main=2,clabels=rownames(gene))
  
  par(mar=c(5,4.2,0,0.7))
  barplot(ME,col=modules,main="",cex.main=2,ylab="eigengene expression",xlab="sample")
  dev.off()
}

##基因共表达模块与性状的关联分析
#患者的临床表型数据
# trait <- read.delim('trait.txt', row.names = 1, check.names = FALSE)

# #使用上一步新组合的共表达模块的结果
# module <- merge_module$newMEs

# #患者基因共表达模块和临床表型的相关性分析
# moduleTraitCor <- cor(module, trait, use = 'p')
# moduleTraitCor[1:6,1:6]  #相关矩阵

# #相关系数的 p 值矩阵
# moduleTraitPvalue <- corPvalueStudent(moduleTraitCor, nrow(module))

# #输出相关系数矩阵或 p 值矩阵
# #write.table(moduleTraitCor, 'moduleTraitCor.txt', sep = '\t', col.names = NA, quote = FALSE)
# #write.table(moduleTraitPvalue, 'moduleTraitPvalue.txt', sep = '\t', col.names = NA, quote = FALSE)

# #相关图绘制
# textMatrix <- paste(signif(moduleTraitCor, 2), '\n(', signif(moduleTraitPvalue, 1), ')', sep = '')
# dim(textMatrix) <- dim(moduleTraitCor)

# par(mar = c(5, 10, 3, 3))
# labeledHeatmap(Matrix = moduleTraitCor, main = paste('Module-trait relationships'), 
#     xLabels = names(trait), yLabels = names(module), ySymbols = names(module),
#     colorLabels = FALSE, colors = greenWhiteRed(50), cex.text = 0.7, zlim = c(-1,1), 
#     textMatrix = textMatrix, setStdMargins = FALSE)

# ##模块内基因的提取
# #基因与模块的对应关系列表
# gene_module <- data.frame(gene_name = colnames(gene), module = mergedColors, stringsAsFactors = FALSE)
# head(gene_module)

# #“black”模块内的基因名称
# gene_module_select <- subset(gene_module, module == 'black')$gene_name

# #“black”模块内基因在各样本中的表达值矩阵（基因表达值矩阵的一个子集）
# gene_select <- t(gene[,gene_module_select])

# #“black”模块内基因的共表达相似度（在 TOM 矩阵中提取子集）
# tom_select <- tom_sim[gene_module_select,gene_module_select]

# #输出
# #write.table(gene_select, 'gene_select.txt', sep = '\t', col.names = NA, quote = FALSE)
# #write.table(tom_select, 'tom_select.txt', sep = '\t', col.names = NA, quote = FALSE)

# ##重要基因的获得，以与 TNM 显著相关的 black 模块为例
# #选择 black 模块内的基因
# gene_black <- gene[ ,gene_module_select]

# #基因的模块成员度（module membership）计算
# #即各基因表达值与相应模块特征基因的相关性，其衡量了基因在全局网络中的位置
# geneModuleMembership <- signedKME(gene_black, module['MEblack'], outputColumnName = 'MM')
# MMPvalue <- as.data.frame(corPvalueStudent(as.matrix(geneModuleMembership), nrow(module)))

# #各基因表达值与临床表型的相关性分析
# geneTraitSignificance <- as.data.frame(cor(gene_black, trait['TNM'], use = 'p'))
# GSPvalue <- as.data.frame(corPvalueStudent(as.matrix(geneTraitSignificance), nrow(trait)))

# #选择显著（p<0.01）、高 black 模块成员度（MM>=0.8），与 TNM 表型高度相关（r>=0.8）的基因
# geneModuleMembership[geneModuleMembership<0.8 | MMPvalue>0.01] <- 0
# geneTraitSignificance[geneTraitSignificance<0.8 | MMPvalue>0.01] <- 0

# select <- cbind(geneModuleMembership, geneTraitSignificance)
# select <- subset(select, geneModuleMembership>=0.8 & geneTraitSignificance>=0.8)
# head(select)

# #候选基因与 TNM 分期的相关性散点图
# dir.create('black_TNM_cor', recursive = TRUE)
 
# for (i in rownames(select)) {
#     png(paste('black_TNM_cor/', i, '-TNM.png', sep = ''), 
#         width = 4, height = 4, res = 400, units = 'in', type = 'cairo')
#     plot(trait[ ,'TNM'], gene[ ,i], xlab = 'TNM', ylab = i, 
#         main = paste('MM_black = ', select[i,'MMblack'], '\ncor_TNM = ', select[i,'TNM']), cex = 0.8, pch = 20)
#     fit <- lm(gene[ ,i]~trait[ ,'TNM'])
#     lines(trait[ ,'TNM'], fitted(fit))
#     dev.off()
# }

# #候选基因间的 TOM 矩阵
# plotNetworkHeatmap(gene,
#     plotGenes = rownames(select),
#     networkType = 'unsigned',
#     useTOM = TRUE,
#     power = powers,
#     main = 'unsigned correlations')

##输出各模块子网络的边列表和节点列表，后续可导入 cytoscape 绘制网络图
#其中，边的权重为 TOM 矩阵中的值，记录了基因间共表达相似性
