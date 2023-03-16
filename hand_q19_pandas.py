import pandas as pd

def q19(lineitem, part):
    var1 = "Brand#12", 
    var2 = "Brand#23", 
    var3 = "Brand#34"
    var4 = 1
    var5 = 11
    var6 = 10
    var7 = 20
    var8 = 20
    var9 = 30

    pa_filt = part[
        ((part.p_brand == var1)
         & (part.p_container.isin(["SM CASE", "SM BOX", "SM PACK", "SM PKG"]))
         & (part.p_size >= 1) & (part.p_size <= 5)) |
        ((part.p_brand == var2)
         & (part.p_container.isin(["MED BAG", "MED BOX", "MED PKG", "MED PACK"]))
         & (part.p_size >= 1) & (part.p_size <= 10)) |
        ((part.p_brand == var3)
         & (part.p_container.isin(["LG CASE", "LG BOX", "LG PACK", "LG PKG"]))
         & (part.p_size >= 1) & (part.p_size <= 15))
        ]

    pa_proj = pa_filt[["p_partkey", "p_brand"]]

    li_filt = lineitem[(((lineitem.l_shipmode == "AIR") | (lineitem.l_shipmode == "AIR REG"))
                        & (lineitem.l_shipinstruct == "DELIVER IN PERSON"))]

    li_pa_join = pa_proj.merge(li_filt, left_on="p_partkey", right_on="l_partkey", how="inner")
    li_pa_join_filt = li_pa_join[
        (
                ((li_pa_join.p_brand == var1)
                 & ((li_pa_join.l_quantity >= var4) & (li_pa_join.l_quantity <= var5)))
                | ((li_pa_join.p_brand == var2)
                   & ((li_pa_join.l_quantity >= var6) & (li_pa_join.l_quantity <= var7)))
                | ((li_pa_join.p_brand == var3)
                   & ((li_pa_join.l_quantity >= var8) & (li_pa_join.l_quantity <= var9)))
        )
    ]

    li_pa_join_filt["revenue"] = li_pa_join_filt['l_extendedprice'] * (1.0 - li_pa_join_filt['l_discount'])

    result = li_pa_join_filt.agg({'revenue': 'sum'})
    
    
    final = pd.DataFrame()
    final['revenue'] = [result]

    return final
