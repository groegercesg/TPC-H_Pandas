import pandas as pd

def q9(lineitem, orders, nation, supplier, part, partsupp):
    var1 = 'green'

    na_su_join = nation.merge(supplier, left_on='n_nationkey', right_on='s_nationkey')

    pa_filt = part[part['p_name'].str.contains(var1)]

    pa_ps_join = pa_filt.merge(partsupp, left_on='p_partkey', right_on='ps_partkey')

    su_ps_join = na_su_join.merge(pa_ps_join, left_on='s_suppkey', right_on='ps_suppkey')

    ord_li_join = orders.merge(lineitem, left_on='o_orderkey', right_on='l_orderkey')

    all_join = su_ps_join.merge(ord_li_join,
                                left_on=['ps_partkey', 'ps_suppkey'],
                                right_on=['l_partkey', 'l_suppkey'])

    all_join['nation'] = all_join['n_name']
    all_join['o_year'] = all_join['o_orderdate'].dt.year
    all_join['amount'] = (all_join['l_extendedprice'] * (1.0 - all_join['l_discount'])) - (
            all_join['ps_supplycost'] * all_join['l_quantity'])

    profit = all_join[['nation', 'o_year', 'amount']]

    result = profit.groupby(['nation', 'o_year'], as_index=False) \
        .agg(sum_profit=('amount', 'sum'))

    return result