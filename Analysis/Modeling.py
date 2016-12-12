
# Import modules for Modeling
import statsmodels.formula.api as sm
from patsy import dmatrices
import pandas as pd
from sklearn.feature_selection import RFECV
import sklearn.linear_model as lm

dfTest = pd.read_csv('~/Git_Repos/Data/miami_cleaned.csv')
df_mod = dfTest.loc[dfTest['residential'] == True]

reg = lm.LinearRegression()

y1, X1 = dmatrices('diff_btwn_prc_jv ~ Blk_Val + const_class + eff_yr_blt + imp_qual + lnd_sqfoot + sale_season1 + tot_lvg_area + no_buldng',
                   data=dfTest, return_type='dataframe')

selector = RFECV(estimator=reg, cv=10, scoring='mean_squared_error')

selector.fit(X1, y1)

print("Optimal number of features: % d" % (selector.n_features_))

print(X1.feature_names[selector.support_])

# Model structure [UPDATE with appropriate / new variables as needed]
# y1, X1=dmatrices('diff_btwn_prc_jv ~ Blk_Val + const_class + eff_yr_blt + imp_qual + lnd_sqfoot + sale_season1 + tot_lvg_area + no_buldng',
#                    data=dfTest, return_type='dataframe')
# mod1=sm.OLS(y1, X1)
# mod_1=mod1.fit()
# print(mod_1.summary())
