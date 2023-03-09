import pandas as pd

def q5(lineitem, customer, orders, region, nation, supplier):
    var1 = "ASIA"
    var2 = "1994-01-01"
    var3 = "1996-12-31"

    re_filt = region[region['r_name'] == var1]

    re_na_join = re_filt.merge(right=nation, left_on='r_regionkey', right_on='n_regionkey')

    na_cu_join = re_na_join.merge(right=customer, left_on='n_nationkey', right_on='c_nationkey')

    ord_filt = orders[(orders['o_orderdate'] >= var2) & (orders['o_orderdate'] < var3)]
    cu_ord_join = na_cu_join.merge(right=ord_filt, left_on='c_custkey', right_on='o_custkey')

    ord_li_join = cu_ord_join.merge(right=lineitem, left_on='o_orderkey', right_on='l_orderkey')

    su_ord_li_join = supplier.merge(right=ord_li_join,
                                    left_on=['s_suppkey', 's_nationkey'],
                                    right_on=['l_suppkey', 'c_nationkey'])

    su_ord_li_join['revenue'] = su_ord_li_join['l_extendedprice'] * (1.0 - su_ord_li_join['l_discount'])

    result = su_ord_li_join.groupby(['n_name'], as_index=False).agg(revenue=('revenue', 'sum'))

    return result