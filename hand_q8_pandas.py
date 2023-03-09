import pandas as pd

def q8(part, supplier, lineitem, orders, customer, nation, region):
    var1 = 'BRAZIL'
    var2 = 'AMERICA'
    var3 = 'ECONOMY ANODIZED STEEL'

    n1 = nation.copy()

    n1.rename({'n_nationkey': 'n1_nationkey',
               'n_name': 'n1_name',
               'n_regionkey': 'n1_regionkey',
               'n_comment': 'n1_comment'}, axis=1, inplace=True)

    n2 = nation.copy()

    n2.rename({'n_nationkey': 'n2_nationkey',
               'n_name': 'n2_name',
               'n_regionkey': 'n2_regionkey',
               'n_comment': 'n2_comment'}, axis=1, inplace=True)

    re_filt = region[(region['r_name'] == var2)]

    re_na_join = re_filt.merge(right=n1, left_on='r_regionkey', right_on='n1_regionkey')

    ord_filt = orders[(orders['o_orderdate'] >= '1995-01-01') & (orders['o_orderdate'] <= '1996-12-31')]

    na_cu_join = re_na_join.merge(right=customer, left_on='n1_nationkey', right_on='c_nationkey')

    cu_ord_join = na_cu_join.merge(right=ord_filt, left_on='c_custkey', right_on='o_custkey')

    ord_li_join = cu_ord_join.merge(right=lineitem, left_on='o_orderkey', right_on='l_orderkey')

    pa_filt = part[part['p_type'] == var3]

    pa_li_join = pa_filt.merge(right=ord_li_join, left_on='p_partkey', right_on='l_partkey')

    su_li_join = supplier.merge(right=pa_li_join, left_on='s_suppkey', right_on='l_suppkey')

    all_join = n2.merge(right=su_li_join, left_on='n2_nationkey', right_on='s_nationkey')

    all_join['o_year'] = all_join['o_orderdate'].dt.year
    all_join['volume'] = all_join['l_extendedprice'] * (1 - all_join['l_discount'])
    all_join['nation'] = all_join['n2_name']

    all_nations = all_join[['o_year', 'volume', 'nation']]

    all_nations['volume_A'] = all_nations.apply(lambda x: x['volume'] if x['nation'] == var1 else 0.0, axis=1)

    all_nations_agg = all_nations.groupby(['o_year'], as_index=False) \
        .agg(A=('volume_A', 'sum'),
             B=('volume', 'sum'))

    all_nations_agg['mkt_share'] = all_nations_agg['A'] / all_nations_agg['B']

    result = all_nations_agg[['o_year', 'mkt_share']]

    return result