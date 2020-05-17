cat("\014") 
options(max.print=1000000)
t1 <- Sys.time()

library(ggplot2)

OUT_FILE  <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/writing/COVID19/REPO_PER_WEEK.pdf"
REPO_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/WEEK_REPOS.csv"
REPO_DF   <- read.csv(REPO_FILE)
print(head(REPO_DF))


pdf(OUT_FILE, width=6, height=3)

the_plot <- ggplot(data=REPO_DF, aes(x=WEEK, y=COUNT, group=1)) + geom_line(color="red") + geom_point(size=0.1) +
  labs(x='Date', y='Count of projects') + 
  theme(text = element_text(size=9), axis.text.x = element_text(angle=45, hjust=1, size=9), axis.text.y = element_text(size=9), axis.title=element_text(size=9, face="bold")) +
  ggtitle('Count of COVID-19 software projects over time') + theme(plot.title = element_text(hjust = 0.5)) + 
  theme(legend.position="none")     

the_plot

dev.off()

t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))