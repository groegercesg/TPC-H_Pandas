import pandas as pd

def q17(lineitem, part):
    var1 = 'Brand#23'
    var2 = 'MED BOX'

    l1 = lineitem.copy()

    part_agg = l1.groupby(['l_partkey'], as_index=False) \
        .agg(sum_quant=('l_quantity', 'sum'),
             count_quant=('l_quantity', 'count'))

    pa_filt = part[(part['p_brand'] == var1) & (part['p_container'] == var2)]

    pa_li_join = pa_filt.merge(part_agg, left_on='p_partkey', right_on='l_partkey')

    pa_li_join = pa_li_join.merge(lineitem, left_on='l_partkey', right_on='l_partkey')
    pa_li_join['l_extendedprice'] = pa_li_join.apply(
        lambda x: x['l_extendedprice'] if (x['l_quantity'] < (0.2 * (x['sum_quant'] / x['count_quant']))) else 0.0,
        axis=1)

    result = pa_li_join['l_extendedprice'].sum() / 7.0

    return result