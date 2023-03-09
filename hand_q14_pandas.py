import pandas as pd

def q14(lineitem, part):
    var1 = "1995-09-01"
    var2 = "1995-10-01"

    li_filt = lineitem[(lineitem['l_shipdate'] >= var1) & (lineitem['l_shipdate'] < var2)]

    li_pa_join = part.merge(li_filt, left_on="p_partkey", right_on="l_partkey", how="inner")

    li_pa_join["A"] = li_pa_join.apply(
        lambda x: x["l_extendedprice"] * (1.0 - x["l_discount"]) if x["p_type"].startswith("PROMO") else 0.0,
        axis=1)
    li_pa_join["B"] = li_pa_join['l_extendedprice'] * (1.0 - li_pa_join['l_discount'])

    result = li_pa_join['A'].sum() * 100.0 / li_pa_join['B'].sum()

    return result