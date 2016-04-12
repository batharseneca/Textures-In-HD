


setwd("/home/nmerwin/Documents/IGPProject/ImageAnalysis-IGP/D3")


data <- read.csv(list.files()[1],header = FALSE)


nhood5 <- data[grepl("nhood_5", data[,1]),]
nhood10 <- data[grepl("nhood_10", data[,1]),]
nhood20 <- data[grepl("nhood_20", data[,1]),]

formatted <- cbind(nhood5[,1],nhood5[,-1], nhood10[,-1], nhood20[-1])


HD <- grepl("q43",formatted[,1])
treated <- grepl("kinetin",formatted[,1])

formatted <- cbind(HD,treated,formatted)

dim(formatted)

# log.HD <- log1p(formatted[, 4:54])



haraNames <- c("Angular Second Moment", "Contrast","Inverse Difference Moment","Entropy", "X-Mean","Y-Mean","X-Standard Deviation", "Y-Standard Deviation", "Correlation","Mean","Variance","Sum Average","Sum Entropy","Difference Entropy","Inertia","Cluster Shade","Cluster Prominence")

nhood10Names <- sapply(haraNames, sub, pattern="^", replacement="10_", simplify=F)
nhood5Names <- sapply(haraNames, sub, pattern="^", replacement="5_", simplify=F)
nhood20Names <- sapply(haraNames, sub, pattern="^", replacement="20_", simplify=F)
allNames <- as.character(c(nhood5Names,nhood10Names,nhood20Names))
length(names(formatted)[4:54])
length(allNames)
names(formatted)[4:54] <- allNames


# apply PCA - scale. = TRUE is highly 
# advisable, but default is FALSE. 
ir.pca <- prcomp(formatted[,4:54],
                 center = TRUE,
                 scale. = TRUE) 


plot(ir.pca,type="l")
summary(ir.pca)
names(data)

sort(ir.pca$rotation[,"PC1"])

ir.pca$x

summary(ir.pca$rotation)

library(ggplot2)

str(ir.pca)

ir.pca$sdev^2

ir.pca$x
summary(ir.pca)

pca_data <- data.frame(ir.pca$x)


myGrouping <- function(HD,treated){
  if(HD & treated){
    return (c("HDTreated"))
  }
  else if(HD & (!treated)){
    return (c("HD"))
  }
  else if( (!HD) ){
    return (c("Healthy"))
  }
}

group <- mapply(myGrouping,HD,treated)
group
pca_data <- cbind(group,pca_data)

pca_data



sub(pattern="_nhood_5",replacement="", x=nhood5[,1][1])


?gsub


write.csv(pca_data, file="pca.csv", quote = F, sep=",",col.names=T, row.names=F)

?write.csv

g<- ggplot(data=pca_data, aes(x=PC1,y=PC2,color=group))
g <- g + geom_point(shape=1)
g

predict(ir.pca, 
        newdata=tail(log.ir, 2))











