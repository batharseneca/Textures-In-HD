


HDx <- rnorm(300,3,0.5)

HDy <- rnorm(300,3,0.5)


HDlab <- c(rep("HD",300))


NOx <- rnorm(300,1,0.5)

Noy <- rnorm(300,1,0.5)

NOlab <- c(rep("NO",300))



HD.df <- data.frame(HDx,HDy,HDlab)

names(HD.df) <- c("x","y","label")

NO.df <- data.frame(NOx,Noy,NOlab)
names(NO.df) <- c("x","y","label")



dframe <- rbind(HD.df,NO.df)




library(ggplot2)

getwd()


?png

setwd("C:/Users/Nishanth/Documents/ImageAnalysis-IGP/GUI_Random/")

png("sampleGraph.png",width=500,height=500,units="px")


g <- ggplot(data=dframe,aes(x=x,y=y))
g <- g + geom_point(aes(color=label),size=5,alpha=0.3) + geom_point(color="black",size=2,alpha=1)
g <- g + theme_bw() + xlab("Texture Feature 1") + ylab("Texture Feature 2")
g <- g + scale_colour_discrete(name="Diseased Condition",breaks=c("HD","NO"),labels=c("Diseased","Healthy"))
g <- g+theme(axis.text=element_text(size=12),axis.title=element_text(size=14,face="bold"))
g <- g + theme(axis.line = element_line(colour = "black"),
               panel.grid.major = element_blank(),
               panel.grid.minor = element_blank(),
               panel.background = element_blank())

g

dev.off()
