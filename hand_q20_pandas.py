import pandas as pd

def q20(supplier, nation, partsupp, part, lineitem):
    var1 = 'forest'
    var2 = '1994-01-01'
    var3 = '1995-01-01'
    var4 = 'CANADA'

    li_filt = lineitem[(lineitem['l_shipdate'] >= var2) & (lineitem['l_shipdate'] < var3)]

    pa_filt = part[part['p_name'].str.startswith(var1)]

    li_filt = li_filt[(li_filt['l_partkey'].isin(pa_filt['p_partkey']))]

    li_filt = li_filt[(li_filt['l_suppkey'].isin(supplier['s_suppkey']))]

    agg_lineitem = li_filt.groupby(['l_partkey', 'l_suppkey'], as_index=False) \
        .agg(sum_quantity=('l_quantity', 'sum'))

    li_ps_join = agg_lineitem.merge(partsupp,
                                    left_on=['l_partkey', 'l_suppkey'],
                                    right_on=['ps_partkey', 'ps_suppkey'])

    li_ps_filt = li_ps_join[li_ps_join['ps_availqty'] > li_ps_join['sum_quantity'] * 0.5]

    na_filt = nation[(nation['n_name'] == var4)]

    su_filt = supplier[(supplier['s_suppkey'].isin(li_ps_filt['l_suppkey']))]

    na_su_join = na_filt.merge(su_filt, left_on='n_nationkey', right_on='s_nationkey')

    result = na_su_join[['s_name', 's_address']]

    return result