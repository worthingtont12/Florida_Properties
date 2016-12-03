
#Import modules for Modeling
import statsmodels.formula.api as sm
from patsy import dmatrices

#Model structure [UPDATE with appropriate / new variables as needed]
y1, X1 = dmatrices('diff_btwn_prc_jv ~ Blk_Val + const_class + eff_yr_blt + imp_qual + lnd_sqfoot + sale_season1 + tot_lvg_area + no_buldng', data=dfhd, return_type='dataframe')
mod1 = sm.OLS(y1, X1)
mod_1 = mod1.fit()
print(mod_1.summary())
