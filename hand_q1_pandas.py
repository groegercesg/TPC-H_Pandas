import pandas as pd

def q1(lineitem):
    var1 = "1998-09-02"

    li_filt = lineitem[(lineitem['l_shipdate'] <= var1)]
    li_filt["disc_price"] = li_filt['l_extendedprice'] * (1.0 - li_filt['l_discount'])
    li_filt["charge"] = li_filt['l_extendedprice'] * (1.0 - li_filt['l_discount']) * (1.0 + li_filt['l_tax'])

    result = li_filt \
        .groupby(["l_returnflag", "l_linestatus"], as_index=False) \
        .agg(sum_qty=("l_quantity", "sum"),
             sum_base_price=("l_extendedprice", "sum"),
             sum_disc_price=("disc_price", "sum"),
             sum_charge=("charge", "sum"),
             avg_qty=("l_quantity", "mean"),
             avg_price=("l_extendedprice", "mean"),
             avg_disc=("l_discount", "mean"),
             count_order=("l_quantity", "count"))

    return result