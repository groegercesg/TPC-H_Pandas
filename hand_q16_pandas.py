import pandas as pd

def q16(partsupp, part, supplier):
    var1 = "Brand#45"
    var2 = "MEDIUM POLISHED"
    var3 = (49, 14, 23, 45, 19, 3, 36, 9)

    pa_filt = part[
        (part.p_brand != var1) &
        (part.p_type.str.startswith(var2) == False) &
        (part.p_size.isin(var3))]
    pa_proj = pa_filt[["p_partkey", "p_brand", "p_type", "p_size"]]

    su_filt = supplier[
        supplier.s_comment.str.contains("Customer")
        & ((supplier.s_comment.str.find("Customer") + 7) < supplier.s_comment.str.find("Complaints"))]
    su_proj = su_filt[["s_suppkey"]]

    ps_filt = partsupp[~partsupp.ps_suppkey.isin(su_proj["s_suppkey"])]

    ps_pa_join = pa_proj.merge(ps_filt, left_on="p_partkey", right_on="ps_partkey", how="inner")

    result = ps_pa_join \
        .groupby(["p_brand", "p_type", "p_size"], as_index=False) \
        .agg(supplier_cnt=("ps_suppkey", lambda x: x.nunique()))

    return result