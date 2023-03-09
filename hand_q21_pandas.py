import pandas as pd

def q21(suppier, lineitem, orders, nation):
    var1 = "SAUDI ARABIA"

    l2 = lineitem.copy()
    l3 = lineitem.copy()

    na_filt = nation[nation['n_name'] == var1]
    na_su_join = na_filt.merge(suppier, left_on='n_nationkey', right_on='s_nationkey')

    ord_filt = orders[orders['o_orderstatus'] == "F"]

    l2_agg = l2.groupby(['l_orderkey'], as_index=False).agg(l2_size=('l_suppkey', 'count'))
    l2_filt = l2_agg[['l_orderkey', 'l2_size']]

    l3_filt = l3[(l3['l_receiptdate'] > l3['l_commitdate'])]
    l3_agg = l3_filt.groupby(['l_orderkey'], as_index=False).agg(l3_size=('l_suppkey', 'count'))
    l3_filt = l3_agg[['l_orderkey', 'l3_size']]

    l1 = lineitem[(lineitem['l_receiptdate'] > lineitem['l_commitdate'])]

    l1_l2_join = l2_filt.merge(l1, left_on='l_orderkey', right_on='l_orderkey')

    l1_l3_join = l3_filt.merge(l1_l2_join, left_on='l_orderkey', right_on='l_orderkey')

    su_li_join = na_su_join.merge(l1_l3_join, left_on='s_suppkey', right_on='l_suppkey')

    ord_li_join = ord_filt.merge(su_li_join, left_on='o_orderkey', right_on='l_orderkey')
    ord_li_join = ord_li_join[(ord_li_join['l2_size'] > 1) & (ord_li_join['l3_size'] == 1)]

    result = ord_li_join.groupby(['s_name'], as_index=False) \
        .agg(numwait=('s_name', 'count'))

    return result