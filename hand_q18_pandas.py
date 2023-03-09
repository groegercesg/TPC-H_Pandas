import pandas as pd

def q18(lineitem, customer, orders):
    var1 = 300

    li_aggr = lineitem \
        .groupby(["l_orderkey"]) \
        .agg(sum_quantity=("l_quantity", "sum"))

    li_filt = li_aggr[li_aggr['sum_quantity'] > var1].reset_index()
    li_proj = li_filt[["l_orderkey"]]

    ord_filt = orders[orders['o_orderkey'].isin(li_proj["l_orderkey"])]

    cu_proj = customer[["c_custkey", "c_name"]]
    cu_ord_join = cu_proj.merge(ord_filt, left_on="c_custkey", right_on="o_custkey", how="inner")
    cu_ord_join = cu_ord_join[["c_name", "c_custkey", "o_orderkey", "o_orderdate", "o_totalprice"]]

    li_ord_join = cu_ord_join.merge(lineitem, left_on="o_orderkey", right_on="l_orderkey", how="inner")

    result = li_ord_join \
        .groupby(["c_name", "c_custkey", "o_orderkey", "o_orderdate", "o_totalprice"], as_index=False) \
        .agg(sum_quantity=("l_quantity", "sum"))

    return result