setwd("C:/Users/hexel/Documents/R/SYS6018/CaseFinal/Florida_Properties/Data Cleaning")

suppressPackageStartupMessages({
  library(purrr)
  library(dplyr)
  library(lubridate)
  library(readr)
  library(stringr)
  require(doParallel)
  library(randomForest)
  library(e1071)
  library(Hmisc)
  library(knitr)
  library(ROCR)
})


# Load the dataframe
df_known <- read.csv("df_cleaned.csv")


# Clean the dataframe
df_known <- subset(df_known, select = -c(X,Unnamed..0_x,county,Unnamed..0_y,CENSUS_TRACT,census_bk))
df_known <- df_known[df_known$residential == 'True', ]
df_known <- df_known[complete.cases(df_known$diff_btwn_prc_jv)==TRUE,]
df_known <- df_known[df_known$landuse_explained  == 'Single Family' ,]
df_known <- df_known[df_known$sale_prc1 > 10 ,]
df_known <- subset(df_known , !duplicated(phy_addr1))
df_known <- df_known[df_known$sale_prc1 < 542200000 ,]
df_known <- df_known[df_known$jv > 2 ,]
df_known <- subset(df_known, !duplicated(phy_addr1))
df_known <- subset(df_known, !duplicated(subset(df_known, select=c(census_tract, act_age, sale_prc1))))


# Generate categorical response variable
df_known$overvalued <- as.factor(ifelse(df_known$diff_btwn_prc_jv > 0, "Overvalued", "Undervalued"))


# Subset the dataframe based on significant variables from linear model
dfSub <- subset(df_known, select = c(overvalued,lnd_sqfoot,no_buldng,vi_cd1_explained,
                                     sale_season1,act_age,Blk_Val,AVG_H_SIZE_RENTER,POV_RATE_SOME_COL,
                                     PCT_WA,PCT_AA,PCT_OTHER))


# Naive Bayes model selection subsets based on various feature categories
dfSub1 <- subset(df_known, select = c(overvalued,PCT_M,PCT_H,PCT_WA,PCT_BA,PCT_AA,PCT_OTHER,M_MED_AGE))

dfSub2 <- subset(df_known, select = c(overvalued,PCT_FAM,PCT_FAM_MARRIED,PCT_FAM_F_ONLY,PCT_FAM_F_ONLY_POV,PCT_FAM_MARRIED_POV,PCT_FAM_POV))

dfSub3 <- subset(df_known, select = c(overvalued,PCT_VAC_HOUSE,PCT_OCC_OWNER,AVG_HOUSE_SIZE,AVG_FAM_SIZE,AVG_H_SIZE_OWNER,AVG_H_SIZE_RENTER))

dfSub4 <- subset(df_known, select = c(overvalued,MHI_TOT,MHI_WA,MHI_BA,MHI_AA,MHI_H,MHI_OTHER))

dfSub5 <- subset(df_known, select = c(overvalued,PCT_LABOR,PCT_EMP,PCT_UNEMP))

dfSub6 <- subset(df_known, select = c(overvalued,Blk_Val,act_age,sale_season1,no_buldng,lnd_sqfoot,lnd_val))

dfSub7 <- subset(df_known, select = c(overvalued,POV_RATE_NO_GED,POV_RATE_GED,POV_RATE_SOME_COL,POV_RATE_BACH_PLUS))


# Testing of the NB subsets
dfSub1 %>%
  names %>%
  discard(~. == "overvalued") %>%
  combo_chr -> combos
set.seed(0451) # consistent runs
dfSub1 %>%
  full_test ->
  res1

dfSub2 %>%
  names %>%
  discard(~. == "overvalued") %>%
  combo_chr -> combos
set.seed(0451) # consistent runs
dfSub2 %>%
  full_test ->
  res2

dfSub3 %>%
  names %>%
  discard(~. == "overvalued") %>%
  combo_chr -> combos
set.seed(0451) # consistent runs
dfSub3 %>%
  full_test ->
  res3

dfSub4 %>%
  names %>%
  discard(~. == "overvalued") %>%
  combo_chr -> combos
set.seed(0451) # consistent runs
dfSub4 %>%
  full_test ->
  res4

dfSub5 %>%
  names %>%
  discard(~. == "overvalued") %>%
  combo_chr -> combos
set.seed(0451) # consistent runs
dfSub5 %>%
  full_test ->
  res5

dfSub6 %>%
  names %>%
  discard(~. == "overvalued") %>%
  combo_chr -> combos
set.seed(0451) # consistent runs
dfSub6 %>%
  full_test ->
  res6

dfSub7 %>%
  names %>%
  discard(~. == "overvalued") %>%
  combo_chr -> combos
set.seed(0451) # consistent runs
dfSub7 %>%
  full_test ->
  res7


# Save the results
saveRDS(res, "res_from_linear.rds")
saveRDS(res1, "res1.rds")
saveRDS(res2, "res2.rds")
saveRDS(res3, "res3.rds")
saveRDS(res4, "res4.rds")
saveRDS(res5, "res5.rds")
saveRDS(res6, "res6.rds")
saveRDS(res7, "res7.rds")


# Open RDS files
res <- readRDS("res_from_linear.rds")
res1 <- readRDS("res1.rds")
res2 <- readRDS("res2.rds")
res3 <- readRDS("res3.rds")
res4 <- readRDS("res4.rds")
res5 <- readRDS("res5.rds")
res6 <- readRDS("res6.rds")
res7 <- readRDS("res7.rds")

# Checking balanced error and accuracy of best models selected
res7 %>% arrange(BalancedErrorRate) %>% kable(format = "markdown") %>% head(7)
'''
|Formula                                                                                                                                |  Accuracy| BalancedErrorRate|
|:--------------------------------------------------------------------------------------------------------------------------------------|---------:|-----------------:|
|overvalued ~ vi_cd1_explained + sale_season1 + act_age + Blk_Val + AVG_H_SIZE_RENTER + POV_RATE_SOME_COL + PCT_WA + PCT_OTHER          | 0.5669514|         0.4330486|
|overvalued ~ vi_cd1_explained + act_age + Blk_Val + AVG_H_SIZE_RENTER + POV_RATE_SOME_COL + PCT_WA + PCT_OTHER                         | 0.5666091|         0.4333909|
|overvalued ~ vi_cd1_explained + sale_season1 + act_age + Blk_Val + AVG_H_SIZE_RENTER + POV_RATE_SOME_COL + PCT_WA + PCT_AA + PCT_OTHER | 0.5665810|         0.4334190|
|:--------------------------------------------------------------------------------------------------------------------------------------|---------:|-----------------:|
|overvalued ~ PCT_M + PCT_WA + PCT_BA + PCT_AA + PCT_OTHER + M_MED_AGE                                                                  | 0.5455528|         0.4544472|
|overvalued ~ PCT_M + PCT_H + PCT_WA + PCT_BA + PCT_AA + PCT_OTHER + M_MED_AGE                                                          | 0.5454956|         0.4545044|
|overvalued ~ PCT_M + PCT_WA + PCT_BA + PCT_OTHER + M_MED_AGE                                                                           | 0.5451395|         0.4548605|
|:--------------------------------------------------------------------------------------------------------------------------------------|---------:|-----------------:|
|overvalued ~ PCT_FAM + PCT_FAM_MARRIED + PCT_FAM_F_ONLY + PCT_FAM_F_ONLY_POV + PCT_FAM_MARRIED_POV + PCT_FAM_POV                       | 0.5546130|         0.4453870|
|overvalued ~ PCT_FAM + PCT_FAM_MARRIED + PCT_FAM_F_ONLY + PCT_FAM_MARRIED_POV + PCT_FAM_POV                                            | 0.5540895|         0.4459105|
|overvalued ~ PCT_FAM_MARRIED + PCT_FAM_F_ONLY + PCT_FAM_F_ONLY_POV + PCT_FAM_MARRIED_POV + PCT_FAM_POV                                 | 0.5540384|         0.4459616|
|:--------------------------------------------------------------------------------------------------------------------------------------|---------:|-----------------:|
|overvalued ~ PCT_VAC_HOUSE + PCT_OCC_OWNER + AVG_HOUSE_SIZE + AVG_FAM_SIZE + AVG_H_SIZE_OWNER + AVG_H_SIZE_RENTER                      | 0.5134835|         0.4865165|
|overvalued ~ PCT_VAC_HOUSE + PCT_OCC_OWNER + AVG_HOUSE_SIZE + AVG_FAM_SIZE + AVG_H_SIZE_OWNER                                          | 0.5122702|         0.4877298|
|overvalued ~ PCT_VAC_HOUSE + PCT_OCC_OWNER + AVG_FAM_SIZE + AVG_H_SIZE_OWNER + AVG_H_SIZE_RENTER                                       | 0.5115399|         0.4884601|
|:--------------------------------------------------------------------------------------------------------------------------------------|---------:|-----------------:|
|overvalued ~ MHI_TOT + MHI_WA + MHI_BA + MHI_AA + MHI_H + MHI_OTHER                                                                    | 0.5620242|         0.4379758|
|overvalued ~ MHI_TOT + MHI_WA + MHI_BA + MHI_AA + MHI_H                                                                                | 0.5557763|         0.4442237|
|overvalued ~ MHI_TOT + MHI_WA + MHI_AA + MHI_H + MHI_OTHER                                                                             | 0.5487707|         0.4512293|
|:--------------------------------------------------------------------------------------------------------------------------------------|---------:|-----------------:|
|overvalued ~ PCT_LABOR + PCT_EMP + PCT_UNEMP                                                                                           | 0.5176647|         0.4823353|
|overvalued ~ PCT_LABOR + PCT_UNEMP                                                                                                     | 0.5171602|         0.4828398|
|overvalued ~ PCT_EMP + PCT_UNEMP                                                                                                       | 0.5167965|         0.4832035|
|:--------------------------------------------------------------------------------------------------------------------------------------|---------:|-----------------:|
|overvalued ~ Blk_Val + act_age + sale_season1 + lnd_val                                                                                | 0.5782387|         0.4217613|
|overvalued ~ Blk_Val + act_age + lnd_val                                                                                               | 0.5767893|         0.4232107|
|overvalued ~ Blk_Val + act_age + lnd_sqfoot + lnd_val                                                                                  | 0.5682869|         0.4317131|
|:--------------------------------------------------------------------------------------------------------------------------------------|---------:|-----------------:|
|overvalued ~ POV_RATE_NO_GED + POV_RATE_GED + POV_RATE_SOME_COL + POV_RATE_BACH_PLUS                                                   | 0.5370467|         0.4629533|
|overvalued ~ POV_RATE_GED + POV_RATE_SOME_COL + POV_RATE_BACH_PLUS                                                                     | 0.5338460|         0.4661540|
|overvalued ~ POV_RATE_NO_GED + POV_RATE_SOME_COL + POV_RATE_BACH_PLUS                                                                  | 0.5317536|         0.4682464|
'''


# Correlation between preditors 
dfSubT <- subset(df_known, select = c(POV_RATE_NO_GED,POV_RATE_GED,POV_RATE_SOME_COL,POV_RATE_BACH_PLUS))

flattenCorrMatrix <- function(cormat, pmat) {
  ut <- upper.tri(cormat)
  data.frame(
    row = rownames(cormat)[row(cormat)[ut]],
    column = rownames(cormat)[col(cormat)[ut]],
    cor  =(cormat)[ut],
    p = pmat[ut]
  )
}

corr <- rcorr(as.matrix(dfSubT))
arrange(flattenCorrMatrix(corr$r, corr$P), cor)

# PCT_M, PCT_WA, PCT_AA
# high corr b/w fam indicators, choose PCT_FAM_POV
# PCT_OCC_OWNER, AVG_HOUSE_SIZE
# very high corr b/w MHI, choose MHI_TOT
# very high corr b/w emp stats, choose PCT_UNEMP
# Blk_Val, sale_season1, act_age, no_buldng, lnd_sqfoot
# some corr b/w pov/edu indicators, probably safe to choose POV_RATE_SOME_COL



### Naive Bayes classifier using selected features  <=  best model
dfSubNB <- subset(df_known, select = c(overvalued, PCT_M, PCT_WA, PCT_AA, PCT_FAM_POV, PCT_OCC_OWNER, AVG_HOUSE_SIZE, MHI_TOT, PCT_UNEMP, 
                                       Blk_Val, act_age, no_buldng, lnd_sqfoot, sale_season1, POV_RATE_SOME_COL))
dfSubNB <- dfSubNB[complete.cases(dfSubNB) == TRUE,]

ptm <- proc.time()
set.seed(0451)
testNB <- k_fold_prob(dfSubNB, overvalued~PCT_M+ PCT_WA+ PCT_AA+ PCT_FAM_POV+ PCT_OCC_OWNER+ AVG_HOUSE_SIZE+ MHI_TOT+ PCT_UNEMP+ 
                        Blk_Val+ act_age+ no_buldng+ lnd_sqfoot+ sale_season1+ POV_RATE_SOME_COL)
proc.time() - ptm   # 74.64s
((testNB$Overvalued_correct / testNB$Overvalued_total)+(testNB$Undervalued_correct / testNB$Undervalued_total))/2
# 0.5680928
((testNB$Overvalued_wrong / testNB$Overvalued_total)+(testNB$Undervalued_wrong / testNB$Undervalued_total))/2
# 0.4319072

# ROC CURVE for naive bayes model
set.seed(0451)
indices = sample(1:nrow(dfSubNB))
train.obs = as.integer(0.75 * length(indices))
train.indices = indices[1:train.obs]
n.train.set = dfSubNB[train.indices,]
test.indices = indices[(train.obs + 1):length(indices)]
n.test.set = dfSubNB[test.indices,]

modNB <- naiveBayes(overvalued~., data=n.train.set, type='raw')

nb.pr <- predict(modNB, type="raw", newdata=n.test.set)[,2]
nb.pred <- prediction(nb.pr, n.test.set$overvalued)
nb.perf <- performance(nb.pred,"tpr","fpr")
nb.auc <- performance(nb.pred, "auc")@y.values[[1]]
plot(nb.perf,main="ROC Curve for Naive Bayes",col=2,lwd=2)
legend("bottomright", legend=paste("AUC =", round(nb.auc,2)), bty = 'n')
abline(a=0,b=1,lwd=2,lty=2,col="gray")



### Naive Bayes classifier using features from linear model variables selection
dfSubNB_L <- subset(df_known, select = c(overvalued,lnd_sqfoot,no_buldng,vi_cd1_explained,
                                     sale_season1,act_age,Blk_Val,AVG_H_SIZE_RENTER,POV_RATE_SOME_COL,
                                     PCT_WA,PCT_AA,PCT_OTHER))
dfSubNB_L <- dfSubNB_L[complete.cases(dfSubNB_L) == TRUE,]

ptm <- proc.time()
set.seed(0451)
testNB_L <- k_fold_prob(dfSubNB_L, overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+
                        POV_RATE_SOME_COL+PCT_WA+PCT_AA+PCT_OTHER)
proc.time() - ptm   # 68.28s
((testNB_L$Overvalued_correct / testNB_L$Overvalued_total)+(testNB_L$Undervalued_correct / testNB_L$Undervalued_total))/2
# 0.554125
((testNB_L$Overvalued_wrong / testNB_L$Overvalued_total)+(testNB_L$Undervalued_wrong / testNB_L$Undervalued_total))/2
# 0.445875



### Random Forest classifier using selected features
dfSubRF <- subset(df_known, select = c(overvalued,PCT_M, PCT_WA, PCT_AA, PCT_FAM_POV, PCT_OCC_OWNER, AVG_HOUSE_SIZE, MHI_TOT, PCT_UNEMP, 
                                         Blk_Val, act_age, no_buldng, lnd_sqfoot, sale_season1, POV_RATE_SOME_COL))
dfSubRF <- dfSubRF[complete.cases(dfSubRF) == TRUE,]

# With node size 30
ptm <- proc.time()
set.seed(0451)
test1 <- k_fold_prob(dfSubRF, overvalued~PCT_M+ PCT_WA+ PCT_AA+ PCT_FAM_POV+ PCT_OCC_OWNER+ AVG_HOUSE_SIZE+ MHI_TOT+ PCT_UNEMP+ 
                      Blk_Val+ act_age+ no_buldng+ lnd_sqfoot+ sale_season1+ POV_RATE_SOME_COL)
proc.time() - ptm   # 654.70s
((test1$Overvalued_correct / test1$Overvalued_total)+(test1$Undervalued_correct / test1$Undervalued_total))/2
# 0.572639
((test1$Overvalued_wrong / test1$Overvalued_total)+(test1$Undervalued_wrong / test1$Undervalued_total))/2
# 0.427361


# With node size 10
ptm <- proc.time()
set.seed(0451)
test2 <- k_fold_prob(dfSubRF, overvalued~PCT_M+ PCT_WA+ PCT_AA+ PCT_FAM_POV+ PCT_OCC_OWNER+ AVG_HOUSE_SIZE+ MHI_TOT+ PCT_UNEMP+ 
                       Blk_Val+ act_age+ no_buldng+ lnd_sqfoot+ sale_season1+ POV_RATE_SOME_COL)
proc.time() - ptm   # 758.53s
((test2$Overvalued_correct / test2$Overvalued_total)+(test2$Undervalued_correct / test2$Undervalued_total))/2
# 0.5838126
((test2$Overvalued_wrong / test2$Overvalued_total)+(test2$Undervalued_wrong / test2$Undervalued_total))/2
# 0.4161874  



### Random Forest on full model acquired via linear model selection

# With node size 30
ptm <- proc.time()
set.seed(0451)
test3 <- k_fold_prob(dfSub, overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
              sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
              PCT_WA+PCT_AA+PCT_OTHER)
proc.time() - ptm   # 510.67s
((test3$Overvalued_correct / test3$Overvalued_total)+(test3$Undervalued_correct / test3$Undervalued_total))/2
# 0.5730077
((test3$Overvalued_wrong / test3$Overvalued_total)+(test3$Undervalued_wrong / test3$Undervalued_total))/2
# 0.4269923


# With node size 10  <=  best model
ptm <- proc.time()
set.seed(0451)
test4 <- k_fold_prob(dfSub, overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
                      sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
                      PCT_WA+PCT_AA+PCT_OTHER)
proc.time() - ptm   # 614.55s
((test4$Overvalued_correct / test4$Overvalued_total)+(test4$Undervalued_correct / test4$Undervalued_total))/2
# 0.5855347
((test4$Overvalued_wrong / test4$Overvalued_total)+(test4$Undervalued_wrong / test4$Undervalued_total))/2
# 0.4144653  

# ROC CURVE for random forest model
set.seed(0451)
indices = sample(1:nrow(dfSubRF))
train.obs = as.integer(0.75 * length(indices))
train.indices = indices[1:train.obs]
f.train.set = dfSubRF[train.indices,]
test.indices = indices[(train.obs + 1):length(indices)]
f.test.set = dfSubRF[test.indices,]

bestmtry <- tuneRF(f.train.set[,-1],f.train.set[,1], ntreeTry=100, 
                   stepFactor=1.5,improve=0.01, trace=TRUE, plot=TRUE, dobest=FALSE)

modRF <- randomForest(overvalued~., data=f.train.set, mtry=2, nodesize=10, importance=TRUE, test=f.test.set)

rf.pr <- predict(modRF, type="prob", newdata=f.test.set)[,2]
rf.pred <- prediction(rf.pr, f.test.set$overvalued)
rf.perf <- performance(rf.pred,"tpr","fpr")
rf.auc <- performance(rf.pred, "auc")@y.values[[1]]
plot(rf.perf,main="ROC Curve for Random Forest",col=2,lwd=2)
legend("bottomright", legend=paste("AUC =", round(rf.auc,2)), bty = 'n')
abline(a=0,b=1,lwd=2,lty=2,col="gray")



# dfSub3 <- subset(df_known, select = c(diff_btwn_prc_jv,lnd_sqfoot,no_buldng,vi_cd1_explained,
#                                      sale_season1,act_age,Blk_Val,AVG_H_SIZE_RENTER,POV_RATE_SOME_COL,
#                                      PCT_WA,PCT_AA,PCT_OTHER))
# 
# dfSub3 <- dfSub3[complete.cases(dfSub3) == TRUE,]
# 
# dfSub3 <- dfSub3[sample(nrow(dfSub3), 20000),]
# 
# pairs(diff_btwn_prc_jv~lnd_sqfoot+no_buldng+vi_cd1_explained+
#         sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
#         PCT_WA+PCT_AA+PCT_OTHER, dfSub3)



### CV Code (written by Erik Langenborg)

if_else_ <- function(.data, .truth, .lhs, .rhs) {
  if (.truth) {
    .lhs(.data)
  } else {
    .rhs(.data)
  }
}

is_invalid <- function(.data) {
  # This function is adapted from Stack Overflow at:
  # http://stackoverflow.com/a/19655909/2601448
  if (is.function(.data)) {
    return(FALSE)
  }
  
  return(is.null(.data) ||
           length(.data) == 0 ||
           all(is.na(.data)) ||
           all(.data == ""))
}

combo_internal <- function(.set, .map_fn) {
  # For invalid choices (empty, or NaN, etc), return an empty list
  if (is_invalid(.set)) {
    return(list())
  }
  
  elements <- .set %>% (function(e) {
    list(e, 1:length(e))
  }) %>% transpose
  
  seq(1, 2^length(.set)) %>% map(function(mask) {
    elements %>% discard(function(pair) {
      # if the pair index is masked (0), drop it. keep if slot is 1
      pair %>% dplyr::nth(2) %>% -1 %>% (function(e) {
        bitwShiftL(1, e)
      }) %>%
        bitwAnd(mask) %>%
        `>`(0)
    }) %>% .map_fn(function(e) {
      dplyr::nth(e, 1)
    })
  }) %>% discard(function(e) {
    length(e) < 1  # ignore empties (probably not useful)
  })
}

combo_chr <- function(.set) {
  combo_internal(.set, purrr::map_chr)
}

k_fold_prob <- function(data, current_formula, k = 5, resample = TRUE) {
  folds <- cut(seq(1, nrow(data)), breaks = k, labels = FALSE) %>% if_else_(resample,
                                                                            sample, identity)
  # NOTE: call to sample is random. For consistent behavior, use set.seed
  
  1:k %>%
    map(function(fold_number) {
      temp.train <- data %>% filter(folds != fold_number)
      temp.test <- data %>% filter(folds == fold_number)
      
      current_formula %>%
        randomForest(data = temp.train, nodesize = 10) %>%
        predict(temp.test) %>%
        factor_scores(temp.test$overvalued)
    }) %>%
    reduce(rbind) %>%
    dmap(sum)
}

factor_scores <- function(predictions, truths) {
  truths %>%
    unique %>%
    map(function(fct) {
      list(truths, predictions) %>%
        transpose %>%
        map(unlist) %>%
        discard(~ .[1] != as.numeric(fct)) -> truths_and_predictions
      
      truths_and_predictions %>%
        length ->
        predictions_total
      
      truths_and_predictions %>%
        keep(~ .[1] == .[2]) %>%
        length ->
        predictions_correct
      
      predictions_total - predictions_correct ->
        predictions_wrong
      
      data.frame(predictions_total, predictions_correct, predictions_wrong) %>%
        `colnames<-`(paste(as.character(fct), c("total", "correct", "wrong"), sep = "_"))
      
    }) %>%
    reduce(cbind)
}

registerDoParallel(cores = detectCores() - 1)

dfSub %>%
  names %>%
  discard(~. == "overvalued") %>%
  combo_chr -> combos

full_test <- function(df) {
  foreach(i = 1:length(combos), .packages=c('purrr','dplyr','lubridate','readr','stringr','doParallel',
                                            'randomForest'), .export=c('combo_chr','combo_internal',
                                                                       'factor_scores','full_test','if_else_',
                                                                       'is_invalid','k_fold_prob','combos')) %dopar% {
    formlChrs <- combos[[i]]
    rhd <- formlChrs %>% paste(collapse = " + ")
    forml <- c("overvalued", rhd) %>% paste(collapse = " ~ ")
    score <- k_fold_prob(df, as.formula(forml))
    data.frame(Formula = forml, score)
  } %>%
    reduce(rbind) %>%
    mutate(
      Accuracy = ((Overvalued_correct / Overvalued_total) +
                    (Undervalued_correct / Undervalued_total)) *
        (1 / 2),
      BalancedErrorRate = ((Overvalued_wrong / Overvalued_total) +
                             (Undervalued_wrong / Undervalued_total)) *
        (1 / 2)) %>%
    select(Formula, Accuracy, BalancedErrorRate)
}

set.seed(0451) # consistent runs
dfSub %>%
  full_test ->
  res

# res %>% glimpse
# 
# res %>%
#   arrange(BalancedErrorRate)


res %>%
  arrange(BalancedErrorRate) %>%
  kable(format = "markdown")


