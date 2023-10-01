#########################################################################
###### Create well presented scatterplots of Chromosome Statistics  #####
######                  A. philippi + A. werdermnni                 #####
#########################################################################
require(plot3D)
require(tcltk2)
require(ggplot2)
require(superheat)
require(fpc)
require(WVPlots)
require(vegan)
library("factoextra")
library("RColorBrewer")
library("viridis")
require('ape')
require("gplots")
require("ggExtra")
require("gridExtra")
require("svglite")

setwd(tk_choose.dir())

#First, lets build the E space and localize the position of the optimal niche 
a=read.csv(tk_choose.files()) #Extracted points from PC ascii
str(a)

df=a #Basic dataset
df=na.omit(df)
rownames(df)=as.vector(paste(df$Infrataxa,seq_len(nrow(df))))

#In case of a hurry, lets check the basic matrix and make a heatplot. In this way, you can evidence 
#quick similarity, checking on the data variation and R+Q clustering. Notice that I will eliminate C1 
#column, as this is univariate and no data provides for the calculation.
#x=scale(as.matrix(df[1:3])) #I will scale the data, as there are several magnitude of difference among variables.

brewer.pal.info #Check info of available palettes
display.brewer.all(n=NULL, 
                   type="qual") #Check available palettes
col <- colorRampPalette(brewer.pal(9, "Spectral"))(9)

str(df)
heatmap.2(as.matrix(df[,4:6]),
          scale     = "column",
          trace     = "none",
          col       = col,
          distfun   = function(x) vegdist(x, method="euclidean", na.rm = T, upper = TRUE), 
          hclustfun = function(x) hclust(x, method="ave"),
          margins=c(4,7), cexCol = 1, cexRow = 0.4)

##### Barplots ####
#We can use barplots to inspect the variables individually

par(mfrow=c(1,1))
ggplot(df, aes(x=Infrataxa, y=MCA, colour=Infrataxa)) + geom_boxplot() + 
  theme(axis.text.x = element_text(angle = 45))
ggplot(df, aes(x=Infrataxa, y=CVCL, colour=Infrataxa)) + geom_boxplot() +
  theme(axis.text.x = element_text(angle = 45))
ggplot(df, aes(x=Infrataxa, y=LTC, colour=Infrataxa)) + geom_boxplot() + 
  theme(axis.text.x = element_text(angle = 45))

# Also, we can use these values to integrate a multiple scatterplot and explore the data.

str(df)
PairPlot(df,
         colnames(df)[4:6],
         "Alstroemeria werdermani Chromosomes",
         group_var = "Infrataxa") +
  ggplot2::geom_point(size=0.1,colour="black")

#Add convex hull code for ggplot
find_hull <- function(df) df[chull(df$CVCL, df$MCA), ]
library(plyr)
#Apply funtion to delimit most external points in geometry 
hulls = ddply(df, ~Infrataxa, find_hull)
#Plot with geometric hull
p1=ggplot(df, aes(x=CVCL, y=MCA, shape=Infrataxa, colour=Infrataxa)) + 
  geom_point(size = 3) + 
  geom_polygon(data = hulls, alpha = 0.2) + 
  scale_shape_manual(values=c(15,16,17,18)) +
  scale_color_manual(values=c("#a6cee3", "#1f78b4", "#b2df8a", "#33a02c")) +
  scale_fill_manual(values=c("#a6cee3", "#1f78b4", "#b2df8a", "#33a02c")) + 
  geom_text(aes(label=Population, size=3))
  

# scale_fill_brewer(palette="Set2") + 
#  scale_color_brewer(palette="Set2")

plot(p1)

p11=p1 + labs (x="CVCL", y="MCA") + 
  theme_bw() +
  theme(legend.position = "none",
        axis.text.y=element_text(size=9),
        axis.text.x=element_text(size=9))

plot(p11)

g1=ggMarginal(p11, groupColour = T, groupFill = T, type = "boxplot")#set the right name axis

plot(g1)

#Repeat for other 2 axes

df=remove_missing(a,na.rm=T,vars=names(a))

#Add convex hull code for ggplot
find_hull <- function(df) df[chull(df$CVCL, df$LTC), ]
#Apply funtion to delimit most external points in geometry 
hulls = ddply(df, ~Infrataxa, find_hull)
#Plot with geometric hull
p2=ggplot(df, aes(x=CVCL, y=LTC, shape=Infrataxa, colour=Infrataxa)) + 
  geom_point(size = 3) + 
  geom_polygon(data = hulls, alpha = 0.2) + 
  scale_shape_manual(values=c(15,16,17,18)) +
  scale_color_manual(values=c("#a6cee3", "#1f78b4", "#b2df8a", "#33a02c")) +
  scale_fill_manual(values=c("#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"))+ 
  geom_text(aes(label=Population, size=3))

p12=p2 + labs (x="CVCL", y="LTC") + 
  theme_bw() +
  theme(legend.position = "none",
        axis.text.y=element_text(size=9),
        axis.text.x=element_text(size=9))
  
plot(p12)
g2=ggMarginal(p12, groupColour = T, groupFill = T, type = "boxplot")

plot(g2)

#Add convex hull code for ggplot
find_hull <- function(df) df[chull(df$MCA, df$LTC), ]
#Apply funtion to delimit most external points in geometry 
hulls = ddply(df, ~Infrataxa, find_hull)
#Plot with geometric hull
p3=ggplot(df, aes(x=MCA, y=LTC, shape=Infrataxa, colour=Infrataxa)) + 
  geom_point(size = 3) + 
  geom_polygon(data = hulls, alpha = 0.2) + 
  scale_shape_manual(values=c(15,16,17,18)) +
  scale_color_manual(values=c("#a6cee3", "#1f78b4", "#b2df8a", "#33a02c")) +
  scale_fill_manual(values=c("#a6cee3", "#1f78b4", "#b2df8a", "#33a02c")) + 
  geom_text(aes(label=Population, size=3))

p13=p3 + labs (x="MCA", y="LTC") + 
  theme_bw() +
  theme(legend.position = "none",
        axis.text.y=element_text(size=9),
        axis.text.x=element_text(size=9))

plot(p13)
g3=ggMarginal(p13, groupColour = T, groupFill = T, type = "boxplot")

plot(g3)

grid.arrange(g1, g2, g3, nrow=2, ncol=2)

# Export the graph as svg
svglite("results_werdermannii.svg", fix_text_size = F)
grid.arrange(g1, g2, g3, nrow=2, ncol=2)
dev.off()

#### Statistical Testing ####
# Non parametric test of multiple modes (Kruskall-Wallis + Dunn Test)
require(dunn.test)

dunn.test(df$MCA, df$Infrataxa, method="bonferroni", list = T)
dunn.test(df$CVCL, df$Infrataxa, method="bonferroni", list = T)
dunn.test(df$LTC, df$Infrataxa, method="bonferroni", list = T)


# Parametric test of discrimination (LDA) 

# Assumption 1: Equal variance and ellipse covariance
#df$Infrataxa=gsub("A_philippi_adrianae","A_phi_ad",df$Infrataxa)

heplots::covEllipses(log10(df[,4:6]), 
                     df$Infrataxa, 
                     fill = TRUE, 
                     pooled = FALSE, 
                     fill.alpha = 0.05,
                     variables = 1:3)

boxm <- heplots::boxM(df[, 4:6], df$Infrataxa)
boxm
plot(boxm)

require(MASS)
require(Momocs)
fit=lda(df$Infrataxa ~ df$MCA + df$CVCL + df$LTC, 
        na.action="na.omit", CV=T)
str(fit)

a=table(df$Infrataxa,fit$class, dnn= c("LDA","Morfologia"))

#svglite("Valid_LDA.svg", pointsize = 18, fix_text_size = F, system_fonts ="Arimo")
plot_CV(a, freq=TRUE, 
        rm0=FALSE, 
        fill=TRUE, 
        labels = TRUE,
        cell.size = 3) + ggplot2::ggtitle("LDA Validation")
#dev.off()

# Unsupervised classification test based on Gaussian Modelling
require(mclust)
require(clustvarsel)

NDMclust = Mclust(df[, 4:6])

#read your result in detail 
summary(NDMclust) #There are 4 significant clusters based on a combination of 3 criteria (VVV)
#inspeccionemos la estimacion de mclust
plot(NDMclust, what = "BIC")             #Modelo de elipticidad mas ajustado a los datos
plot(NDMclust, what = "classification")  #Clasificacion propuesta por mclust
plot(NDMclust, what = "uncertainty")     #Puntos considerados "inciertos" dentro de la clasificacion propuesta
plot(NDMclust, what = "density", type="hd")         #Densidad de los grupos estimados
names(NDMclust)
a=table(df$Infrataxa,NDMclust$classification, dnn= c("MCLUST","Morfologia"))

#svglite("Valid_MCLUST.svg", pointsize = 18, fix_text_size = F, scaling = 1.5)
plot_CV(a, freq=TRUE, 
        rm0=FALSE, 
        fill=TRUE, 
        labels = TRUE) + ggplot2::ggtitle("MCLUST validation")
#dev.off()
sum(diag(prop.table(table(df$Infrataxa, NDMclust$classification)))) #Porcentage predicho