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
})

df_known <- read.csv("df_cleaned.csv")
df_known <- df_known[df_known$residential == 'True', ]
df_known <- df_known[complete.cases(df_known$diff_btwn_prc_jv)==TRUE,]
df_known <- df_known[df_known$landuse_explained  == 'Single Family' ,]
df_known <- df_known[df_known$sale_prc1 > 10 ,]
df_known <- subset(df_known , !duplicated(phy_addr1))
df_known <- df_known[df_known$sale_prc1 < 542200000 ,]
df_known <- df_known[df_known$jv > 2 ,]
df_known <- subset(df_known , !duplicated(phy_addr1))
df_known <- subset(df_known, !duplicated(subset(df_known, select=c(census_tract, act_age, sale_prc1))))
df_known$overvalued <- as.factor(ifelse(df_known$diff_btwn_prc_jv > 0, 'Overvalued', 'Undervalued'))

# Sub dataframe with variables selected by linear model selection
dfSub <- subset(df_known, select = c(overvalued,lnd_sqfoot,no_buldng,vi_cd1_explained,
                                      sale_season1,act_age,Blk_Val,AVG_H_SIZE_RENTER,POV_RATE_SOME_COL,
                                      PCT_WA,PCT_AA,PCT_OTHER))

# Sub dataframe to complete cases only
dfSub <- dfSub[complete.cases(dfSub) == TRUE,]



# mod_test1 <- randomForest(overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
#                             sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
#                             PCT_WA+PCT_AA+PCT_OTHER, data = dfSub, na.action = na.omit, nodesize = 1)
# ((mod_test1$Overvalued_correct / mod_test1$Overvalued_total)+(mod_test1$Undervalued_correct / mod_test1$Undervalued_total))/2
# 
# 
# ptm <- proc.time()
# mod_test2 <- randomForest(overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
#                            sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
#                            PCT_WA+PCT_AA+PCT_OTHER, data = dfSub, na.action = na.omit, nodesize = 5)
# proc.time() - ptm
# 
# ptm <- proc.time()
# mod_test3 <- randomForest(overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
#                            sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
#                            PCT_WA+PCT_AA+PCT_OTHER, data = dfSub, na.action = na.omit, nodesize = 10)
# proc.time() - ptm
# 
# ptm <- proc.time()
# mod_test4 <- randomForest(overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
#                            sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
#                            PCT_WA+PCT_AA+PCT_OTHER, data = dfSub, na.action = na.omit, nodesize = 20)
# proc.time() - ptm
# 
# ptm <- proc.time()
# mod_test5 <- randomForest(overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
#                             sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
#                             PCT_WA+PCT_AA+PCT_OTHER, data = dfSub, na.action = na.omit, nodesize = 30)
# proc.time() - ptm
# varImpPlot(mod_test1)


### Random Forest on full model acquired via linear model selection

# With node size 30
ptm <- proc.time()
set.seed(0451)
test <- k_fold_prob(dfSub, overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
              sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
              PCT_WA+PCT_AA+PCT_OTHER)
proc.time() - ptm   # 510.67s
((test$Overvalued_correct / test$Overvalued_total)+(test$Undervalued_correct / test$Undervalued_total))/2
# 0.5730077
((test$Overvalued_wrong / test$Overvalued_total)+(test$Undervalued_wrong / test$Undervalued_total))/2
# 0.4269923


# With node size 10  <=  best model
ptm <- proc.time()
set.seed(0451)
test2 <- k_fold_prob(dfSub, overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
                      sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
                      PCT_WA+PCT_AA+PCT_OTHER)
proc.time() - ptm   # 614.55s
((test2$Overvalued_correct / test2$Overvalued_total)+(test2$Undervalued_correct / test2$Undervalued_total))/2
# 0.5855347
((test2$Overvalued_wrong / test2$Overvalued_total)+(test2$Undervalued_wrong / test2$Undervalued_total))/2
# 0.4144653  


# With node size 1
ptm <- proc.time()
set.seed(0451)
test3 <- k_fold_prob(dfSub, overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
                       sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
                       PCT_WA+PCT_AA+PCT_OTHER)
proc.time() - ptm   # 709.94s
((test3$Overvalued_correct / test3$Overvalued_total)+(test3$Undervalued_correct / test3$Undervalued_total))/2
# 0.5852579
((test3$Overvalued_wrong / test3$Overvalued_total)+(test3$Undervalued_wrong / test3$Undervalued_total))/2
# 0.4147421 



# ### Support Vector Machines on full model acquired via linear model selection
# 
# dfSub2 <- dfSub[sample(nrow(dfSub), 20000),]
# 
# ptm <- proc.time()
# set.seed(0451)
# test4 <- k_fold_prob(dfSub2, overvalued~lnd_sqfoot+no_buldng+vi_cd1_explained+
#                        sale_season1+act_age+Blk_Val+AVG_H_SIZE_RENTER+POV_RATE_SOME_COL+
#                        PCT_WA+PCT_AA+PCT_OTHER)
# proc.time() - ptm   # 614.55s
# ((test4$Overvalued_correct / test4$Overvalued_total)+(test4$Undervalued_correct / test4$Undervalued_total))/2
# # 0.5852579
# ((test4$Overvalued_wrong / test4$Overvalued_total)+(test4$Undervalued_wrong / test4$Undervalued_total))/2
# # 0.4147421 



### CV Code   
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
        svm(data = temp.train, kernel = "linear") %>%
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
  foreach(i = 1:length(combos), .packages=c('purrr','dplyr','lubridate','readr','stringr','doParallel','randomForest'), .export=c('combo_chr','combo_internal','factor_scores','full_test','if_else_','is_invalid','k_fold_prob','combos')) %dopar% {
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



res %>% glimpse

res %>%
  arrange(BalancedErrorRate)

library(knitr)
res %>%
  arrange(BalancedErrorRate) %>%
  kable(format = "markdown")

