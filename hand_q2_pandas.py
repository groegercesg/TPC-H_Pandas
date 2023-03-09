import pandas as pd

def q2(part, supplier, partsupp, nation, region):
    var1 = 15
    var2 = 'BRASS'
    var3 = 'EUROPE'

    ps1 = partsupp.copy()

    re_filt = region[region['r_name'] == var3]

    re_na_join = re_filt.merge(nation, left_on='r_regionkey', right_on='n_regionkey')
    re_na_join = re_na_join[['n_nationkey', 'n_name']]

    na_su_join = re_na_join.merge(supplier, left_on='n_nationkey', right_on='s_nationkey')
    na_su_join = na_su_join[['s_suppkey', 's_acctbal', 's_name', 'n_name', 's_address', 's_phone', 's_comment']]

    pa_filt = part[(part['p_type'].str.endswith(var2)) & (part['p_size'] == var1)]
    pa_filt = pa_filt[['p_partkey', 'p_mfgr']]

    su_ps1_join = na_su_join.merge(ps1, left_on='s_suppkey', right_on='ps_suppkey')

    min_agg = su_ps1_join.groupby(['ps_partkey'], as_index=False) \
        .agg({'ps_supplycost': 'sum'})

    min_agg.rename({'ps_supplycost': 'min_supplycost'}, axis=1, inplace=True)

    pa_ps_join = pa_filt.merge(partsupp, left_on='p_partkey', right_on='ps_partkey')

    pa_ps_min = min_agg.merge(pa_ps_join, left_on='ps_partkey', right_on='ps_partkey')

    all_join = na_su_join.merge(pa_ps_min, left_on='s_suppkey', right_on='ps_suppkey')
    all_join = all_join[all_join['ps_supplycost'] == all_join['min_supplycost']]

    result = all_join[['s_acctbal', 's_name', 'n_name', 'p_partkey', 'p_mfgr', 's_address', 's_phone', 's_comment']]

    return result