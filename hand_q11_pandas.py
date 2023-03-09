import pandas as pd

def q11(partsupp, supplier, nation):
    var1 = 'GERMANY'

    na_filt = nation[(nation['n_name'] == var1)]

    na_su_join = na_filt.merge(supplier, left_on='n_nationkey', right_on='s_nationkey')

    all_join = na_su_join.merge(partsupp, left_on='s_suppkey', right_on='ps_suppkey')

    agg_val = (all_join['ps_supplycost'] * all_join['ps_availqty']).sum() * 0.0001

    all_join_filt = all_join.groupby(['ps_partkey']).filter(
        lambda x: (x['ps_supplycost'] * x['ps_availqty']).sum() > agg_val
    )

    all_join_filt['value'] = all_join_filt['ps_supplycost'] * all_join_filt['ps_availqty']

    result = all_join_filt.groupby(['ps_partkey'], as_index=False) \
        .agg({'value': 'sum'})

    return result