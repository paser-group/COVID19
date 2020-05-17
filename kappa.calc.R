cat("\014") 
options(max.print=1000000)
t1 <- Sys.time()

library("psych")

# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/REPO_CATEG_RATING.csv"
# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/REPO_CATEG_CLOSED_CODING.csv"
# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/BUG_CATEG_OPEN_CODING.csv"
# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/BUG_CATEG_CLOSED_CODING.csv"
# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/ISSUE_LABELING_CLOSED_CODING.csv"
# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/FAR_ISSUE_LABELING_CLOSED_CODING.csv"
# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/FAR_BUG_CATEG_CLOSED_CODING.csv"
# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/FAR_REPO_CATEG_CLOSED_CODING.csv"

# AGREEMENT_FILE <- "/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/Microservices/SECDEV_WRITING/RATER_VERIFICATION.csv"

AGREEMENT_DF   <- read.csv(AGREEMENT_FILE)
# Two raters 
# AGREEMENT_DF   <- AGREEMENT_DF[ -c(1) ]

# Additional rater : Farzana vs Akond 
# AGREEMENT_DF   <- AGREEMENT_DF[ -c(1, 4) ]
# Additional rater : Farzana vs Effat 
AGREEMENT_DF   <- AGREEMENT_DF[ -c(1, 3) ]
print(head(AGREEMENT_DF))

KAPPA_SCORES <- cohen.kappa(AGREEMENT_DF)
print(KAPPA_SCORES)

t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))


# Kappa value interpretation Landis & Koch (1977):
# <0         No agreement
#  0 — .20   Slight
# .21 — .40  Fair
# .41 — .60  Moderate
# .61 — .80  Substantial
# .81–1.0    Perfect