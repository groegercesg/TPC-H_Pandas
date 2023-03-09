import pandas as pd

def q13(customer, orders):
    var1 = 'special'
    var2 = 'requests'

    ord_filt = orders[~((orders['o_comment'].str.find(var1) != -1)
                        & (orders['o_comment'].str.find(var2) > (orders['o_comment'].str.find(var1) + 6)))]

    cu_ord_join = ord_filt.merge(customer, how='right', left_on='o_custkey', right_on='c_custkey')

    c_orders = cu_ord_join.groupby(['c_custkey'], as_index=False) \
        .agg(c_count=('o_orderkey', 'count'))

    result = c_orders.groupby(['c_count'], as_index=False) \
        .agg(custdist=('c_custkey', 'count'))

    return result