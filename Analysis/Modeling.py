
#Import modules for Modeling
import statsmodels.formula.api as sm
from patsy import dmatrices

#Create residential-only dataset for modeling
df_mod = dfTest.loc[dfTest['residential'] == True]

#Model structure [UPDATE with appropriate / new variables as needed]
y1, X1 = dmatrices('diff_btwn_prc_jv ~ Blk_Val + const_class + eff_yr_blt + imp_qual + lnd_sqfoot + sale_season1 + tot_lvg_area + no_buldng', data=dfTest, return_type='dataframe')
mod1 = sm.OLS(y1, X1)
mod_1 = mod1.fit()
print(mod_1.summary())

#2nd iteration: including JV as predictor
y1, X2 = dmatrices('diff_btwn_prc_jv ~ jv + Blk_Val + const_class + eff_yr_blt + imp_qual + lnd_sqfoot + sale_season1 + tot_lvg_area + no_buldng', data=dfTest, return_type='dataframe')
mod2 = sm.OLS(y1, X2)
mod_2 = mod2.fit()
print(mod_2.summary())
