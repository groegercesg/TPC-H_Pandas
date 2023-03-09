import pandas as pd

def q15(lineitem, supplier):
    var1 = "1996-01-01"
    var2 = "1996-04-01"
    var3 = 1772627.2087

    li_filt = lineitem[(lineitem['l_shipdate'] >= var1) & (lineitem['l_shipdate'] < var2)]
    li_filt["revenue"] = li_filt['l_extendedprice'] * (1.0 - li_filt['l_discount'])

    li_aggr = li_filt \
        .groupby(["l_suppkey"]) \
        .agg(total_revenue=("revenue", "sum"))
    
    li_aggr = li_aggr[li_aggr['total_revenue'] == var3]

    su_proj = supplier[["s_suppkey", "s_name", "s_address", "s_phone"]]
    li_su_join = su_proj.merge(li_aggr, left_on="s_suppkey", right_on="l_suppkey", how="inner")

    result = li_su_join[["s_suppkey", "s_name", "s_address", "s_phone", "total_revenue"]]

    return result