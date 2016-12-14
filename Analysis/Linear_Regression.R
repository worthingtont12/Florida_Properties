library(readr)
library(car)
require(leaps)
require(MASS)
library("DAAG")
library(Amelia)

#Importing dataframe
df_known <- read_csv("/Users/tylerworthington/Downloads/df_cleaned.csv")

#Data Cleaning
df_known <-df_known[df_known$residential == 'True', ]
df_known <- df_known[complete.cases(df_known$diff_btwn_prc_jv)==TRUE,]
df_known <-df_known[df_known$landuse_explained  == 'Single Family' ,]
df_known <-df_known[df_known$sale_prc1 > 10 ,]
summary(df_known$diff_btwn_prc_jv)
df_known <- subset(df_known , !duplicated(phy_addr1))
df_known <-df_known[df_known$sale_prc1 < 542200000 ,]
df_known <-df_known[df_known$jv > 2 ,]
df_known <- subset(df_known , !duplicated(phy_addr1))
df_known <- subset(df_known, !duplicated(subset(df_known, select=c(census_tract, act_age, sale_prc1))))

#results of data cleaning
summary(df_known$diff_btwn_prc_jv) 
sd(df_known$diff_btwn_prc_jv)

#missingness map
missmap(df_known)

#variable selection
regsubsets.out <-
  regsubsets(diff_btwn_prc_jv ~ bas_strt+pa_uc+lnd_sqfoot+no_buldng+const_class_explained+vi_cd1_explained+sale_season1+act_age+Blk_Val+TOT_POP+TOT_MED_AGE+PCT_M+M_MED_AGE+PCT_F+F_MED_AGE+AVG_HOUSE_SIZE+AVG_FAM_SIZE+HOME_VAC_RATE+RENT_VAC_RATE+AVG_H_SIZE_RENTER+PCT_UNEMP+TOT_FAM+PCT_FAM_POV+TOT_FAM_MARRIED+PCT_FAM_MARRIED_POV + TOT_FAM_F_ONLY+PCT_FAM_F_ONLY_POV+POV_RATE_NO_GED+POV_RATE_SOME_COL+POV_RATE_BACH_PLUS+PCT_H+PCT_WA+PCT_BA+PCT_AA+PCT_OTHER+PCT_TOT_POP_18+PCT_VAC_HOUSE+PCT_FAM+PCT_FAM_MARRIED,
             data = df_known,
             nbest = 1,       # 1 best model for each number of predictors
             nvmax = NULL,    # NULL for no limit on number of variables
             force.in = NULL, force.out = NULL,
             method = "exhaustive")
regsubsets.out

summary.out <- summary(regsubsets.out)
y <- as.data.frame(summary.out$outmat)

x <- as.data.frame(summary.out$which[which.max(summary.out$adjr2),])

#Model Building
lm1 <- lm(diff_btwn_prc_jv ~lnd_sqfoot + no_buldng + const_class_explained + vi_cd1_explained + sale_season1 + act_age +
            Blk_Val + TOT_POP + PCT_F + AVG_HOUSE_SIZE + AVG_FAM_SIZE + AVG_H_SIZE_RENTER + PCT_FAM_POV + TOT_FAM_MARRIED
          + PCT_FAM_MARRIED_POV + POV_RATE_SOME_COL + PCT_WA + PCT_AA + PCT_OTHER + PCT_TOT_POP_18 + PCT_FAM + PCT_FAM_MARRIED, data=df_known) 

summary(lm1)
vif(lm1)

#multicollinearity testing
lm2 <- lm(diff_btwn_prc_jv ~lnd_sqfoot + no_buldng + vi_cd1_explained + sale_season1 + act_age + Blk_Val + AVG_H_SIZE_RENTER 
          + POV_RATE_SOME_COL+ PCT_WA + PCT_AA + PCT_OTHER, data=df_known) 

vif(lm2)
summary(lm2)

#residual Analysis
#qqplot
qqnorm(rstudent(lm2))
qqline(rstudent(lm2))

#predicted vs residuals
plot(lm2$fitted.values,rstudent(lm2))
abline(a=0,b=0)


#cross validation
df_sub <- subset(df_known, select = c(diff_btwn_prc_jv,lnd_sqfoot,no_buldng,vi_cd1_explained,
                                      sale_season1,act_age,Blk_Val,AVG_H_SIZE_RENTER,POV_RATE_SOME_COL,
                                      PCT_WA,PCT_AA,PCT_OTHER))
df_sub <- df_sub[complete.cases(df_sub)==TRUE,]
cv.lm(data=df_sub, form.lm=lm2, m=5, plotit=F)
